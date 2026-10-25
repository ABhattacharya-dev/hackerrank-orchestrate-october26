"""Research-only activity candidate graph and explicitly conditional ablations.

No public labels, numeric identity conventions or strict-certification hooks.
B/C deliberately test a weak ownership assumption and are not certification.
D requires separate eligible ownership corroboration before entering planning.
"""
from collections import defaultdict
from copy import copy
import re
from ghostgraph.contract import timestamp
from ghostgraph.evidence import identities
from ghostgraph.prediction import PredictionAuditor
from ghostgraph.temporal import scope_key
MAPPING={'COMPLETE':'SUCCESS','PARTIALLY_COMPLETE':'PARTIAL','NOT_STARTED':'FAILED'}
WINDOW=(-7200,1800)  # Reviewer hypothesis fixed before evaluation, not optimized.
REFS=['user_id','subject_reference','customer_reference','subject_selector','subject_ref']

def account_ids(row):
    import json
    return {s['resource_id'] for s in json.loads(row['steps_json']) if s['system_id']=='account_service'}

def worker(a):
    return (a.get('source_system')=='deletion_worker' and a.get('event_type')=='DELETE_RECORD'
            and a.get('target_system')=='account_service' and re.fullmatch(r'account_\d+',a.get('resource_id','')) is not None)

def raw_edges(q,activities,window=WINDOW):
    report=timestamp(q['reported_at']);out=[]
    for a in activities:
        if not worker(a):continue
        delta=timestamp(a['event_time'])-report
        if not window[0]<=delta<=window[1]:continue
        reasons=[]
        if a['reported_result']!=MAPPING.get(q['reported_status']):reasons.append('STATUS_RESULT_MISMATCH')
        if timestamp(a['event_time'])<timestamp(q['requested_at']):reasons.append('EVENT_PRECEDES_REQUEST')
        if timestamp(a['event_time'])>timestamp(q['audit_at']):reasons.append('EVENT_AFTER_AUDIT')
        if timestamp(q['reported_at'])>timestamp(q['audit_at']):reasons.append('WORKFLOW_REPORT_AFTER_AUDIT')
        out.append(dict(activity_id=a['activity_id'],resource_id=a['resource_id'],system_id=a['target_system'],
            event_time=a['event_time'],reported_result=a['reported_result'],workflow_status=q['reported_status'],
            requested_at=q['requested_at'],reported_at=q['reported_at'],audit_at=q['audit_at'],delta_seconds=delta,
            locator='system_activity.csv/'+a['activity_id'],rejections=reasons))
    return out

def ownership(store,identity,q,resource):
    cutoff=timestamp(q['audit_at']);tokens,uid,note=identity.resolve(q['email'],cutoff)
    own=[];foreign=[]
    if note and 'multiple' in note:return dict(tier='REJECTED',own=[],foreign=[],rejections=['AMBIGUOUS_HISTORICAL_IDENTITY'])
    scopes=defaultdict(list)
    for o in store.by_resource.get(('account_service',resource),[]):
        if max(o.available,o.observed)<=cutoff:scopes[scope_key(o)].append(o)
    for observations in scopes.values():
        newest=max(o.observed for o in observations)
        for o in observations:
            if o.observed!=newest:continue
            users={t for t in identities({k:o.fields[k] for k in REFS if k in o.fields}) if t.startswith('user_')}
            ref=dict(evidence_id=o.evidence_id,source=o.source,locator=o.locator,available=o.available,observed=o.observed)
            if uid and users and users!={uid}:foreign.append(ref)
            elif users and not uid:foreign.append(dict(ref,reason='subject cannot be resolved independently'))
            elif tokens & o.subject_tokens:own.append(ref)
    for when,system,target,linked,eid in store.links:
        if when<=cutoff and system=='account_service' and target==resource:
            users={t for t in linked if t.startswith('user_')}
            if uid and users and users!={uid}:foreign.append(dict(evidence_id=eid,available=when,locator='explicit catalog/'+resource))
            elif tokens & linked:own.append(dict(evidence_id=eid,available=when,locator='explicit catalog/'+resource))
    # Explicit source-resource references are scoped facts, not numeric IDs or
    # page-level co-occurrence. No state is inferred from this relationship.
    for token in tokens:
        for o in store.by_token.get(token,[]):
            if max(o.available,o.observed)>cutoff:continue
            users={t for t in identities({k:o.fields[k] for k in REFS if k in o.fields}) if t.startswith('user_')}
            if uid and users and users!={uid}:continue
            if any(o.fields.get(f)==resource for f in ['source_resource_id','upstream_resource_id','replica_of']):
                own.append(dict(evidence_id=o.evidence_id,source=o.source,locator=o.locator,available=o.available,observed=o.observed,relationship='typed source reference'))
    return dict(tier='REJECTED' if foreign else 'CORROBORATED' if own else 'TIME_STATUS_CANDIDATE',
                own=own,foreign=foreign,rejections=['FOREIGN_OR_CONFLICTING_OWNER'] if foreign else [])

class CandidateGraph:
    def __init__(self,requests,activities,store,identity,window=WINDOW):
        self.requests=requests;self.activities=activities;self.store=store;self.identity=identity;self.window=window
        self.raw={q['case_id']:raw_edges(q,activities,window) for q in requests}
    def select(self,q,variant,baseline):
        records=[dict(e) for e in self.raw[q['case_id']]]
        viable=[e for e in records if not e['rejections']]
        for e in records:
            e['case_id']=q['case_id'];e['selected']=False;e['tier']='REJECTED' if e['rejections'] else 'TIME_STATUS_CANDIDATE'
        if len(viable)!=1:
            for e in viable:e['rejections']=e['rejections']+['MULTIPLE_CANDIDATE_EVENTS']
            return None,records
        edge=next(e for e in records if e['activity_id']==viable[0]['activity_id'])
        verdict=ownership(self.store,self.identity,q,edge['resource_id']);edge.update(verdict)
        known=account_ids(baseline)
        if known and edge['resource_id'] not in known:
            edge['rejections'].append('DISAGREES_WITH_EXISTING_RESOURCE_SET')
        edge['already_grounded']=edge['resource_id'] in known
        if variant in ['C','D']:
            cutoff=timestamp(q['audit_at']);_,uid,_=self.identity.resolve(q['email'],cutoff);peers=[]
            for other in self.requests:
                if other['case_id']==q['case_id']:continue
                # Future requests, statuses and identity snapshots cannot influence
                # even collision rejection in an earlier case.
                if max(timestamp(other['requested_at']),timestamp(other['reported_at']))>cutoff:continue
                linked=[x for x in self.raw[other['case_id']] if not x['rejections'] and x['activity_id']==edge['activity_id']]
                if not linked:continue
                _,peer_uid,_=self.identity.resolve(other['email'],cutoff)
                if not uid or peer_uid!=uid:peers.append(other['case_id'])
            edge['conflicting_request_candidates']=peers
            if peers:edge['rejections'].append('CROSS_SUBJECT_EVENT_COLLISION')
        if variant=='D' and verdict['tier']!='CORROBORATED':edge['rejections'].append('NO_INDEPENDENT_OWNERSHIP_CORROBORATION')
        if edge['rejections']:edge['tier']='REJECTED';return None,records
        edge['selected']=True
        edge['assumption']='positive eligible ownership link' if verdict['tier']=='CORROBORATED' else 'unique time/status implies target; UNSUPPORTED OWNERSHIP HYPOTHESIS'
        return edge,records

class AssignmentAuditor(PredictionAuditor):
    """Isolated prediction ablation, never used by normal main.py/certification."""
    def __init__(self,store,identity,intent):
        super().__init__(store,identity,intent);self.edge=None
    def ledger(self,tokens,cutoff,subject_id=None):
        if not self.edge or self.edge.get('already_grounded'):
            return super().ledger(tokens,cutoff,subject_id)
        # The ordinary ledger needs a discovery seed. It is explicitly relabeled
        # as a research hypothesis before any policy/planner diagnostics consume it.
        original=self.store;view=copy(original);e=self.edge
        view.links=list(original.links)+[(timestamp(e['event_time']),e['system_id'],e['resource_id'],set(tokens),e['activity_id'])]
        self.store=view
        try:
            ledger,issues=super().ledger(tokens,cutoff,subject_id)
            key=(e['system_id'],e['resource_id'])
            self.linkage[key]=[dict(via='V6 research assignment, not direct catalog proof',tier=e['tier'],
                evidence_id=e['activity_id'],assumption=e['assumption'],corroboration=e['own'],locator=e['locator'])]
            return ledger,issues
        finally:self.store=original


def preserve_case_status(baseline,prediction,diagnostics):
    """An account-only discovery cannot discharge the whole case's proof gaps."""
    if baseline['deletion_status']!='COMPLETE' and prediction['deletion_status']=='COMPLETE':
        diagnostics['v6_whole_case_upgrade_blocked']='account evidence alone cannot establish overall deletion completion'
        return dict(baseline)
    return prediction
