"""Milestone 4 acceptance: supplied rule coverage, preservation and ledger shape."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code'))
from evaluation.main import evaluate
from ghostgraph.policy import PolicyEngine


def main():
    suite=unittest.defaultTestLoader.discover(str(ROOT/'code/tests'),pattern='test_policy*.py')
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():return 1
    evaluate(ROOT)
    policy=PolicyEngine(ROOT/'dataset/deletion_rules.csv')
    diagnostics=json.loads((ROOT/'.ghostgraph/sample_diagnostics.json').read_text())
    required={'identity_linkage','rule_id','condition','applicability','required_state',
              'observed_state','supporting_evidence','remediation_required','verification_obligations'}
    count=0;categories=set()
    for case in diagnostics:
        for entry in case.get('obligation_ledger',[]):
            assert required<=entry.keys()
            assert entry['category']=='DATA_FLOW' or entry['category'] in policy.by_category
            if entry['policy_action']=='RETAIN' or entry['category']=='ACCOUNT_TOMBSTONE':
                assert entry['treatment']!='DELETE'
            count+=1;categories.add(entry['category'])
        plan=case.get('remediation_plan',{})
        execution=plan.get('execution_order')
        if execution is not None:
            for edge in plan.get('dependencies',[]):assert execution.index(edge['before'])<execution.index(edge['after'])
    report=dict(policy_tests_run=result.testsRun,policy_tests_passed=True,supplied_categories=len(policy.by_category),
                public_obligation_entries=count,public_categories=sorted(categories),preservation_checks_passed=True)
    (ROOT/'.ghostgraph/policy_acceptance.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
