"""Independent V5.1 end-to-end consent tests through the real subprocess CLI.

Expected interpretations were authored before the integration correction.
"""
import json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from ghostgraph.contract import read_csv,check_rows,resource_registry
from ghostgraph.evidence import EvidenceStore
from intent_cli_fixtures import dataset,requests,csv_file,TIME,EMAIL

class AuthorizationCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name)
        shutil.copytree(Path(__file__).resolve().parents[1],cls.root/'code',ignore=shutil.ignore_patterns('__pycache__'))
        dataset(cls.root)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def run_cases(self,texts,authorized):
        q=requests(self.root,texts);output=self.root/'prediction.csv';output.unlink(missing_ok=True)
        p=subprocess.run([sys.executable,str(self.root/'code/main.py'),'--mode','predict','--output',str(output)],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        rows=read_csv(output);self.assertEqual(len(rows),len(texts))
        store=EvidenceStore(self.root/'dataset').load()
        self.assertEqual(check_rows(rows,q,store.citation_times,known_resource_pairs=resource_registry(store)),[])
        for row,yes in zip(rows,authorized):
            with self.subTest(case=row['case_id']):
                self.assertEqual(row['deletion_status'],'INCOMPLETE' if yes else 'NOT_APPLICABLE')
                steps=json.loads(row['steps_json'])
                if not yes:self.assertEqual(steps,[])
                else:
                    self.assertEqual([s['operation'] for s in steps],['REPORT_REMAINING_RECORD','DELETE_RECORD','VERIFY_RECORD_ABSENT'])
                    self.assertEqual([s['evidence_id'] for s in steps],['evidence_fixture','',''])
                    self.assertEqual([s['resource_id'] for s in steps],['account_731']*3)
        return json.loads((self.root/'.ghostgraph/full_diagnostics.json').read_text())
    def test_unfulfilled_conditions(self):
        ds=self.run_cases(['If the replacement device arrives, erase my membership. It has not arrived; do not act yet.',
                          'Erase my registration only after I explicitly approve. I have not approved.'],[False,False])
        for d in ds:
            self.assertTrue(d['intent']['ambiguous'])
            self.assertIn('CONSENT_NOT_ESTABLISHED',[i['code'] for i in d['issues']])
    def test_hypothetical_and_quoted(self):
        self.run_cases(['How would my records be treated if I ever requested account erasure?',
                        'Please translate “Erase my membership and personal records” into Italian.'],[False,False])
    def test_third_party_authority(self):
        ds=self.run_cases(["Erase my colleague's profile without consulting them.",
                           "I say I am a legal representative; erase my client's registration."],[False,False])
        self.assertTrue(ds[1]['intent']['ambiguous'])
    def test_legitimate_request_and_uncertain_consent(self):
        self.run_cases(['Please permanently erase my customer registration and personal data.',
                        'I am not sure whether to erase my membership. I need more time to decide.'],[True,False])
    def test_separate_authorized_and_refused_actions(self):
        self.run_cases(['Do not remove the invoice records; permanently erase my customer profile.',
                        'Do not delete my registration. Please send an export.'],[True,False])
    def test_multilingual_requests(self):
        self.run_cases(['Ne supprimez pas mon compte. Je veux uniquement une copie de mes informations.',
                        'Quiero eliminar permanentemente mi cuenta y mis datos personales.',
                        'アカウントを削除しないでください。コピーを送ってください。'],[False,True,False])
    def test_continuation_of_prior_erasure(self):
        self.run_cases(['I previously deleted my registration. Inspect it for residual personal copies and finish the cleanup.'],[True])
    def test_novel_sentence_structure(self):
        self.run_cases(['With regard to my customer profile, please erase it and its personal records permanently.'],[True])
    def test_authorized_but_ambiguous_identity_is_not_non_applicable(self):
        path=self.root/'dataset/user_identities.csv';original=path.read_bytes()
        try:
            rows=read_csv(path);rows.append(dict(rows[0],user_id='user_902'))
            csv_file(path,list(rows[0]),rows)
            requests(self.root,['Please erase my account permanently.']);output=self.root/'blocked.csv';output.unlink(missing_ok=True)
            p=subprocess.run([sys.executable,str(self.root/'code/main.py'),'--mode','predict','--output',str(output)],capture_output=True,text=True)
            self.assertEqual(p.returncode,2);self.assertFalse(output.exists())
            ds=json.loads((self.root/'.ghostgraph/full_diagnostics.json').read_text())
            self.assertTrue(ds[0]['intent']['authorized'])
            self.assertIn('AMBIGUOUS_IDENTITY',[i['code'] for i in ds[0]['issues']])
            self.assertIn('NO_SUPPORTED_STEPS',p.stderr)
        finally:path.write_bytes(original)

    def test_topic_prefaces_preserve_refusal_and_inquiry_scope(self):
        self.run_cases(['Regarding my profile, do not erase it.',
                        'Concerning my registration, explain erasure before I decide.',
                        "As for my aunt's account, erase her personal profile without consent.",
                        'With respect to my account, permanently erase the personal data.'],[False,False,False,True])
    def test_classifier_uncertainty_blocks_export_and_preserves_existing_output(self):
        requests(self.root,['Unrecognized fictional instruction.'])
        output=self.root/'existing.csv';output.write_text('protected-existing-artifact')
        script="""
import runpy,sys
sys.path.insert(0,'code')
import ghostgraph.intent as original
original.IntentClassifier.classify=lambda self,text:dict(authorized=True,probability=.51,decision_source='fault-injected uncertain classifier',model='fault-injection',ambiguous=False,low_confidence=True)
sys.argv=['code/main.py','--mode','predict','--output','existing.csv']
runpy.run_path('code/main.py',run_name='__main__')
"""
        p=subprocess.run([sys.executable,'-c',script],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(p.returncode,2);self.assertEqual(output.read_text(),'protected-existing-artifact')
        self.assertIn('authorization classifications unresolved',p.stderr)
        ds=json.loads((self.root/'.ghostgraph/full_blocked_cases.json').read_text())
        self.assertEqual(ds[0]['intent']['authorization_state'],'CLASSIFICATION_UNRESOLVED')
        self.assertIn('AUTHORIZATION_CLASSIFICATION_UNRESOLVED',[i['code'] for i in ds[0]['issues']])
    def test_runtime_package_has_no_research_imports(self):
        import ast
        for path in (self.root/'code/ghostgraph').glob('*.py'):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node,ast.Import):
                    self.assertFalse(any(n.name.split('.')[0]=='research' for n in node.names),path)
                if isinstance(node,ast.ImportFrom):
                    self.assertNotEqual((node.module or '').split('.')[0],'research',path)
