# V4 evidence recovery research

Branch experiment/evidence-recovery-v4 starts at production freeze 3b942ac.
No V3 temporal matching or ineffective graph inference is imported. The V3
prediction-mode mismatch Markdown is reused as diagnostic tooling only.
Protected output.csv, code.zip, official datasets and frozen tags are untouched.

From this experimental checkout, with the existing pinned dependencies:

```bash
python3 code/research/v4_baseline.py
python3 code/research/v4_audit.py
python3 code/research/v4_intent.py
PYTHONPATH=code python3 -m unittest discover -s code/tests -v > .ghostgraph/v4/tests.txt 2>&1
python3 code/research/v4_source_measure.py
python3 code/research/v4_results.py
```

These commands never generate protected submission artifacts. Predictions and
raw diagnostic records stay under ignored .ghostgraph/v4. Research Markdown
contains actual metrics, source locators, limitations and stop decisions. Read
v4_evidence_gap_report.md, v4_source_facts.md and v4_experiment_results.md.

## Milestones and decisions

0. Reproduced frozen prediction mode, 9/32 exact, 29/32 statuses, 159/193 steps;
   all 518 rows equal protected output bytes and pass strict structure.
1. Inspected original JSON records, readback lines/traces, SQL boundaries and
   global operation histories for every missing step. Six targets are available
   only in later captures; twelve have normalized states but no owner; sixteen
   have no original manifest target/ownership record. None is a demonstrated
   recoverable parser loss. The extra object-browser finding was checked against
   the actual multi-row image plus its explicit exclusive catalog relationship.
2. No production document parser or vision-admission modification: no measured
   new source fact supports one. Existing vision proposals stay diagnostic.
3. Built a research-only Tier A/B validator. Unlike V3, Tier B need not find the
   subject in prior normalization: it reopens the exact source JSON record,
   checks authoritative owner fields, original system/container/time, alias
   conflicts and state. Non-JSON regions remain diagnostic without an independent
   region verifier. Synthetic normalization-loss tests show the distinction;
   real data yielded 276 already-normalized facts and zero novel ones. The initial
   prefix-only prototype's two apparent novelties were scope errors, corrected
   after original-source inspection and protected by mutation tests.
4. Hosted multimodal experiment NOT RUN: no configured deployable credentials/
   model and no plausible missing scoped image fact was established. No keys were
   requested, no hosted token/cost or accuracy gains fabricated.
5. Canonical conventions audited against policy: do not omit justified extras or
   invent absent resource IDs merely to fit canonical examples. Future empty
   verification citations do not authorize discovering target IDs from later files.
6. Compared fixed guards, frozen learned classifier and a real local LinearSVC
   alternative on 32 new held-out probes. Frozen and alternative each score
   21/32 with 11 false authorizations; no replacement or tuned guard is adopted.
   This failure is disclosed separately from public all-deletion intent scores.
7. A measured; C measured as original-source validation with no new facts. B/E
   have no justified changes, D unavailable and F retains frozen inference. No
   fabricated variant executions or scores. All 133 software tests pass, including
   18 new source-boundary/mutation tests; classifier challenge errors remain errors.
8. Reject promotion: no meaningful score gain, novel fact or better replacement.
   No new candidate ZIP, output replacement or main merge is prepared. Production
   code and artifacts stay frozen. No claim of a newly validated V4 clean package.

Tests use temporary fictional records, never mutate supplied evidence. No
canonical case ID is consulted by the source validator or intent model. Labels
remain inside audit/evaluation tooling. Local tokens are not API token units;
compute is unpriced. Transcript snapshots remain real append-only summaries;
unavailable original sessions and exact engineering runtime model metadata are
not reconstructed. The participant handles the separate interview.
