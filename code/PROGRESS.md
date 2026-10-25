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

## Requested Milestone 1 — ingestion/provenance acceptance

Objective: process every artifact with source traceability and detectable failures. Deliverables: per-file outcomes, transactional parser failures, CSV observations, preserved activity/audit rows, idempotent global indexes, trace API and optional configured vision escalation. Dependencies: local PDF/OCR tools; remote vision remains unconfigured. Actual results: 94 outcomes (89 processed, 5 processed_unresolved), zero parser failures, 2,906 observations, 116 scopes, 4,317 original global CSV rows. All 32 tests passed; final ingestion-focused rerun passed 8 tests. Failures discovered and corrected: malformed JSON rows escaped the narrow exception handler; partial artifacts now roll back. Remaining risks: five multimodal artifacts await configured review, remote vision transport unverified, and prior audit coverage gaps remain. Exit criterion met; see code/INGESTION.md.

## Requested Milestone 2 — intent and historical identity

Objective: defensible consent and subject linkage without cross-user plans. Deliverables: v4 local ML/scope classification, cancellation/hypothetical/ambiguity guards, cutoff-specific grounded resource/catalog identity links, per-alias provenance, and standalone public acceptance runner. Dependencies: existing evidence store and local scikit-learn. Actual tests: 32/32 public intents, 32/32 unique subject resolutions with eligible alias proofs, all 38 software tests passing; full predictor regression executed. Failures corrected: ambiguous identities could still plan; foreign dependencies could propagate; cancellation and how-to wording could authorize incorrectly. Remaining risks: finite ML language coverage, unknown ownership boundaries and unresolved full-audit coverage. Exit criterion met for the documented public/adversarial acceptance.

## Requested Milestone 3 — temporal reconstruction

Objective: defensible state at audit_at with explicit uncertainty. Deliverables: standalone temporal reducer, per-scope explanations, mutation-claim invalidation, snapshot-time/coverage metadata, trace-link availability and indexed claims. Dependencies: prior ingestion/identity layers. Actual tests: all 55 software tests pass, including 17 temporal cases and end-to-end repeated-user cutoff/replication tests; full regression and fresh-directory reproduction executed. Failures corrected: quality discarded contradictions, conflict order depended on input, collector scope alignment was implicit, and a scoped absence test lacked coverage uncertainty. Remaining risks: unknown scope alignment/coverage and source-state gaps; stricter guards now block 457 full cases. Exit criterion met for documented temporal/replica tests; no final-submission readiness claim.

## Requested Milestone 4 — policy, obligations and resurrection risk

Objective: conditional policy decisions, complete known-resource obligations and safe resurrection controls. Deliverables: policy.py, risks.py, obligation ledgers, condition provenance, process histories/current state, dependency plans and dedicated acceptance runner. Dependencies: supplied CSV and prior temporal/identity layers. Actual results: all 76 tests pass; 21 focused acceptance tests cover all 15 supplied categories and emitted retained-record safety; 80 public ledger entries across 11 categories validate. Full regression and cold reproduction executed. Corrections: replaced category-only applicability, added independent retained-archive presence obligations, blocked clean-label contradictions and unmitigated process preconditions, and separated canonical order from execution dependencies. Remaining risks: missing predicate facts and prior temporal/linkage gaps leave 490 cases unresolved; current sample status 28/32 and exact rows 1/32. Exit criteria met for category coverage and custom preservation tests, not final submission acceptance.

## Requested Milestone 5 — deterministic planning and generation

Objective: assemble exact decisions/plans without inventing proof or execution.
Deliverables: planner.py, stricter contract validator, source namespace checks,
14 planner tests, planning_acceptance.py and PLANNING.md. Dependencies: preceding
intent/identity/temporal/policy ledgers and their unresolved evidence conditions.
Actual acceptance: 90 software tests pass; public reference 32/32 structurally
valid; generated sample 24/32 valid with 13 violations across eight cases.
Failures: five cases lack supported findings, three restore risks lack full
supported remediation. An obligation-compilation regression for missing retained
records was caught and corrected. Future required checks improve exact rows from
1/32 to 2/32 without copying labels. Remaining risks: full 490 unresolved cases,
namespace/extraction limits and incomplete evidence linkage. **Exit criterion
NOT MET**; no next milestone or final submission readiness is claimed.

## Requested Milestone 6 — AI integration and accuracy optimization

Objective: measure all sample errors and optimize inference based on experiments.
Deliverables: full mismatch taxonomy/Markdown explanations, F1, frozen 24-probe
four-arm AI ablation, selective routing/dedup and seven added regression tests.
Dependencies: current pipeline and unresolved M5 foundation. Actual results:
97 tests pass; sample status 28/32, step P/R/F1 96.5217/57.5130/72.0779 percent,
field 53.2198%, citation 58.6667%, exact sequence 2/32. Guarded selective intent
matches eager decisions (32/32 public, 24/24 authored probes), using 4 vs 32
public model calls; full calls fall 375 to 5 with unchanged candidate bytes.
Failures/corrections: rejected a document-role reclassification that added three
extra operations; fixed evaluator alignment/multiplicity and isolated cached
responses. Remaining risks: 82 missing/4 extra operations, eight structurally
blocked sample cases and 490 unresolved full cases; remote vision unconfigured.
**Exit criterion NOT MET** because generated all-case structural acceptance still
fails. See OPTIMIZATION.md and evaluation/mismatch_report.md; no later milestone
or final readiness is claimed.

## Requested Milestone 7 — adversarial scenarios and full acceptance

Objective: new independent file-to-CLI tests plus exact full-dataset publication.
Deliverables: seven new temporary-data scenarios, explicit SQL database scopes,
full_acceptance.py, full_dataset_report.md and ADVERSARIAL.md. Dependencies: existing
pipeline and unresolved prior proof/structural gates. Actual tests: 7/7 new
scenarios and 104/104 complete regressions pass, no skips/errors/failures. The
replica fixture initially failed because identical SQL table names merged across
physical databases; explicit database_id and matching absence scopes corrected it.
Full run: 518 exactly keyed/sorted provisional rows, 729 matching internal cited
proofs; strict structure passes 420 rows and reports 171 errors across 98 cases.
Strict root output.csv attempt refuses 490 unresolved semantic cases and writes
no final file. Actual candidate usage is 5 local inference calls, 370 deterministic
scope decisions, 143 cache hits, zero paid API calls/tokens/cost; local compute
unpriced. Remaining risks: missing links, condition facts, copy/state proofs and
restore capability. **Exit criterion NOT MET**; no fabricated rows or renamed
candidate to conceal the failure. Detailed evidence in ADVERSARIAL.md and reports.

## Recovery V2

Checkpoint a0437e3 retained as recovery-checkpoint-a0437e3. Historical isolated
code snapshots and current baseline reproduced. Added separately selected
prediction mode without changing default certification behavior. Actual results:
107 tests pass; exact rows 2 -> 9, status 28 -> 29/32, exact steps 111 -> 159/193,
field 719 -> 1068/1351, citations 44 -> 59/75. Full structural errors 171 -> 2,
affected cases 98 -> 1; uncertainty-bearing cases remain 490 by design. The target
to exceed initial 9 exact rows was not achieved. Root output.csv is blocked by
case_55: archive presence and unrelated historic restores do not establish its
restore permission. Stronger final predictions would require legitimate evidence
links rather than null lookups or suffix-based identity guesses. Best-effort
output.prediction.candidate.csv and detailed recovery report delivered.

## Final restore blocker and prediction submission

Objective: ground the remaining restore-risk prediction and publish valid output.
Read actual image: target detail contains verified checksum, prior target drill,
archive path and retention in healthy same production domain; eligible catalog
links subject and target. Added prediction-only typed inference with source/locator
and catalog-time provenance. Other archive restores, future evidence, disabled
service, foreign domain and explicit target blocks cannot supply active risk.
Seven counterfactual tests added; 114/114 total tests pass. Full output now 518
rows with zero structural violations (formerly two in one case). Public metrics
unchanged: 9/32 exact, 29/32 status, 159/193 steps. Cold source-copy output matches
bytes; 1,032 cited steps pass internal eligible provenance checks. Certification
remains conservative; 490 prediction cases carry uncertainty. Source extraction
required Activity-section scoping and an OCR storage-scheme variant correction.
Final reports lead with prediction results and disclose inferred restore capability
versus directly observed authorization. No further ungrounded identity shortcut
adopted for anonymous/null-linked sample artifacts.

## Submission audit and freeze

Protected b513080 with submission-baseline-b513080 tag and original artifact
backup. Corrected an overstated target drill: it predates archive creation, so
is only history. Added chronology regression, retained explicitly uncertain
operational-domain prediction; no prediction rows changed. Clarified successful
README quick-start (--mode predict) versus separately failing conservative
certification (--mode certify). 115 tests pass; 518 rows validate, zero official
structural violations; cold reproduction matches original output bytes. Public
metrics unchanged. Local structured trace locations checked: no sessions present;
agent-trace.zip cannot be honestly exported. Source package regenerated for
chronology correctness, clear documentation and test coverage, not scoring changes.


## V5 experimental authorization safety

Objective: reduce false authorization without changing competition output. Deliverables: consent-layer wrapper, pre-authored probes, failure analysis and reproducible evaluation. Dependencies: existing local sklearn model and participant-facing data. Acceptance: complete regression, baseline public metrics and byte-identical 518 predictions with zero full structural errors. Failures: neutral follow-up conditions, own-account modifier attribution and sample-only completion-audit deferrals; corrected through explicit clause/request scope. Actual results and remaining uncertainty are in research/v5_report.md and v5_results.md. Production artifacts and frozen tags are preserved; no automatic merge.
