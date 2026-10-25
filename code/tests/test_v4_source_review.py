from pathlib import Path
from types import SimpleNamespace
import tempfile,json,unittest
from research.v4_source_review import validate_source
from research.v4_audit import json_records

class SourceReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name);(root/'evidence').mkdir();self.path=root/'evidence/input.json'
        self.meta=dict(file_id='evidence_71',file_path='evidence/input.json',captured_at='2026-02-01T00:00:00Z',origin='account_service')
        self.store=SimpleNamespace(dataset=root,manifest=[self.meta],by_resource={})
        self.identity=SimpleNamespace(resolve=lambda email,cutoff:({'user_710','subject@example.test'},'user_710',None))
        self.request=dict(email='subject@example.test',audit_at='2026-02-02T00:00:00Z')
        self.proposal=dict(subject='user_710',system_id='account_service',resource_id='account_811',evidence_id='evidence_71',locator='/records/0')
        self.record=dict(resource_id='account_811',subject_reference='user_710',observed_at='2026-02-01T00:00:00Z',status_code=404)
    def run_review(self,records=None,proposal=None):
        self.path.write_text(json.dumps({'records':records if records is not None else [self.record]}))
        return validate_source(proposal or self.proposal,self.store,self.identity,self.request)
    def test_novel_scoped_fact_can_be_validated_when_normalized_observation_missing(self):
        observation,reason=self.run_review()
        self.assertIsNotNone(observation);self.assertTrue(reason.startswith('TIER_B'))
        self.assertEqual(observation.state,'ABSENT');self.assertEqual(observation.evidence_id,'evidence_71')
    def test_neighboring_record_subject_is_not_target_ownership(self):
        self.record.pop('subject_reference')
        self.assertIsNone(self.run_review([self.record,dict(resource_id='account_812',subject_reference='user_710')])[0])
    def test_wrong_record_locator_cannot_recover_target(self):
        self.assertIsNone(self.run_review(proposal=dict(self.proposal,locator='/records/1'))[0])
    def test_free_text_mentions_are_not_authoritative_owner_fields(self):
        self.record.pop('subject_reference');self.record['notes']='user_710 requested a copy of unrelated data'
        self.assertIsNone(self.run_review()[0])
    def test_future_capture_or_observation_is_rejected(self):
        self.meta['captured_at']='2026-02-03T00:00:00Z';self.assertIsNone(self.run_review()[0])
        self.meta['captured_at']='2026-02-01T00:00:00Z';self.record['observed_at']='2026-02-03T00:00:00Z';self.assertIsNone(self.run_review()[0])
    def test_conflicting_stable_subject_is_rejected(self):
        self.record['customer_reference']='user_999';self.assertIsNone(self.run_review()[0])
    def test_source_mutation_removing_owner_invalidates_previous_proposal(self):
        self.assertIsNotNone(self.run_review()[0]);self.record['subject_reference']=None;self.assertIsNone(self.run_review()[0])
    def test_model_cannot_add_state_or_confidence_to_override_source(self):
        self.assertIsNone(self.run_review(proposal=dict(self.proposal,state='ABSENT',confidence=1))[0])
    def test_image_page_cooccurrence_is_not_structured_record_proof(self):
        self.meta['file_path']='evidence/input.png';self.assertIsNone(self.run_review()[0])
    def test_source_system_cannot_be_invented(self):
        self.assertIsNone(self.run_review(proposal=dict(self.proposal,system_id='security_service'))[0])
    def test_json_audit_reader_preserves_sibling_record_boundaries(self):
        data={'snapshots':[{'records':[dict(resource_id='account_811'),dict(resource_id='account_812',subject_reference='user_710')]}]}
        records=list(json_records(data));self.assertEqual([p for p,r in records],['/snapshots/0/records/0','/snapshots/0/records/1'])
        self.assertNotIn('subject_reference',records[0][1])

    def test_invalid_original_time_is_rejected_detectably(self):
        self.record['observed_at']='not-a-time'
        self.assertEqual(self.run_review()[1],'invalid original observation timestamp')

    def test_explicit_original_system_overrides_prefix_ontology(self):
        self.record['system']='different_service'
        self.assertEqual(self.run_review()[1],'unverified source system')
    def test_snapshot_system_and_time_are_part_of_original_scope(self):
        self.proposal['locator']='/snapshots/0/records/0'
        self.path.write_text(json.dumps({'snapshots':[dict(data_store='different_service',captured_at='2026-02-01T00:00:00Z',records=[self.record])]}))
        self.assertEqual(validate_source(self.proposal,self.store,self.identity,self.request)[1],'unverified source system')
        self.path.write_text(json.dumps({'snapshots':[dict(data_store='account_service',captured_at='2026-02-04T00:00:00Z',records=[dict(self.record,observed_at=None)])]}))
        self.assertEqual(validate_source(self.proposal,self.store,self.identity,self.request)[1],'future observation')
    def test_tombstone_state_is_preserved_in_a_novel_extraction(self):
        self.record.pop('status_code');self.record['account_status']='DELETED'
        observation,_=self.run_review()
        self.assertEqual(observation.category,'ACCOUNT_TOMBSTONE')
        self.assertEqual(observation.state,'REDACTED')

    def test_negative_array_index_is_not_a_precise_original_locator(self):
        self.assertIsNone(self.run_review(proposal=dict(self.proposal,locator='/records/-1'))[0])
    def test_successful_operation_claim_is_not_a_direct_state_observation(self):
        self.record.pop('status_code');self.record['reported_result']='SUCCESS'
        self.assertEqual(self.run_review()[1],'operation claim is not a state observation')

    def test_conflicting_record_and_container_scope_is_not_silently_chosen(self):
        self.record['system']='account_service';self.proposal['locator']='/snapshots/0/records/0'
        self.path.write_text(json.dumps({'snapshots':[dict(data_store='different_service',records=[self.record])]}))
        self.assertEqual(validate_source(self.proposal,self.store,self.identity,self.request)[1],'conflicting original system scopes')
