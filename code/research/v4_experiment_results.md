# V4 evidence-recovery experiment results

**Recommendation: reject promotion.** Branch experiment/evidence-recovery-v4 starts at frozen 3b942ac. Production artifacts, tags and code are untouched; no V3 temporal matching or ineffective graph changes are imported. No hidden labels are available.

## Actual baseline reproduction

| Metric | Frozen baseline / V4 unchanged prediction |
| --- | ---: |
| Correct statuses | 90.625000% |
| Exact rows | 28.125000% |
| Step precision | 97.546012% |
| Step recall | 82.383420% |
| Step F1 | 89.325843% |
| Citation accuracy | 78.666667% |
| Field accuracy | 79.052554% |
| Exact sequence accuracy | 28.125000% |

Counts: 29/32 statuses; 9/32 exact rows; 159/193 exact steps; 1068/1351 fields; 59/75 canonical citations. All 518 full rows pass the official structural validator and match frozen output bytes. Sample-only missing-ID gaps still cause six structural errors in three public cases; no claim that the sample pipeline is fully compliant is made.

There are 23 exact-case failures and three status errors, caused by missing supported verification/resource attribution rather than public-sample intent errors. All 32 public texts authorize deletion. The aligned operations have zero wrong states, zero wrong citations and zero relative ordering errors; the 34 missing and four extra operations dominate. Citation loss is omitted cited steps, not evidence-ID substitutions. Extraction and policy/planner errors are not assumed where the source lacks the necessary fact.

## Original-source audit

Every missing operation has an original-source/normalized comparison and exact locator in v4_evidence_gap_report.md. The 34 gaps comprise: 16 absent original target records/ownership edges; 12 normalized states with erased or missing subject selectors; six records captured only after the case cutoff. The audit found no recoverable new scoped ownership fact and no justified production parser correction. Missing and extra operations, classification errors, policy uncertainty and canonical disagreements are separated in the matrix. This is a conclusion about inspected participant evidence, not proof the dataset or canonical answers are wrong.

Global activity/anonymization history for these targets was also inspected. Worker/policy events name resources but contain no eligible matching subject identifier or authoritative relation. Their operation-result claims are not independent state proof. Historical aliases and explicit catalog links already enter the frozen index. No temporal-candidate matching was repeated.

## Controlled variants and stop decisions

| Variant | Execution / outcome | Prediction impact |
| --- | --- | --- |
| A frozen baseline | Executed on 32 samples and all 518 requests; metrics above | 0 differences, 0 full structural errors |
| B improved deterministic document parsing | NOT IMPLEMENTED: no recoverable source-field loss established | No candidate; no invented B scores |
| C original-source validation | Executed against real matching JSON records; synthetic normalized-loss/mutation tests pass | 0 novel facts; no new ledger admission or changed outputs |
| D targeted multimodal extraction | NOT RUN: no configured deployable hosted model/credentials and no plausible missing image fact demonstrated | No D accuracy, tokens or gains assigned |
| E policy-convention correction | Audit completed; no evidence-backed correction justified | No candidate; supported extra findings retained |
| F best validated combination | Frozen inference retained because C adds no novel facts and B/D/E supply no justified changes | No new candidate or new F model benchmark claimed |

Unchanged before/after metrics describe the retained frozen predictor, not fabricated executions of unimplemented variants. This research does not claim all six models were run. The user-directed stop criterion applies after original-source information fails to support recovery.

## Tier A / Tier B validation

Tier A validates a timestamp-eligible scoped normalized record. Tier B reopens the exact original JSON pointer, independently confirms resource and authoritative subject fields in that record, checks original system/container scope, ownership/reassignment conflicts and capture/observation timestamps, and creates a typed observation from source state. It does not require an earlier normalized subject match. Model confidence and proposed states cannot override source facts. Free-text mentions, neighboring rows, parent-page co-occurrence and unsupported image/PDF regions remain diagnostic proposals.

Actual source validation: `{'future capture': 224, 'accepted_already_normalized': 276, 'future observation': 2}`. All 276 accepted facts are already normalized; 224 future captures and two future observations are rejected; zero novel facts enter any ledger. Exact accepted/rejected proposals and reasons are stored under ignored .ghostgraph/v4/source_validation.json. No actual hosted model proposal was generated.

An initial prototype appeared to find two novel legal-hold facts. Direct source review showed those records were already parsed under explicit legal_service scope; prefix-only finance_service normalization had created artificial novelty. The validator now honors original record/container system scope and inherited snapshot times. New independent tests catch this, timestamp mutation, erased owners, cross-record attribution, invented system/fields and retained tombstones. This was a research-validator defect, not an accuracy gain or a production parser loss.

No production vision integration is adopted: the existing optional adapter’s vision_review_required proposals cannot be self-validating observations. Original image regions would require an independent geometric/field verifier or an authoritative catalog relationship. The object-browser extra already has such a catalog link; image-wide filenames are not joined to unrelated subjects.

## Canonical-convention audit

The inspected SQL failover capture permits scoped absence checks for independently linked resource IDs, but cannot supply ownership of absent account IDs. Null-subject analytics can prove an anonymized state, not which customer owned the record; common product names/metrics are not authoritative order links. Retained audit records captured later cannot name earlier plan targets merely because future verification citations are empty. The explicit exclusive object catalog and independent second account readback support the four extra steps, so suppressing them only to fit the reference is not adopted. No generic rule choosing one account per user or omitting required retained checks is supported by the official contract.

## Independent intent comparison

32 new authored probes were frozen before evaluation and checked for exact overlap with the authored training corpus. They cover multilingual deletion/negation, implicit consent, hypothetical requests, temporary deactivation, marketing, export, correction, translation/forwarded quotes, conditional consent, third-party and duplicate deletion instructions. Conditional unconfirmed consent expects deferral. Labels are research expectations and are not hidden benchmark truth.

| Method | Correct | False authorizations | Missed deletion | Abstentions |
| --- | ---: | ---: | ---: | ---: |
| guards | 9/32 | 8 | 8 | 16 |
| baseline | 21/32 | 11 | 0 | 1 |
| guarded_svc | 21/32 | 11 | 0 | 1 |

The alternative is an actually executed local LinearSVC with the same word/character TF-IDF features and unchanged authored training corpus, C=1, balanced weights, deterministic seed and the same scope guards. It does not improve reliability, so it is rejected. No training or guard changes were tuned against probe failures. The learned component improves multilingual/implicit coverage relative to guards alone, but this new challenge set exposes false authorization in quoted, conditional, third-party and other out-of-scope requests. Public samples contain no non-deletion cases and cannot reveal these failures. All texts and per-arm errors are in v4_intent.py and the ignored intent_comparison.json.

## Tests, runtime and actual usage

All 133 software tests pass, including the 115 frozen tests and 18 new source-boundary/mutation tests. Classifier challenge failures above remain failures of accuracy, not mislabeled passing assertions. No old tests are disabled. Production safety and output validation are unchanged.

| Run | Learned calls / cache hits | Runtime seconds | Paid API calls / tokens / USD |
| --- | ---: | ---: | --- |
| Sample baseline | 4 / 0 | 1.591874 | 0 / 0 / 0.00 |
| 518-request baseline | 5 / 143 | 12.434355 | 0 / 0 / 0.00 |
| Intent comparison | frozen 15; SVC 32; two fits | 0.293398 | 0 / 0 / 0.00 |
| Source-validation measurement | 0 / N/A | 5.742851 | 0 / 0 / 0.00 |

Local TF-IDF/SVC token units are not applicable; no text-token estimate is invented. No paid provider tariff applies and local CPU/storage cost is unpriced. Hosted evaluation is NOT RUN, not an observed zero-gain model. Engineering image review is not a deployed paid extraction call. Key/model presence was checked without printing secrets; no credentials were requested.

## Promotion and artifacts

Reject V4 promotion: no recoverable new source fact, no meaningful public gain, and no better tested intent replacement. Aspirational accuracy increases are not forced. No protected CSV/ZIP/tag is overwritten, no new competition ZIP is prepared and no experimental code is merged into main. The source prototype remains research-only. The existing production reproduction remains valid because production is unchanged; no new V4 candidate is claimed to have passed clean installation/reproduction.

The append-only shared transcript is preserved separately. Original local structured session directories were unavailable in prior verified checks; missing traces or engineering runtime model metadata are not reconstructed or fabricated. The participant handles the separate AI interview. No leaderboard point estimate is inferred from these accuracy metrics.
