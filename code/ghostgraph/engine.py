"""Deterministic resource ledger, supplied-policy application and proof-backed plans."""

from collections import defaultdict
from dataclasses import replace
import json

from .contract import ordered, read_csv, step, timestamp
from .evidence import DEFAULTS, Observation, identities, prefix, truth
from .temporal import reconstruct
from .policy import PolicyEngine
from .risks import process_analysis, plan_dependencies
from .planner import build_decision

TREATMENTS = {
    "DELETE": ("REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT", {"ABSENT"}),
    "REDACT": ("REPORT_EXPOSED_PII", "REDACT_RECORD", "VERIFY_RECORD_REDACTED", {"REDACTED"}),
    "ANONYMIZE": ("REPORT_EXPOSED_PII", "ANONYMIZE_RECORD", "VERIFY_RECORD_ANONYMIZED", {"ANONYMIZED"}),
    "RETAIN": (None, None, "VERIFY_RECORD_PRESENT", {"PRESENT"}),
    "FLOW": ("REPORT_ACTIVE_DATA_FLOW", "DISABLE_DATA_FLOW", "VERIFY_DATA_FLOW_DISABLED", {"DISABLED"}),
    "RESTORE": ("REPORT_RESTORE_RISK", "BLOCK_RESTORE", "VERIFY_RESTORE_BLOCKED", {"BLOCKED"}),
}


class AuthorizationUnresolved(ValueError):
    """No contract row can be inferred from an uncertain classifier result."""
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__('authorization classification unresolved for '+diagnostics['case_id'])


class Auditor:
    def __init__(self, store, identity, intent):
        self.store, self.identity, self.intent = store, identity, intent
        self.policy_engine = PolicyEngine(store.dataset / "deletion_rules.csv")
        self.rules = self.policy_engine.rules
        self.rule_by_category = {r["data_category"]: r for r in self.rules}
        if len(self.rule_by_category) != len(self.rules):
            raise ValueError("overlapping category rules need explicit condition resolution")
        if any(r["required_action"] not in {"DELETE", "REDACT", "ANONYMIZE", "RETAIN"} for r in self.rules):
            raise ValueError("unsupported policy action")

    def reduce_state(self, observations, cutoff, claims):
        return reconstruct(observations,cutoff,claims)

    def ledger(self, tokens, cutoff, subject_id=None):
        selected = {}
        linkage = defaultdict(list)
        self.temporal = {}
        def foreign_reference(obs):
            refs = identities({k: obs.fields[k] for k in
                ["user_id", "customer_reference", "subject_reference", "subject_ref", "subject_selector"]
                if k in obs.fields})
            stable = {t for t in refs if t.startswith("user_")}
            return bool(subject_id and stable and subject_id not in stable)
        # Build grounded subject → scoped-resource edges from eligible evidence only.
        resources = set()
        for token in tokens:
            for obs in self.store.by_token.get(token, []):
                if max(obs.available, obs.observed) <= cutoff:
                    if foreign_reference(obs):
                        continue
                    resources.add(obs.key)
                    linkage[obs.key].append({"via": "strong identifier in eligible observation", "evidence_id": obs.evidence_id, "locator": obs.locator})
        for when, system, resource, linked_tokens, link_id in self.store.links:
            if when <= cutoff and tokens & linked_tokens:
                resources.add((system, resource))
                linkage[(system, resource)].append({"via": "explicit catalog subject link", "evidence_id": link_id})
        # Follow explicit structured source/dependency references, never numeric
        # naming conventions or unrelated IDs mentioned in free-form prose.
        pending = list(resources)
        while pending:
            key = pending.pop()
            for obs in self.store.by_resource.get(key, []):
                if max(obs.available, obs.observed) > cutoff: continue
                if foreign_reference(obs):continue
                for field in ("source_resource_id", "upstream_resource_id", "replica_of"):
                    target = obs.fields.get(field)
                    if not isinstance(target, str) or prefix(target) not in DEFAULTS: continue
                    related = DEFAULTS[prefix(target)][0], target
                    if related not in resources:
                        resources.add(related)
                        linkage[related].append({"via": field, "from_system": key[0], "from_resource": key[1], "evidence_id": obs.evidence_id, "locator": obs.locator})
                        pending.append(related)
        issues = []
        for key in sorted(resources):
            observations = [o for o in self.store.by_resource.get(key, [])
                            if max(o.available, o.observed) <= cutoff]
            if observations:
                newest = max(o.observed for o in observations)
                if any(foreign_reference(o) and o.observed == newest for o in observations):
                    issues.append(dict(code="RESOURCE_IDENTITY_CHANGED", system=key[0], resource=key[1]))
                    continue
            # Full SQL tables supply absence for independently identified resources;
            # do not manufacture IDs from user/case suffixes or worker success claims.
            for scope in self.store.scopes:
                if timestamp(scope["meta"]["captured_at"]) > cutoff or key[1] in scope["resources"]:
                    continue
                compatible = scope["system"] == key[0]
                category = DEFAULTS.get(prefix(key[1]), (None, None))[1]
                policy = self.rule_by_category.get(category, {})
                if compatible and scope.get("exhaustive", False) and scope["category"] == category and policy.get("required_action") == "DELETE":
                    # Restrict absence to tables that actually cover that system/category.
                    # Generic replicas export all platform resource records; primary rows
                    # and replica rows remain separate scopes.
                    observations.append(Observation(scope["meta"]["file_id"], scope["meta"]["file_path"],
                        "table:" + scope["table"] + "/exhaustive-resource-lookup", timestamp(scope["meta"]["captured_at"]),
                        scope.get("observed", timestamp(scope["meta"]["captured_at"])), key[0], key[1],
                        DEFAULTS[prefix(key[1])][1], "ABSENT", tokens,
                        {"exhaustive_lookup": True}, scope.get("scope_id",scope["table"]), 4))
            if not observations:
                issues.append(dict(code="NO_STATE_PROOF", system=key[0], resource=key[1]))
                continue
            claims=getattr(self.store,'claims_by_resource',{}).get(key[1],getattr(self.store,'claims',[]))
            result = self.reduce_state(observations,cutoff,claims)
            self.temporal[key] = result.explain()
            issues.extend(dict(item,system=key[0],resource=key[1]) for item in result.issues)
            if result.witness is not None:
                selected[key] = result.witness
        self.linkage = linkage
        return selected, issues

    def treatment(self, obs, cutoff):
        decision=self.policy_engine.evaluate(obs.category,obs.state,obs.fields,cutoff)
        return decision.treatment, (decision.rule_id or 'process')+': '+decision.condition

    def audit(self, request):
        cutoff = timestamp(request["audit_at"])
        intent = self.intent.classify(request["request_text"])
        diagnostics = {"case_id": request["case_id"], "intent": intent, "issues": [], "proofs": []}
        if intent["low_confidence"]:
            diagnostics["issues"].append({"code": "INTENT_LOW_CONFIDENCE"})
        if intent.get('authorization_state') == 'CLASSIFICATION_UNRESOLVED':
            diagnostics['issues'].append({'code': 'AUTHORIZATION_CLASSIFICATION_UNRESOLVED'})
            raise AuthorizationUnresolved(diagnostics)
        if intent.get('ambiguous'):
            # Unfulfilled/undecided consent does not presently authorize deletion.
            # Keep that distinction internally; do not invent a policy finding.
            diagnostics['issues'].append({'code': 'CONSENT_NOT_ESTABLISHED'})
            return self.row(request,"NOT_APPLICABLE",[]),diagnostics
        if not intent["authorized"]:
            return self.row(request, "NOT_APPLICABLE", []), diagnostics
        tokens, uid, identity_issue = self.identity.resolve(request["email"], cutoff)
        diagnostics["subject_id"] = uid
        if hasattr(self.identity,'explain'):
            diagnostics['identity_provenance']=self.identity.explain(request['email'],cutoff)
        if identity_issue:
            diagnostics["identity_note"] = identity_issue
            if "multiple" in identity_issue:
                diagnostics["issues"].append({"code": "AMBIGUOUS_IDENTITY"})
                return self.row(request,"INCOMPLETE",[]),diagnostics
        ledger, issues = self.ledger(tokens, cutoff, subject_id=uid)
        diagnostics["issues"].extend(issues)
        diagnostics["temporal_ledger"]=[dict(system=k[0],resource=k[1],**v) for k,v in sorted(self.temporal.items())]
        findings, remediation, verification = [], [], []
        relevant_observations=[o for key in self.linkage for o in self.store.by_resource.get(key,[])]
        if hasattr(self.store,'claims_by_resource'):
            relevant_claims=[c for key in self.linkage for c in self.store.claims_by_resource.get(key[1],[])]
        else:relevant_claims=getattr(self.store,'claims',[])
        risks=process_analysis(relevant_observations,self.temporal,relevant_claims,cutoff)
        diagnostics['process_analysis']=risks
        diagnostics['obligation_ledger']=[]
        process_by_key={(r['system'],r['resource']):r for r in risks}
        for key in sorted(set(self.linkage)|set(self.temporal)):
            eligible=[o for o in self.store.by_resource.get(key,[]) if max(o.available,o.observed)<=cutoff]
            obs=ledger.get(key)
            representative=obs or (max(eligible,key=lambda o:o.observed) if eligible else None)
            category=representative.category if representative else DEFAULTS.get(prefix(key[1]),(None,None))[1]
            fields=dict(representative.fields) if representative else {}
            fields['_subject_identifiers']=sorted(tokens)
            condition_sources={}
            state=self.temporal.get(key,{}).get('state','UNKNOWN')
            process=process_by_key.get(key)
            if process and process['issues']:
                state='UNKNOWN'
                diagnostics['issues'].extend(dict(code=i,resource=key[1]) for i in process['issues'])
            # Explicit catalog exclusivity is a condition fact, not an ID heuristic.
            for when,system,resource,linked,activity_id in self.store.links:
                if resource!=key[1] or when>cutoff or not tokens & linked:continue
                row=getattr(self.store,'source_rows',{}).get((activity_id,'system_activity.csv'),{})
                detail=row.get('details','').lower()
                if 'belongs only to' in detail and 'no other subject' in detail:
                    fields['subject_only']=True
                    condition_sources['subject_only']=[dict(evidence_id=activity_id,source='system_activity.csv',locator=resource,available=when)]
            decision=self.policy_engine.evaluate(category,state,fields,cutoff)
            entry=dict(system=key[0],resource=key[1],category=category,
                category_source='observation' if representative else 'resource type pending state evidence',
                identity_linkage=self.linkage.get(key,[]),
                supporting_evidence=[ref for scope in self.temporal.get(key,{}).get('scopes',[]) for ref in scope['evidence']],
                scoped_observed_state=obs.state if obs else None,**decision.explain())
            condition_fields=['shared_context','order_reference','subject_only','subject_count','attributable','subject_email_present',
                'email','recipient_email','retention_until','retained_until','retention_from','hold_active','hold_until','hold_from',
                'restore_block_supported','archive_present','account_status','account_deleted','stable_reference_required']
            entry['condition_facts']={name:dict(value=fields[name],provenance=condition_sources.get(name,
                [dict(evidence_id=representative.evidence_id,source=representative.source,locator=representative.locator,available=representative.available)] if representative else []))
                for name in condition_fields if name in fields}
            diagnostics['obligation_ledger'].append(entry)
            diagnostics['issues'].extend(dict(code=code,system=key[0],resource=key[1],rule_id=decision.rule_id) for code in decision.issues)
            if obs is None or state in {'UNKNOWN','CONFLICT'}:continue
            policy=(decision.rule_id or 'process')+': '+decision.condition
            if decision.treatment is None:
                # Process risk is observable even when safe record treatment or
                # restore-block capability still needs proof. Do not invent a remedy.
                if process and process['active_at_cutoff'] is True:
                    operation='REPORT_RESTORE_RISK' if category=='BACKUP_ARCHIVE' else 'REPORT_ACTIVE_DATA_FLOW'
                    findings.append(step(operation,obs.system,obs.resource,obs.evidence_id))
                else:continue
            else:
                finding,remedy,verify,acceptable=TREATMENTS[decision.treatment]
                if decision.remediation_required is None:continue
                if decision.remediation_required:
                    findings.append(step(finding,obs.system,obs.resource,obs.evidence_id))
                    remediation.append(step(remedy,obs.system,obs.resource))
                verification.append(step(verify,obs.system,obs.resource,obs.evidence_id))
                if category=='BACKUP_ARCHIVE':
                    if truth(fields.get('archive_present')) is True:
                        verification.append(step('VERIFY_RECORD_PRESENT',obs.system,obs.resource,obs.evidence_id))
                        diagnostics['proofs'].append(dict(system=obs.system,resource=obs.resource,category=category,
                            state='PRESENT',policy=policy,source=obs.source,locator=obs.locator,evidence_id=obs.evidence_id,
                            observed=obs.observed,available=obs.available,scope=obs.scope,subject_linkage=self.linkage.get(key,[])))
                    else:diagnostics['issues'].append(dict(code='RETAINED_ARCHIVE_PRESENCE_UNKNOWN',resource=obs.resource))
            diagnostics['proofs'].append(dict(system=obs.system,resource=obs.resource,category=obs.category,
                state=obs.state,policy=policy,source=obs.source,locator=obs.locator,evidence_id=obs.evidence_id,
                observed=obs.observed,available=obs.available,scope=obs.scope,subject_linkage=self.linkage.get(key,[])))
        diagnostics['prediction_inferences']=[dict(resource=o.resource,evidence_id=o.evidence_id,source=o.source,locator=o.locator,available=o.available,basis=o.fields['prediction_inference']) for o in ledger.values() if 'prediction_inference' in o.fields]
        plan=plan_dependencies(remediation,list(ledger.values()),cutoff,risks)
        diagnostics['remediation_plan']=plan
        diagnostics['issues'].extend(dict(code=code) for code in plan['issues'])
        if not ledger:
            diagnostics["issues"].append({"code": "NO_LINKED_RESOURCE_PROOFS"})
        # A retained audit record or clean downstream copy does not establish
        # primary-account removal. Keep this coverage obligation explicit even
        # when the available partial observations are all compliant.
        if not any(p["category"] in {"USER_PROFILE", "ACCOUNT_TOMBSTONE"} for p in diagnostics["proofs"]):
            diagnostics["issues"].append({"code": "NO_PRIMARY_PROFILE_PROOF"})
        row,violations=build_decision(request['case_id'],True,findings,remediation,verification,
                                     issues=diagnostics['issues'],obligations=diagnostics['obligation_ledger'],allow_partial=True)
        diagnostics['planning_issues']=violations
        diagnostics['issues'].extend(dict(item) for item in violations)
        return row,diagnostics

    @staticmethod
    def row(request, status, steps):
        return {"case_id": request["case_id"], "deletion_status": status,
                "steps_json": json.dumps(steps, ensure_ascii=False, separators=(",", ":"))}
