"""Independent fictional CLI dataset; no participant labels or evidence reused."""
import csv,json
from pathlib import Path

TIME='2026-02-03T12:00:00Z'
EMAIL='river.owner@example.test'

def csv_file(path,fields,rows):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def dataset(root):
    d=Path(root)/'dataset';(d/'evidence').mkdir(parents=True)
    csv_file(d/'user_identities.csv',['user_id','name','email','phone','email_hash','updated_at'],[
        dict(user_id='user_901',name='Fictional River',email=EMAIL,phone='',email_hash='',updated_at=TIME)])
    csv_file(d/'user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[])
    csv_file(d/'system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[])
    csv_file(d/'deletion_rules.csv',['rule_id','data_category','condition','required_action'],[
        dict(rule_id='rule_fixture',data_category='USER_PROFILE',condition='Always',required_action='DELETE')])
    csv_file(d/'evidence_files.csv',['file_id','file_path','origin','captured_at'],[
        dict(file_id='evidence_fixture',file_path='evidence/readback.json',origin='fictional_account_readback',captured_at=TIME)])
    (d/'evidence/readback.json').write_text(json.dumps(dict(captured_at=TIME,records=[
        dict(resource_id='account_731',record_type='USER_PROFILE',status_code=200,user_id='user_901',email=EMAIL,observed_at=TIME)])))
    requests(root,['If the replacement device arrives, erase my membership. It has not arrived; do not act yet.'])
    return d

def requests(root,texts,email=EMAIL):
    rows=[dict(case_id=f'fictional_{i:02}',email=email,requested_at=TIME,reported_at=TIME,audit_at='2026-02-04T12:00:00Z',reported_status='NOT_STARTED',request_text=text) for i,text in enumerate(texts)]
    csv_file(Path(root)/'dataset/deletion_requests.csv',['case_id','email','requested_at','reported_status','reported_at','audit_at','request_text'],rows)
    return rows
