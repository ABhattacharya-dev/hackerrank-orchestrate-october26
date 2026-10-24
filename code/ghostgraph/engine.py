"""Deterministic resource ledger, supplied-policy application and proof-backed plans."""

from collections import defaultdict
from dataclasses import replace
import json

from .contract import ordered, read_csv, step, timestamp
from .evidence import DEFAULTS, Observation, identities, prefix

TREATMENTS = {
    "DELETE": ("REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT", {"ABSENT"}),
    "REDACT": ("REPORT_EXPOSED_PII", "REDACT_RECORD", "VERIFY_RECORD_REDACTED", {"REDACTED"}),
    "ANONYMIZE": ("REPORT_EXPOSED_PII", "ANONYMIZE_RECORD", "VERIFY_RECORD_ANONYMIZED", {"ANONYMIZED"}),
    "RETAIN": (None, None, "VERIFY_RECORD_PRESENT", {"PRESENT"}),
    "FLOW": ("REPORT_ACTIVE_DATA_FLOW", "DISABLE_DATA_FLOW", "VERIFY_DATA_FLOW_DISABLED", {"DISABLED"}),
    "RESTORE": ("REPORT_RESTORE_RISK", "BLOCK_RESTORE", "VERIFY_RESTORE_BLOCKED", {"BLOCKED"}),
}


class Auditor:
    def __init__(self, store, identity, intent):
        self.store, self.identity, self.intent = store, identity, intent
        self.rules = read_csv(store.dataset / "deletion_rules.csv")
        self.rule_by_category = {r["data_category"]: r for r in self.rules}
        if len(self.rule_by_category) != len(self.rules):
            raise ValueError("overlapping category rules need explicit condition resolution")
        if any(r["required_action"] not in {"DELETE", "REDACT", "ANONYMIZE", "RETAIN"} for r in self.rules):
            raise ValueError("unsupported policy action")

    def ledger(self, tokens, cutoff, subject_id=None):
        selected = {}
        linkage = defaultdict(list)
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
                if compatible and scope["category"] == category and policy.get("required_action") == "DELETE":
                    # Restrict absence to tables that actually cover that system/category.
                    # Generic replicas export all platform resource records; primary rows
                    # and replica rows remain separate scopes.
                    observations.append(Observation(scope["meta"]["file_id"], scope["meta"]["file_path"],
                        "table:" + scope["table"] + "/exhaustive-resource-lookup", timestamp(scope["meta"]["captured_at"]),
                        timestamp(scope["meta"]["captured_at"]), key[0], key[1],
                        DEFAULTS[prefix(key[1])][1], "ABSENT", tokens,
                        {"exhaustive_lookup": True}, scope["table"], 4))
            if not observations:
                issues.append(dict(code="NO_STATE_PROOF", system=key[0], resource=key[1]))
                continue
            # Different physical replicas must not erase one another. A later
            # authoritative logical readback covers the canonical resource, while
            # a physical replica remains evidence of a copy until its own removal.
            physical = defaultdict(list)
            for obs in observations:
                physical[obs.scope].append(obs)
            latest = []
            for scope, items in physical.items():
                newest_time = max(o.observed for o in items)
                simultaneous = [o for o in items if o.observed == newest_time]
                quality = max(o.quality for o in simultaneous)
                simultaneous = [o for o in simultaneous if o.quality == quality]
                if len({o.state for o in simultaneous}) > 1:
                    issues.append(dict(code="CONFLICT", system=key[0], resource=key[1], scope=scope))
                # Prefer violating state on unresolved equal-time disagreement;
                # still flag it, and strict export refuses the unresolved case.
                simultaneous.sort(key=lambda o: (o.state not in {"PRESENT", "IDENTIFIABLE", "ACTIVE"}, o.evidence_id, o.locator))
                latest.append(simultaneous[0])
            violating_copies = [o for o in latest if o.scope != "logical" and o.state in {"PRESENT", "IDENTIFIABLE", "ACTIVE"}]
            if violating_copies:
                obs = max(violating_copies, key=lambda o: (o.observed, o.quality, o.evidence_id))
            else:
                obs = max(latest, key=lambda o: (o.observed, o.quality, o.evidence_id))
            selected[key] = obs
        self.linkage = linkage
        return selected, issues

    def treatment(self, obs, cutoff):
        if obs.category == "DATA_FLOW": return "FLOW", "process configuration"
        if obs.category == "BACKUP_ARCHIVE": return "RESTORE", "retained archive with restore controls"
        rule = self.rule_by_category.get(obs.category)
        if not rule: raise ValueError("no supplied policy for " + obs.category)
        # Conditions are checked against observation structure where represented.
        # Retaining a security/legal record is conservative when no expiry is given;
        # no expiration period is invented and no retained record is deleted.
        expiry = obs.fields.get("retention_until") or obs.fields.get("retained_until")
        if rule["required_action"] == "RETAIN" and expiry and timestamp(expiry) < cutoff:
            return None, "retention expired; supplied rules do not specify subsequent treatment"
        return rule["required_action"], rule["rule_id"] + ": " + rule["condition"]

    def audit(self, request):
        cutoff = timestamp(request["audit_at"])
        intent = self.intent.classify(request["request_text"])
        diagnostics = {"case_id": request["case_id"], "intent": intent, "issues": [], "proofs": []}
        if intent["low_confidence"]:
            diagnostics["issues"].append({"code": "INTENT_LOW_CONFIDENCE"})
        if intent.get('ambiguous'):
            return self.row(request,"INCOMPLETE",[]),diagnostics
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
        findings, remediation, verification = [], [], []
        for key, obs in ledger.items():
            if obs.state == "UNKNOWN":
                diagnostics["issues"].append({"code": "INSUFFICIENT_OBSERVED_FIELDS", "resource": obs.resource})
                continue
            action, policy = self.treatment(obs, cutoff)
            if action is None:
                diagnostics["issues"].append({"code": "POLICY_UNDERSPECIFIED", "resource": obs.resource})
                continue
            finding, remedy, verify, acceptable = TREATMENTS[action]
            compliant = obs.state in acceptable
            if action in {"REDACT", "ANONYMIZE"} and obs.state == "ABSENT":
                # Missing records cannot be asserted to be redacted/retained.
                diagnostics["issues"].append({"code": "REQUIRED_RECORD_MISSING", "resource": obs.resource})
                continue
            if action == "RETAIN" and not compliant:
                diagnostics["issues"].append({"code": "RETAINED_RECORD_MISSING", "resource": obs.resource})
                continue
            if not compliant:
                findings.append(step(finding, obs.system, obs.resource, obs.evidence_id))
                remediation.append(step(remedy, obs.system, obs.resource))
            verification.append(step(verify, obs.system, obs.resource, obs.evidence_id))
            diagnostics["proofs"].append({"system": obs.system, "resource": obs.resource,
                "category": obs.category, "state": obs.state, "policy": policy,
                "source": obs.source, "locator": obs.locator, "evidence_id": obs.evidence_id,
                "observed": obs.observed, "available": obs.available, "scope": obs.scope})
            diagnostics["proofs"][-1]["subject_linkage"] = self.linkage.get(key, [])
        if not ledger:
            diagnostics["issues"].append({"code": "NO_LINKED_RESOURCE_PROOFS"})
        # A retained audit record or clean downstream copy does not establish
        # primary-account removal. Keep this coverage obligation explicit even
        # when the available partial observations are all compliant.
        if not any(p["category"] in {"USER_PROFILE", "ACCOUNT_TOMBSTONE"} for p in diagnostics["proofs"]):
            diagnostics["issues"].append({"code": "NO_PRIMARY_PROFILE_PROOF"})
        if findings:
            status = "INCOMPLETE"
            for item in verification: item["evidence_id"] = ""
            steps = findings + remediation + verification
        elif not verification:
            # No unsupported status is exported as a trusted answer. The CLI may
            # explicitly write a provisional candidate plus unresolved diagnostics.
            status, steps = "INCOMPLETE", []
        else:
            # This is the best available provisional assessment, not certification
            # of complete coverage. Any issue blocks strict export in the CLI.
            status, steps = "COMPLETE", verification
        return self.row(request, status, ordered(steps)), diagnostics

    @staticmethod
    def row(request, status, steps):
        return {"case_id": request["case_id"], "deletion_status": status,
                "steps_json": json.dumps(steps, ensure_ascii=False, separators=(",", ":"))}
