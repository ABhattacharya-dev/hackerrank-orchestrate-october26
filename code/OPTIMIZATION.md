# Milestone 6: AI integration and accuracy optimization

## Objective and deliverables

Measure complete public-sample behavior, diagnose every error type and test whether
selective learned inference improves intent coverage over deterministic scope rules.
Deliverables are the enhanced evaluator, mismatch report renderer, frozen AI
ablation, selective inference/cache routing and seven added regression tests.
Dependencies are the existing ingestion/identity/temporal/policy/planning pipeline.
Milestone 5's unresolved evidence/structural blockers remain binding; this work does
not advance final-submission readiness past that broken foundation.

## Measured results and decisions

The 32-case public run produces status accuracy 28/32 (87.5%), exact step precision
111/115 (96.5217%), recall 111/193 (57.5130%), F1 72.0779%, field accuracy 719/1351
(53.2198%), canonical citation accuracy 44/75 (58.6667%) and exact sequence accuracy
2/32 (6.25%). Missing expected citations count wrong in citation accuracy. The
full mismatch taxonomy and per-case explanations are in
`evaluation/mismatch_report.md`; no hidden accuracy is claimed.

The measured 82 missing operations dominate four extra operations. There are no
wrong states/citations on aligned operations or relative ordering errors among
shared steps; this does not make omitted fields, evidence or step numbers correct.
Missing operation types, cutoff/coverage issues and policy unknowns are documented.
Prioritize grounded absent-target identity linkage and state/retention evidence;
formatting and additional intent training cannot supply these facts.

A proposed PDF document-role reclassification added three extra operations without
recovering an expected step and lacked stronger source proof. It was reverted.
Initial experimental document tests failed because their synthetic manifest was
missing; those fixtures were removed with the rejected change. Failures and the
final passing regression counts remain distinct. No parser/policy assumption was
weakened solely to match labels.

The retained optimization applies existing consent/scope guards before ML
inference. Pure deterministic scope rules cover 28/32 public intents; guarded
selective inference handles 32/32 with four learned calls, matching guarded eager
inference's decisions with 32 calls. On 24 independently authored multilingual,
implicit and ambiguous probes, rules alone score 8/24 (including correct ambiguity
abstention), raw ML 23/24, and guarded eager/selective 24/24. These small curated
probes are development diagnostics, not a multilingual generalization estimate.
They were frozen before the first experiment and checked for exact training overlap;
the training corpus was not tuned against them. Ambiguous consent is deferred by
the existing guard, not claimed to be resolved by model confidence.

In the actual full run, learned calls drop from 375 to 5. There are 375 unique
normalized texts, 370 deterministic scope decisions and 143 cache hits. Same-model
and training hashes plus canonical text deduplicate inference; cached responses
are copied to prevent mutation. Deterministic decisions have probability null.
Candidate bytes are unchanged; no full-audit accuracy gain is claimed. Inference
call reduction excludes the single model fit per process and is not a measured
runtime or compute-cost reduction. Local execution has no metered API tokens/cost.

Both optional vision settings were absent; no hosted vision extraction or image
accuracy experiment ran. Five artifacts remain unresolved. The local supervised
classifier actually participates in the pipeline without remote credentials.

## Acceptance and remaining risks

All 97 software tests pass, including evaluator tests for F1, duplicate
multiplicity, missing steps versus wrong states/citations, status/order errors,
and selective/eager equivalence and cache isolation. Regressions ran after each
significant experiment. Cold-cache source-copy reproduction and strict refusal
are exercised by the existing evaluation commands and reported with actual run
records. The root instructions and supplied dataset remain unchanged.

All 32 public references pass strict structural validation; generated output still
has 13 violations across eight cases, with 24/32 rows passing. Those cases lack
supported findings or a fully supported restore remedy. The full run retains 490
unresolved cases and writes only output.candidate.csv in explicit partial mode.
**Milestone 6 exit criterion is not met because all structural checks do not pass.**
The complete mismatch report does not cure these proof gaps. No final output.csv
or complete competitive-submission claim is made.

## Reproduce from the repository root

```bash
python3 code/evaluation/verify.py
python3 code/evaluation/ai_ablation.py
python3 code/evaluation/planning_acceptance.py
python3 code/evaluation/reproduce.py
python3 code/evaluation/optimization_report.py
python3 code/evaluation/write_reports.py
python3 code/package.py
```

Verify and planning acceptance exit 2 for diagnosed blockers; software failures
remain failures, never silently treated as successful readiness. Diagnostics
under .ghostgraph are excluded from source submission; Markdown includes metrics,
methods, every remaining mismatch and limitations for source review.
