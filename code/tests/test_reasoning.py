from collections import defaultdict
import csv
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from ghostgraph.contract import ordered, step, timestamp, validate_rows
from ghostgraph.engine import Auditor
from ghostgraph.evidence import Observation
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier

T0 = timestamp("2026-01-01T00:00:00Z")


def observation(resource, state, category="USER_PROFILE", system="account_service", **changes):
    args = dict(evidence_id="evidence_1", source="evidence/test.json", locator="records/0",
                available=T0, observed=T0, system=system, resource=resource, category=category,
                state=state, subject_tokens={"person@example.test"}, fields={})
    args.update(changes)
    return Observation(**args)


class ReasoningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.intent = IntentClassifier()

    def make_auditor(self, observations):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dataset = Path(tmp.name)
        (dataset/"deletion_rules.csv").write_text(
            "rule_id,data_category,condition,required_action\n"
            "r1,USER_PROFILE,Always,DELETE\n"
            "r2,ACCOUNT_TOMBSTONE,Stable reference required,REDACT\n"
            "r3,SECURITY_AUDIT_LOG,Within retention,RETAIN\n"
            "r4,ANALYTICS_PROFILE,Attributable,ANONYMIZE\n")
        by_token, by_resource = defaultdict(list), defaultdict(list)
        for obs in observations:
            by_resource[obs.key].append(obs)
            for token in obs.subject_tokens: by_token[token].append(obs)
        store = SimpleNamespace(dataset=dataset, by_token=by_token, by_resource=by_resource,
                                scopes=[], links=[])
        identity = SimpleNamespace(resolve=lambda email, cutoff: ({email}, "user_test", None))
        return Auditor(store, identity, self.intent)

    def request(self, **changes):
        return dict(case_id="adversarial", email="person@example.test", audit_at="2026-01-02T00:00:00Z",
                    request_text="Erase my account permanently.", **changes)

    def test_multilingual_non_deletion_and_negation(self):
        examples = [
            "Please export the data and keep my account active.",
            "Je veux une copie de mes données. Ne supprimez rien.",
            "No eliminen mi cuenta, solo cambien el teléfono.",
            "アカウントを削除しないでください。コピーだけください。",
            "계정은 유지하고 전화번호만 변경해 주세요.",
            "Correct my nickname without erasing any of my records.",
        ]
        for text in examples:
            with self.subTest(text=text): self.assertFalse(self.intent.classify(text)["authorized"])

    def test_multilingual_authorization(self):
        for text in ["Je souhaite supprimer définitivement ce profil.", "Quiero eliminar permanentemente mi perfil.",
                     "このアカウントの削除をお願いします。", "계정의 영구 삭제를 부탁합니다."]:
            with self.subTest(text=text): self.assertTrue(self.intent.classify(text)["authorized"])

    def test_future_capture_cannot_prove_earlier_deletion(self):
        present = observation("account_7", "PRESENT")
        future = observation("account_7", "ABSENT", available=T0+200000, observed=T0+100)
        row, diag = self.make_auditor([present,future]).audit(self.request())
        self.assertEqual(row["deletion_status"], "INCOMPLETE")
        self.assertEqual(diag["proofs"][0]["state"], "PRESENT")

    def test_cutoff_inclusive_and_cases_independent(self):
        first = observation("account_7", "PRESENT")
        later = observation("account_7", "ABSENT", available=T0+86400, observed=T0+86400)
        auditor=self.make_auditor([first,later])
        row,_=auditor.audit(self.request())
        self.assertEqual(row["deletion_status"],"COMPLETE")
        early=self.request();early['audit_at']='2026-01-01T12:00:00Z'
        row,_=auditor.audit(early)
        self.assertEqual(row["deletion_status"],"INCOMPLETE")

    def test_replica_tombstone_flow_and_restore(self):
        observations=[
            observation("account_7","ABSENT",scope="primary"),
            observation("account_7","PRESENT",scope="replica"),
            observation("tombstone_8","REDACTED",category="ACCOUNT_TOMBSTONE",system="identity_service"),
            observation("audit_record_9","PRESENT",category="SECURITY_AUDIT_LOG",system="security_service"),
            observation("data_flow_4","ACTIVE",category="DATA_FLOW",system="integration_service"),
            observation("backup_5","ACTIVE",category="BACKUP_ARCHIVE",system="backup_service"),
        ]
        row,diag=self.make_auditor(observations).audit(self.request())
        import json
        steps=json.loads(row['steps_json'])
        remedies=[s['operation'] for s in steps if s['phase']=='REMEDIATION']
        self.assertEqual(remedies,['DISABLE_DATA_FLOW','BLOCK_RESTORE','DELETE_RECORD'])
        self.assertNotIn('REDACT_RECORD',remedies)
        self.assertEqual(row['deletion_status'],'INCOMPLETE')
        self.assertFalse(diag['issues'])

    def test_equal_time_conflict_not_silently_complete(self):
        row,diag=self.make_auditor([observation("account_7","ABSENT"),observation("account_7","PRESENT")]).audit(self.request())
        self.assertEqual(row['deletion_status'],'INCOMPLETE')
        self.assertIn('CONFLICT',[i['code'] for i in diag['issues']])

    def test_no_resource_id_invented(self):
        row,diag=self.make_auditor([]).audit(self.request())
        self.assertEqual(row['steps_json'],'[]')
        self.assertIn('NO_LINKED_RESOURCE_PROOFS',[i['code'] for i in diag['issues']])
        with self.assertRaises(AssertionError):
            validate_rows([row],[self.request()],{},require_proofs=True)

    def test_reused_alias_never_merges_subjects(self):
        index=IdentityIndex.__new__(IdentityIndex)
        index.current=[dict(user_id='user_1',email='shared@example.test',phone='',email_hash='',updated_at='2026-01-01T00:00:00Z'),
                       dict(user_id='user_2',email='shared@example.test',phone='',email_hash='',updated_at='2026-01-01T00:00:00Z')]
        index.audit=[]
        tokens,uid,issue=index.resolve('shared@example.test',T0)
        self.assertIsNone(uid)
        self.assertEqual(tokens,{'shared@example.test'})
        self.assertIn('multiple',issue)

    def test_future_alias_snapshot_excluded(self):
        index=IdentityIndex.__new__(IdentityIndex)
        index.current=[dict(user_id='user_1',email='later@example.test',phone='',email_hash='',updated_at='2026-02-01T00:00:00Z')]
        index.audit=[]
        tokens,uid,_=index.resolve('later@example.test',T0)
        self.assertEqual(tokens,{'later@example.test'})
        self.assertIsNone(uid)

    def test_shared_historical_phone_is_not_a_unique_subject_link(self):
        index=IdentityIndex.__new__(IdentityIndex)
        index.current=[dict(user_id='user_1',email='a@example.test',phone='+44 20 1234 5678',email_hash='',updated_at='2026-01-01T00:00:00Z'),
                       dict(user_id='user_2',email='b@example.test',phone='+44 20 1234 5678',email_hash='',updated_at='2026-01-01T00:00:00Z')]
        index.audit=[]
        tokens,uid,issue=index.resolve('a@example.test',T0)
        self.assertEqual(uid,'user_1')
        self.assertNotIn('442012345678',tokens)
        self.assertIsNone(issue)

    def test_foreign_stable_reference_beats_shared_contact_match(self):
        foreign=observation('account_99','PRESENT',fields={'user_id':'user_2'})
        auditor=self.make_auditor([foreign])
        ledger,_=auditor.ledger({'person@example.test'},T0,subject_id='user_1')
        self.assertFalse(ledger)

    def test_reassigned_resource_is_not_deleted_as_former_owner_data(self):
        old=observation('account_99','PRESENT',fields={'user_id':'user_1'})
        new=observation('account_99','PRESENT',fields={'user_id':'user_2'},available=T0+10,observed=T0+10)
        auditor=self.make_auditor([old,new])
        ledger,issues=auditor.ledger({'person@example.test'},T0+20,subject_id='user_1')
        self.assertFalse(ledger)
        self.assertIn('RESOURCE_IDENTITY_CHANGED',[i['code'] for i in issues])

    def test_explicit_source_reference_links_without_suffix_guessing(self):
        search = observation("search_92", "PRESENT", category="ANALYTICS_PROFILE", system="search_service",
                             fields={"source_resource_id": "account_407"})
        account = observation("account_407", "ABSENT", subject_tokens=set())
        auditor = self.make_auditor([search, account])
        ledger,issues = auditor.ledger({"person@example.test"}, T0)
        self.assertIn(("account_service", "account_407"),ledger)
        self.assertNotIn(("account_service", "account_92"),ledger)
        self.assertFalse(issues)

    def test_redaction_and_anonymization_policy_actions(self):
        obs=[observation('tombstone_19','IDENTIFIABLE',category='ACCOUNT_TOMBSTONE',system='identity_service'),
             observation('analytics_8','IDENTIFIABLE',category='ANALYTICS_PROFILE',system='analytics_platform')]
        row,diag=self.make_auditor(obs).audit(self.request())
        import json
        steps=json.loads(row['steps_json'])
        self.assertEqual([s['operation'] for s in steps if s['phase']=='REMEDIATION'],['REDACT_RECORD','ANONYMIZE_RECORD'])
        self.assertTrue(all(s['evidence_id']=='' for s in steps if s['phase']!='FINDING'))
        self.assertFalse(diag['issues'])

    def test_retained_missing_record_does_not_get_invented_repair(self):
        row,diag=self.make_auditor([observation('audit_record_2','ABSENT',category='SECURITY_AUDIT_LOG',system='security_service')]).audit(self.request())
        self.assertIn('RETAINED_RECORD_MISSING',[i['code'] for i in diag['issues']])
        self.assertEqual(row['steps_json'],'[]')

    def test_consent_exceptions_keep_anonymous_statistics(self):
        result=self.intent.classify("I'm deleting the profile, but you may retain anonymous statistical totals.")
        self.assertTrue(result['authorized'])

    def test_reported_success_alone_never_generates_absence(self):
        auditor=self.make_auditor([observation('account_7','PRESENT')])
        auditor.store.claims=[dict(event_type='DELETE_RECORD',resource_id='account_7',reported_result='SUCCESS')]
        row,diag=auditor.audit(self.request())
        self.assertEqual(row['deletion_status'],'INCOMPLETE')
        self.assertEqual(diag['proofs'][0]['state'],'PRESENT')

    def test_retained_audit_alone_does_not_satisfy_primary_coverage(self):
        row,diag=self.make_auditor([observation('audit_record_4','PRESENT',category='SECURITY_AUDIT_LOG',system='security_service')]).audit(self.request())
        self.assertIn('NO_PRIMARY_PROFILE_PROOF',[i['code'] for i in diag['issues']])
        self.assertTrue(diag['proofs'])  # Preserve partial proofs; strict CLI blocks.


if __name__=='__main__':unittest.main()
