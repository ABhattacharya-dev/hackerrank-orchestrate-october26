import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from ghostgraph.evidence import EvidenceStore

class OutcomesTests(unittest.TestCase):
    def fixture(self, files):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root=Path(tmp.name);(root/'evidence').mkdir()
        with (root/'evidence_files.csv').open('w') as stream:
            writer=csv.writer(stream);writer.writerow(['file_id','file_path','origin','captured_at'])
            for i,(name,content) in enumerate(files,1):
                if content is not None:(root/'evidence'/name).write_text(content)
                writer.writerow([f'evidence_{i}','evidence/'+name,'test','2026-01-01T00:00:00Z'])
        (root/'system_activity.csv').write_text('activity_id,event_time,event_type,source_system,target_system,resource_id,reported_result,details\n')
        (root/'user_audit_log.csv').write_text('audit_id,user_id,event_time,field_name,old_value,new_value\n')
        return root

    def test_failures_do_not_skip_remaining_manifest(self):
        root=self.fixture([('broken.json','{'),('missing.json',None),('ok.csv','resource_id,record_type,result,subject_reference\naccount_9,USER_PROFILE,FOUND,user_1\n')])
        store=EvidenceStore(root).load()
        self.assertEqual(len(store.coverage),3)
        self.assertEqual(len(store.failures),2)
        self.assertEqual(store.observations[0].resource,'account_9')
        self.assertEqual(store.trace(store.observations[0])['locator'],'row:2')
        self.assertTrue(store.trace(store.observations[0])['sha256'])
        count=len(store.observations);store.load();self.assertEqual(len(store.observations),count)

    def test_failed_partial_adapter_rolls_back(self):
        root=self.fixture([('bad.json','{"records":[{"resource_id":"account_1","result":"FOUND"},null]}')])
        store=EvidenceStore(root).load()
        self.assertEqual(len(store.failures),1)
        self.assertFalse(store.observations)

    def test_ambiguous_document_is_escalated_without_state_promotion(self):
        root=self.fixture([('screen.png','fixture')])
        class Extractor:
            def extract(self,path,meta,reason):return {'text':'Unclear fields','uncertain':True}
        with patch.object(EvidenceStore,'extracted_text',return_value='Unclear screenshot'):
            store=EvidenceStore(root,vision_extractor=Extractor()).load()
        self.assertEqual(store.unresolved[0]['status'],'vision_review_required')
        self.assertFalse(store.observations)
        self.assertEqual(store.coverage[0]['status'],'processed_unresolved')

    def test_no_config_remains_explicitly_unresolved(self):
        root=self.fixture([('screen.png','fixture')])
        with patch.object(EvidenceStore,'extracted_text',return_value='Unclear screenshot'):
            store=EvidenceStore(root).load()
        self.assertEqual(store.unresolved[0]['status'],'vision_not_configured')

if __name__=='__main__':unittest.main()
