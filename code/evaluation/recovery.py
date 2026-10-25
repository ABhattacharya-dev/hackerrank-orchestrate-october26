"""Actual recovery evaluation; labels are confined to this module."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import run
from evaluation.main import metrics
from ghostgraph.contract import read_csv,check_rows,resource_registry
from ghostgraph.evidence import EvidenceStore
ROOT=Path(__file__).resolve().parents[2]

def main():
    store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load()
    reports={}
    for tag,requests,output in [('recovery_sample','sample_deletion_requests.csv','.ghostgraph/recovery_sample.csv'),('prediction','deletion_requests.csv','output.prediction.candidate.csv')]:
        rows,ds,usage=run(ROOT,ROOT/'dataset'/requests,ROOT/output,allow_unresolved=True,tag=tag,mode='predict')
        errors=check_rows(rows,read_csv(ROOT/'dataset'/requests),store.citation_times,known_resource_pairs=resource_registry(store))
        report=dict(rows=len(rows),violations=errors,uncertain_cases=sum(bool(d['issues']) for d in ds),usage=usage)
        if tag=='recovery_sample':report['metrics']=metrics(rows,read_csv(ROOT/'dataset/sample_output.csv'))
        reports[tag]=report
    (ROOT/'.ghostgraph/recovery_results.json').write_text(json.dumps(reports,indent=2))
    final=reports['prediction']
    if not final['violations']:
        from ghostgraph.contract import write_csv
        write_csv(ROOT/'output.csv',read_csv(ROOT/'output.prediction.candidate.csv'))
    print({k:dict(rows=v['rows'],violations=len(v['violations']),uncertain=v['uncertain_cases'],metrics=v.get('metrics',{}).get('counts')) for k,v in reports.items()})
    return 2 if final['violations'] else 0
if __name__=='__main__':raise SystemExit(main())
