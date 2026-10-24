from pathlib import Path
import unittest
from ghostgraph.contract import timestamp,step
from ghostgraph.policy import PolicyEngine
from ghostgraph.risks import process_analysis,plan_dependencies
from ghostgraph.evidence import Observation
from ghostgraph.temporal import reconstruct

CUTOFF=timestamp('2026-01-02T00:00:00Z')

def observation(resource,state,category='DATA_FLOW',system='integration_service',when=CUTOFF,**fields):
    return Observation('evidence_1','evidence/config.json','records/0',when,when,system,resource,category,state,fields=fields)

class PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.policy=PolicyEngine(Path(__file__).resolve().parents[2]/'dataset/deletion_rules.csv')

    def test_every_supplied_category_has_a_positive_condition_fixture(self):
        fixtures={
          'SUPPORT_MESSAGE':('IDENTIFIABLE',{'shared_context':True}),
          'SUPPORT_ATTACHMENT':('PRESENT',{'subject_only':True}),
          'ANALYTICS_PROFILE':('IDENTIFIABLE',{}),'PRODUCT_TELEMETRY':('IDENTIFIABLE',{}),
          'EMAIL_DELIVERY_LOG':('IDENTIFIABLE',{'subject_email_present':True}),
          'SECURITY_AUDIT_LOG':('PRESENT',{'retention_until':'2026-02-01T00:00:00Z'}),
          'LEGAL_HOLD_RECORD':('PRESENT',{'hold_active':True}),
          'BACKUP_ARCHIVE':('ACTIVE',{'restore_block_supported':True}),
          'ACCOUNT_TOMBSTONE':('IDENTIFIABLE',{'account_status':'DELETED','stable_reference_required':True})}
        covered=set()
        for rule in self.policy.rules:
            category=rule['data_category'];state,fields=fixtures.get(category,('PRESENT',{}))
            with self.subTest(category=category):
                d=self.policy.evaluate(category,state,fields,CUTOFF)
                self.assertEqual(d.rule_id,rule['rule_id']);self.assertEqual(d.policy_action,rule['required_action'])
                self.assertEqual(d.applicability,'SATISFIED');self.assertFalse(d.issues)
                self.assertTrue(d.verification_obligations);covered.add(category)
        self.assertEqual(len(covered),15)

    def test_retained_security_and_legal_records_are_never_deleted(self):
        for category,fields in [('SECURITY_AUDIT_LOG',{'retention_until':'2026-02-01T00:00:00Z'}),('LEGAL_HOLD_RECORD',{'hold_active':True})]:
            for state in ['PRESENT','ABSENT','UNKNOWN']:
                d=self.policy.evaluate(category,state,fields,CUTOFF)
                self.assertEqual(d.policy_action,'RETAIN');self.assertNotEqual(d.treatment,'DELETE')
                self.assertIn('VERIFY_RECORD_PRESENT',d.verification_obligations)
                if state=='ABSENT':self.assertIn('RETAINED_RECORD_MISSING',d.issues)

    def test_missing_or_expired_retention_has_no_delete_fallback(self):
        for fields in [{},{'retention_until':'2025-01-01T00:00:00Z'}]:
            d=self.policy.evaluate('SECURITY_AUDIT_LOG','PRESENT',fields,CUTOFF)
            self.assertIsNone(d.treatment);self.assertIsNone(d.remediation_required)
            self.assertTrue(d.issues);self.assertTrue(d.preserve)

    def test_retention_cutoff_is_inclusive(self):
        d=self.policy.evaluate('SECURITY_AUDIT_LOG','PRESENT',{'retention_until':'2026-01-02T00:00:00Z'},CUTOFF)
        self.assertEqual(d.applicability,'SATISFIED')

    def test_shared_support_is_redacted_not_deleted(self):
        d=self.policy.evaluate('SUPPORT_MESSAGE','IDENTIFIABLE',{'shared_context':True},CUTOFF)
        self.assertEqual(d.treatment,'REDACT');self.assertTrue(d.preserve)
        d=self.policy.evaluate('SUPPORT_MESSAGE','IDENTIFIABLE',{},CUTOFF)
        self.assertIsNone(d.treatment);self.assertIn('POLICY_CONDITION_UNKNOWN',d.issues)

    def test_attachment_exclusivity_is_required(self):
        for facts in [{'subject_count':2},{}]:
            self.assertIsNone(self.policy.evaluate('SUPPORT_ATTACHMENT','PRESENT',facts,CUTOFF).treatment)
        self.assertEqual(self.policy.evaluate('SUPPORT_ATTACHMENT','PRESENT',{'subject_count':1},CUTOFF).treatment,'DELETE')

    def test_tombstone_preserves_reference_and_only_redacts(self):
        fields={'account_status':'DELETED','stable_reference_required':True}
        d=self.policy.evaluate('ACCOUNT_TOMBSTONE','IDENTIFIABLE',fields,CUTOFF)
        self.assertEqual(d.treatment,'REDACT');self.assertIn('stable internal subject reference',d.preserve)
        self.assertFalse(self.policy.evaluate('ACCOUNT_TOMBSTONE','REDACTED',fields,CUTOFF).remediation_required)

    def test_backup_preservation_and_restore_block_are_both_obligations(self):
        d=self.policy.evaluate('BACKUP_ARCHIVE','ACTIVE',{'restore_block_supported':True},CUTOFF)
        self.assertEqual(d.policy_action,'RETAIN');self.assertEqual(d.treatment,'RESTORE')
        self.assertEqual(d.verification_obligations,['VERIFY_RECORD_PRESENT','VERIFY_RESTORE_BLOCKED'])
        self.assertNotEqual(d.treatment,'DELETE')

    def test_already_anonymous_still_requires_verification(self):
        d=self.policy.evaluate('ANALYTICS_PROFILE','ANONYMIZED',{},CUTOFF)
        self.assertFalse(d.remediation_required);self.assertEqual(d.verification_obligations,['VERIFY_RECORD_ANONYMIZED'])

    def test_historical_sync_and_future_activation_are_not_current_risks(self):
        earlier=observation('data_flow_1','ACTIVE',when=CUTOFF-10,connector_name='replication_import_sync_index')
        disabled=observation('data_flow_1','DISABLED',when=CUTOFF,connector_name='replication_import_sync_index')
        future=observation('data_flow_1','ACTIVE',when=CUTOFF+10)
        obs=[earlier,disabled,future]
        temporal={earlier.key:reconstruct(obs,CUTOFF).explain()}
        history=[dict(activity_id='activity_1',resource_id='data_flow_1',event_type='SYNC_RECORD',event_time='2026-01-01T00:00:00Z')]
        r=process_analysis(obs,temporal,history,CUTOFF)[0]
        self.assertFalse(r['active_at_cutoff']);self.assertEqual(set(r['types']),{'replication','import','synchronization','indexing'})
        self.assertEqual(len(r['historical_events']),1)
        later={earlier.key:reconstruct(obs,CUTOFF+10).explain()}
        self.assertTrue(process_analysis(obs,later,history,CUTOFF+10)[0]['active_at_cutoff'])

    def test_historical_activity_claim_alone_does_not_create_live_process(self):
        claims=[dict(activity_id='activity_1',resource_id='account_1',event_type='SYNC_RECORD',event_time='2026-01-01T00:00:00Z')]
        self.assertEqual(process_analysis([],{},claims,CUTOFF),[])

    def test_control_configuration_conflict_is_unknown(self):
        o=observation('data_flow_1','ACTIVE',enabled=False)
        r=process_analysis([o],{o.key:reconstruct([o],CUTOFF).explain()},[],CUTOFF)[0]
        self.assertIsNone(r['active_at_cutoff']);self.assertIn('PROCESS_CONFIGURATION_CONFLICT',r['issues'])

    def test_dependencies_and_canonical_order_are_separate(self):
        changes=[step('DELETE_RECORD','account_service','account_1'),step('DELETE_RECORD','search_service','search_9'),
                 step('DISABLE_DATA_FLOW','integration_service','data_flow_7'),step('BLOCK_RESTORE','backup_service','backup_3')]
        downstream=observation('search_9','PRESENT',category='SEARCH_INDEX_ENTRY',system='search_service',source_resource_id='account_1')
        p=plan_dependencies(changes,[downstream],CUTOFF)
        execution=p['execution_order'];canonical=p['canonical_order']
        a=('DELETE_RECORD','account_service','account_1');b=('DELETE_RECORD','search_service','search_9')
        self.assertLess(execution.index(b),execution.index(a));self.assertLess(canonical.index(a),canonical.index(b))
        self.assertIn('CANONICAL_DEPENDENCY_ORDER_CONFLICT',p['issues'])
        self.assertEqual([n[0] for n in canonical[:2]],['DISABLE_DATA_FLOW','BLOCK_RESTORE'])

    def test_dependency_cycle_is_not_called_safe(self):
        changes=[step('DELETE_RECORD','account_service','account_1'),step('DELETE_RECORD','account_service','account_2')]
        obs=[observation('account_1','PRESENT',source_resource_id='account_2'),observation('account_2','PRESENT',source_resource_id='account_1')]
        p=plan_dependencies(changes,obs,CUTOFF)
        self.assertIsNone(p['execution_order']);self.assertIn('DEPENDENCY_CYCLE',p['issues'])

    def test_unmitigated_active_restore_blocks_execution_of_record_changes(self):
        changes=[step('DELETE_RECORD','account_service','account_1')]
        risk=dict(system='backup_service',resource='backup_5',category='BACKUP_ARCHIVE',types=['restore'],active_at_cutoff=True)
        p=plan_dependencies(changes,[],CUTOFF,[risk])
        self.assertIsNone(p['execution_order']);self.assertIn('UNRESOLVED_PROCESS_PRECONDITION',p['issues'])

    def test_malformed_retention_is_explicitly_unknown_and_preserved(self):
        d=self.policy.evaluate('SECURITY_AUDIT_LOG','PRESENT',{'retention_until':'not-a-date'},CUTOFF)
        self.assertIsNone(d.treatment);self.assertTrue(d.preserve)
        self.assertIn('INVALID_POLICY_CONDITION_FACT',d.issues)

    def test_logfmt_and_sql_boolean_condition_facts(self):
        self.assertEqual(self.policy.evaluate('LEGAL_HOLD_RECORD','PRESENT',{'hold_active':'true'},CUTOFF).policy_action,'RETAIN')
        self.assertEqual(self.policy.evaluate('SUPPORT_ATTACHMENT','PRESENT',{'subject_only':1},CUTOFF).treatment,'DELETE')

    def test_clean_label_cannot_override_prohibited_stored_identifiers(self):
        for category,state,fields in [('ANALYTICS_PROFILE','ANONYMIZED',{'email_hash':'a'*64}),
            ('ACCOUNT_TOMBSTONE','REDACTED',{'email':'person@example.test','account_status':'DELETED','stable_reference_required':True})]:
            d=self.policy.evaluate(category,state,fields,CUTOFF)
            self.assertEqual(d.observed_state,'CONFLICT');self.assertIsNone(d.remediation_required)
            self.assertIn('POLICY_STATE_FACT_CONFLICT',d.issues)

    def test_lookup_subject_metadata_is_not_stored_analytics_attribution(self):
        d=self.policy.evaluate('ANALYTICS_PROFILE','ANONYMIZED',{'subject_reference':'user_1','query':'person@example.test'},CUTOFF)
        self.assertFalse(d.remediation_required);self.assertFalse(d.issues)

    def test_process_category_selects_control_not_connector_name(self):
        o=observation('data_flow_1','ACTIVE',connector_name='backup_restore_import',enabled=True)
        risk=process_analysis([o],{o.key:reconstruct([o],CUTOFF).explain()},[],CUTOFF)[0]
        changes=[step('DISABLE_DATA_FLOW','integration_service','data_flow_1'),step('DELETE_RECORD','account_service','account_7')]
        self.assertFalse(plan_dependencies(changes,[],CUTOFF,[risk])['unresolved_preconditions'])
        o.fields['connector_name']='async_worker'
        risk=process_analysis([o],{o.key:reconstruct([o],CUTOFF).explain()},[],CUTOFF)[0]
        self.assertNotIn('synchronization',risk['types'])

if __name__=='__main__':unittest.main()
