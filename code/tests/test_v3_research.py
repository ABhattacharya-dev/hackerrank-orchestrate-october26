"""Independent V3 adversarial fixtures; no public rows or labels are used."""
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
import shutil,tempfile,unittest,json
from ghostgraph.evidence import Observation
from ghostgraph.contract import timestamp,check_rows
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier
from research.linkage import temporal_candidates,graph
from research.auditor import ResearchAuditor
from research.review import verify_proposal

T=timestamp('2026-05-01T12:00:00Z')
def obs(rid='account_765',uid='user_765',state='PRESENT',system='account_service',category='USER_PROFILE',**kw):
    values=dict(evidence_id='evidence_88',source='fixture.json',locator='records/0',available=T-10,observed=T-10,system=system,resource=rid,category=category,state=state,subject_tokens={uid,uid+'@example.test'},fields={'user_id':uid},scope='primary')
    values.update(kw);return Observation(**values)
def req(cid='one',uid='user_765'):
    return dict(case_id=cid,email=uid+'@example.test',requested_at='2026-05-01T11:00:00Z',reported_at='2026-05-01T12:00:00Z',audit_at='2026-05-01T12:05:00Z',reported_status='COMPLETE',request_text='Permanently delete my account and personal records.')
def claim(rid='account_765',detail='',when='2026-05-01T12:00:10Z',eid='activity_88'):
    return dict(activity_id=eid,event_time=when,event_type='DELETE_RECORD',source_system='deletion_worker',target_system='account_service',resource_id=rid,reported_result='SUCCESS',details=detail)
class V3Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)
        shutil.copy2(Path(__file__).resolve().parents[2]/'dataset/deletion_rules.csv',self.path/'deletion_rules.csv')
        self.identity=SimpleNamespace(resolve=lambda email,cutoff:({email,email.split('@')[0]},email.split('@')[0],None))
    def store(self,observations=(),claims=()):
        by_resource=defaultdict(list);by_token=defaultdict(list)
        for o in observations:
            by_resource[o.key].append(o)
            for t in o.subject_tokens:by_token[t].append(o)
        return SimpleNamespace(dataset=self.path,observations=list(observations),claims=list(claims),links=[],scopes=[],by_resource=by_resource,by_token=by_token,documents=[],source_rows={})
    def test_nearby_requests_do_not_share_an_action_without_subject_proof(self):
        store=self.store(claims=[claim(detail='Subject user_765 target account_765')])
        links=temporal_candidates(store,self.identity,[req(),req('two','user_766')])
        self.assertEqual([c['case_id'] for c in links if c['stage']=='corroborated_derived'],['one'])
        self.assertEqual(next(c for c in links if c['case_id']=='two')['stage'],'rejected')
    def test_multiple_events_require_each_target_ownership_not_nearest_choice(self):
        store=self.store(claims=[claim(detail='user_765'),claim('account_766','user_765',eid='activity_89'),claim('account_767','user_767',eid='activity_90')])
        cs=temporal_candidates(store,self.identity,[req()]);strong=[c for c in cs if c['stage']=='corroborated_derived']
        self.assertEqual({c['resource_id'] for c in strong},{'account_765','account_766'})
        self.assertTrue(all(c['corroborated_workflow_targets']==2 for c in strong))
    def test_successful_claim_does_not_delete_replica_pii(self):
        store=self.store([obs(state='ABSENT'),obs(state='PRESENT',scope='regional')],[claim(detail='user_765')])
        row,d=ResearchAuditor(store,self.identity,IntentClassifier(),graph_enabled=True).audit(req())
        self.assertEqual(row['deletion_status'],'INCOMPLETE')
        steps=json.loads(row['steps_json']);self.assertEqual([s['operation'] for s in steps],['REPORT_REMAINING_RECORD','DELETE_RECORD','VERIFY_RECORD_ABSENT'])
        self.assertEqual(steps[0]['evidence_id'],'evidence_88')
    def test_primary_absence_never_hides_a_known_replica(self):
        store=self.store([obs(state='ABSENT'),obs(state='PRESENT',scope='replica')])
        row,_=ResearchAuditor(store,self.identity,IntentClassifier()).audit(req())
        self.assertEqual(row['deletion_status'],'INCOMPLETE')
    def test_temporal_only_foreign_action_is_never_accepted(self):
        cs=temporal_candidates(self.store([obs(uid='user_999')],[claim(detail='unrelated success')]),self.identity,[req()])
        self.assertEqual(cs[0]['stage'],'weak_candidate')
    def test_reassigned_historical_email_is_ambiguous(self):
        index=IdentityIndex.__new__(IdentityIndex);index.current=[]
        index.audit=[dict(audit_id='audit_'+str(i),user_id=uid,event_time='2026-05-01T10:00:00Z',field_name='email',old_value='shared@example.test',new_value=uid+'@example.test') for i,uid in enumerate(['user_765','user_766'])]
        r=req();r['email']='shared@example.test'
        cs=temporal_candidates(self.store(claims=[claim(detail='user_765')]),index,[r])
        self.assertEqual(cs[0]['stage'],'rejected')
    def test_future_worker_event_is_rejected_even_with_subject(self):
        cs=temporal_candidates(self.store(claims=[claim(detail='user_765',when='2026-05-01T12:06:00Z')]),self.identity,[req()],900)
        self.assertEqual(cs[0]['stage'],'rejected')
    def test_retained_tombstone_security_and_no_unsafe_delete(self):
        observations=[obs('tombstone_765',category='ACCOUNT_TOMBSTONE',system='identity_service',state='REDACTED',fields=dict(subject_reference='user_765',account_status='DELETED',stable_reference_required=True)),
                      obs('audit_record_765',category='SECURITY_AUDIT_LOG',system='security_service')]
        row,_=ResearchAuditor(self.store(observations),self.identity,IntentClassifier(),graph_enabled=True).audit(req())
        steps=json.loads(row['steps_json']);self.assertEqual(row['deletion_status'],'COMPLETE')
        self.assertEqual([s['operation'] for s in steps],['VERIFY_RECORD_PRESENT','VERIFY_RECORD_REDACTED'])
    def test_inventory_without_restore_capability_does_not_infer_live_risk(self):
        from ghostgraph.restore_prediction import console_facts
        self.assertIsNone(console_facts('Vault Recovery Manager Healthy Archive backup_765 user_765@example.test',dict(origin='backup_service',captured_at='2026-05-01T12:00:00Z')))
    def test_multilingual_non_deletion_never_uses_temporal_deletion_candidate(self):
        r=req();r['request_text']='Ne supprimez rien, je veux seulement une copie de mes données.'
        row,_=ResearchAuditor(self.store([obs()],[claim(detail='user_765')]),self.identity,IntentClassifier(),graph_enabled=True).audit(r)
        self.assertEqual((row['deletion_status'],row['steps_json']),('NOT_APPLICABLE','[]'))
    def test_reverse_graph_rejects_foreign_copy_and_future_copy(self):
        own=obs();child=obs('search_765',system='search_service',category='SEARCH_INDEX_ENTRY',subject_tokens=set(),fields={'source_resource_id':'account_765'})
        nodes,_=graph(self.store([own,child]),self.identity,req(),True)
        self.assertEqual(nodes[child.key]['stage'],'corroborated_derived')
        child.fields['user_id']='user_999';self.assertNotIn(child.key,graph(self.store([own,child]),self.identity,req(),True)[0])
        child.fields.pop('user_id');child.available=T+999;self.assertNotIn(child.key,graph(self.store([own,child]),self.identity,req(),True)[0])
    def test_global_assignment_collision_is_rejected(self):
        r1=req();r2=req('two','user_766');key=('account_service','account_765')
        proof=dict(stage='direct',available=T,proofs=[{'evidence_id':'evidence_88'}])
        cs=temporal_candidates(self.store(claims=[claim()]),self.identity,[r1,r2],graphs={'one':{key:proof},'two':{key:proof}})
        self.assertTrue(all(c['stage']=='rejected' for c in cs))
    def test_review_gate_rejects_inventions_future_and_wrong_locators(self):
        o=obs();store=self.store([o]);p=dict(subject='user_765',system_id=o.system,resource_id=o.resource,relationship='record owner',evidence_id=o.evidence_id,locator=o.locator,explanation='explicit stable reference',uncertainty=.01)
        self.assertTrue(verify_proposal(p,store,{'user_765'},T)[0])
        for bad in [dict(p,resource_id='account_999'),dict(p,locator='page unrelated'),dict(p,subject='user_999')]:self.assertFalse(verify_proposal(bad,store,{'user_765'},T)[0])
        self.assertFalse(verify_proposal(p,store,{'user_765'},T-999)[0])

    def test_future_reported_workflow_timestamp_is_not_corroboration(self):
        r=req();r['reported_at']='2026-05-01T12:06:00Z'
        cs=temporal_candidates(self.store(claims=[claim(detail='user_765')]),self.identity,[r],900)
        self.assertEqual(cs[0]['stage'],'rejected')

    def test_foreign_explicit_email_overrides_temporal_subject_token(self):
        def resolve(email,cutoff):
            uid='user_999' if email=='other@example.test' else 'user_765'
            return {uid,email},uid,None
        identity=SimpleNamespace(resolve=resolve)
        cs=temporal_candidates(self.store(claims=[claim(detail='user_765 contact other@example.test')]),identity,[req()])
        self.assertEqual(cs[0]['stage'],'rejected')
