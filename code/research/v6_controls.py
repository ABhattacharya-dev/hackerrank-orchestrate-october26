"""Fixed placebo schedules/status permutations, no fitting to public labels."""
import json,random
from collections import Counter
from datetime import datetime,timedelta
from pathlib import Path
from ghostgraph.contract import read_csv
from research.v6_assignment import raw_edges,account_ids
ROOT=Path(__file__).resolve().parents[2]
def main():
 q=read_csv(ROOT/'dataset/deletion_requests.csv');baseline={r['case_id']:r for r in read_csv(ROOT/'output.csv')};qs=[r for r in q if baseline[r['case_id']]['deletion_status']!='NOT_APPLICABLE'];activities=read_csv(ROOT/'dataset/system_activity.csv')
 def measure(requests):
  unique=[];agreements=0;wrong=[];grounded_unique=0
  for r in requests:
   eligible=[e for e in raw_edges(r,activities) if not e['rejections']]
   if len(eligible)!=1:continue
   e=eligible[0];unique.append(dict(case_id=r['case_id'],activity_id=e['activity_id'],resource_id=e['resource_id']))
   known=account_ids(baseline[r['case_id']])
   if known:
    grounded_unique+=1
    if e['resource_id'] in known:agreements+=1
    else:wrong.append(dict(case_id=r['case_id'],resource=e['resource_id'],known=sorted(known)))
  return dict(unique_count=len(unique),grounded_unique=grounded_unique,grounded_agreements=agreements,grounded_disagreements=wrong,edges=unique)
 result={'unmutated':measure(qs),'schedule_shifts':{},'status_permutations':[],'seed':611,'permutations':30}
 for days in [-30,-7,-1,1,7,30]:
  shifted=[]
  for r in qs:
   copy=dict(r)
   for key in ['requested_at','reported_at','audit_at']:
    copy[key]=(datetime.fromisoformat(r[key].replace('Z','+00:00'))+timedelta(days=days)).isoformat().replace('+00:00','Z')
   shifted.append(copy)
  result['schedule_shifts'][str(days)]=measure(shifted)
 rng=random.Random(611);statuses=[r['reported_status'] for r in qs]
 for i in range(30):
  shuffled=statuses.copy();rng.shuffle(shuffled)
  result['status_permutations'].append(measure([dict(r,reported_status=s) for r,s in zip(qs,shuffled)]))
 (ROOT/'.ghostgraph/v6/placebos.json').write_text(json.dumps(result,indent=2))
 for name,r in [('unmutated',result['unmutated'])]+list(result['schedule_shifts'].items()):
  print(name,{k:len(v) if isinstance(v,list) else v for k,v in r.items() if k!='edges'})
 print('Permutation unique min/max:',min(r['unique_count'] for r in result['status_permutations']),max(r['unique_count'] for r in result['status_permutations']))
 print('Permutation grounded disagreements:',sum(len(r['grounded_disagreements']) for r in result['status_permutations']))
if __name__=='__main__':main()
