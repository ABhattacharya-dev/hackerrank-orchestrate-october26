"""Independent public-sample evaluation. Labels never enter the predictor."""

from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import run
from ghostgraph.contract import read_csv


def step_key(step, citation=True):
    keys = ["phase", "system_id", "resource_id", "operation", "state"]
    if citation: keys.append("evidence_id")
    return tuple(step[k] for k in keys)


def metrics(predictions, labels):
    predicted = {r['case_id']:r for r in predictions}
    truth = {r['case_id']:r for r in labels}
    if set(predicted) != set(truth): raise ValueError('evaluation case IDs differ')
    counts=Counter()
    mismatches=[]
    for cid,target in sorted(truth.items()):
        actual=predicted[cid]
        ps,ts=json.loads(actual['steps_json']),json.loads(target['steps_json'])
        counts['cases']+=1
        counts['status_correct']+=actual['deletion_status']==target['deletion_status']
        counts['exact_sequences']+=ps==ts
        counts['exact_rows']+=ps==ts and actual['deletion_status']==target['deletion_status']
        counts['predicted_steps']+=len(ps);counts['expected_steps']+=len(ts)
        for citation,name in [(True,'exact_step_matches'),(False,'structural_step_matches')]:
            counts[name]+=sum((Counter(step_key(s,citation) for s in ps)&Counter(step_key(s,citation) for s in ts)).values())
        align={tuple(s[k] for k in ['phase','system_id','resource_id','operation']):s for s in ps}
        for expected in ts:
            key=tuple(expected[k] for k in ['phase','system_id','resource_id','operation'])
            actual_step=align.get(key,{})
            counts['expected_fields']+=len(expected)
            counts['field_matches']+=sum(actual_step.get(k)==v for k,v in expected.items())
            if expected['evidence_id']:
                counts['expected_citations']+=1
                counts['canonical_citation_matches']+=actual_step.get('evidence_id')==expected['evidence_id']
        if ps!=ts or actual['deletion_status']!=target['deletion_status']:
            mismatches.append(dict(case_id=cid, predicted_status=actual['deletion_status'],expected_status=target['deletion_status'],
                missing=[s for s in ts if step_key(s) not in {step_key(p) for p in ps}],
                extra=[s for s in ps if step_key(s) not in {step_key(t) for t in ts}]))
    ratio=lambda a,b: counts[a]/counts[b] if counts[b] else None
    return dict(counts=counts,status_accuracy=ratio('status_correct','cases'),
                exact_row_accuracy=ratio('exact_rows','cases'), exact_sequence_accuracy=ratio('exact_sequences','cases'),
                step_precision=ratio('exact_step_matches','predicted_steps'), step_recall=ratio('exact_step_matches','expected_steps'),
                structural_step_precision=ratio('structural_step_matches','predicted_steps'),structural_step_recall=ratio('structural_step_matches','expected_steps'),
                field_accuracy=ratio('field_matches','expected_fields'),canonical_evidence_accuracy=ratio('canonical_citation_matches','expected_citations'),
                mismatches=mismatches)


def evaluate(root):
    predictions,diagnostics,usage=run(root,root/'dataset/sample_deletion_requests.csv',root/'.ghostgraph/sample_predictions.csv',allow_unresolved=True,tag='sample')
    result=metrics(predictions,read_csv(root/'dataset/sample_output.csv'))
    (root/'.ghostgraph/sample_metrics.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='mismatches'},indent=2))
    return result


if __name__=='__main__':evaluate(Path(__file__).resolve().parents[2])
