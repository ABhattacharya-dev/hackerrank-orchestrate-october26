"""Execute readiness checks and write machine-readable actual outcomes.

Exit 2 means the software checks ran but unresolved evidence blocks final export.
"""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from main import run
from ghostgraph.contract import read_csv, timestamp, validate_rows
from ghostgraph.evidence import EvidenceStore
from evaluation.main import evaluate


def verify_provenance(rows, diagnostics, requests):
    cases = {r['case_id']:r for r in requests}
    ds = {d['case_id']:d for d in diagnostics}
    checked = 0
    for row in rows:
        cutoff = timestamp(cases[row['case_id']]['audit_at'])
        for item in json.loads(row['steps_json']):
            if not item['evidence_id']: continue
            proofs=[p for p in ds[row['case_id']]['proofs'] if p['system']==item['system_id']
                    and p['resource']==item['resource_id'] and p['evidence_id']==item['evidence_id']]
            assert proofs, 'citation lacks matching ledger proof'
            assert all(max(p['available'],p['observed'])<=cutoff for p in proofs)
            assert all(p.get('subject_linkage') for p in proofs), 'missing grounded linkage explanation'
            if row['deletion_status']=='COMPLETE':
                assert item['state'] in {p['state'] for p in proofs}, 'verification asserts unobserved state'
            checked += 1
    return checked


def main():
    suite=unittest.defaultTestLoader.discover(str(ROOT/'code/tests'))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    stats={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
           'skipped':len(result.skipped),'successful':result.wasSuccessful()}
    (ROOT/'.ghostgraph').mkdir(exist_ok=True)
    (ROOT/'.ghostgraph/test_results.json').write_text(json.dumps(stats,indent=2))
    if not result.wasSuccessful(): return 1
    evaluate(ROOT)
    rows,diagnostics,usage=run(ROOT,ROOT/'dataset/deletion_requests.csv',ROOT/'output.candidate.csv',
                               allow_unresolved=True,tag='full')
    requests=read_csv(ROOT/'dataset/deletion_requests.csv')
    assert len(rows)==518
    store=EvidenceStore(ROOT/'dataset',ROOT/'.ghostgraph/extraction').load()
    validate_rows(rows,requests,store.citation_times,require_proofs=False)
    checked=verify_provenance(rows,diagnostics,requests)
    strict_output=ROOT/'.ghostgraph/strict_output.csv'
    if strict_output.exists(): strict_output.unlink()
    blocked=None
    try:
        run(ROOT,ROOT/'dataset/deletion_requests.csv',strict_output,tag='strict')
    except ValueError as exc:
        blocked=str(exc)
        assert not strict_output.exists(), 'strict mode wrote a blocked submission'
    checks={'candidate_rows':len(rows),'cited_steps_with_matching_ledger_proofs':checked,
            'input_hashes_verified':all(__import__('hashlib').sha256((ROOT/'dataset'/name).read_bytes()).hexdigest()==digest
                for name,digest in usage['input_hashes'].items()),
            'strict_export_blocked':blocked,'unresolved_cases':[dict(case_id=d['case_id'],issues=d['issues']) for d in diagnostics if d['issues']]}
    (ROOT/'.ghostgraph/verification.json').write_text(json.dumps(checks,indent=2))
    print(json.dumps({k:v for k,v in checks.items() if k!='unresolved_cases'},indent=2))
    print(f"Unresolved cases: {len(checks['unresolved_cases'])}; details in .ghostgraph/verification.json")
    return 2 if blocked else 0


if __name__=='__main__':raise SystemExit(main())
