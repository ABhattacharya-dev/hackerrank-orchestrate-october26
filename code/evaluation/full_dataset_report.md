# Full-dataset acceptance report

**Acceptance: blocked.** A candidate is not a final submission. No invalid or unsupported rows are padded to meet the row count.

| Check | Actual result |
| --- | ---: |
| Request / candidate rows | 518 / 518 |
| Exactly keyed and sorted | True |
| Strict structural passing rows | 420 / 518 |
| Strict structural violations / affected cases | 171 / 98 |
| Cited steps checked against source/linkage/cutoff ledger | 729 |
| Cases with unresolved proof obligations | 490 |
| Software tests / failures / errors / skipped | 104 / 0 / 0 / 0 |
| Dataset / root instructions unchanged | True / True |
| Newly generated strict root output.csv | False |

Strict structural validation includes exact header/keys/count, statuses, phase/operation/state enums, consecutive numbering, official phase/operation/lexicographic ordering, source system/resource membership, duplicate and contradictory steps, complete finding/remedy/verification sequences, citation existence/cutoffs and blank future citations. Ledger provenance checks also trace each cited step to internal source, subject linkage and timestamp proof. They do not independently establish hidden canonical correctness.

The strict command was attempted against the actual repository-root output.csv path. Failure preserves any existing destination and records the blocker; it does not publish output.candidate.csv under a new name.

Strict export result: `490 unresolved cases; no final output written. Inspect .ghostgraph/final_attempt_diagnostics.json. --allow-unresolved writes a PROVISIONAL candidate only.`.

## New on-disk adversarial scenarios

All seven new tests execute as part of the successful regression suite in `code/tests/test_adversarial_pipeline.py`. They exercise real evidence files and the CLI, not mocked final predictions.

1. **Empty primary SQL table, same-named regional replica table with PII, live import connector.** Explicit database IDs must preserve both scopes. A successful deletion activity claim cannot erase replica presence. Expected: disable connector, then delete the remaining copy; cite the replica snapshot.
2. **Historical email boundary with equal-time contradiction and later capture.** Before the change, use the old alias; at the inclusive change time, resolve the new alias through audit history. A later-captured ABSENT observation cannot backdate state. Equal-time opposing eligible observations block strict export.
3. **Compliant retained tombstone, security retention, active legal hold and unsafe restore.** Explicit supplied condition facts apply the real policy. Expected: block restore, preserve every required record and verify tombstone redaction; no record deletion.
4. **Repeated subject with later tombstone redaction, requests in reverse temporal order.** Expected earlier INCOMPLETE and later COMPLETE, with unchanged results when request input order reverses.
5. **Two users sharing a historical email.** Ambiguous request must produce no destructive plan; a uniquely grounded alias may plan only the correct user’s record.
6. **French, Spanish and Korean negation with live PII.** Expected NOT_APPLICABLE and no steps; available data never creates authorization.
7. **Manifest names a missing artifact.** Expected detectable MissingFile failure and no strict output.

The first scenario initially failed because the adapter used table name alone as the copy scope. The correction honors explicit snapshot_scope.database_id and propagates it into absence scopes. It never guesses database identity from filenames. All seven tests and the broader regression passed after correction. Supplied dataset bytes were not changed.

## Actual final candidate-run model usage

- Provider/model: `local scikit-learn / ghostgraph-intent-hybrid-word-char-logreg-v5-selective`.
- 518 requests; 5 actual learned inference calls, 370 deterministic unique scope decisions, 143 classification cache hits.
- OCR/PDF extraction: `{'cache_hits': 15}`. Separate cold reproduction is reported in usage_report.md.
- Paid model/API calls: zero. API input tokens: 0; API output tokens: 0. Token units do not apply to local TF-IDF/logistic regression, OCR or PDF extraction; no text-token estimate was invented.
- Metered API cost: USD 0.00 total and per request. No paid provider tariff was used, so no external token pricing applies. Local CPU/storage cost is unpriced, not asserted to be free. Model fitting is reported separately from inference calls in usage_report.md.
- The strict attempt and adversarial/public/regression/reproducibility runs are separate validation work, excluded from the candidate-run counters. No completed final-submission run is claimed.

Application runs executed by this acceptance command (test fixtures and cold reproduction are separate):

| Phase | Requests | Learned calls | Cache hits | API input/output tokens | API cost USD |
| --- | ---: | ---: | ---: | ---: | ---: |
| sample | 32 | 4 | 0 | 0/0 | 0.00 |
| full | 518 | 5 | 143 | 0/0 | 0.00 |
| strict | 518 | 5 | 143 | 0/0 | 0.00 |
| final_attempt | 518 | 5 | 143 | 0/0 | 0.00 |

Candidate SHA-256: `b83ff6a9b086a53ceda99b3f527eefda36ec49f69db392f84be51fdecb01e7c3`.

## Every strict structural blocker

| Case | Failed checks |
| --- | --- |
| case_103 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_107 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_108 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_111 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_123 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_124 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_135 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_137 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_147 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_157 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_159 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_160 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_162 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_171 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_179 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_206 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_207 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_232 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_253 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_255 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_257 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_260 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_265 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_267 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_279 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_280 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_282 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_291 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_303 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_304 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_309 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_315 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_34 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_342 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_354 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_362 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_363 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_369 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_383 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_387 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_392 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_399 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_403 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_408 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_409 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_411 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_412 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_42 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_43 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_435 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_447 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_45 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_456 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_457 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_458 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_459 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_46 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_462 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_47 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_471 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_479 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_483 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_484 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_495 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_503 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_506 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_507 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_508 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_512 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_516 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_519 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_520 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_521 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_522 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_53 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_531 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_543 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_544 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_545 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_546 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_547 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_548 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_549 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_55 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_550 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_58 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_59 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_60 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_66 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_67 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_75 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_76 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_83 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_84 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_86 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_87 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |
| case_88 | INCOMPLETE_WITHOUT_FINDING, NO_SUPPORTED_STEPS |
| case_99 | FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION |

These failures do not authorize invented resources, findings, capabilities or evidence. A structurally passing row can still have incomplete semantic coverage; the separate unresolved proof count remains binding. Full strict acceptance and the root output.csv milestone remain unmet.
