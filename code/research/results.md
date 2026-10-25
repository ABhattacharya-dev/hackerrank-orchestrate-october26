# V3 controlled experiment results

Baseline 3b942ac / submission-freeze-verified. Work is isolated in experiment/evidence-linkage-v3. Frozen output.csv and code.zip are never written. No hidden labels are available.

| Arm | Exact rows | Status | Step P / R / F1 | Citation | Field | Sequence | Sample / full structural violations | Full rows changed | Seconds sample / full |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | 9/32 | 90.6250% | 97.55% / 82.38% / 89.33% | 78.67% | 79.05% | 28.1250% | 6 / 0 | 0 | 0.415 / 2.368 |
| B | 9/32 | 90.6250% | 97.55% / 82.38% / 89.33% | 78.67% | 79.05% | 28.1250% | 6 / 0 | 0 | 0.190 / 2.769 |
| C | 9/32 | 90.6250% | 97.55% / 82.38% / 89.33% | 78.67% | 79.05% | 28.1250% | 6 / 0 | 0 | 0.664 / 6.336 |
| D | 9/32 | 90.6250% | 97.55% / 82.38% / 89.33% | 78.67% | 79.05% | 28.1250% | 6 / 0 | 0 | 0.182 / 2.597 |
| F | 9/32 | 90.6250% | 97.55% / 82.38% / 89.33% | 78.67% | 79.05% | 28.1250% | 6 / 0 | 0 | 0.635 / 6.734 |

A frozen prediction; B corroborated temporal-only (360 seconds); C staged bidirectional structured-reference graph; D verification audit with frozen planner (no unsupported new obligation rule); F B+C+existing planner. E targeted LLM review: NOT RUN; no configured review/vision credentials and model. E is not assigned baseline scores or a fabricated zero-effect experiment. The validated proposal gate is implemented but no hosted inference advantage is claimed.

## Window investigation

| Requests | Window seconds | Candidate cases | Unique cases | Multi-candidate cases | Stage counts (events) |
| --- | ---: | ---: | ---: | ---: | --- |
| sample | 60 | 2 | 2 | 0 | {'weak_candidate': 2} |
| sample | 300 | 7 | 7 | 0 | {'weak_candidate': 6, 'corroborated_derived': 1} |
| sample | 360 | 8 | 8 | 0 | {'weak_candidate': 7, 'corroborated_derived': 1} |
| sample | 900 | 9 | 7 | 2 | {'weak_candidate': 11, 'corroborated_derived': 2} |
| sample | 3600 | 30 | 13 | 17 | {'weak_candidate': 54, 'corroborated_derived': 8} |
| full | 60 | 22 | 22 | 0 | {'weak_candidate': 22} |
| full | 300 | 120 | 118 | 2 | {'weak_candidate': 122} |
| full | 360 | 124 | 111 | 13 | {'weak_candidate': 137} |
| full | 900 | 145 | 24 | 121 | {'weak_candidate': 360} |
| full | 3600 | 483 | 173 | 310 | {'weak_candidate': 994, 'corroborated_derived': 82} |

Candidates are timestamp proposals only. Ownership must come from an eligible explicit subject-target event, scoped record, catalog or structured source/copy proof. Success/PARTIAL, reported workflow status, uniqueness, relative timestamp and readback absence never establish ownership. One event cannot identify distinct subjects; repeated same-subject workflows remain permitted. Multiple actions require independent proofs for every target. Event time must fall within requested_at..audit_at. A 303-second candidate is outside 300 seconds; rounding it into the window would be incorrect.

Candidate readback/snapshot state is always reconstructed independently. Worker SUCCESS never establishes absence; explicit replica presence survives primary absence. Wide windows increase incidental collisions. The staged graph records direct, corroborated-derived, weak and rejected relations separately with locators and availability.

## Usage, generalization and decision

Each arm executes the same genuine local intent model and deterministic policy/planning pipeline. Per-arm calls and cache hits are in the table below. All API input/output tokens and paid-model cost are zero; local TF-IDF tokens are not applicable and CPU cost is unpriced. No paid provider tariff or LLM accuracy gain is claimed. Ingestion and graph/window investigation time are recorded separately in the JSON research artifact, not conflated with arm prediction runtime.

| Arm | Sample learned calls / cache hits | Full learned calls / cache hits | API tokens / cost |
| --- | ---: | ---: | --- |
| A | 4 / 0 | 5 / 143 | 0 / USD 0.00 |
| B | 4 / 0 | 5 / 143 | 0 / USD 0.00 |
| C | 4 / 0 | 5 / 143 | 0 / USD 0.00 |
| D | 4 / 0 | 5 / 143 | 0 / USD 0.00 |
| F | 4 / 0 | 5 / 143 | 0 / USD 0.00 |

Shared ingestion 0.324s; window/ownership investigation 6.853s; total runner 31.262s. Arm timings exclude model fit and shared ingestion; each arm/dataset fits one local model, ten fits total. These are single-run measurements, not a runtime significance claim.

Promotion recommendation: **REJECT promotion**: no measured meaningful exact-row improvement. Keep frozen production submission.

Risks: structured dependencies can express shared context rather than exclusive ownership, and stale identifiers can be reassigned. Reverse edges reject foreign stable references and known foreign/ambiguous contact ownership, but uncommon schema semantics still need validation. Temporal uniqueness is not evidence independence. Review validators can confirm exact parsed-record linkage but cannot certify novel semantic relationships; an LLM must not bypass them. No experimental arm is merged or exported over baseline artifacts.

Regression: 130 tests executed; 0 failures, 0 errors, 0 skipped. Includes 15 independent V3 tests and all 115 frozen tests.

Fresh source/data copy, different working directory and empty OCR cache reproduced all 518 combination rows byte-identically in 24.095s. Same installed pinned runtime; not a new dependency installation. SHA-256 61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891. Cold extraction used {'tesseract_calls': 11, 'pdftotext_calls': 4}; 5 local intent calls and 143 classification cache hits. This separate validation is excluded from arm counters.
