# V3 research phase decisions

## Experiment 0 — rebuild current diagnostics

Objective: stop evaluating the old certification mismatch artifact. Deliverables:
fresh prediction-mode mismatch_report.md and unlabeled coverage.md for all 518
requests. Dependencies: frozen engine and immutable participant data. Acceptance:
reproduce 9/32 exact, 29/32 statuses, 159/193 matching steps and all 518 baseline
rows. Actual: reproduced; A rows equal protected output.csv exactly. Baseline
sample-only structural gaps remain six errors in three public cases; full target
submission has zero. No hidden labels or semantic coverage assertions were added.

## Experiments 1/2 — candidate matching and staged graph

Objective: recover targets only from independently corroborated ownership.
Deliverables: time windows 60/300/360/900/3600, multi-action/collision control,
provenance chains and bidirectional structured source/copy graph. Dependencies:
cutoff-specific identity resolver and eligible global evidence. Acceptance: never
admit a temporal-only target; preserve replicas, historical ambiguity and time
boundaries. Actual: 15 new adversarial tests pass. The 300-second full-input search
reproduces 118 unique and two multiple-candidate cases, but none has independent
corroboration in that window. At 360 seconds the public search-source pointer
supports one candidate already known to the baseline. No new predicted rows.
Risk: shared/contextual dependency references are not always exclusive ownership;
foreign-reference checks are necessary but not a full schema proof.

## Experiment 3 — verification audit

Objective: identify an omitted check whose identity, policy and state proof already
exist. Source inspection and fresh missing-step diagnostics find the recurring
missing targets fail attribution or state/citation prerequisites. The current
planner already propagates applicable known-resource future goals. No new D
planning rule was justified; D is explicitly a frozen-planner no-op control.
No unsupported verification is inserted to simulate an improvement. Planner
suppression is distinguished from missing source facts in the new mismatch report.

## Experiment 4 — bounded AI review

Objective: compare verified relationship proposals against deterministic extraction.
Deliverables available: source prompt/schema and exact-scoped-source validation
gate, independently tested for inventions, wrong locators/subjects and future
sources. Missing dependency: hosted review/vision model and credentials. Actual
hosted experiment: NOT RUN; zero extra paid calls, no reported recovery or F1 gain.
No claim of a completed live LLM integration. A model proposal that merely guesses
ownership from time or null selectors would not supply independent corroboration.

## Experiments 5/6 — generalization and controlled ablation

Objective: protect the submission and distinguish general capability from measured
gain. Actual acceptance: all 130 tests pass, no skips/errors/failures. A/B/C/D/F
produce the same 9/32 exact rows and 159/193 exact steps. Each 518-row arm has zero
structural violations and zero row changes. The combination is reproduced from
a fresh source/data copy with empty extraction cache and a different working
directory, using the same installed dependencies; output is byte-identical to the
baseline. Timings and actual model calls are in results.md; API tokens/cost are
zero, local token units not applicable and compute unpriced. C/F are slower in
this measured run without accuracy gain; no statistical runtime claim is made.

Promotion recommendation: **reject V3 promotion**. Meaningful measured improvement
is absent; the aspirational 16/32 and 90% recall targets were not achieved.
The experimental implementation is retained for review on its branch. The frozen
CSV, ZIP, tags, production code and official input files are unchanged. No new
submission archive or promoted candidate is generated. Original transcript is
appended separately; source-only research artifacts do not replace session traces.
