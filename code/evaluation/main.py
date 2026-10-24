"""Independent public-sample evaluation. Labels never enter the predictor."""
from collections import Counter, defaultdict, deque
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import run
from ghostgraph.contract import read_csv


def step_key(step, citation=True):
    keys = ['phase', 'system_id', 'resource_id', 'operation', 'state']
    if citation: keys.append('evidence_id')
    return tuple(step[k] for k in keys)


def identity(step):
    return tuple(step[k] for k in ['phase','system_id','resource_id','operation'])


def compare_steps(predicted, expected):
    """Align operations without masking wrong states/citations as omissions.

    Occurrence queues preserve duplicate multiplicity for diagnostic inputs.
    Ordering compares common step identities, so omissions alone are not called
    ordering errors. Absolute step-number shifts remain field/sequence errors.
    """
    remaining=defaultdict(deque)
    for i,step in enumerate(predicted):remaining[identity(step)].append((i,step))
    pairs=[];missing=[];used=set()
    for i,step in enumerate(expected):
        if remaining[identity(step)]:
            j,actual=remaining[identity(step)].popleft()
            pairs.append((i,j,step,actual));used.add(j)
        else:missing.append(step)
    extra=[s for i,s in enumerate(predicted) if i not in used]
    wrong_states=[dict(identity=identity(e),expected=e['state'],predicted=p['state']) for _,_,e,p in pairs if e['state']!=p['state']]
    wrong_evidence=[dict(identity=identity(e),expected=e['evidence_id'],predicted=p['evidence_id']) for _,_,e,p in pairs if e['evidence_id']!=p['evidence_id']]
    matched_order=[j for _,j,_,_ in pairs]
    wrong_order=matched_order!=sorted(matched_order)
    return dict(missing_steps=missing,extra_steps=extra,wrong_states=wrong_states,
                wrong_evidence=wrong_evidence,incorrect_ordering=wrong_order),pairs


def metrics(predictions, labels):
    predicted = {r['case_id']:r for r in predictions}
    truth = {r['case_id']:r for r in labels}
    if len(predicted)!=len(predictions) or len(truth)!=len(labels):raise ValueError('duplicate evaluation case IDs')
    if set(predicted) != set(truth) or not truth:raise ValueError('evaluation case IDs differ or empty')
    counts=Counter();mismatches=[]
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
        difference,pairs=compare_steps(ps,ts)
        aligned={i:p for i,_,_,p in pairs}
        for i,expected in enumerate(ts):
            actual_step=aligned.get(i,{})
            counts['expected_fields']+=len(expected)
            counts['field_matches']+=sum(actual_step.get(k)==v for k,v in expected.items())
            if expected['evidence_id']:
                counts['expected_citations']+=1
                counts['canonical_citation_matches']+=actual_step.get('evidence_id')==expected['evidence_id']
        counts['ordering_errors']+=difference['incorrect_ordering']
        for key in ['missing_steps','extra_steps','wrong_states','wrong_evidence']:counts[key]+=len(difference[key])
        if ps!=ts or actual['deletion_status']!=target['deletion_status']:
            # Retain original multiset comparison for compatibility and auditability.
            def subtract(a,b):
                available=Counter(step_key(s) for s in b);out=[]
                for s in a:
                    key=step_key(s)
                    if available[key]:available[key]-=1
                    else:out.append(s)
                return out
            mismatches.append(dict(case_id=cid,predicted_status=actual['deletion_status'],expected_status=target['deletion_status'],
                incorrect_classification=actual['deletion_status']!=target['deletion_status'],
                missing=subtract(ts,ps),extra=subtract(ps,ts),**difference))
    ratio=lambda a,b:counts[a]/counts[b] if counts[b] else None
    precision=ratio('exact_step_matches','predicted_steps');recall=ratio('exact_step_matches','expected_steps')
    f1=2*counts['exact_step_matches']/(counts['predicted_steps']+counts['expected_steps']) if counts['predicted_steps']+counts['expected_steps'] else None
    return dict(counts=counts,status_accuracy=ratio('status_correct','cases'),
                exact_row_accuracy=ratio('exact_rows','cases'),exact_sequence_accuracy=ratio('exact_sequences','cases'),
                step_precision=precision,step_recall=recall,step_f1=f1,
                structural_step_precision=ratio('structural_step_matches','predicted_steps'),structural_step_recall=ratio('structural_step_matches','expected_steps'),
                field_accuracy=ratio('field_matches','expected_fields'),canonical_evidence_accuracy=ratio('canonical_citation_matches','expected_citations'),mismatches=mismatches)


def evaluate(root):
    predictions,diagnostics,usage=run(root,root/'dataset/sample_deletion_requests.csv',root/'.ghostgraph/sample_predictions.csv',allow_unresolved=True,tag='sample')
    result=metrics(predictions,read_csv(root/'dataset/sample_output.csv'))
    (root/'.ghostgraph/sample_metrics.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='mismatches'},indent=2))
    return result

if __name__=='__main__':evaluate(Path(__file__).resolve().parents[2])
