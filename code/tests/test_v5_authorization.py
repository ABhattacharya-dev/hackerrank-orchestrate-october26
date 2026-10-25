"""Development/fault-injection regressions; sealed examples are not test tuning."""
import unittest
from research.v5_intent import AuthorizationIntent
from research.v5_probes import DEVELOPMENT

class AuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.model=AuthorizationIntent()
    def decide(self,text):
        r=self.model.classify(text)
        return None if r['low_confidence'] or r['ambiguous'] else r['authorized']
    def test_development_authorization_contract(self):
        for name,text,expected in DEVELOPMENT:
            with self.subTest(name=name):self.assertEqual(self.decide(text),expected)
    def test_negation_is_local_to_its_resource_instruction(self):
        self.assertTrue(self.decide('Do not erase my legally retained invoices; please delete my account.'))
        self.assertFalse(self.decide('Do not erase my account; supply a copy instead.'))
    def test_same_account_contradiction_requires_clarification(self):
        self.assertIsNone(self.decide('Do not delete my profile. Erase my account.'))
    def test_model_uncertainty_cannot_reach_engine_as_authorization(self):
        model=AuthorizationIntent()
        model.base.classify=lambda text:dict(authorized=True,probability=.51,decision_source='semantic ML inference',model='fault-injection',ambiguous=False,low_confidence=True)
        r=model.classify('不明な指示')
        self.assertFalse(r['authorized']);self.assertTrue(r['ambiguous']);self.assertTrue(r['low_confidence'])
    def test_cached_diagnostic_evidence_is_copy_isolated(self):
        text='Please erase my account permanently.';a=self.model.classify(text)
        original=a['evidence'][0]['negative'];a['evidence'][0]['negative']=not original
        b=self.model.classify(text)
        self.assertEqual(b['evidence'][0]['negative'],original)
    def test_quote_adoption_is_distinct_from_quotation(self):
        self.assertFalse(self.decide('Translate "erase my account" into another language.'))
        self.assertTrue(self.decide('I adopt this as my own instruction: "erase my account".'))
    def test_neutral_followup_does_not_condition_current_consent(self):
        self.assertTrue(self.decide('Please delete my account. Please contact me if you need identification.'))
        self.assertTrue(self.decide('Please erase my account. Let me know once the deletion request is reviewed.'))
    def test_no_train_or_probe_lookup_in_decision_path(self):
        # Different identifiers and punctuation exercise the same speech act.
        self.assertFalse(self.decide('Summarize this ticket: "Erase my customer profile immediately".'))
        self.assertTrue(self.decide('Please erase my existing personal account immediately.'))


import test_reasoning as frozen_reasoning
class ExistingReasoningWithV5(frozen_reasoning.ReasoningTests):
    @classmethod
    def setUpClass(cls):cls.intent=AuthorizationIntent()

class ContinuationRegression(unittest.TestCase):
    def test_requester_linked_audits_and_retention_scope(self):
        from research.v5_continuation import PROBES
        from research.v5_evaluate import decision
        model=AuthorizationIntent()
        for name,text,expected in PROBES:
            with self.subTest(name=name):
                self.assertIs(decision(model.classify(text)),expected)
