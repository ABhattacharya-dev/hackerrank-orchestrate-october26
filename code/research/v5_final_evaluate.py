"""Final, explicitly post-feedback regression; never relabel as unseen testing."""
import json,time,hashlib
from pathlib import Path
from research.v5_evaluate import measure,decision
from research.v5_intent import AuthorizationIntent
from research.v5_probes import DEVELOPMENT,SEALED
from research.v5_prospective import PROSPECTIVE
from research.v5_continuation import PROBES
from ghostgraph.intent import IntentClassifier
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.prediction import PredictionAuditor
from ghostgraph.contract import read_csv,check_rows,resource_registry,write_csv
from evaluation.main import metrics
ROOT=Path(__file__).resolve().parents[2];CACHE=ROOT/'.ghostgraph/v5'
def main():
 result={'intent':{},'competition':{}}
 for name,probes in [('development',DEVELOPMENT),('observed40',SEALED),('observed24',PROSPECTIVE),('continuation16',PROBES)]:
  arms={'baseline':IntentClassifier(),'v5':AuthorizationIntent()};rows=[];start=time.perf_counter()
  for id,text,expected,*category in probes:
   row={'id':id,'expected':expected,'category':category[0] if category else 'continuation'}
   for arm,model in arms.items():row[arm]=decision(model.classify(text))
   rows.append(row)
  result['intent'][name]={'rows':rows,'metrics':{a:measure(rows,a) for a in arms},'runtime_seconds':time.perf_counter()-start,'calls':{a:m.calls for a,m in arms.items()}}
 store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load()
 for name,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]:
  q=read_csv(ROOT/'dataset'/file);pred={};reports={}
  for arm,model in [('baseline',IntentClassifier()),('v5',AuthorizationIntent())]:
   auditor=PredictionAuditor(store,IdentityIndex(ROOT/'dataset',store),model);start=time.perf_counter()
   pairs=[auditor.audit(r) for r in sorted(q,key=lambda x:x['case_id'])];rows,ds=map(list,zip(*pairs));pred[arm]=rows
   reports[arm]={'runtime_seconds':time.perf_counter()-start,'calls':model.calls,'cache_hits':model.cache_hits,'violations':check_rows(rows,q,store.citation_times,known_resource_pairs=resource_registry(store))}
   if name=='sample':reports[arm]['metrics']=metrics(rows,read_csv(ROOT/'dataset/sample_output.csv'))
   if arm=='v5':reports[arm]['changed_rows']=[{'before':b,'after':r} for b,r in zip(pred['baseline'],rows) if b!=r]
   write_csv(CACHE/(name+'_final_'+arm+'.csv'),rows)
  result['competition'][name]=reports
 result['full_byte_identical']=(CACHE/'full_final_v5.csv').read_bytes()==(ROOT/'output.csv').read_bytes()
 (CACHE/'final.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({'intent':{k:{a:m['correct'] for a,m in v['metrics'].items()} for k,v in result['intent'].items()},'competition':{k:{a:{'changes':len(v.get('changed_rows',[])),'violations':len(v['violations']),'counts':v.get('metrics',{}).get('counts',{})} for a,v in r.items()} for k,r in result['competition'].items()},'identical':result['full_byte_identical']},indent=2))
if __name__=='__main__':main()
