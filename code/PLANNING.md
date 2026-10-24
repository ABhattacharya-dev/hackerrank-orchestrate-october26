# Deterministic planning and submission contract

Milestone 5 implementation is tested; its full sample acceptance is **blocked**.
No final output.csv is produced and no proposed mutation is represented as executed.

## Planner and validation

`ghostgraph/planner.py` builds NOT_APPLICABLE only from non-deletion authorization,
with an empty array. Supported findings select INCOMPLETE. In their absence,
COMPLETE requires cited verification and no unresolved upstream proof obligation.
Unknown cases remain explicitly provisional in candidate mode; strict export refuses them.

Findings require source evidence. Remediation has empty citations; all verification
in an incomplete plan describes future checks and has empty citations. Satisfied
policy applicability can add required future checks to a supported finding plan,
including retained-record presence checks. This does not prove current compliance
or supply missing remediation capabilities. Missing retained records cannot be
repaired with an invented operation or converted into a complete decision.

The planner copies its inputs, merges equivalent steps deterministically, checks
required obligations, rejects contradictory final goals and orders by official
phase/operation precedence followed by lexicographic system/resource IDs. It then
assigns consecutive step numbers. Dependency safety remains a separate internal
execution graph; order conflicts block strict export.

`ghostgraph/contract.py` checks exact fields/types, enums, numbers, duplicate
steps, contradictory goals, complete finding/remedy/check pairs, citations and
cutoffs, and row membership/order. Explicit exceptions remain active under Python
optimization. JSON rejects duplicate keys and nonfinite numbers. Serialization
uses compact UTF-8 JSON with stable keys and standard CSV quoting/newlines;
writes replace the destination only after a temporary CSV is closed.

Generation enforces a source-derived system/resource registry. Registry membership
is a namespace guard, not proof of subject linkage or state; those remain ledger
obligations. Absent target IDs need not occur as captured records, so reference
validation defaults to syntax/citation availability. `--check-registry` adds
source membership checking; it must not be mistaken for independent semantic
verification of the public answers.

## Executed acceptance

- 90 software tests passed, zero failures/errors/skips, including 14 planner tests.
- All 32 public reference rows pass strict structural validation.
- 24/32 generated sample rows pass; 13 violations remain across eight cases.
- case_01, case_02, case_04, case_31 and case_32 lack supported findings/steps.
- case_09, case_14 and case_17 contain restore findings without a supported full
  remedy/check sequence; unknown policy conditions are not fabricated.
- The 24-row passing subset has zero structural violations and is a diagnostic
  artifact only. It does not satisfy the required 32-row sample pipeline.
- Public status accuracy is 28/32 (87.5%); exact rows/sequences 2/32 (6.25%).
  Exact step precision is 111/115, recall 111/193. These are development regression
  measurements, not held-out generalization or structural acceptance claims.
- Full-run strict export remains blocked on 490/518 cases. Full candidate grammar
  checking explicitly permits partial plans; it does not certify completeness.

The first obligation-compilation implementation added a standalone future check
for a missing retained record despite having no supported finding. The existing
integration test caught this; compilation now requires a finding plan and the
missing-record case remains unresolved without an invented repair.

Commands from the repository root:

```bash
python3 code/evaluation/planning_acceptance.py
python3 code/evaluation/validate_output.py --output dataset/sample_output.csv --requests dataset/sample_deletion_requests.csv
PYTHONPATH=code python3 -m unittest discover -s code/tests -v
```

The acceptance command exits 2 for the eight diagnosed blockers, distinct from
software failure. Its ignored .ghostgraph/planning_acceptance.json records every
violation; it never silently drops blocked cases from the original predictions.
The milestone must not be marked complete until all 32 generated rows pass.
