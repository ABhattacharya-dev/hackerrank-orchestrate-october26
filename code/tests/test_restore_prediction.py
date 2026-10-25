import unittest
from ghostgraph.restore_prediction import console_facts,infer_restore
from ghostgraph.evidence import Observation
from ghostgraph.contract import step,validate_rows
from ghostgraph.planner import build_decision

META=dict(file_id='evidence_7',file_path='evidence/console.png',origin='backup_service',captured_at='2026-03-15T00:00:00Z')
TEXT='''Vault Recovery Manager Production Healthy
Archive backup_740 account@example.test
Selected backup_740
Path s3://tenant-storage/weekly/customer.tar
Checksum Verified
Created 05 Mar 2026 02:00 UTC
Last drill 10 Mar 2026
Retention end 15 Jun 2026
Other backup_741 restored Completed
'''
from ghostgraph.contract import timestamp
T=timestamp('2026-03-16T00:00:00Z')

class RestorePredictionTests(unittest.TestCase):
    def infer(self,text=TEXT,meta=META,observations=(),cutoff=T,linked={'user_707'}):
        return infer_restore(console_facts(text,meta),meta,cutoff,linked,observations)
    def test_applicable_target_capability_exact_plan_and_citations(self):
        o=self.infer();self.assertIsNotNone(o);self.assertEqual(o.kind,'prediction_inference')
        row,errors=build_decision('independent',True,[step('REPORT_RESTORE_RISK',o.system,o.resource,o.evidence_id)],
            [step('BLOCK_RESTORE',o.system,o.resource)],[step('VERIFY_RESTORE_BLOCKED',o.system,o.resource)])
        self.assertFalse(errors)
        import json
        steps=json.loads(row['steps_json']);self.assertEqual([s['operation'] for s in steps],['REPORT_RESTORE_RISK','BLOCK_RESTORE','VERIFY_RESTORE_BLOCKED'])
        self.assertEqual([s['evidence_id'] for s in steps],['evidence_7','',''])
        validate_rows([row],[dict(case_id='independent',audit_at='2026-03-16T00:00:00Z')],{'evidence_7':timestamp(META['captured_at'])})
    def test_explicit_target_block_overrides_capability(self):
        blocked=Observation('evidence_8','fixture','row',T-1,T-1,'backup_service','backup_740','BACKUP_ARCHIVE','BLOCKED')
        self.assertIsNone(self.infer(observations=[blocked]))
    def test_disabled_service_does_not_produce_active_risk(self):
        self.assertIsNone(self.infer(TEXT+'\nService disabled'))
    def test_other_restores_do_not_establish_target_eligibility(self):
        self.assertIsNone(self.infer(TEXT.replace('Last drill 10 Mar 2026','Other archive drill 10 Mar 2026')))
    def test_future_capture_or_future_target_drill_excluded(self):
        self.assertIsNone(self.infer(cutoff=T-172800))
        self.assertIsNone(self.infer(TEXT.replace('10 Mar','20 Mar')))
    def test_foreign_service_or_unlinked_tenant_excluded(self):
        self.assertIsNone(self.infer(meta=dict(META,origin='other_backup_tenant')))
        self.assertIsNone(self.infer(linked=set()))
    def test_retained_archive_is_never_deleted(self):
        from ghostgraph.prediction import PredictionPolicy
        from pathlib import Path
        o=self.infer();decision=PredictionPolicy(Path(__file__).resolve().parents[2]/'dataset/deletion_rules.csv').evaluate(o.category,o.state,o.fields,T)
        self.assertEqual(decision.treatment,'RESTORE');self.assertEqual(decision.policy_action,'RETAIN')
        self.assertNotEqual(decision.treatment,'DELETE')


class RestoreChronologyTests(unittest.TestCase):
    def test_drill_before_creation_is_not_a_target_drill(self):
        text=TEXT.replace('05 Mar','12 Mar')
        self.assertIsNone(console_facts(text,META))
        operational=text+'\nCustomer-platform archives Restore request Service health'
        facts=console_facts(operational,META)
        self.assertFalse(facts['target_drill_proven'])
        self.assertIsNone(facts['target_drill_at'])
        self.assertTrue(facts['applicable_live_controls'])
        self.assertLess(facts['drill_history_at'],facts['archive_created_at'])
        self.assertIsNotNone(infer_restore(facts,META,T,{'user_707'},[]))
