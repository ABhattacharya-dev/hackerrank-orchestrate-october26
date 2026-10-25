"""Independent V6 controls; B/C's weak assumptions are measured, not blessed."""
import unittest
from types import SimpleNamespace
from collections import defaultdict
from ghostgraph.contract import timestamp
from ghostgraph.evidence import Observation
from ghostgraph.prediction import PredictionAuditor
from research.v6_assignment import CandidateGraph,ownership,AssignmentAuditor,raw_edges
T='2026-03-02T12:00:00Z';CUT='2026-03-03T12:00:00Z'
def request(id='alpha',email='owner@fiction.test',**kw):
    return dict(dict(case_id=id,email=email,requested_at='2026-03-01T12:00:00Z',reported_at=T,audit_at=CUT,reported_status='COMPLETE'),**kw)
def activity(id='worker_a',resource='account_987',**kw):
    return dict(dict(activity_id=id,event_time=T,event_type='DELETE_RECORD',source_system='deletion_worker',target_system='account_service',resource_id=resource,reported_result='SUCCESS'),**kw)
def store(observations=(),links=()):
    by_resource=defaultdict(list);by_token=defaultdict(list)
    for o in observations:
        by_resource[o.key].append(o)
        for t in o.subject_tokens:by_token[t].append(o)
    return SimpleNamespace(by_resource=by_resource,by_token=by_token,links=list(links))
def observation(user='user_71',state='ABSENT',available=None,scope='primary',**fields):
    return Observation('evidence_fixture','evidence/fixture.json','row:1',available or timestamp(T),timestamp(T),'account_service','account_987','USER_PROFILE',state,{user},dict(user_id=user,**fields),scope)
class Identity:
    def resolve(self,email,cutoff):
        uid='user_71' if email=='owner@fiction.test' else 'user_83'
        return {email,uid},uid,None
EMPTY=dict(case_id='alpha',steps_json='[]',deletion_status='INCOMPLETE')
class V6Controls(unittest.TestCase):
    def select(self,qs,events,variant='D',evidence=None):
        g=CandidateGraph(qs,events,evidence or store(),Identity())
        return g.select(qs[0],variant,EMPTY)
    def test_unrelated_unique_worker_is_not_ownership(self):
        q=request();a=activity()
        self.assertIsNotNone(self.select([q],[a],'B')[0])  # demonstrable false attribution, not an acceptable safeguard
        edge,records=self.select([q],[a],'D');self.assertIsNone(edge)
        self.assertIn('NO_INDEPENDENT_OWNERSHIP_CORROBORATION',records[0]['rejections'])
    def test_overlapping_distinct_subject_requests_reject_collisions(self):
        qs=[request(),request('beta','foreign@fiction.test')]
        self.assertIsNotNone(self.select(qs,[activity()],'B')[0])
        self.assertIsNone(self.select(qs,[activity()],'C')[0])
    def test_one_event_can_cover_repeated_same_subject_requests(self):
        qs=[request(),request('repeat')]
        self.assertIsNotNone(self.select(qs,[activity()],'C')[0])
    def test_multiple_legitimate_resources_are_not_forced_to_one(self):
        events=[activity(),activity('worker_b','account_252')]
        edge,records=self.select([request()],events);self.assertIsNone(edge)
        self.assertEqual(len(records),2)
        self.assertTrue(all('MULTIPLE_CANDIDATE_EVENTS' in r['rejections'] for r in records))
    def test_status_result_mismatch(self):
        edge,records=self.select([request()],[activity(reported_result='FAILED')],'B')
        self.assertIsNone(edge);self.assertIn('STATUS_RESULT_MISMATCH',records[0]['rejections'])
    def test_missing_events(self):self.assertIsNone(self.select([request()],[],'B')[0])
    def test_event_after_audit_or_before_request(self):
        for q in [request(audit_at='2026-03-02T11:59:00Z'),request(requested_at='2026-03-02T12:01:00Z')]:
            self.assertIsNone(self.select([q],[activity()],'B')[0])
    def test_post_cutoff_capture_cannot_corroborate_or_conflict(self):
        q=request();future=timestamp(CUT)+1
        self.assertIsNone(self.select([q],[activity()],'D',store([observation(available=future)]))[0])
        own=observation();foreign=observation('user_83',available=future,scope='replica')
        e,_=self.select([q],[activity()],'D',store([own,foreign]));self.assertIsNotNone(e)
        self.assertTrue(all(p['available']<=timestamp(CUT) for p in e['own']))
    def test_explicit_foreign_owner_rejected_even_if_email_shared(self):
        o=observation('user_83');o.subject_tokens.add('owner@fiction.test')
        self.assertIsNone(self.select([request()],[activity()],'B',store([o]))[0])
    def test_ambiguous_historical_reassignment_rejected(self):
        g=CandidateGraph([request()],[activity()],store(),SimpleNamespace(resolve=lambda email,cutoff:({email},None,'identifier belongs to multiple subjects')))
        e,r=g.select(request(),'B',EMPTY);self.assertIsNone(e)
        self.assertIn('AMBIGUOUS_HISTORICAL_IDENTITY',r[0]['rejections'])
    def test_current_and_deleted_prior_accounts_preserved(self):
        old=observation();current=observation();current.resource='account_252';current.state='PRESENT'
        verdict=ownership(store([old,current]),Identity(),request(),'account_987')
        self.assertEqual(verdict['tier'],'CORROBORATED')
    def test_future_peer_request_does_not_create_collision(self):
        qs=[request(),request('future','foreign@fiction.test',requested_at='2026-03-04T00:00:00Z',reported_at='2026-03-04T12:00:00Z')]
        self.assertIsNotNone(self.select(qs,[activity()],'C')[0])
    def test_batch_and_timestamp_clustering_reject_uniqueness(self):
        events=[activity(),activity('batch_2','account_252'),activity('batch_3','account_633')]
        self.assertIsNone(self.select([request()],events,'B')[0])
        shifted=[activity(event_time='2026-03-02T18:00:00Z')]
        self.assertIsNone(self.select([request()],shifted,'B')[0])
    def test_success_claim_does_not_create_state(self):
        o=ownership(store(),Identity(),request(),'account_987');self.assertEqual(o['own'],[])
        self.assertNotEqual(o['tier'],'CORROBORATED')
    def test_primary_absence_replica_presence_is_not_complete(self):
        auditor=object.__new__(PredictionAuditor)
        result=auditor.reduce_state([observation(),observation(state='PRESENT',scope='replica')],timestamp(CUT),[])
        self.assertEqual(result.state,'PRESENT')
    def test_already_grounded_ledger_delegates_without_replacement(self):
        from unittest.mock import patch
        auditor=object.__new__(AssignmentAuditor);auditor.edge={'already_grounded':True}
        expected=({'original':'proof'},[])
        with patch.object(PredictionAuditor,'ledger',return_value=expected) as method:
            self.assertEqual(auditor.ledger({'user_71'},timestamp(CUT),'user_71'),expected)
            method.assert_called_once()

    def test_account_absence_cannot_upgrade_whole_case_to_complete(self):
        from research.v6_assignment import preserve_case_status
        import json
        baseline=dict(case_id='independent',deletion_status='INCOMPLETE',steps_json='[]')
        proposed=dict(case_id='independent',deletion_status='COMPLETE',steps_json=json.dumps([dict(operation='VERIFY_RECORD_ABSENT',resource_id='account_987')]))
        diagnostics={}
        self.assertEqual(preserve_case_status(baseline,proposed,diagnostics),baseline)
        self.assertIn('v6_whole_case_upgrade_blocked',diagnostics)
