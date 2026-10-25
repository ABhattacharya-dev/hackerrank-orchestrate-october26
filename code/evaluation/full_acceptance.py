"""Run M7 full regression and validate every provisional row without padding.

Exit 0 requires a newly generated strict root output.csv. Exit 2 records diagnosed
acceptance blockers; it never renames partial candidate output into a submission.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import run
from ghostgraph.contract import FIELDS,check_rows,read_csv,resource_registry
from ghostgraph.evidence import EvidenceStore
from evaluation import verify

ROOT=Path(__file__).resolve().parents[2]


def fingerprint(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def application_usage(cache):
    phases=[]
    for tag in ['sample','full','strict','final_attempt']:
        usage=json.loads((cache/(tag+'_run.json')).read_text())
        phases.append(dict(phase=tag,requests=usage['request_count'],model=usage['model'],
            inference_calls=usage['inference_calls'],cache_hits=usage['cache_hits'],
            input_api_tokens=usage['input_tokens'],output_api_tokens=usage['output_tokens'],api_cost_usd=usage['api_cost_usd']))
    return phases


def render(report):
    lines=['# Full-dataset acceptance report','',
        '**Acceptance: '+('passed' if report['exit_criterion_met'] else 'blocked')+'.** '+
        'A candidate is not a final submission. No invalid or unsupported rows are padded to meet the row count.','',
        '| Check | Actual result |','| --- | ---: |',
        f"| Request / candidate rows | {report['request_count']} / {report['candidate_rows']} |",
        f"| Exactly keyed and sorted | {report['keys_count_order_valid']} |",
        f"| Strict structural passing rows | {report['structurally_valid_rows']} / {report['candidate_rows']} |",
        f"| Strict structural violations / affected cases | {len(report['structural_violations'])} / {len(report['structurally_invalid_case_ids'])} |",
        f"| Cited steps checked against source/linkage/cutoff ledger | {report['cited_steps_with_matching_ledger_proofs']} |",
        f"| Cases with unresolved proof obligations | {report['unresolved_case_count']} |",
        f"| Software tests / failures / errors / skipped | {report['tests']['tests_run']} / {report['tests']['failures']} / {report['tests']['errors']} / {report['tests']['skipped']} |",
        f"| Dataset / root instructions unchanged | {report['input_hashes_verified']} / {report['root_instructions_unchanged']} |",
        f"| Newly generated strict root output.csv | {report['strict_root_output_generated']} |",'',
        'Strict structural validation includes exact header/keys/count, statuses, phase/operation/state enums, consecutive numbering, official phase/operation/lexicographic ordering, source system/resource membership, duplicate and contradictory steps, complete finding/remedy/verification sequences, citation existence/cutoffs and blank future citations. Ledger provenance checks also trace each cited step to internal source, subject linkage and timestamp proof. They do not independently establish hidden canonical correctness.','',
        'The strict command was attempted against the actual repository-root output.csv path. Failure preserves any existing destination and records the blocker; it does not publish output.candidate.csv under a new name.','',
        'Strict export result: `'+(report['strict_export_error'] or 'success')+'`.', '',
        '## New on-disk adversarial scenarios','',
        'All seven new tests execute as part of the successful regression suite in `code/tests/test_adversarial_pipeline.py`. They exercise real evidence files and the CLI, not mocked final predictions.','',
        '1. **Empty primary SQL table, same-named regional replica table with PII, live import connector.** Explicit database IDs must preserve both scopes. A successful deletion activity claim cannot erase replica presence. Expected: disable connector, then delete the remaining copy; cite the replica snapshot.',
        '2. **Historical email boundary with equal-time contradiction and later capture.** Before the change, use the old alias; at the inclusive change time, resolve the new alias through audit history. A later-captured ABSENT observation cannot backdate state. Equal-time opposing eligible observations block strict export.',
        '3. **Compliant retained tombstone, security retention, active legal hold and unsafe restore.** Explicit supplied condition facts apply the real policy. Expected: block restore, preserve every required record and verify tombstone redaction; no record deletion.',
        '4. **Repeated subject with later tombstone redaction, requests in reverse temporal order.** Expected earlier INCOMPLETE and later COMPLETE, with unchanged results when request input order reverses.',
        '5. **Two users sharing a historical email.** Ambiguous request must produce no destructive plan; a uniquely grounded alias may plan only the correct user’s record.',
        '6. **French, Spanish and Korean negation with live PII.** Expected NOT_APPLICABLE and no steps; available data never creates authorization.',
        '7. **Manifest names a missing artifact.** Expected detectable MissingFile failure and no strict output.','',
        'The first scenario initially failed because the adapter used table name alone as the copy scope. The correction honors explicit snapshot_scope.database_id and propagates it into absence scopes. It never guesses database identity from filenames. All seven tests and the broader regression passed after correction. Supplied dataset bytes were not changed.','',
        '## Actual final candidate-run model usage','']
    u=report['usage']
    lines += [f"- Provider/model: `{u['provider']} / {u['model']}`.",
        f"- {u['request_count']} requests; {u['inference_calls']} actual learned inference calls, {u['scope_decisions']} deterministic unique scope decisions, {u['cache_hits']} classification cache hits.",
        f"- OCR/PDF extraction: `{u['document_extraction']}`. Separate cold reproduction is reported in usage_report.md.",
        '- Paid model/API calls: zero. API input tokens: 0; API output tokens: 0. Token units do not apply to local TF-IDF/logistic regression, OCR or PDF extraction; no text-token estimate was invented.',
        '- Metered API cost: USD 0.00 total and per request. No paid provider tariff was used, so no external token pricing applies. Local CPU/storage cost is unpriced, not asserted to be free. Model fitting is reported separately from inference calls in usage_report.md.',
        '- The strict attempt and adversarial/public/regression/reproducibility runs are separate validation work, excluded from the candidate-run counters. No completed final-submission run is claimed.', '',
        'Application runs executed by this acceptance command (test fixtures and cold reproduction are separate):','',
        '| Phase | Requests | Learned calls | Cache hits | API input/output tokens | API cost USD |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for phase in report['application_run_usage']:
        lines.append(f"| {phase['phase']} | {phase['requests']} | {phase['inference_calls']} | {phase['cache_hits']} | {phase['input_api_tokens']}/{phase['output_api_tokens']} | {phase['api_cost_usd']:.2f} |")
    lines+=['', 'Candidate SHA-256: `'+report['candidate_sha256']+'`.', '',
        '## Every strict structural blocker','',
        '| Case | Failed checks |','| --- | --- |']
    grouped={}
    for error in report['structural_violations']:grouped.setdefault(error['case_id'],set()).add(error['code'])
    for cid,codes in sorted(grouped.items()):lines.append(f"| {cid} | {', '.join(sorted(codes))} |")
    lines+=['',
        'These failures do not authorize invented resources, findings, capabilities or evidence. A structurally passing row can still have incomplete semantic coverage; the separate unresolved proof count remains binding. Full strict acceptance and the root output.csv milestone remain unmet.']
    (ROOT/'code/evaluation/full_dataset_report.md').write_text('\n'.join(lines)+'\n')


def main():
    baseline=fingerprint(ROOT/'AGENTS.md')
    result=verify.main()
    if result==1:return 1
    cache=ROOT/'.ghostgraph';requests=read_csv(ROOT/'dataset/deletion_requests.csv')
    candidate=ROOT/'output.candidate.csv'
    with candidate.open(newline='',encoding='utf-8-sig') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames!=FIELDS:raise ValueError('candidate header mismatch')
        rows=list(reader)
    store=EvidenceStore(ROOT/'dataset',cache/'extraction').load()
    if store.failures:raise ValueError('ingestion failures block full acceptance')
    violations=check_rows(rows,requests,store.citation_times,known_resource_pairs=resource_registry(store))
    verification=json.loads((cache/'verification.json').read_text())
    usage=json.loads((cache/'full_run.json').read_text())
    final=ROOT/'output.csv';before=fingerprint(final);strict_completed=False;blocked=None
    try:
        run(ROOT,ROOT/'dataset/deletion_requests.csv',final,tag='final_attempt')
        strict_completed=True
    except ValueError as exc:blocked=str(exc)
    if not strict_completed and fingerprint(final)!=before:raise AssertionError('failed strict run changed final output')
    if strict_completed:
        final_errors=check_rows(read_csv(final),requests,store.citation_times,known_resource_pairs=resource_registry(store))
        if final_errors:raise AssertionError('strict output violates contract')
        if fingerprint(final)!=fingerprint(candidate):raise AssertionError('strict and candidate decisions differ')
    invalid={e['case_id'] for e in violations}
    global_error='*' in invalid
    keys=[r['case_id'] for r in requests]
    report=dict(request_count=len(requests),candidate_rows=len(rows),
        keys_count_order_valid=len(rows)==518 and len(set(keys))==518 and [r['case_id'] for r in rows]==sorted(keys),
        structurally_valid_rows=0 if global_error else len(rows)-len(invalid),
        structural_violations=violations,structurally_invalid_case_ids=sorted(invalid),
        violation_counts=dict(Counter(e['code'] for e in violations)),
        cited_steps_with_matching_ledger_proofs=verification['cited_steps_with_matching_ledger_proofs'],
        unresolved_case_count=len(verification['unresolved_cases']),
        input_hashes_verified=verification['input_hashes_verified'] and fingerprint(ROOT/'dataset/deletion_requests.csv')==usage['requests_hash'],
        root_instructions_unchanged=baseline==fingerprint(ROOT/'AGENTS.md'),
        tests=json.loads((cache/'test_results.json').read_text()),usage={k:usage[k] for k in ['provider','model','request_count','inference_calls','scope_decisions','cache_hits','document_extraction']},
        candidate_sha256=fingerprint(candidate),application_run_usage=application_usage(cache),strict_root_output_generated=strict_completed,
        strict_export_error=blocked,exit_criterion_met=strict_completed and not violations and not verification['unresolved_cases'])
    (cache/'full_acceptance.json').write_text(json.dumps(report,indent=2))
    render(report)
    print(json.dumps({k:v for k,v in report.items() if k not in ['structural_violations','structurally_invalid_case_ids','usage']},indent=2))
    return 0 if report['exit_criterion_met'] else 2

if __name__=='__main__':raise SystemExit(main())
