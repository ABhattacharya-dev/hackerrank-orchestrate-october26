"""One-shot held-out evaluation plus full competition impact. No protected writes."""
from pathlib import Path
import sys,json,time,hashlib
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.intent import IntentClassifier
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.prediction import PredictionAuditor
from ghostgraph.contract import read_csv,write_csv,check_rows,resource_registry
from evaluation.main import metrics
from research.v5_intent import AuthorizationIntent
from research.v5_probes import DEVELOPMENT,SEALED
from research.v4_intent import PROBES
ROOT=Path(__file__).resolve().parents[2];CACHE=ROOT/'.ghostgraph/v5'

def decision(result):return None if result['low_confidence'] or result.get('ambiguous') else result['authorized']
def name(value):return 'authorized' if value is True else 'rejected' if value is False else 'defer'
def measure(rows,arm):
    confusion={e:{p:0 for p in ['authorized','rejected','defer']} for e in ['authorized','rejected','defer']}
    for r in rows:confusion[name(r['expected'])][name(r[arm])]+=1
    positives=sum(r['expected'] is True for r in rows);nonpositive=len(rows)-positives
    negatives=sum(r['expected'] is False for r in rows)
    false=sum(r['expected'] is not True and r[arm] is True for r in rows)
    missed=sum(r['expected'] is True and r[arm] is not True for r in rows)
    return dict(confusion=confusion,total=len(rows),correct=sum(r['expected']==r[arm] for r in rows),false_authorizations=false,
        false_authorization_rate=false/nonpositive if nonpositive else None,missed_authorizations=missed,
        missed_authorization_rate=missed/positives if positives else None,correct_rejections=sum(r['expected'] is False and r[arm] is False for r in rows),negatives=negatives,
        failures=[r['id'] for r in rows if r['expected']!=r[arm]])

def main():
    CACHE.mkdir(exist_ok=True)
    protected={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['output.csv','code.zip']}
    frozen=json.loads((CACHE/'implementation_freeze.json').read_text());probe_freeze=json.loads((CACHE/'probe_freeze.json').read_text())
    assert hashlib.sha256((ROOT/'code/research/v5_intent.py').read_bytes()).hexdigest()==frozen['sha256']
    assert hashlib.sha256((ROOT/'code/research/v5_probes.py').read_bytes()).hexdigest()==probe_freeze['sha256']
    if (CACHE/'evaluation.json').exists():raise RuntimeError('Sealed evaluation already exists; do not tune/rerun it silently')
    result=dict(implementation_sha256=frozen['sha256'],probe_sha256=probe_freeze['sha256'],intent={},competition={})
    for dataset,probes in [('development',DEVELOPMENT),('known_v4',PROBES),('sealed',SEALED)]:
        baseline=IntentClassifier();v5=AuthorizationIntent();rows=[];start=time.perf_counter()
        for item in probes:
            identifier,text,expected=item[:3];a=baseline.classify(text);b=v5.classify(text)
            rows.append(dict(id=identifier,text=text,category=item[3] if len(item)>3 else identifier,expected=expected,
                baseline=decision(a),v5=decision(b),baseline_source=a['decision_source'],v5_source=b['decision_source'],evidence=b['evidence']))
        result['intent'][dataset]=dict(rows=rows,baseline=measure(rows,'baseline'),v5=measure(rows,'v5'),runtime_seconds=time.perf_counter()-start,
            baseline_calls=baseline.calls,v5_calls=v5.calls,baseline_cache_hits=baseline.cache_hits,v5_cache_hits=v5.cache_hits)
    store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load();assert not store.failures
    for dataset,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]:
        requests=read_csv(ROOT/'dataset'/file);runs={};baseline_rows=None
        for arm,model in [('baseline',IntentClassifier()),('v5',AuthorizationIntent())]:
            auditor=PredictionAuditor(store,IdentityIndex(ROOT/'dataset',store),model)
            start=time.perf_counter();pairs=[auditor.audit(r) for r in sorted(requests,key=lambda x:x['case_id'])];rows,diagnostics=map(list,zip(*pairs))
            errors=check_rows(rows,requests,store.citation_times,known_resource_pairs=resource_registry(store))
            if arm=='baseline':baseline_rows=rows
            report=dict(runtime_seconds=time.perf_counter()-start,violations=errors,calls=model.calls,cache_hits=model.cache_hits,rows_changed=sum(r!=b for r,b in zip(rows,baseline_rows)),
                changed=[dict(before=b,after=r) for r,b in zip(rows,baseline_rows) if r!=b],uncertain_cases=sum(bool(d['issues']) for d in diagnostics))
            if dataset=='sample':report['metrics']=metrics(rows,read_csv(ROOT/'dataset/sample_output.csv'))
            if dataset=='full':
                report['not_applicable']=[r['case_id'] for r in rows if r['deletion_status']=='NOT_APPLICABLE']
            write_csv(CACHE/(dataset+'_'+arm+'.csv'),rows)
            (CACHE/(dataset+'_'+arm+'_diagnostics.json')).write_text(json.dumps(diagnostics,indent=2))
            runs[arm]=report
        result['competition'][dataset]=runs
    result['byte_identical_full']=(CACHE/'full_v5.csv').read_bytes()==(ROOT/'output.csv').read_bytes()
    result['api_usage']=dict(input_tokens=0,output_tokens=0,paid_calls=0,api_cost_usd=0,local_token_units_applicable=False)
    for p,digest in protected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest
    (CACHE/'evaluation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:{a:v[a] for a in ['baseline','v5']} for k,v in result['intent'].items() if k!='development'},indent=2))
    print('Full byte-identical:',result['byte_identical_full'],'Full changes:',result['competition']['full']['v5']['rows_changed'])
if __name__=='__main__':main()
