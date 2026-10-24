from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
import json
import shutil
import tempfile
import unittest
from ghostgraph.engine import Auditor
from ghostgraph.evidence import Observation
from ghostgraph.intent import IntentClassifier
from ghostgraph.contract import timestamp,validate_rows

NOW=timestamp('2026-01-02T00:00:00Z')

class PolicyIntegrationTests(unittest.TestCase):
    def test_actual_rules_preserve_security_legal_archive_and_tombstone(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            shutil.copy2(Path(__file__).resolve().parents[2]/'dataset/deletion_rules.csv',root/'deletion_rules.csv')
            specifications=[
              ('account_service','account_1','USER_PROFILE','PRESENT',{}),
              ('security_service','audit_record_2','SECURITY_AUDIT_LOG','PRESENT',{'retention_until':'2030-01-01T00:00:00Z'}),
              ('finance_service','legal_hold_3','LEGAL_HOLD_RECORD','PRESENT',{'hold_active':True}),
              ('identity_service','tombstone_4','ACCOUNT_TOMBSTONE','REDACTED',{'account_status':'DELETED','stable_reference_required':True}),
              ('backup_service','backup_5','BACKUP_ARCHIVE','ACTIVE',{'restore_block_supported':True,'archive_present':True}),
              ('integration_service','data_flow_6','DATA_FLOW','ACTIVE',{'enabled':True,'connector_name':'replication_sync'})]
            obs=[];by_token=defaultdict(list);by_resource=defaultdict(list)
            for system,resource,category,state,fields in specifications:
                o=Observation('evidence_1','evidence/fixture.json','resource:'+resource,NOW,NOW,system,resource,category,state,{'person@example.test'},fields)
                obs.append(o);by_token['person@example.test'].append(o);by_resource[o.key].append(o)
            store=SimpleNamespace(dataset=root,observations=obs,by_token=by_token,by_resource=by_resource,scopes=[],links=[],claims=[],source_rows={})
            identity=SimpleNamespace(resolve=lambda email,cutoff:({email},'user_1',None))
            request=dict(case_id='independent',email='person@example.test',audit_at='2026-01-02T00:00:00Z',request_text='Delete my account permanently.')
            row,diagnostics=Auditor(store,identity,IntentClassifier()).audit(request)
            steps=json.loads(row['steps_json'])
            deletes=[s['resource_id'] for s in steps if s['operation']=='DELETE_RECORD']
            self.assertEqual(deletes,['account_1'])
            self.assertFalse(diagnostics['issues'])
            self.assertEqual(len(diagnostics['obligation_ledger']),6)
            for resource in ['audit_record_2','legal_hold_3','backup_5']:
                self.assertTrue(any(s['resource_id']==resource and s['operation']=='VERIFY_RECORD_PRESENT' for s in steps))
            self.assertTrue(any(s['resource_id']=='tombstone_4' and s['operation']=='VERIFY_RECORD_REDACTED' for s in steps))
            self.assertEqual([s['operation'] for s in steps if s['phase']=='REMEDIATION'],['DISABLE_DATA_FLOW','BLOCK_RESTORE','DELETE_RECORD'])
            validate_rows([row],[request],{'evidence_1':NOW})

if __name__=='__main__':unittest.main()
