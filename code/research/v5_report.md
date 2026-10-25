# V5 authorization safety research

## Decision and scope

Proposed code-quality improvement for review only; no automatic merge or production artifact replacement. CSV accuracy is unchanged, so no improvement in Output CSV points is claimed. The baseline is `3b942ac`, tag `submission-freeze-verified`. Research branch: `experiment/intent-safety-v5`.

The unchanged local TF-IDF logistic regression and its 296 authored training examples remain the learned component. A bounded deterministic speech-act/consent layer precedes it. No evidence, identity, policy, temporal, or planner modules were rebuilt. Diagnostics store clause indices and roles, not duplicate request text. Ambiguity/low-confidence defers authorization; no deletion plan is inferred from that uncertainty. Third-party representative assertions require external authority validation and defer. This agent produces plans, never executes deletion.

## V4 failure analysis, before implementation

The exact V4 script was replayed: frozen and guarded LinearSVC each 21/32, eleven false authorizations, zero missed authorizations. Replacing the estimator alone cannot fix a positive guard. Every failed interpretation below withholds present requester consent; unfulfilled conditions defer rather than imply a permanent refusal.

| Probe | Responsible path | Interpretation | Error / justified target |
|---|---|---|---|
| fr_negation | learned fallback | French explicitly requests access, excludes deletion | false authorization / reject |
| hypothetical_two | positive guard | possible future choice, no current instruction | false authorization / reject |
| deactivation | learned fallback | temporary holiday deactivation preserving data | false authorization / reject |
| quoted | positive guard | translate quoted instruction | false authorization / reject |
| forwarded | positive guard | forwarded quote for translation | false authorization / reject |
| conditional | positive guard | refund not yet received, explicitly wait | false authorization / defer |
| conditional_two | positive guard | separate confirmation not yet provided | false authorization / defer |
| third_party | positive guard | neighbor without consent | false authorization / reject |
| third_party_two | positive guard | observer discussing another customer | false authorization / reject |
| question | positive guard | asks consequences before deciding | false authorization / reject |
| cancel | learned fallback | withdraw prior deletion, preserve registration | false authorization / reject |

All 518 texts were classified before implementation; no hidden answers were accessed. The ten baseline non-authorizations are case_533 (phone correction), case_534 (marketing opt-out), case_535 (export), case_536 (login recovery), case_537 (surname correction), case_538 (marketing only), case_539 (access), case_540 (invoice copy), case_541 (email correction), case_542 (explicitly no deletion). All ten remain NOT_APPLICABLE. Other requests include current deletion and completion/audit of prior deletion. These are text interpretations, not hidden correctness labels.

## Evaluation chronology and leakage boundaries

1. Authored 24 development and 40 sealed probes before implementation; hashes recorded below. V4's 32 probes are known regression only.
2. Development detected 144 changed full-set authorizations caused by neutral `if`/`once` follow-ups. Consent conditions were scoped to erasure clauses before sealed testing.
3. First sealed evaluation: 39/40, zero false authorizations, one missed own-account instruction after mention of a cousin. Baseline 25/40, fifteen false authorizations. This is the honest first held-out score.
4. Authored and froze 24 new prospective probes before generic possessive-head correction. Round two: 24/24 vs baseline 11/24. First 40 became observed regression (40/40), not another unseen claim. No training weights or thresholds were selected from these labels.
5. Final competition audit found six sample-only deferrals not visible in full-output equality. Earlier checks had not surfaced this; claims that sample metrics were unchanged in those rounds were incorrect. Round two was 8/32 exact, 26/32 statuses, 134/193 steps and 18 sample structural errors. It was not promotable.
6. Authored 16 continuation/retention probes before correcting requester-linked prior-erasure audits, residual cleanup, and optional retained-reference conditions. The first continuation pass missed a hypothetical retention question; a generic hypothetical-request rule corrected it. A subsequent sample run still deferred one inspection of a failed own request; generic requester-linked request context corrected it. All final test sets are now observed regression. Do not interpret final perfect challenge scores as fresh held-out validation of these later changes.

The sealed40 and prospective24 were self-authored, small and targeted, not an external benchmark. Round-one and round-two source snapshots are retained. Final added audit rules need broader independent review; no hidden-set generalization claim is made.

## Confusion matrices

Rows are actual authorization A, rejection R, and unresolved consent D; columns are predicted A/R/D. False authorization rate denominator is R+D; missed authorization rate denominator is A. Correct out-of-scope rejection uses R alone. Deferral is internal, not a fourth CSV status.

### First held-out 40 — baseline

| Actual | A | R | D |
|---|---:|---:|---:|
| A | 18 | 0 | 0 |
| R | 12 | 7 | 0 |
| D | 3 | 0 | 0 |

Correct 25/40; false authorization 15 (68.18%); missed authorization 0 (0.00%); correct rejection 7/19.

### First held-out 40 — v5

| Actual | A | R | D |
|---|---:|---:|---:|
| A | 17 | 1 | 0 |
| R | 0 | 19 | 0 |
| D | 0 | 0 | 3 |

Correct 39/40; false authorization 0 (0.00%); missed authorization 1 (5.56%); correct rejection 19/19.

### Prospective round-two 24 — baseline

| Actual | A | R | D |
|---|---:|---:|---:|
| A | 9 | 2 | 1 |
| R | 7 | 2 | 0 |
| D | 2 | 1 | 0 |

Correct 11/24; false authorization 9 (75.00%); missed authorization 3 (25.00%); correct rejection 2/9.

### Prospective round-two 24 — v5

| Actual | A | R | D |
|---|---:|---:|---:|
| A | 12 | 0 | 0 |
| R | 0 | 9 | 0 |
| D | 0 | 0 | 3 |

Correct 24/24; false authorization 0 (0.00%); missed authorization 0 (0.00%); correct rejection 9/9.

## Targeted language and conditional subsets

In the first held-out40, the ten multilingual probes improved 8/10→10/10, and the five conditional-consent/polite-condition probes improved 3/5→5/5. These are subsets of the same test set, not additional independent trials. Known V4 regression multilingual probes also pass; they were available during development. Prospective24 includes French/Spanish/Portuguese scope paraphrases, all passing. Counts are small and not estimates of language-wide accuracy.

## Final post-feedback regression and competition comparison

| Set | Baseline correct | V5 correct | V5 false authorizations | V5 misses |
|---|---:|---:|---:|---:|
| development | 14/24 | 24/24 | 0 | 0 |
| observed40 | 25/40 | 40/40 | 0 | 0 |
| observed24 | 11/24 | 24/24 | 0 | 0 |
| continuation16 | 10/16 | 16/16 | 0 | 0 |

Known V4 regression: 21/32 → 32/32. Multilingual probes include French, Spanish, Portuguese, German, Japanese and Korean; these few examples do not establish comprehensive support. Explicit unfulfilled conditional consent defers; procedural export and ordinary retention clauses do not cancel separate authorized cleanup. Scope-specific negation cannot suppress a separate own-account instruction.

| Public metric | Frozen | Final V5 |
|---|---:|---:|
| status_accuracy | 90.62% | 90.62% |
| exact_row_accuracy | 28.12% | 28.12% |
| step_precision | 97.55% | 97.55% |
| step_recall | 82.38% | 82.38% |
| step_f1 | 89.33% | 89.33% |
| field_accuracy | 79.05% | 79.05% |
| canonical_evidence_accuracy | 78.67% | 78.67% |
| exact_sequence_accuracy | 28.12% | 28.12% |

Final public outputs are compared row by row below in retained results. Public-sample prediction validation has six pre-existing errors in case_01, case_02, case_04 (no supported steps); these are not the submitted full-set rows. Full518 has zero violations, unchanged sorted IDs and byte-identical CSV. Certification still reports unresolved evidence obligations; passing competition validation does not imply strict certification.

## Implementation, usage and remaining risks

Clause-local refusal, quote masking, explicit quote adoption, condition gates, foreign possessor checks and request frames precede the frozen classifier. The model still participates in the normal full run (five learned calls). It receives ambiguous semantic cases after deterministic scope checks, not final JSON. Cache results are isolated deep copies. Low confidence is normalized to unresolved consent so Engine cannot inadvertently build a plan.

Regex scope analysis is bounded and cannot prove arbitrary natural-language consent. Novel quoting, syntax and languages may fail; representative authority is not independently established by text. Continuation audits authorize investigation/planning, not evidence that prior deletion succeeded. No future evidence or operation claim is promoted to state proof. Code-quality promotion is recommended for review only, conditional on the final reproducibility record; no CSV score improvement or strict certification success is claimed. Additional blinded externally authored intent tests would strengthen confidence.

## Reproduction

```bash
python3 -m pip install -r code/requirements.txt
PYTHONPATH=code python3 -m research.v5_final_evaluate
PYTHONPATH=code python3 -m unittest discover -s code/tests -v
python3 code/main.py --mode predict --output .ghostgraph/v5/reproduced.csv
```

The prediction command applies V5. Strict certification is separately `python3 code/main.py --mode certify`; it is expected to reject unresolved proof obligations and is not the normal successful prediction quick-start. One-shot historical scripts use ignored freeze metadata to prevent silently relabeling a tuned evaluation as held-out; use the final evaluator for clean reproducible regression.

## Freeze records

```json
{
  "implementation_freeze.json": {
    "sha256": "f562a5df3c136f41b8fed3f137a30a159cd699a7225f2f1f2ea1b9329a00684f",
    "note": "Final implementation before first sealed evaluation; accounting/copy-isolation fixes completed. No sealed scores examined."
  },
  "probe_freeze.json": {
    "sha256": "86bca6efb26c74c29e4671208395b1e272000cfa5fbe94d2cad8d7a1e69c0072",
    "note": "Frozen before V5 implementation; no model changes or heldout evaluation yet"
  },
  "prospective_freeze.json": {
    "sha256": "196b692d1965e6b8e9384423f5e86cdcadf253e7f351a60512f8ed3807b031bf",
    "note": "Frozen before version-two ownership correction; no scores evaluated"
  },
  "round2_implementation_freeze.json": {
    "sha256": "659731c81a7aa4cd77f8686f643279d10aca552a241d879196ba0bbf6a2952b4",
    "note": "Before first prospective round-two scoring"
  }
}
```
