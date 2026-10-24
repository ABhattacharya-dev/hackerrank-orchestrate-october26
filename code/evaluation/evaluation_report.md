# GhostGraph evaluation report

## Submission acceptance: blocked

The implemented pipeline executes and produces a **provisional 518-row candidate**.
It is not a fully verified submission. Strict export refuses final `output.csv`
because **335 cases have explicit proof/coverage gaps**.
The candidate's fallback statuses and partial plans must not be presented as
certified deletion decisions. Additional authoritative subject/resource links or
state evidence are needed; case-number inference and sample-label lookup are
prohibited. No hidden-set accuracy is known.

## Actual public-sample results

Command: `python3 code/evaluation/main.py`. Labels are loaded by the evaluator
after predictions; they never enter intent training or prediction. These 32
public samples were used during development, so results are regression scores,
not an independent held-out estimate. Samples contain no NOT_APPLICABLE cases.

| Metric | Result |
| --- | ---: |
| Deletion-status accuracy | 29/32 (90.62%) |
| Exact row accuracy (status and full step array) | 9/32 (28.12%) |
| Exact sequence accuracy | 9/32 (28.12%) |
| Step precision, including exact canonical citation | 159/163 (97.55%) |
| Step recall, including exact canonical citation | 159/193 (82.38%) |
| Structural step precision, ignoring citation | 97.55% |
| Structural step recall, ignoring citation | 82.38% |
| Field accuracy | 1068/1351 (79.05%) |
| Canonical evidence-reference accuracy | 59/75 (78.67%) |

Step precision/recall use multiset intersection over phase, system, resource,
operation, state and (for exact matching) evidence ID; step number is evaluated
in sequence/field accuracy. Fields align on phase/system/resource/operation;
missing expected fields count wrong. Canonical reference accuracy compares
expected cited steps, including omitted ones as incorrect. The provenance check
independently verifies internal source/linkage/cutoff consistency, but is not an
independent semantic-entailment judge and does not prove hidden correctness.

## Actual software and full-run checks

- `38` unit/regression tests ran: `0` failures,
  `0` errors, `0` skipped; all passed.
- All 94 manifest files processed: 26 logs, 28 JSON, 1 text, 11 PNG, 24 SQL,
  4 PDF. 2906 observations and
  116 SQL table scopes retained.
- Candidate IDs/count/header/order, allowed enums, field sets, step numbers,
  duplicate detection and citation availability were validated for 518 rows.
- 1030 cited candidate steps
  matched internal ledger proofs with eligible timestamps and explicit linkage
  explanations. This is provenance validation, not a claim of full coverage.
- Input hashes verified unchanged; supplied evidence and root AGENTS.md were not
  edited. Candidate status counts: `{'INCOMPLETE': 355, 'COMPLETE': 153, 'NOT_APPLICABLE': 10}` (provisional).
- Warm-cache full run: 6.016 seconds. A fresh source copy,
  different working directory and empty extraction cache reproduced identical
  candidate bytes in 19.478 seconds, executing
  11 OCR calls and
  4 PDF extraction calls.
- Strict refusal was exercised; it returned an evidence blocker and wrote no
  final output. Readiness verification exits 2 for that diagnosed blocker,
  distinct from unit-test failure (exit 1).

Candidate SHA-256: `6113f1cfae238c24e89d9997533c174ab5f85cc8fdaf580efdedf1bf508ceeca`.

## Independent adversarial cases executed

Fixtures and assertions are in `code/tests/test_reasoning.py`; they are authored
independently of public sample labels and do not mutate supplied evidence.

1. **Multilingual access-only and negation.** Requests ask only for an export,
   correction or a copy in English, French, Spanish, Japanese and Korean. Expected:
   authorization false; no destructive plan. All language subcases passed.
2. **Future capture describing an earlier state.** `account_7` is observed PRESENT
   at 2026-01-01T00:00:00Z. A later-captured ABSENT observation describes an earlier
   event but is unavailable at the 2026-01-02 cutoff. Expected: INCOMPLETE from
   eligible presence; the future capture cannot prove deletion. Passed.
3. **Replica drift plus retained records and recreation.** `account_7` is absent
   from primary and present in a replica; `tombstone_8` is redacted;
   `audit_record_9` is retained; `data_flow_4` and `backup_5` are active. Expected:
   INCOMPLETE; disable flow, block restore, delete the remaining copy in official
   order; preserve the compliant tombstone and audit record. Passed.
4. **Reused alias.** Two stable subjects share a supplied email. Expected: no
   automatic merge or guessed owner. Passed.
5. **Retained audit without primary proof.** Only a retained audit record is
   observed. Expected: explicit NO_PRIMARY_PROFILE_PROOF; partial observations
   cannot certify account deletion. Passed.

Other executed tests cover cutoff inclusivity, repeated cases, equal-time
conflicts, future identity snapshots, explicit source-resource edges, redaction,
anonymization, missing retained records, claims versus observations, path escape,
all six log envelopes and invalid output/citations.

## Failures, corrections and remaining risks

Initial sample status accuracy was 19/32, with 6/32 exact rows. Independent
training examples, Unicode/contraction normalization, explicit scope guards,
bounded document matching and structured source edges improved these to the
scores above. Pure-ML training expansion introduced portability/negation
regressions; generic consent/scope guards corrected those rather than memorizing
sample answers. All final fixtures passed after the corrections.

Cloud log envelopes originally hid nested event fields; unwrapping was fixed.
SQL loading initially rejected the supplied foreign_keys pragma; only that safe
pragma is now permitted. A legitimate empty SQL snapshot is counted as table-scope
evidence. Document matching originally allowed reference substrings and unrelated
page rows to create false links; token boundaries, source compatibility and
scoped excerpts corrected those paths. Cutoff-specific identity caching reduced
observed warm runtime from roughly 18 seconds to roughly four seconds.

The final proof audit exposed a serious readiness weakness: compliant downstream
or retained records do not establish primary deletion. Strict export now checks
that coverage explicitly instead of relying on status scores or a nonempty ledger.

Current blocker counts (overlap is possible): `{'NO_PRIMARY_PROFILE_PROOF': 334, 'INSUFFICIENT_OBSERVED_FIELDS': 1, 'NO_STATE_PROOF': 1, 'NO_LINKED_RESOURCE_PROOFS': 1}`.

Investigated examples:

- `case_01` and `case_02` public expected absent account IDs have no supplied
  subject link in the eligible evidence; a worker claim without a subject cannot
  supply that link. Do not infer IDs from user/case numbering.
- Anonymous analytics records, including `analytics_901` and `analytics_9406`,
  expose no subject identifier. State can be read, but attribution needs a grounded
  historical/catalog link. Some expected verification steps remain unreproduced.
- Public `case_09` expects account/security verification cited to `evidence_93`,
  whose readback contains only one backup target. Corresponding ordinary-log
  observations occur in a file captured after that case's cutoff; they cannot
  repair earlier provenance under the root contract.
- Full `case_46`: the retained-reference screenshot does not expose enough fields
  to certify redaction of `tombstone_17`.
- Full `case_55`: archive existence and unrelated restore history do not establish
  restore permission for `backup_9287` at cutoff. No ACTIVE state is invented.

These are diagnosed limitations of the present evidence-backed implementation,
not proof that every remaining mismatch is a dataset defect. More extraction or
authoritative linkage may resolve some gaps. OCR fidelity, conditional policy
coverage, anonymous attribution and exact reference selection remain risks.
Public sample recall and exact-row accuracy are materially below complete
correctness. The candidate is **not submission-ready**.
