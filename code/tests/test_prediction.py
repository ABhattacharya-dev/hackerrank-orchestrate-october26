import unittest
from pathlib import Path
from ghostgraph.prediction import PredictionPolicy,PredictionAuditor
from ghostgraph.policy import PolicyEngine
from ghostgraph.temporal import reconstruct
from ghostgraph.evidence import Observation
from ghostgraph.contract import timestamp

class PredictionTests(unittest.TestCase):
    def test_retention_inference_preserves_record_but_certification_stays_unknown(self):
        path=Path(__file__).resolve().parents[2]/'dataset/deletion_rules.csv'
        strict=PolicyEngine(path).evaluate('SECURITY_AUDIT_LOG','PRESENT',{},timestamp('2026-01-01T00:00:00Z'))
        prediction=PredictionPolicy(path).evaluate('SECURITY_AUDIT_LOG','PRESENT',{},timestamp('2026-01-01T00:00:00Z'))
        self.assertEqual(strict.applicability,'UNKNOWN');self.assertEqual(prediction.treatment,'RETAIN')
        self.assertFalse(prediction.remediation_required)
        expired=PredictionPolicy(path).evaluate('SECURITY_AUDIT_LOG','PRESENT',{'retention_until':'2025-01-01T00:00:00Z'},timestamp('2026-01-01T00:00:00Z'))
        self.assertIsNone(expired.treatment)

    def test_prediction_known_scope_does_not_weaken_certification(self):
        o=Observation('evidence_1','fixture','row',10,10,'account_service','account_78','USER_PROFILE','ABSENT',scope='primary')
        predictor=PredictionAuditor.__new__(PredictionAuditor)
        self.assertEqual(reconstruct([o],20).state,'UNKNOWN')
        self.assertEqual(predictor.reduce_state([o],20,[]).state,'ABSENT')
        replica=Observation('evidence_2','fixture','row',10,10,'account_service','account_78','USER_PROFILE','PRESENT',scope='replica')
        self.assertEqual(predictor.reduce_state([o,replica],20,[]).state,'PRESENT')
        replica.available=30
        self.assertEqual(predictor.reduce_state([o,replica],20,[]).state,'ABSENT')

    def test_prediction_does_not_resolve_equal_time_conflicts(self):
        a=Observation('evidence_1','fixture','row',10,10,'account_service','account_78','USER_PROFILE','ABSENT')
        from dataclasses import replace
        self.assertEqual(PredictionAuditor.__new__(PredictionAuditor).reduce_state([a,replace(a,state='PRESENT')],20,[]).state,'CONFLICT')
