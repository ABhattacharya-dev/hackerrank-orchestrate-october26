"""Milestone 2 public acceptance: intent and grounded identity, not audit verdicts."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.contract import read_csv,timestamp
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier

def evaluate(root):
    data=root/'dataset';store=EvidenceStore(data,root/'.ghostgraph/extraction').load()
    index=IdentityIndex(data,store);model=IntentClassifier()
    labels={r['case_id']:r['deletion_status']!='NOT_APPLICABLE' for r in read_csv(data/'sample_output.csv')}
    results=[]
    for request in read_csv(data/'sample_deletion_requests.csv'):
        result=model.classify(request['request_text']);cutoff=timestamp(request['audit_at'])
        proof=index.explain(request['email'],cutoff)
        results.append(dict(case_id=request['case_id'],intent_pass=result['authorized']==labels[request['case_id']] and not result['low_confidence'],
            subject_linked=proof['subject_id'] is not None,
            provenance_valid=bool(proof['aliases']) and all(a['proofs'] and all(p['available']<=cutoff for p in a['proofs']) for a in proof['aliases'])))
    (root/'.ghostgraph/intent_identity_acceptance.json').write_text(json.dumps(results,indent=2))
    assert len(results)==32 and all(r['intent_pass'] and r['subject_linked'] and r['provenance_valid'] for r in results)
    print('PASS: 32/32 sample intents and 32/32 grounded subject resolutions; no full-audit correctness claim.')

if __name__=='__main__':evaluate(Path(__file__).resolve().parents[2])
