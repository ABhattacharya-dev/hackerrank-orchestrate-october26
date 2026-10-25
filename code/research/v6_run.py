"""Controlled end-to-end ablations. Canonical labels are opened only to score."""
import json,time,hashlib
from pathlib import Path
from collections import Counter
from ghostgraph.contract import read_csv,write_csv,check_rows,resource_registry
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.authorization import AuthorizationIntent
from ghostgraph.prediction import PredictionAuditor
from research.v6_assignment import CandidateGraph,AssignmentAuditor,account_ids,preserve_case_status
from evaluation.main import metrics,step_key
ROOT=Path(__file__).resolve().parents[2];CACHE=ROOT/'.ghostgraph/v6'
def main():
    CACHE.mkdir(parents=True,exist_ok=True);store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load();assert not store.failures
    results={}
    for name,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]:
        requests=read_csv(ROOT/'dataset'/file);identity=IdentityIndex(ROOT/'dataset',store);model=AuthorizationIntent();baseline=PredictionAuditor(store,identity,model)
        start=time.perf_counter();pairs=[baseline.audit(q) for q in sorted(requests,key=lambda r:r['case_id'])];rows,ds=map(list,zip(*pairs));byid={r['case_id']:r for r in rows}
        runs={'A':dict(rows=rows,diagnostics=ds,runtime_seconds=time.perf_counter()-start,calls=model.calls,cache_hits=model.cache_hits,edges=[])}
        graph=CandidateGraph(requests,read_csv(ROOT/'dataset/system_activity.csv'),store,identity)
        for variant in ['B','C','D']:
            model=AuthorizationIntent();auditor=AssignmentAuditor(store,identity,model);out=[];ds=[];edges=[];start=time.perf_counter()
            for q in sorted(requests,key=lambda r:r['case_id']):
                row=byid[q['case_id']]
                edge,records=graph.select(q,variant,row) if row['deletion_status']!='NOT_APPLICABLE' else (None,[])
                edges.extend(records);auditor.edge=edge
                if edge:
                    prediction,d=auditor.audit(q);d['v6_assignment']=edge
                    prediction=preserve_case_status(row,prediction,d)
                else:prediction=row;d={'case_id':q['case_id'],'unchanged':True}
                out.append(prediction);ds.append(d)
            runs[variant]=dict(rows=out,diagnostics=ds,edges=edges,runtime_seconds=time.perf_counter()-start,calls=model.calls,cache_hits=model.cache_hits)
        reports={}
        # Public labels enter only after every variant has produced predictions.
        truth=read_csv(ROOT/'dataset/sample_output.csv') if name=='sample' else None
        for variant,run in runs.items():
            write_csv(CACHE/(name+'_'+variant+'.csv'),run['rows'])
            (CACHE/(name+'_'+variant+'_edges.json')).write_text(json.dumps(run['edges'],indent=2))
            (CACHE/(name+'_'+variant+'_diagnostics.json')).write_text(json.dumps(run['diagnostics'],indent=2))
            changes=[]
            for old,new in zip(rows,run['rows']):
                if old==new:continue
                p,n=json.loads(old['steps_json']),json.loads(new['steps_json'])
                common={step_key(s):s['step_no'] for s in p}
                changes.append(dict(case_id=new['case_id'],before_status=old['deletion_status'],after_status=new['deletion_status'],
                    added=[s for s in n if step_key(s) not in common],removed=[s for s in p if step_key(s) not in {step_key(x) for x in n}],
                    renumbered=sum(s['step_no']!=common[step_key(s)] for s in n if step_key(s) in common)))
            report={k:v for k,v in run.items() if k not in ['rows','diagnostics','edges']}
            report.update(changes=changes,violations=check_rows(run['rows'],requests,store.citation_times,known_resource_pairs=resource_registry(store)),
                selected_edges=[e for e in run['edges'] if e['selected']],rejections=dict(Counter(reason for e in run['edges'] for reason in e['rejections'])))
            if truth:
                report['metrics']=metrics(run['rows'],truth)
                truth_ids={r['case_id']:account_ids(r) for r in truth}
                report['incorrect_account_assignments']=[e for e in report['selected_edges'] if e['resource_id'] not in truth_ids[e['case_id']]]
            reports[variant]=report
        results[name]=reports
        if name=='full':assert (CACHE/'full_A.csv').read_bytes()==(ROOT/'output.csv').read_bytes()
    (CACHE/'results.json').write_text(json.dumps(results,indent=2))
    for name,reports in results.items():
        for v,r in reports.items():
            print(name,v,'changes',len(r['changes']),'selected',len(r['selected_edges']),'violations',len(r['violations']),
                  'metrics',r.get('metrics',{}).get('counts',{}),'incorrectIDs',len(r['incorrect_account_assignments']) if 'incorrect_account_assignments' in r else 'UNLABELED')
if __name__=='__main__':main()
