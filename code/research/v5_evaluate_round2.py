"""Prospective round two. First sealed probes are now observed regression only."""
import sys,json,hashlib,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.v5_evaluate import measure,decision
from research.v5_intent import AuthorizationIntent
from research.v5_round1 import AuthorizationIntent as Round1
from research.v5_prospective import PROSPECTIVE
from research.v5_probes import SEALED
from ghostgraph.intent import IntentClassifier
from ghostgraph.contract import read_csv,check_rows,resource_registry,write_csv
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.prediction import PredictionAuditor
from evaluation.main import metrics
ROOT=Path(__file__).resolve().parents[2];CACHE=ROOT/'.ghostgraph/v5'
def main():
    if (CACHE/'round2.json').exists():raise RuntimeError('Prospective round already evaluated; do not silently tune and rerun')
    freeze=json.loads((CACHE/'prospective_freeze.json').read_text())
    assert hashlib.sha256((ROOT/'code/research/v5_prospective.py').read_bytes()).hexdigest()==freeze['sha256']
    result=dict(implementation_sha256=hashlib.sha256((ROOT/'code/research/v5_intent.py').read_bytes()).hexdigest(),prospective_sha256=freeze['sha256'],intent={},competition={})
    for dataset,probes in [('observed_round1_regression',SEALED),('prospective_round2',PROSPECTIVE)]:
        models={'baseline':IntentClassifier(),'round1':Round1(),'v5':AuthorizationIntent()};rows=[];started=time.perf_counter()
        for name,text,expected,category in probes:
            row=dict(id=name,text=text,expected=expected,category=category)
            for arm,model in models.items():
                prediction=model.classify(text);row[arm]=decision(prediction);row[arm+'_source']=prediction['decision_source']
            rows.append(row)
        result['intent'][dataset]=dict(rows=rows,metrics={arm:measure(rows,arm) for arm in models},usage={arm:dict(calls=model.calls,cache_hits=model.cache_hits) for arm,model in models.items()},runtime_seconds=time.perf_counter()-started)
    store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load();assert not store.failures
    for dataset,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]:
        q=read_csv(ROOT/'dataset'/file);rows_by_arm={};reports={}
        for arm,model in [('baseline',IntentClassifier()),('v5',AuthorizationIntent())]:
            auditor=PredictionAuditor(store,IdentityIndex(ROOT/'dataset',store),model);start=time.perf_counter()
            pairs=[auditor.audit(r) for r in sorted(q,key=lambda x:x['case_id'])];rows,ds=map(list,zip(*pairs));rows_by_arm[arm]=rows
            report=dict(calls=model.calls,cache_hits=model.cache_hits,scope_decisions=model.scope_decisions,runtime_seconds=time.perf_counter()-start,
                violations=check_rows(rows,q,store.citation_times,known_resource_pairs=resource_registry(store)))
            if dataset=='sample':report['metrics']=metrics(rows,read_csv(ROOT/'dataset/sample_output.csv'))
            if arm=='v5':
                report['changed_rows']=[dict(before=b,after=r) for b,r in zip(rows_by_arm['baseline'],rows) if b!=r]
                (CACHE/(dataset+'_round2_diagnostics.json')).write_text(json.dumps(ds,indent=2))
            write_csv(CACHE/(dataset+'_round2_'+arm+'.csv'),rows)
            reports[arm]=report
        result['competition'][dataset]=reports
    result['byte_identical_full']=(CACHE/'full_round2_v5.csv').read_bytes()==(ROOT/'output.csv').read_bytes()
    (CACHE/'round2.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({key:value['metrics'] for key,value in result['intent'].items()},indent=2));print('Full byte identical:',result['byte_identical_full'])
if __name__=='__main__':main()
