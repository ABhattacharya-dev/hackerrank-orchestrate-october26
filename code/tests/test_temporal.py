from dataclasses import replace
import unittest
from ghostgraph.evidence import Observation
from ghostgraph.temporal import reconstruct


def obs(state,t=10,capture=None,scope='primary',**kw):
    values=dict(evidence_id='evidence_1',source='evidence/snapshot.json',locator='records/0',available=t if capture is None else capture,
                observed=t,system='account_service',resource='account_7',category='USER_PROFILE',state=state,scope=scope)
    values.update(kw);return Observation(**values)

class TemporalTests(unittest.TestCase):
    def test_future_capture_and_future_event_both_excluded(self):
        for future in [obs('ABSENT',11,capture=30),obs('ABSENT',30,capture=11)]:
            self.assertEqual(reconstruct([obs('PRESENT'),future],20).state,'PRESENT')

    def test_observation_time_wins_not_late_export(self):
        old=obs('PRESENT',10,capture=29);new=obs('ABSENT',20,fields={'_covers_all_copies':True})
        self.assertEqual(reconstruct([old,new],30).state,'ABSENT')

    def test_quality_cannot_hide_same_time_contradiction(self):
        result=reconstruct([obs('PRESENT',quality=1),obs('ABSENT',quality=99)],20)
        self.assertEqual(result.state,'CONFLICT');self.assertIsNone(result.witness)

    def test_primary_absence_does_not_clear_replica(self):
        result=reconstruct([obs('PRESENT',scope='replica'),obs('ABSENT',20)],30)
        self.assertEqual(result.state,'PRESENT')

    def test_replica_absence_does_not_clear_primary(self):
        self.assertEqual(reconstruct([obs('PRESENT'),obs('ABSENT',20,scope='replica')],30).state,'PRESENT')

    def test_later_replica_snapshot_can_clear_its_own_copy(self):
        result=reconstruct([obs('PRESENT',scope='replica'),obs('ABSENT',20,scope='replica',fields={'_covers_all_copies':True})],30)
        self.assertEqual(result.state,'ABSENT')

    def test_unscoped_query_absence_retains_uncertainty(self):
        result=reconstruct([obs('ABSENT',scope='logical')],30)
        self.assertEqual(result.state,'UNKNOWN')
        self.assertEqual(result.issues[0]['code'],'COPY_COVERAGE_UNPROVEN')

    def test_claim_success_cannot_override_direct_presence(self):
        result=reconstruct([obs('PRESENT'),obs('ABSENT',20,kind='claim',quality=99)],30)
        self.assertEqual(result.state,'PRESENT')

    def test_same_user_cutoffs_are_independent_and_inclusive(self):
        history=[obs('PRESENT'),obs('ABSENT',20,fields={'_covers_all_copies':True})]
        for _ in range(3):
            self.assertEqual(reconstruct(history,19).state,'PRESENT')
            self.assertEqual(reconstruct(history,20).state,'ABSENT')
            self.assertEqual(reconstruct(history,9).state,'UNKNOWN')

    def test_collector_origin_alone_cannot_establish_store_alignment(self):
        a=obs('PRESENT',scope='logical',fields={'_source_origin':'replica_export'})
        b=obs('ABSENT',20,scope='logical',fields={'_source_origin':'primary_export'})
        self.assertEqual(reconstruct([a,b],30).state,'UNKNOWN')
        self.assertIn('SCOPE_ALIGNMENT_UNKNOWN',[i['code'] for i in reconstruct([a,b],30).issues])

    def test_unknown_latest_state_does_not_reuse_old_certainty(self):
        result=reconstruct([obs('ABSENT',fields={'_covers_all_copies':True}),obs('UNKNOWN',20)],30)
        self.assertEqual(result.state,'UNKNOWN');self.assertIsNone(result.witness)

    def test_permutations_do_not_change_conflict(self):
        a,b=obs('PRESENT'),obs('ABSENT')
        self.assertEqual(reconstruct([a,b],20).explain(),reconstruct([b,a],20).explain())

    def test_direct_recreation_after_absence_changes_later_cutoff(self):
        history=[obs('ABSENT',10,fields={'_covers_all_copies':True}),obs('PRESENT',20)]
        self.assertEqual(reconstruct(history,15).state,'ABSENT')
        self.assertEqual(reconstruct(history,20).state,'PRESENT')

    def test_snapshot_time_is_not_row_update_or_export_time(self):
        from pathlib import Path
        import tempfile
        from ghostgraph.evidence import EvidenceStore
        from ghostgraph.contract import timestamp
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'evidence_files.csv').write_text('file_id,file_path,origin,captured_at\n')
            path=root/'snapshot.sql'
            path.write_text("CREATE TABLE snapshot_scope(origin_system TEXT,captured_at TEXT);"
                "INSERT INTO snapshot_scope VALUES('account_service','2026-01-02T00:00:00Z');"
                "CREATE TABLE customer_profiles(resource_id TEXT,email TEXT,updated_at TEXT);"
                "INSERT INTO customer_profiles VALUES('account_7','person@example.test','2026-01-01T00:00:00Z');")
            meta=dict(file_id='evidence_1',file_path='evidence/snapshot.sql',origin='account_service',captured_at='2026-01-03T00:00:00Z')
            store=EvidenceStore(root);store.sql_file(path,meta)
            self.assertEqual(store.observations[0].observed,timestamp('2026-01-02T00:00:00Z'))
            self.assertEqual(store.observations[0].available,timestamp('2026-01-03T00:00:00Z'))
            self.assertTrue(store.scopes[0]['exhaustive'])

    def test_mutation_claim_invalidates_certainty_without_proving_new_state(self):
        from datetime import datetime,timezone
        when=datetime.fromtimestamp(20,timezone.utc).isoformat()
        for previous,operation in [('PRESENT','DELETE_RECORD'),('ABSENT','RESTORE_BACKUP')]:
            result=reconstruct([obs(previous,fields={'_covers_all_copies':True})],30,
                [dict(activity_id='activity_1',resource_id='account_7',event_type=operation,event_time=when,reported_result='SUCCESS')])
            self.assertEqual(result.state,'UNKNOWN');self.assertIsNone(result.witness)
            self.assertIn('UNVERIFIED_MUTATION_AFTER_OBSERVATION',[i['code'] for i in result.issues])

    def test_future_claim_does_not_change_earlier_state(self):
        from datetime import datetime,timezone
        claim=dict(activity_id='activity_1',resource_id='account_7',event_type='DELETE_RECORD',
                   event_time=datetime.fromtimestamp(40,timezone.utc).isoformat())
        self.assertEqual(reconstruct([obs('PRESENT')],30,[claim]).state,'PRESENT')

    def test_future_trace_context_cannot_link_earlier_readback(self):
        from pathlib import Path
        import tempfile
        from ghostgraph.evidence import EvidenceStore
        from ghostgraph.contract import timestamp
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'evidence_files.csv').write_text('file_id,file_path,origin,captured_at\n')
            path=root/'trace.log'
            path.write_text('2026-01-03T00:00:00Z service=account_service trace_id=x event=profile_lookup_started lookup_key=person@example.test\n'
                '2026-01-01T00:00:00Z service=account_service trace_id=x event=profile_lookup_completed resource_id=account_7 rows=0 http_status=404\n')
            store=EvidenceStore(root);store.log_file(path,dict(file_id='evidence_1',file_path='evidence/trace.log',origin='collector',captured_at='2026-01-01T00:00:00Z'))
            self.assertEqual(reconstruct(store.observations,timestamp('2026-01-02T00:00:00Z')).state,'UNKNOWN')
            self.assertGreater(store.observations[0].available,timestamp('2026-01-02T00:00:00Z'))

if __name__=='__main__':unittest.main()
