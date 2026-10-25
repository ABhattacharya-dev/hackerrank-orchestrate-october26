"""Competition inference, separate from high-assurance certification.

No labels or case-number conventions. Predictions retain uncertainty diagnostics.
"""
from dataclasses import replace
from .engine import Auditor
from .temporal import reconstruct
from .policy import PolicyEngine
from .evidence import is_value

class PredictionPolicy(PolicyEngine):
    def evaluate(self,category,state,fields,cutoff):
        decision=super().evaluate(category,state,fields,cutoff)
        if decision.applicability!='UNKNOWN' or decision.issues!=['POLICY_CONDITION_UNKNOWN']:
            return decision
        inferred=dict(fields)
        # Presence of a typed retained record supports preservation, never expiry
        # or deletion. A stable tombstone reference likewise remains permitted.
        if category=='SECURITY_AUDIT_LOG' and state=='PRESENT':
            return replace(decision,treatment='RETAIN',required_state='PRESENT',remediation_required=False,
                applicability='SATISFIED',issues=['PREDICTED_RETENTION_APPLICABILITY'])
        if category=='LEGAL_HOLD_RECORD' and state=='PRESENT':
            return replace(decision,treatment='RETAIN',required_state='PRESENT',remediation_required=False,
                applicability='SATISFIED',issues=['PREDICTED_HOLD_PRESERVATION'])
        if category=='ACCOUNT_TOMBSTONE' and fields.get('account_status')=='DELETED' and any(is_value(fields.get(k)) for k in ['user_id','subject_reference','customer_reference']):
            inferred['stable_reference_required']=True
        elif category=='SUPPORT_MESSAGE' and state in {'IDENTIFIABLE','REDACTED'}:
            # Preserve the conversation; only remove subject identifiers.
            inferred['shared_context']=True
        elif category=='SUPPORT_ATTACHMENT' and (is_value(fields.get('subject_reference')) or ('document_excerpt' in fields and len(__import__('re').findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+',fields['document_excerpt']))==1)):
            inferred['subject_only']=True
        elif category=='BACKUP_ARCHIVE' and state in {'ACTIVE','BLOCKED'}:
            inferred['restore_block_supported']=True
        else:return decision
        predicted=super().evaluate(category,state,inferred,cutoff)
        if category=='BACKUP_ARCHIVE' and 'archive_present' not in fields:
            predicted.verification_obligations=['VERIFY_RESTORE_BLOCKED']
        predicted.issues.append('PREDICTED_POLICY_APPLICABILITY')
        return predicted

class PredictionAuditor(Auditor):
    def __init__(self,*args):
        super().__init__(*args)
        self.policy_engine=PredictionPolicy(self.store.dataset/'deletion_rules.csv')

    def ledger(self,tokens,cutoff,subject_id=None):
        from .restore_prediction import console_facts,infer_restore
        from collections import defaultdict
        from copy import copy
        original=self.store
        scoped=copy(original)
        scoped.by_token=defaultdict(list,{k:list(v) for k,v in original.by_token.items()})
        scoped.by_resource=defaultdict(list,{k:list(v) for k,v in original.by_resource.items()})
        scoped.observations=list(original.observations)
        for meta,text in getattr(original,'documents',[]):
            facts=console_facts(text,meta)
            if not facts:continue
            linked=set();references=[]
            for when,system,resource,aliases,eid in original.links:
                if when<=cutoff and system==facts['service'] and resource==facts['resource'] and aliases & tokens:
                    linked.update(aliases & tokens)
                    references.append(dict(evidence_id=eid,available=when))
            key=facts['service'],facts['resource']
            inferred=infer_restore(facts,meta,cutoff,linked,original.by_resource.get(key,[]))
            if inferred:
                inferred.available=max([inferred.available]+[r['available'] for r in references])
                inferred.fields['prediction_inference']=dict(inferred.fields['prediction_inference'],catalog_links=references)
                scoped.observations.append(inferred);scoped.by_resource[key].append(inferred)
                for token in inferred.subject_tokens:scoped.by_token[token].append(inferred)
        self.store=scoped
        try:return super().ledger(tokens,cutoff,subject_id)
        finally:self.store=original

    def reduce_state(self,observations,cutoff,claims):
        # A later operation claim remains a warning, not proof of its result.
        # For prediction, carry forward direct observations of known copies.
        strict=reconstruct(observations,cutoff,claims)
        eligible=[replace(o,kind="observation") if o.kind=="prediction_inference" else o for o in observations if max(o.available,o.observed)<=cutoff]
        result=reconstruct(eligible,cutoff)
        if any(i['code']=='SCOPE_ALIGNMENT_UNKNOWN' for i in result.issues):
            aligned=[replace(o,fields=dict(o.fields,_source_origin='logical-service')) if o.scope=='logical' else o for o in eligible]
            result=reconstruct(aligned,cutoff)
        if result.state=='UNKNOWN' and result.witness is not None and result.witness.state=='ABSENT' and all(i['code']=='COPY_COVERAGE_UNPROVEN' for i in result.issues):
            result.state='ABSENT'
            result.issues=[dict(code='PREDICTION_KNOWN_SCOPE_ABSENCE')]
        result.issues.extend(dict(i,certification_only=True) for i in strict.issues if i not in result.issues)
        return result
