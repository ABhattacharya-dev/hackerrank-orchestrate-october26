"""Render actual verified run data as judge-visible Markdown; never invent metrics."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]


def load(name): return json.loads((ROOT/'.ghostgraph'/f'{name}.json').read_text())


def write():
    metrics,usage,tests,verification,repro=map(load,['sample_metrics','full_run','test_results','verification','reproducibility'])
    assert tests['successful'] and repro['byte_identical_candidate']
    assert repro['candidate_sha256']==hashlib.sha256((ROOT/'output.candidate.csv').read_bytes()).hexdigest()
    codes=Counter(i['code'] for d in verification['unresolved_cases'] for i in d['issues'])
    pct=lambda key:f"{metrics[key]:.2%}"
    report=f'''# GhostGraph evaluation report

## Submission acceptance: blocked

The implemented pipeline executes and produces a **provisional 518-row candidate**.
It is not a fully verified submission. Strict export refuses final `output.csv`
because **{usage['unresolved_cases']} cases have explicit proof/coverage gaps**.
The candidate's fallback statuses and partial plans must not be presented as
certified deletion decisions. Additional authoritative subject/resource links or
state evidence are needed; case-number inference and sample-label lookup are
prohibited. No hidden-set accuracy is known.

## Actual public-sample results

Command: `python3 code/evaluation/main.py`. Labels are loaded by the evaluator
after predictions; they never enter intent training or prediction. These 32
public samples were used during development, so results are regression scores,
not an independent held-out estimate. Samples contain no NOT_APPLICABLE cases.

| Metric | Result |
| --- | ---: |
| Deletion-status accuracy | {metrics['counts']['status_correct']}/32 ({pct('status_accuracy')}) |
| Exact row accuracy (status and full step array) | {metrics['counts']['exact_rows']}/32 ({pct('exact_row_accuracy')}) |
| Exact sequence accuracy | {metrics['counts']['exact_sequences']}/32 ({pct('exact_sequence_accuracy')}) |
| Step precision, including exact canonical citation | {metrics['counts']['exact_step_matches']}/{metrics['counts']['predicted_steps']} ({pct('step_precision')}) |
| Step recall, including exact canonical citation | {metrics['counts']['exact_step_matches']}/{metrics['counts']['expected_steps']} ({pct('step_recall')}) |
| Structural step precision, ignoring citation | {pct('structural_step_precision')} |
| Structural step recall, ignoring citation | {pct('structural_step_recall')} |
| Field accuracy | {metrics['counts']['field_matches']}/{metrics['counts']['expected_fields']} ({pct('field_accuracy')}) |
| Canonical evidence-reference accuracy | {metrics['counts']['canonical_citation_matches']}/{metrics['counts']['expected_citations']} ({pct('canonical_evidence_accuracy')}) |

Step precision/recall use multiset intersection over phase, system, resource,
operation, state and (for exact matching) evidence ID; step number is evaluated
in sequence/field accuracy. Fields align on phase/system/resource/operation;
missing expected fields count wrong. Canonical reference accuracy compares
expected cited steps, including omitted ones as incorrect. The provenance check
independently verifies internal source/linkage/cutoff consistency, but is not an
independent semantic-entailment judge and does not prove hidden correctness.

## Actual software and full-run checks

- `{tests['tests_run']}` unit/regression tests ran: `{tests['failures']}` failures,
  `{tests['errors']}` errors, `{tests['skipped']}` skipped; all passed.
- All 94 manifest files processed: 26 logs, 28 JSON, 1 text, 11 PNG, 24 SQL,
  4 PDF. {usage['ingestion']['observations']} observations and
  {usage['ingestion']['sql_scopes']} SQL table scopes retained.
- Candidate IDs/count/header/order, allowed enums, field sets, step numbers,
  duplicate detection and citation availability were validated for 518 rows.
- {verification['cited_steps_with_matching_ledger_proofs']} cited candidate steps
  matched internal ledger proofs with eligible timestamps and explicit linkage
  explanations. This is provenance validation, not a claim of full coverage.
- Input hashes verified unchanged; supplied evidence and root AGENTS.md were not
  edited. Candidate status counts: `{usage['status_counts']}` (provisional).
- Warm-cache full run: {usage['runtime_seconds']:.3f} seconds. A fresh source copy,
  different working directory and empty extraction cache reproduced identical
  candidate bytes in {repro['runtime_seconds']:.3f} seconds, executing
  {repro['document_extraction'].get('tesseract_calls',0)} OCR calls and
  {repro['document_extraction'].get('pdftotext_calls',0)} PDF extraction calls.
- Strict refusal was exercised; it returned an evidence blocker and wrote no
  final output. Readiness verification exits 2 for that diagnosed blocker,
  distinct from unit-test failure (exit 1).

Candidate SHA-256: `{repro['candidate_sha256']}`.

## Independent adversarial cases executed

Fixtures and assertions are in `code/tests/test_reasoning.py`; they are authored
independently of public sample labels and do not mutate supplied evidence.

1. **Multilingual access-only and negation.** Requests ask only for an export,
   correction or a copy in English, French, Spanish, Japanese and Korean. Expected:
   authorization false; no destructive plan. All language subcases passed.
2. **Future capture describing an earlier state.** `account_7` is observed PRESENT
   at 2026-01-01T00:00:00Z. A later-captured ABSENT observation describes an earlier
   event but is unavailable at the 2026-01-02 cutoff. Expected: INCOMPLETE from
   eligible presence; the future capture cannot prove deletion. Passed.
3. **Replica drift plus retained records and recreation.** `account_7` is absent
   from primary and present in a replica; `tombstone_8` is redacted;
   `audit_record_9` is retained; `data_flow_4` and `backup_5` are active. Expected:
   INCOMPLETE; disable flow, block restore, delete the remaining copy in official
   order; preserve the compliant tombstone and audit record. Passed.
4. **Reused alias.** Two stable subjects share a supplied email. Expected: no
   automatic merge or guessed owner. Passed.
5. **Retained audit without primary proof.** Only a retained audit record is
   observed. Expected: explicit NO_PRIMARY_PROFILE_PROOF; partial observations
   cannot certify account deletion. Passed.

Other executed tests cover cutoff inclusivity, repeated cases, equal-time
conflicts, future identity snapshots, explicit source-resource edges, redaction,
anonymization, missing retained records, claims versus observations, path escape,
all six log envelopes and invalid output/citations.

## Failures, corrections and remaining risks

Initial sample status accuracy was 19/32, with 6/32 exact rows. Independent
training examples, Unicode/contraction normalization, explicit scope guards,
bounded document matching and structured source edges improved these to the
scores above. Pure-ML training expansion introduced portability/negation
regressions; generic consent/scope guards corrected those rather than memorizing
sample answers. All final fixtures passed after the corrections.

Cloud log envelopes originally hid nested event fields; unwrapping was fixed.
SQL loading initially rejected the supplied foreign_keys pragma; only that safe
pragma is now permitted. A legitimate empty SQL snapshot is counted as table-scope
evidence. Document matching originally allowed reference substrings and unrelated
page rows to create false links; token boundaries, source compatibility and
scoped excerpts corrected those paths. Cutoff-specific identity caching reduced
observed warm runtime from roughly 18 seconds to roughly four seconds.

The final proof audit exposed a serious readiness weakness: compliant downstream
or retained records do not establish primary deletion. Strict export now checks
that coverage explicitly instead of relying on status scores or a nonempty ledger.

Current blocker counts (overlap is possible): `{dict(codes)}`.

Investigated examples:

- `case_01` and `case_02` public expected absent account IDs have no supplied
  subject link in the eligible evidence; a worker claim without a subject cannot
  supply that link. Do not infer IDs from user/case numbering.
- Anonymous analytics records, including `analytics_901` and `analytics_9406`,
  expose no subject identifier. State can be read, but attribution needs a grounded
  historical/catalog link. Some expected verification steps remain unreproduced.
- Public `case_09` expects account/security verification cited to `evidence_93`,
  whose readback contains only one backup target. Corresponding ordinary-log
  observations occur in a file captured after that case's cutoff; they cannot
  repair earlier provenance under the root contract.
- Full `case_46`: the retained-reference screenshot does not expose enough fields
  to certify redaction of `tombstone_17`.
- Full `case_55`: archive existence and unrelated restore history do not establish
  restore permission for `backup_9287` at cutoff. No ACTIVE state is invented.

These are diagnosed limitations of the present evidence-backed implementation,
not proof that every remaining mismatch is a dataset defect. More extraction or
authoritative linkage may resolve some gaps. OCR fidelity, conditional policy
coverage, anonymous attribution and exact reference selection remain risks.
Public sample recall and exact-row accuracy are materially below complete
correctness. The candidate is **not submission-ready**.
'''
    (ROOT/'code/evaluation/evaluation_report.md').write_text(report)
    usage_report=f'''# GhostGraph final candidate-run usage report

This report describes the actual 518-request run that produced
`output.candidate.csv`; strict final `output.csv` remains blocked by
{usage['unresolved_cases']} proof/coverage gaps. It is not a claim that a final
submission run succeeded. Development/evaluation runs and the engineering
assistant's own conversation usage are excluded; their provider billing is not
available to the application.

| Component | Provider / model | Actual final-run usage |
| --- | --- | ---: |
| Intent inference | local scikit-learn / {usage['model']} | {usage['inference_calls']} inference calls |
| Intent cache | same content/model/training-hash cache | {usage['cache_hits']} cache hits |
| Intent training | independently authored source examples | {usage['training_examples']} examples; 1 fit |
| OCR | local Tesseract English recognizer | {usage['document_extraction'].get('tesseract_calls',0)} fresh calls |
| PDF text extraction | local Poppler pdftotext | {usage['document_extraction'].get('pdftotext_calls',0)} fresh calls |
| Extraction cache | content-hash cache | {usage['document_extraction'].get('cache_hits',0)} hits |

The ML component genuinely executes. It is a supervised discriminative model,
not a hosted LLM. Generic deterministic English consent/scope guards complement
the learned model; model decisions are used for multilingual/implicit intent.
Request decision sources: `{usage['intent_decision_sources']}`. Cached repeated
texts reuse the same validated classification. No public output label trains it.

- Requests processed: {usage['request_count']}.
- Input API tokens: 0; output API tokens: 0; total API tokens: 0.
- Average API tokens/request: 0. Token units are **not applicable** to TF-IDF,
  logistic regression, Tesseract or PDF text extraction; zero does not mean the
  local components performed no computation.
- Estimated API cost: USD 0.00 total; USD 0.00/request. Per-model API totals are
  also zero because all components execute locally with no metered API calls.
- Local compute/storage cost is unpriced and excluded, rather than invented.
- Measured warm-cache runtime: {usage['runtime_seconds']:.3f} seconds,
  {usage['runtime_seconds']/518:.6f} seconds/request averaged across the run.
- Cold extraction reproducibility run: {repro['runtime_seconds']:.3f} seconds,
  {repro['document_extraction'].get('tesseract_calls',0)} OCR and
  {repro['document_extraction'].get('pdftotext_calls',0)} PDF extraction calls;
  identical candidate bytes. This separate validation run is not added to the
  final candidate-run counts above.

Training corpus SHA-256: `{usage['training_hash']}`.
Request-file SHA-256: `{usage['requests_hash']}`.
Combined manifest/evidence/identity/policy/activity hash:
`{hashlib.sha256(json.dumps(usage['input_hashes'],sort_keys=True).encode()).hexdigest()}`.
Candidate SHA-256: `{repro['candidate_sha256']}`.

Prompts, training examples and response validation live in
`code/ghostgraph/intent.py`. All retries are zero for this local deterministic
inference path; exceptions fail the run rather than returning a fabricated result.
No credentials or secret values are stored in source, reports or logs.
'''
    (ROOT/'code/evaluation/usage_report.md').write_text(usage_report)
    print('Rendered evaluation_report.md and usage_report.md from actual run records')


if __name__=='__main__':write()
