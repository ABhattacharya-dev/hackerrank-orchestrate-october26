"""Staged, time-bounded evidence graph and worker candidate investigation.

Timestamp proximity only proposes a candidate. It cannot provide subject ownership
or prove deletion. Independent direct/catalog/copy-reference evidence is required.
"""
from collections import defaultdict
from ghostgraph.contract import timestamp
from ghostgraph.evidence import identities,DEFAULTS,prefix,EMAIL

REFERENCE_FIELDS=('source_resource_id','upstream_resource_id','replica_of')


def foreign(obs,uid,identity,cutoff):
    refs=identities({k:obs.fields[k] for k in ['user_id','subject_reference','customer_reference','subject_ref'] if k in obs.fields})
    stable={t for t in refs if t.startswith('user_')}
    if stable and (uid is None or stable!={uid}):return True
    for field in ['email','owner_email','requester_email','customer_email']:
        for email in EMAIL.findall(str(obs.fields.get(field,''))):
            _,owner,note=identity.resolve(email,cutoff)
            if owner and uid and owner!=uid:return True
            if note and 'multiple' in note:return True
    return False


def graph(store,identity,request,reverse=True):
    cutoff=timestamp(request['audit_at']);tokens,uid,note=identity.resolve(request['email'],cutoff)
    nodes={};rejected=[]
    if uid is None or (note and 'multiple' in note):return nodes,[dict(stage='rejected',reason='no unique stable subject')]
    eligible=[o for o in store.observations if max(o.available,o.observed)<=cutoff and o.kind=='observation']
    for o in eligible:
        if o.subject_tokens & tokens and not foreign(o,uid,identity,cutoff):
            nodes.setdefault(o.key,dict(stage='direct',available=max(o.available,o.observed),proofs=[dict(evidence_id=o.evidence_id,locator=o.locator,relationship='strong subject in record')]))
    for when,system,rid,aliases,eid in store.links:
        if when<=cutoff and aliases & tokens:
            nodes.setdefault((system,rid),dict(stage='direct',available=when,proofs=[dict(evidence_id=eid,locator=rid,relationship='explicit catalog')]))
    pending=True
    while pending:
        pending=False
        for o in eligible:
            if o.key in nodes:
                for field in REFERENCE_FIELDS:
                    source=o.fields.get(field)
                    if not isinstance(source,str) or prefix(source) not in DEFAULTS:continue
                    source_key=DEFAULTS[prefix(source)][0],source
                    if source_key in nodes:continue
                    target=[x for x in eligible if x.key==source_key]
                    if target:
                        latest=max(x.observed for x in target)
                        if any(foreign(x,uid,identity,cutoff) for x in target if x.observed==latest):continue
                    nodes[source_key]=dict(stage='corroborated_derived',available=max(o.available,o.observed,nodes[o.key]['available']),proofs=nodes[o.key]['proofs']+[dict(evidence_id=o.evidence_id,locator=o.locator,relationship=field+' child-to-source',source_resource=o.resource)])
                    pending=True
                continue
            if not reverse:continue
            if foreign(o,uid,identity,cutoff):
                continue
            for field in REFERENCE_FIELDS:
                source=o.fields.get(field)
                if not isinstance(source,str) or prefix(source) not in DEFAULTS:continue
                key=DEFAULTS[prefix(source)][0],source
                if key not in nodes:continue
                nodes[o.key]=dict(stage='corroborated_derived',available=max(o.available,o.observed,nodes[key]['available']),
                    proofs=nodes[key]['proofs']+[dict(evidence_id=o.evidence_id,locator=o.locator,relationship=field,source_system=key[0],source_resource=source)])
                pending=True;break
    return nodes,rejected


def temporal_candidates(store,identity,requests,window=300,graphs=None):
    candidates=[]
    for request in requests:
        cutoff=timestamp(request['audit_at']);reported=timestamp(request['reported_at']);start=timestamp(request['requested_at'])
        nodes=graphs[request['case_id']] if graphs is not None else graph(store,identity,request,reverse=False)[0]
        tokens,uid,note=identity.resolve(request['email'],cutoff)
        for claim in store.claims:
            if claim.get('event_type')!='DELETE_RECORD' or claim.get('target_system')!='account_service':continue
            when=timestamp(claim['event_time']);delta=when-reported
            if abs(delta)>window:continue
            key=claim['target_system'],claim['resource_id']
            stage='weak_candidate';reason='time proximity only; no independent subject corroboration'
            proof=nodes.get(key)
            explicit=identities(claim.get('details',''))
            foreign_users={t for t in explicit if t.startswith('user_')} - ({uid} if uid else set())
            foreign_contact=False
            for email in EMAIL.findall(claim.get('details','')):
                _,owner,identity_note=identity.resolve(email,cutoff)
                if (owner and owner!=uid) or (identity_note and 'multiple' in identity_note):foreign_contact=True
            if proof is None and uid and explicit & tokens and not foreign_users and not foreign_contact:
                proof=dict(stage='corroborated_derived',available=when,proofs=[dict(evidence_id=claim['activity_id'],locator='system_activity.csv:'+claim['activity_id'],relationship='explicit unique request-subject identifier and target in worker event')])
            if when>cutoff or when<start or reported>cutoff:stage='rejected';reason='outside request/cutoff interval or unavailable workflow timestamp'
            elif uid is None:stage='rejected';reason='ambiguous or unresolved subject'
            elif foreign_users or foreign_contact:stage='rejected';reason='explicit event subject contradicts candidate subject'
            elif proof:stage='corroborated_derived';reason='independent time-eligible graph ownership; worker state claim not trusted'
            candidates.append(dict(case_id=request['case_id'],subject_id=uid,activity_id=claim['activity_id'],resource_id=key[1],system_id=key[0],
                event_time=claim['event_time'],available=proof['available'] if proof else when,delta_seconds=delta,stage=stage,reason=reason,proofs=proof['proofs'] if proof else [],reported_result=claim.get('reported_result'),uncertainty='ownership unproven' if proof is None else 'ownership corroborated; operation result is not observed state'))
    # Same action cannot independently identify two distinct/unknown subjects.
    owners=defaultdict(set)
    for c in candidates:
        if c['stage']=='corroborated_derived':owners[c['activity_id']].add(c['subject_id'])
    per_request=defaultdict(list)
    for c in candidates:
        if c['stage']=='corroborated_derived':per_request[c['case_id']].append(c)
    for c in candidates:
        if len(owners[c['activity_id']])>1:
            c.update(stage='rejected',reason='cross-subject assignment collision')
        # Multiple corroborated targets are allowed as a workflow only because
        # each has independent ownership proof, never because one is nearest.
        c['corroborated_workflow_targets']=len(per_request[c['case_id']])
    return candidates
