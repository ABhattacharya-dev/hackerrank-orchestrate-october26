"""Measure Tier B novel fact admission against actual original JSON records.

Proposal discovery uses only original owner fields and resolved request aliases,
not public labels. Accepted observations are never inserted into production here.
"""
from pathlib import Path
import sys,json,time
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.v4_audit import json_records
from research.v4_source_review import validate_source,OWNER_FIELDS
from ghostgraph.contract import read_csv,timestamp
from ghostgraph.evidence import EvidenceStore,identities,DEFAULTS,prefix
from ghostgraph.identity import IdentityIndex
ROOT=Path(__file__).resolve().parents[2]

def main():
    start=time.perf_counter();store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load();identity=IdentityIndex(ROOT/'dataset',store)
    records=[]
    for meta in store.manifest:
        path=store.dataset/meta['file_path']
        if path.suffix!='.json':continue
        for locator,record in json_records(json.loads(path.read_text())):
            owners={k:record[k] for k in OWNER_FIELDS if k in record}
            if isinstance(record.get('profile'),dict):owners.update({k:record['profile'][k] for k in OWNER_FIELDS if k in record['profile']})
            records.append((meta,locator,record,identities(owners)))
    facts=[];counts=Counter();new=[]
    for request in read_csv(ROOT/'dataset/deletion_requests.csv'):
        cutoff=timestamp(request['audit_at']);tokens,uid,note=identity.resolve(request['email'],cutoff)
        if uid is None:continue
        for meta,locator,record,owner_tokens in records:
            overlap=tokens&owner_tokens
            if not overlap:continue
            system=record.get('system')
            parts=locator.split('/')[1:]
            if not system and len(parts)>1 and parts[0]=='service_exports':system=parts[1]
            if not system and len(parts)>1 and parts[0]=='snapshots':
                doc=json.loads((store.dataset/meta['file_path']).read_text());system=doc['snapshots'][int(parts[1])].get('data_store')
            system=system or DEFAULTS.get(prefix(record['resource_id']),(None,None))[0]
            if not system:continue
            proposal=dict(subject=sorted(overlap)[0],system_id=system,resource_id=record['resource_id'],evidence_id=meta['file_id'],locator=locator)
            observation,reason=validate_source(proposal,store,identity,request)
            if observation is None:counts[reason]+=1
            else:
                existing=any(o.evidence_id==observation.evidence_id and proposal['subject'] in o.subject_tokens and max(o.available,o.observed)<=cutoff for o in store.by_resource.get(observation.key,[]))
                counts['accepted_already_normalized' if existing else 'accepted_novel']+=1
                if not existing:new.append(dict(case_id=request['case_id'],proposal=proposal,reason=reason))
            facts.append(dict(case_id=request['case_id'],proposal=proposal,accepted=observation is not None,reason=reason))
    result=dict(counts=counts,novel=new,proposals=facts,runtime_seconds=time.perf_counter()-start,hosted_ai_calls=0,input_api_tokens=0,output_api_tokens=0,api_cost_usd=0)
    (ROOT/'.ghostgraph/v4/source_validation.json').write_text(json.dumps(result,indent=2))
    lines=['# V4 accepted and rejected original-source proposals','',
        'Actual deterministic proposals, not LLM outputs or hidden labels. Accepted facts are already normalized; none is admitted as novel. Subjects are grounded request aliases, and exact original owner fields are available at the listed locators.','',
        '| Request | Resource | Source system | Evidence | Original locator | Accepted | Validation rationale |','| --- | --- | --- | --- | --- | --- | --- |']
    for row in facts:
        proposal=row['proposal']
        lines.append(f"| {row['case_id']} | {proposal['resource_id']} | {proposal['system_id']} | {proposal['evidence_id']} | {proposal['locator']} | {row['accepted']} | {row['reason']} |")
    (ROOT/'code/research/v4_source_facts.md').write_text('\n'.join(lines)+'\n')
    print(dict(counts=counts,novel=new,runtime_seconds=result['runtime_seconds']))
if __name__=='__main__':main()
