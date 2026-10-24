import unittest
from types import SimpleNamespace
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier
from ghostgraph.contract import timestamp

T=timestamp('2026-01-03T00:00:00Z')

class IntentIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.model=IntentClassifier()

    def index(self):
        x=IdentityIndex.__new__(IdentityIndex)
        x.current=[dict(user_id='user_1',name='Same Name',email='new@example.test',phone='',email_hash='a'*64,updated_at='2026-01-02T00:00:00Z'),
                   dict(user_id='user_2',name='Same Name',email='other@example.test',phone='',email_hash='b'*64,updated_at='2026-01-02T00:00:00Z')]
        x.audit=[dict(audit_id='audit_7',user_id='user_1',event_time='2026-01-01T00:00:00Z',field_name='email',old_value='old@example.test',new_value='new@example.test')]
        return x

    def test_changed_email_hash_and_duplicate_name(self):
        x=self.index();tokens,uid,note=x.resolve('OLD@EXAMPLE.TEST',T)
        self.assertEqual(uid,'user_1');self.assertIn('a'*64,tokens)
        self.assertNotIn('b'*64,tokens);self.assertNotIn('other@example.test',tokens)
        self.assertTrue(any(p['evidence_id']=='audit_7' for a in x.explain('old@example.test',T)['aliases'] for p in a['proofs']))
        self.assertEqual(x.resolve('old@example.test',T),(tokens,uid,note))

    def test_grounded_catalog_identity_and_future_link(self):
        x=self.index();x.current=[];x.audit=[]
        x.store=SimpleNamespace(observations=[],links=[(T,'account_service','account_7',{'user_9','known@example.test'},'activity_7'),
                       (T+10,'account_service','account_8',{'user_8','future@example.test'},'activity_8')])
        self.assertEqual(x.resolve('known@example.test',T)[1],'user_9')
        self.assertIsNone(x.resolve('future@example.test',T)[1])

    def test_non_deletion_categories_and_hypotheticals(self):
        for text in ['Cancel my request to erase my account.','I do not want to delete my account.',
                     'How do I delete my account?','Please reset my password so I can use my account.',
                     'Send an access report only.','Correct my telephone number.','Unsubscribe me from your newsletter.']:
            with self.subTest(text=text):self.assertFalse(self.model.classify(text)['authorized'])

    def test_uncertain_authorization_is_flagged(self):
        self.assertTrue(self.model.classify('I am not sure whether to delete my account.')['ambiguous'])

if __name__=='__main__':unittest.main()
