# GhostGraph milestone record

## M1 — Contracts and ingestion

- Objective: preserve participant evidence, provenance and source/time boundaries.
- Deliverables: official contract validator, six adapters, isolated SQL loading,
  extraction cache, identity tokens and input inspection command.
- Dependencies: Python 3.12, pdftotext, Tesseract; no model API or server.
- Acceptance tests: six log envelopes, complete identifier boundaries, explicit
  timezone handling, path traversal rejection; all 94 manifest files processed.
- Actual results: four unit tests passed after cloud-envelope fixes. Full-input
  acceptance passed: 94 files, 2,913 observations, 116 SQL table scopes, 3,999
  activity claims and 12 catalog links; all six formats processed.
- Failures: cloud messages lost nested event fields; broad pragma rejection
  blocked supplied SQL; observation-only coverage incorrectly rejected an empty
  exported table.
- Corrections: unwrap cloud messages; permit only foreign_keys=ON; distinguish
  table-scope evidence from row observations in coverage.
- Remaining risks: OCR is fallible; some documents need catalog links; unsupported
  subject/resource links must remain unresolved. Later milestones are not yet
  declared complete at that stage.

## M2 — Intent, identity and temporal isolation

- Objective: execute real ML inference and exclude unsupported historical links.
- Deliverables: independently trained local intent model, time-bounded alias
  index, per-case ledger, identity/conflict diagnostics and strict export guard.
- Dependencies: M1 acceptance passed; installed pinned scikit-learn stack.
- Acceptance tests: multilingual positive/negative authorization, alias reuse,
  future snapshots/captures, inclusive cutoff, repeated independent audits,
  equal-time conflict, and refusal to invent resource IDs.
- Actual results: 13 total unit tests passed, including all nine new reasoning
  tests. The model trained and inferred locally; no API key or network needed.
- Failures discovered: dataset subject/resource proof gaps, not repaired by
  sample labels or numeric suffix assumptions.
- Corrections: preserve ambiguous identity as unresolved and reject strict
  exports; treat unavailable later evidence as ineligible.
- Remaining risks: small-model language coverage; anonymous resources without
  explicit subject links cannot be attributed safely.

## M3 — Policy, replicas and plan ordering

- Objective: produce only policy-backed findings and correctly ordered plans.
- Deliverables: supplied-rule loader, ledger treatment, replica preservation,
  flow/restore controls, tombstone and retention handling, canonical serializer.
- Dependencies: M1/M2 acceptance passed.
- Acceptance tests: synthetic primary/replica drift with retained tombstone,
  retained audit, active connector and unsafe backup in one adversarial case.
- Actual results: the combined test passed, verifying DISABLE_DATA_FLOW then
  BLOCK_RESTORE then DELETE_RECORD, without redacting a compliant tombstone.
- Failures discovered: expired retention and missing required records do not
  have a universal action in the official vocabulary.
- Corrections: flag policy gaps rather than invent operations.
- Remaining risks: public sample comparison and full-run coverage remain to be
  measured; this milestone establishes tested mechanisms, not full accuracy.

## M4 — Evaluation and corrective experiments

- Objective: measure actual sample performance, test adversarial behavior and
  detect misleading readiness claims.
- Deliverables: independent evaluator, 26 software tests, provenance verification,
  strict export guard, per-case coverage obligations and judge-visible reports.
- Dependencies: executed M1–M3 mechanism tests; public labels isolated from the
  predictor; no organizer material inspected.
- Acceptance tests: full public evaluation, output/citation checks, retained-record
  coverage, all policy actions, no future leakage and no invented subject links.
- Actual results: 26 tests passed, no failures/errors/skips. Public status accuracy
  29/32 (90.625%); exact rows/sequences 9/32 (28.125%); exact step precision
  159/163 (97.546%); recall 159/193 (82.383%). Metrics are regression scores,
  not hidden-set accuracy. Exact-row acceptance for a final submission is unmet.
- Failures: pure-ML training changes regressed access-only scope; document substring
  and cross-row associations over-linked evidence; some expected anonymous/absent
  resources have no reconstructed subject link. Final coverage inspection found
  that a retained audit alone had incorrectly appeared sufficient for readiness.
- Corrections: generic consent/scope guards, scoped document extraction, explicit
  structured source edges, cutoff-specific index caching and a mandatory primary
  profile proof obligation. Preserve partial predictions for evaluation; strict
  export rejects unresolved proof coverage.
- Additional identity regression checks: shared historical identifiers cannot
  create unique links; conflicting stable references override contact matches;
  resource reassignment produces an explicit unresolved identity state.
- Remaining risks: 335 full cases have diagnosed gaps, including 334 primary-proof
  gaps and two specific state uncertainties with overlap. More authoritative
  linkage/state evidence or justified extraction improvements are needed. This
  evaluation milestone is measured and diagnosed; final submission acceptance
  remains blocked.

## M5 — Reproducibility, source packaging and repository integration

- Objective: deliver reproducible source and candid artifacts without calling an
  unresolved candidate a final submission.
- Deliverables: deterministic code.zip builder, output.candidate.csv, Markdown
  evaluation/usage reports and documented setup/run commands.
- Dependencies: executed software/evaluation checks; final coverage blockers are
  retained explicitly, not bypassed to pass this milestone.
- Acceptance tests: 518 candidate rows, matching internal citation provenance,
  immutable input hashes, strict refusal, fresh-directory cold extraction,
  identical candidate bytes and archive membership/integrity checks.
- Actual results: candidate schema checks and 1,030 internal cited-step provenance
  checks passed; strict export refused 335 unresolved cases and wrote no final
  output. Cold reproduction and archive/integration results are recorded in the
  evaluation report and final session completion log after execution.
- Failures: full verified output.csv cannot yet be produced from the implemented
  eligible ledger. An archive of source is useful but does not complete a final
  competition submission.
- Corrections: candidate has a distinct filename; strict mode remains the default;
  all artifacts disclose unresolved coverage and actual metrics.
- Remaining risks: this milestone is not marked complete as a submission. No
  hosted full session trace is available, and exact engineering runtime model
  metadata is not exposed for the root log's model field.

## Requested Milestone 0 — reconnaissance acceptance

Objective: inventory all major participant inputs and verify the initial output contract. Deliverables: code/INVENTORY.md and standalone validate_output.py, extending the existing contract validator. Dependencies: existing read-only adapters and supplied data. Actual acceptance: all 32 sample rows pass; all six validator regression tests pass, including column order and operation-order rejection. The standalone entry point closes the previous CLI gap. No evidence or root instructions changed. Remaining risks: schema validity does not prove semantic correctness; previously reported linkage/coverage gaps remain outside this milestone. Reconnaissance exit criterion met.
