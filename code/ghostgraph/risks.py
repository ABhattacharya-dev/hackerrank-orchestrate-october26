"""Current process configuration and dependency planning, separate from CSV order."""
from collections import defaultdict
import re
from .contract import ordered, timestamp
from .evidence import truth

PROCESS_WORDS={'sync':'synchronization','import':'import','index':'indexing','replic':'replication','restore':'restore'}


def process_analysis(observations,temporal,claims,cutoff):
    result=[]
    for key,state in sorted(temporal.items()):
        candidates=[o for o in observations if o.kind=='observation' and o.key==key and max(o.available,o.observed)<=cutoff
                    and o.category in {'DATA_FLOW','BACKUP_ARCHIVE'}]
        if not candidates:continue
        newest=max(o.observed for o in candidates)
        recent=[o for o in candidates if o.observed==newest]
        fields=recent[0].fields
        text=' '.join(str(o.fields.get(k,'')) for o in recent for k in ['connector_name','mode','destination','process_type']).lower()
        words=re.split(r'[^a-z]+',text)
        kinds=sorted({meaning for word,meaning in PROCESS_WORDS.items() if any(token.startswith(word) for token in words)})
        if recent[0].category=='BACKUP_ARCHIVE':kinds=['restore']
        active=True if state['state']=='ACTIVE' else False if state['state'] in {'DISABLED','BLOCKED'} else None
        issues=[]
        if any((active is True and truth(o.fields.get('enabled')) is False) or (active is False and truth(o.fields.get('enabled')) is True) for o in recent):
            active=None;issues.append('PROCESS_CONFIGURATION_CONFLICT')
        history=[dict(activity_id=c['activity_id'],event_type=c['event_type'],event_time=c['event_time'],claim=True)
                 for c in claims if c.get('resource_id')==key[1] and timestamp(c['event_time'])<=cutoff]
        result.append(dict(system=key[0],resource=key[1],category=recent[0].category,types=kinds or ['data flow'],active_at_cutoff=active,
            observed_state=state['state'],historical_events=history,issues=issues,
            evidence=[dict(evidence_id=o.evidence_id,locator=o.locator,available=o.available,observed=o.observed) for o in recent]))
    return result


def plan_dependencies(remediation,observations,cutoff,processes=()):
    def node(step):return step['operation'],step['system_id'],step['resource_id']
    steps={node(s):s for s in remediation};edges=set()
    controls=[n for n in steps if n[0] in {'DISABLE_DATA_FLOW','BLOCK_RESTORE'}]
    records=[n for n in steps if n[0] in {'DELETE_RECORD','REDACT_RECORD','ANONYMIZE_RECORD'}]
    for control in controls:
        for record in records:edges.add((control,record))
    by_resource=defaultdict(list)
    for n in records:by_resource[n[2]].append(n)
    for obs in observations:
        if max(obs.available,obs.observed)>cutoff:continue
        for key in ['source_resource_id','upstream_resource_id','replica_of']:
            upstream=obs.fields.get(key)
            for child in by_resource.get(obs.resource,[]):
                for parent in by_resource.get(upstream,[]):
                    if child!=parent:edges.add((child,parent))
    canonical=[node(s) for s in ordered(list(remediation))]
    rank={n:i for i,n in enumerate(canonical)}
    pending=set(steps);execution=[]
    while pending:
        ready=sorted([n for n in pending if not any(b==n and a in pending for a,b in edges)],key=lambda n:rank[n])
        if not ready:break
        execution.extend(ready);pending.difference_update(ready)
    conflicts=[dict(before=a,after=b) for a,b in sorted(edges) if rank[a]>rank[b]]
    issues=(['DEPENDENCY_CYCLE'] if pending else [])+(['CANONICAL_DEPENDENCY_ORDER_CONFLICT'] if conflicts else [])
    preconditions=[]
    if records:
        for process in processes:
            required='BLOCK_RESTORE' if process['category']=='BACKUP_ARCHIVE' else 'DISABLE_DATA_FLOW'
            control=(required,process['system'],process['resource'])
            if process['active_at_cutoff'] is None or (process['active_at_cutoff'] and control not in steps):
                preconditions.append(dict(system=process['system'],resource=process['resource'],required_control=required))
    if preconditions:issues.append('UNRESOLVED_PROCESS_PRECONDITION')
    return dict(execution_order=execution if not pending and not preconditions else None,canonical_order=canonical,
                unresolved_preconditions=preconditions,
                dependencies=[dict(before=a,after=b) for a,b in sorted(edges)],ordering_conflicts=conflicts,issues=issues)
