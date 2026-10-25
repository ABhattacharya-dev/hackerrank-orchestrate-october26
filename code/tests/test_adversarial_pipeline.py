"""New M7 on-disk scenarios: real parsers, identity, temporal engine and CLI.

Fixtures are authored here, never derived from sample answers. Supplied policy is
copied read-only; all evidence and identities are written under temporary roots.
"""
import contextlib
import csv
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from main import run
from ghostgraph.contract import check_rows,read_csv,resource_registry,timestamp
from ghostgraph.evidence import EvidenceStore
from evaluation.verify import verify_provenance

SOURCE=Path(__file__).resolve().parents[2]
BASE='2026-04-01T00:'
def at(minute):return BASE+f'{minute:02}:00Z'


class Fixture:
    def __init__(self,root):
        self.root=Path(root);self.data=self.root/'dataset';self.data.mkdir()
        (self.data/'evidence').mkdir();self.manifest=[]
        shutil.copy2(SOURCE/'dataset/deletion_rules.csv',self.data/'deletion_rules.csv')
        self.csv('user_identities.csv',['user_id','name','email','phone','email_hash','updated_at'],[
            dict(user_id='user_780',name='Fictional Customer',email='after@example.test',phone='',email_hash='',updated_at=at(55))])
        self.csv('user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[])
        self.csv('system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[])
    def csv(self,name,fields,rows):
        with (self.data/name).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    def artifact(self,name,body,minute,origin='account_service'):
        path=self.data/'evidence'/name
        path.write_text(body if isinstance(body,str) else json.dumps(body))
        self.manifest.append(dict(file_id='evidence_'+str(len(self.manifest)+1),file_path='evidence/'+name,origin=origin,captured_at=at(minute)))
    def records(self,name,records,minute,origin='account_service'):
        self.artifact(name,dict(records=records,captured_at=at(minute)),minute,origin)
    def request(self,cid='independent',email='before@example.test',minute=35,text='Permanently erase my profile and personal records.'):
        return dict(case_id=cid,email=email,requested_at=at(0),reported_status='COMPLETE',reported_at=at(1),audit_at=at(minute),request_text=text)
    def finish(self,requests):
        self.csv('evidence_files.csv',['file_id','file_path','origin','captured_at'],self.manifest)
        self.csv('deletion_requests.csv',list(requests[0]),requests)
    def execute(self,requests,partial=False):
        self.finish(requests)
        with contextlib.redirect_stdout(io.StringIO()):
            return run(self.root,self.data/'deletion_requests.csv',self.root/'output.csv',allow_unresolved=partial)
    def validate(self,rows,diagnostics,requests):
        store=EvidenceStore(self.data,self.root/'.ghostgraph/extraction').load()
        if store.failures:raise AssertionError(store.failures)
        errors=check_rows(rows,requests,store.citation_times,known_resource_pairs=resource_registry(store))
        if errors:raise AssertionError(errors)
        verify_provenance(rows,diagnostics,requests)
        return store


class AdversarialPipelineTests(unittest.TestCase):
    def fixture(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        return Fixture(tmp.name)

    def test_deleted_primary_identical_table_in_replica_and_live_import(self):
        f=self.fixture()
        f.artifact('primary.sql',f"""CREATE TABLE snapshot_scope(origin_system TEXT,captured_at TEXT,database_id TEXT);
INSERT INTO snapshot_scope VALUES('account_service','{at(20)}','primary_database');
CREATE TABLE customer_profiles(resource_id TEXT,email TEXT,subject_reference TEXT);
""",20)
        f.artifact('replica.sql',f"""CREATE TABLE snapshot_scope(origin_system TEXT,captured_at TEXT,database_id TEXT);
INSERT INTO snapshot_scope VALUES('account_service','{at(20)}','regional_replica');
CREATE TABLE customer_profiles(resource_id TEXT,email TEXT,subject_reference TEXT);
INSERT INTO customer_profiles VALUES('account_807','before@example.test','user_780');
""",20)
        f.records('connector.json',[dict(resource_id='data_flow_611',subject_reference='user_780',enabled=True,
            connector_name='nightly_import_sync',source_resource_id='account_807')],22,'integration_service')
        f.csv('system_activity.csv',['activity_id','event_time','event_type','source_system','target_system','resource_id','reported_result','details'],[
            dict(activity_id='activity_1',event_time=at(15),event_type='DELETE_RECORD',source_system='account_service',target_system='account_service',resource_id='account_807',reported_result='SUCCESS',details='Primary database deletion claimed complete')])
        requests=[f.request()];rows,diags,_=f.execute(requests)
        f.validate(rows,diags,requests)
        steps=json.loads(rows[0]['steps_json'])
        self.assertEqual(rows[0]['deletion_status'],'INCOMPLETE')
        self.assertEqual([(s['operation'],s['resource_id']) for s in steps if s['phase']=='REMEDIATION'],[
            ('DISABLE_DATA_FLOW','data_flow_611'),('DELETE_RECORD','account_807')])
        finding=next(s for s in steps if s['operation']=='REPORT_REMAINING_RECORD')
        self.assertEqual(finding['evidence_id'],'evidence_2')
        scopes=diags[0]['temporal_ledger'][0]['scopes']
        self.assertEqual({s['state'] for s in scopes},{'PRESENT','ABSENT'})
        self.assertEqual(len({s['scope'] for s in scopes}),2)

    def test_history_cutoff_conflict_and_later_capture_do_not_backdate_state(self):
        f=self.fixture()
        f.csv('user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[
            dict(audit_id='audit_1',user_id='user_780',event_time=at(30),field_name='email',old_value='before@example.test',new_value='after@example.test')])
        base=dict(resource_id='account_906',subject_reference='user_780')
        f.records('earlier.json',[dict(base,email='before@example.test',result='FOUND')],10)
        f.records('contradiction.json',[dict(base,result='FOUND'),dict(base,result='NOT_FOUND')],40)
        f.records('later_capture.json',[dict(base,result='NOT_FOUND',observed_at=at(20))],59)
        requests=[f.request('history_conflict','after@example.test',40),f.request('history_before',minute=25),
                  f.request('history_boundary','after@example.test',30)]
        rows,diags,_=f.execute(requests,partial=True)
        byid={r['case_id']:r for r in rows};ds={d['case_id']:d for d in diags}
        for cid in ['history_before','history_boundary']:
            d=ds[cid];self.assertEqual(d['subject_id'],'user_780')
            self.assertFalse(d['issues']);self.assertEqual(byid[cid]['deletion_status'],'INCOMPLETE')
            steps=json.loads(byid[cid]['steps_json'])
            self.assertEqual(steps[0]['evidence_id'],'evidence_1')
            f.validate([byid[cid]],[d],[next(r for r in requests if r['case_id']==cid)])
        self.assertEqual(byid['history_conflict']['steps_json'],'[]')
        self.assertIn('CONFLICT',{i['code'] for i in ds['history_conflict']['issues']})
        self.assertFalse(any(p['evidence_id']=='evidence_3' for d in diags for p in d['proofs']))
        # A conflicting fixture must fail strict export, not manufacture a verdict.
        (f.root/'output.csv').unlink()
        with self.assertRaisesRegex(ValueError,'unresolved cases'):f.execute(requests)
        self.assertFalse((f.root/'output.csv').exists())

    def test_retained_tombstone_legal_security_and_restore_without_deletion(self):
        f=self.fixture()
        f.records('retained.json',[
            dict(resource_id='tombstone_509',subject_reference='user_780',record_type='ACCOUNT_TOMBSTONE',account_status='DELETED',stable_reference_required=True,name=None,email=None,phone=None,email_hash=None),
            dict(resource_id='audit_record_312',subject_reference='user_780',retention_until='2027-04-01T00:00:00Z'),
            dict(resource_id='legal_hold_415',subject_reference='user_780',hold_active=True,hold_until='2027-04-01T00:00:00Z'),
            dict(resource_id='backup_928',subject_reference='user_780',restore_allowed=True,restore_block_supported=True,archive_present=True),
        ],20,'records_snapshot')
        # Establish the request's historical alias without relying on future current identity.
        f.csv('user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[
            dict(audit_id='audit_1',user_id='user_780',event_time=at(5),field_name='email',old_value='before@example.test',new_value='after@example.test')])
        requests=[f.request()];rows,diags,_=f.execute(requests);f.validate(rows,diags,requests)
        steps=json.loads(rows[0]['steps_json'])
        self.assertEqual([s['operation'] for s in steps if s['phase']=='REMEDIATION'],['BLOCK_RESTORE'])
        self.assertEqual({s['resource_id'] for s in steps if s['operation']=='VERIFY_RECORD_PRESENT'},
                         {'audit_record_312','legal_hold_415','backup_928'})
        self.assertTrue(any(s['operation']=='VERIFY_RECORD_REDACTED' and s['resource_id']=='tombstone_509' for s in steps))
        self.assertTrue(all(s['evidence_id']=='' for s in steps if s['phase']!='FINDING'))

    def test_repeated_user_cutoffs_redaction_and_request_order_are_isolated(self):
        f=self.fixture()
        common=dict(resource_id='tombstone_820',subject_reference='user_780',account_status='DELETED',stable_reference_required=True)
        f.records('unredacted.json',[dict(common,email='before@example.test')],10,'identity_service')
        f.records('redacted.json',[dict(common,email=None,name=None,phone=None,email_hash=None)],30,'identity_service')
        f.csv('user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[
            dict(audit_id='audit_1',user_id='user_780',event_time=at(5),field_name='email',old_value='before@example.test',new_value='after@example.test')])
        requests=[f.request('repeat_z_early',minute=20),f.request('repeat_a_late',minute=30)]
        rows,diags,_=f.execute(requests);f.validate(rows,diags,requests)
        result={r['case_id']:r for r in rows}
        self.assertEqual(result['repeat_a_late']['deletion_status'],'COMPLETE')
        self.assertEqual(result['repeat_z_early']['deletion_status'],'INCOMPLETE')
        late=json.loads(result['repeat_a_late']['steps_json'])
        self.assertEqual([(s['operation'],s['evidence_id']) for s in late],[('VERIFY_RECORD_REDACTED','evidence_2')])
        rows2,_,_=f.execute(list(reversed(requests)))
        self.assertEqual(rows,rows2)

    def test_cross_user_historical_alias_collision_does_not_authorize_foreign_plan(self):
        f=self.fixture()
        f.csv('user_audit_log.csv',['audit_id','user_id','event_time','field_name','old_value','new_value'],[
            dict(audit_id='audit_1',user_id='user_780',event_time=at(5),field_name='email',old_value='shared@example.test',new_value='one@example.test'),
            dict(audit_id='audit_2',user_id='user_781',event_time=at(6),field_name='email',old_value='shared@example.test',new_value='two@example.test')])
        f.records('customers.json',[dict(resource_id='account_717',user_id='user_780',email='shared@example.test'),
            dict(resource_id='account_718',user_id='user_781',email='shared@example.test')],20)
        request=f.request('collision','shared@example.test')
        rows,diags,_=f.execute([request],partial=True)
        self.assertEqual(rows[0]['steps_json'],'[]')
        self.assertIn('AMBIGUOUS_IDENTITY',{i['code'] for i in diags[0]['issues']})
        own=f.request('unique','one@example.test');rows,diags,_=f.execute([own]);f.validate(rows,diags,[own])
        self.assertEqual({s['resource_id'] for s in json.loads(rows[0]['steps_json'])},{'account_717'})

    def test_multilingual_negation_runs_cli_without_deletion_findings(self):
        f=self.fixture()
        f.records('live.json',[dict(resource_id='account_930',subject_reference='user_780',email='before@example.test')],20)
        texts=['Ne supprimez rien : je souhaite uniquement recevoir une copie de mes factures.',
               'No eliminen mis datos; solo necesito corregir el número de teléfono.',
               '계정을 삭제하지 마세요. 저장된 데이터 사본만 필요합니다.']
        requests=[f.request('negation_'+str(i),text=text) for i,text in enumerate(texts)]
        rows,diags,_=f.execute(requests);f.validate(rows,diags,requests)
        self.assertTrue(all(r['deletion_status']=='NOT_APPLICABLE' and r['steps_json']=='[]' for r in rows))

    def test_missing_manifest_artifact_is_detectable_and_blocks_final_export(self):
        f=self.fixture()
        f.manifest.append(dict(file_id='evidence_1',file_path='evidence/missing.json',origin='account_service',captured_at=at(20)))
        request=f.request('missing')
        with self.assertRaisesRegex(ValueError,'ingestion failures'):f.execute([request])
        self.assertFalse((f.root/'output.csv').exists())
        report=json.loads((f.root/'.ghostgraph/ingestion_report.json').read_text())
        self.assertEqual(report['failures'][0]['error_type'],'MissingFile')

if __name__=='__main__':unittest.main()
