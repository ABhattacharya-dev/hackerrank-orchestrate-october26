"""Descriptive source-CSV reproduction. Canonical IDs are evaluator-only here."""
import json
from collections import Counter
from pathlib import Path
from ghostgraph.contract import read_csv,timestamp
ROOT=Path(__file__).resolve().parents[2]
MAPPING={'COMPLETE':'SUCCESS','PARTIALLY_COMPLETE':'PARTIAL','NOT_STARTED':'FAILED'}
WINDOWS={'five_minutes':(-300,300),'wide_review':(-7200,1800),'half_hour':(-1800,1800),'two_hours':(-7200,7200),'one_day':(-86400,86400)}
def edges(q,activities,window,status=True,bounds=False):
    low,high=window;report=timestamp(q['reported_at'])
    return [a for a in activities if low<=timestamp(a['event_time'])-report<=high
        and (not status or a['reported_result']==MAPPING.get(q['reported_status']))
        and (not bounds or timestamp(q['requested_at'])<=timestamp(a['event_time'])<=timestamp(q['audit_at']))]
def account_ids(row):
    return sorted({s['resource_id'] for s in json.loads(row['steps_json']) if s['system_id']=='account_service'})
def main():
    activities=[a for a in read_csv(ROOT/'dataset/system_activity.csv') if a['event_type']=='DELETE_RECORD' and a['target_system']=='account_service' and a['source_system']=='deletion_worker']
    full=read_csv(ROOT/'dataset/deletion_requests.csv');base={r['case_id']:r for r in read_csv(ROOT/'output.csv')};sample=read_csv(ROOT/'dataset/sample_deletion_requests.csv');labels={r['case_id']:r for r in read_csv(ROOT/'dataset/sample_output.csv')}
    authorized=[q for q in full if base[q['case_id']]['deletion_status']!='NOT_APPLICABLE'];missing=[q for q in authorized if not account_ids(base[q['case_id']])]
    result={'mapping_assumption':MAPPING,'activity_count':len(activities),'authorized':len(authorized),'missing_account':len(missing),'windows':{}}
    for name,window in WINDOWS.items():
      for status in [False,True]:
       for bounds in [False,True]:
        report={};groups={'missing_full':missing,'grounded_full':[q for q in authorized if account_ids(base[q['case_id']])],'sample':sample}
        for group,qs in groups.items():
         unique=[];conflicts=[];matches=0;states=Counter();multi=0
         for q in qs:
          aa=edges(q,activities,window,status,bounds)
          if len(aa)>1:multi+=1
          if len(aa)!=1:continue
          a=aa[0];known=account_ids((labels if group=='sample' else base)[q['case_id']]);good=a['resource_id'] in known
          if good:matches+=1
          if known and not good:conflicts.append(dict(case_id=q['case_id'],activity_id=a['activity_id'],candidate=a['resource_id'],known=known,delta_seconds=timestamp(a['event_time'])-timestamp(q['reported_at'])))
          unique.append(dict(case_id=q['case_id'],activity=a['activity_id'],resource=a['resource_id'],delta_seconds=timestamp(a['event_time'])-timestamp(q['reported_at'])))
          if group=='missing_full':states[base[q['case_id']]['deletion_status']]+=1
         report[group]=dict(unique=len(unique),matches=matches,conflicts=conflicts,statuses=dict(states),multiple=multi,edges=unique)
        result['windows'][f'{name}:status={status}:bounds={bounds}']=report
    cache=ROOT/'.ghostgraph/v6';cache.mkdir(parents=True,exist_ok=True);(cache/'review_reproduction.json').write_text(json.dumps(result,indent=2))
    print({k:v for k,v in result.items() if k!='windows'})
    for k,v in result['windows'].items():
      if k.startswith(('five_minutes','wide_review')):print(k,{g:{x:len(y) if x=='conflicts' else y for x,y in r.items() if x!='edges'} for g,r in v.items()})
if __name__=='__main__':main()
