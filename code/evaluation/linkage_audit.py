"""Evaluation-only audit of recurring missing-step linkage; never prediction input."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.contract import read_csv,timestamp
ROOT=Path(__file__).resolve().parents[2]
def main():
    results=json.loads((ROOT/'.ghostgraph/recovery_results.json').read_text())
    requests={r['case_id']:r for r in read_csv(ROOT/'dataset/sample_deletion_requests.csv')}
    store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load();identity=IdentityIndex(ROOT/'dataset',store)
    lines=['# Post-validity missing-link audit','',
        'Performed after the valid submission checkpoint. Public expected steps are used only to select evaluation targets. No answer enters prediction. Counts are retrieval diagnostics, not proof that unlinked or absent data belongs to a subject.','',
        '| Case | Missing resource / operation | Eligible direct observations | With subject identifier overlap | Eligible catalog links |','| --- | --- | ---: | ---: | ---: |']
    for case in results['recovery_sample']['metrics']['mismatches']:
        request=requests[case['case_id']];cutoff=timestamp(request['audit_at']);tokens,_,_=identity.resolve(request['email'],cutoff)
        for step in case['missing_steps']:
            key=step['system_id'],step['resource_id']
            obs=[o for o in store.by_resource.get(key,[]) if max(o.available,o.observed)<=cutoff]
            links=[r for r in store.links if r[0]<=cutoff and (r[1],r[2])==key and r[3]&tokens]
            lines.append(f"| {case['case_id']} | {key[1]} / {step['operation']} | {len(obs)} | {sum(bool(o.subject_tokens&tokens) for o in obs)} | {len(links)} |")
    lines+=['',
        'No new linkage rule was adopted. Known anonymous readbacks with null customer references and null lookup selectors cannot acquire ownership from a nearby trace or matching numeric suffix. Account-absence checks need independently grounded target IDs; an empty snapshot cannot supply them. Retained records without eligible subject links likewise cannot be assigned by canonical labels. Existing catalog-backed additional resources are not suppressed solely because reference answers omit them. The valid 518-row submission and all public metrics are preserved.']
    (ROOT/'code/evaluation/linkage_audit.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
