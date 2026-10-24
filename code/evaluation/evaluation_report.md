# GhostGraph evaluation report

## Submission acceptance: blocked

The implemented pipeline executes and produces a **provisional 518-row candidate**.
It is not a fully verified submission. Strict export refuses final `output.csv`
because **490 cases have explicit proof/coverage gaps**.
The candidate's fallback statuses and partial plans must not be presented as
certified deletion decisions. Additional authoritative subject/resource links or
state evidence are needed; case-number inference and sample-label lookup are
prohibited. No hidden-set accuracy is known.

## Actual public-sample results

Milestone 5 strict planning acceptance: 24/32 generated
rows pass the complete structural contract; 13
violations remain in 8 cases. All 32 public reference
rows pass structural validation. The passing subset is diagnostic only and cannot
replace the required full sample output. See `code/PLANNING.md`. Candidate checks
below use an explicitly relaxed completeness mode; they do not establish that
every incomplete case has a full plan. The milestone exit criterion is unmet.

Command: `python3 code/evaluation/main.py`. Labels are loaded by the evaluator
after predictions; they never enter intent training or prediction. These 32
public samples were used during development, so results are regression scores,
not an independent held-out estimate. Samples contain no NOT_APPLICABLE cases.

| Metric | Result |
| --- | ---: |
| Deletion-status accuracy | 28/32 (87.50%) |
| Exact row accuracy (status and full step array) | 2/32 (6.25%) |
| Exact sequence accuracy | 2/32 (6.25%) |
| Step precision, including exact canonical citation | 111/115 (96.52%) |
| Step recall, including exact canonical citation | 111/193 (57.51%) |
| Structural step precision, ignoring citation | 96.52% |
| Structural step recall, ignoring citation | 57.51% |
| Field accuracy | 719/1351 (53.22%) |
| Canonical evidence-reference accuracy | 44/75 (58.67%) |

Step precision/recall use multiset intersection over phase, system, resource,
operation, state and (for exact matching) evidence ID; step number is evaluated
in sequence/field accuracy. Fields align on phase/system/resource/operation;
missing expected fields count wrong. Canonical reference accuracy compares
expected cited steps, including omitted ones as incorrect. The provenance check
independently verifies internal source/linkage/cutoff consistency, but is not an
independent semantic-entailment judge and does not prove hidden correctness.

## Actual software and full-run checks

- `90` unit/regression tests ran: `0` failures,
  `0` errors, `0` skipped; all passed.
- All 94 manifest files processed: 26 logs, 28 JSON, 1 text, 11 PNG, 24 SQL,
  4 PDF. 2906 observations and
  116 SQL table scopes retained.
- Candidate IDs/count/header/order, allowed enums, field sets, step numbers,
  duplicate detection and citation availability were validated for 518 rows.
- 729 cited candidate steps
  matched internal ledger proofs with eligible timestamps and explicit linkage
  explanations. This is provenance validation, not a claim of full coverage.
- Input hashes verified unchanged; supplied evidence and root AGENTS.md were not
  edited. Candidate status counts: `{'INCOMPLETE': 400, 'COMPLETE': 108, 'NOT_APPLICABLE': 10}` (provisional).
- Warm-cache full run: 6.875 seconds. A fresh source copy,
  different working directory and empty extraction cache reproduced identical
  candidate bytes in 19.435 seconds, executing
  11 OCR calls and
  4 PDF extraction calls.
- Strict refusal was exercised; it returned an evidence blocker and wrote no
  final output. Readiness verification exits 2 for that diagnosed blocker,
  distinct from unit-test failure (exit 1).

Candidate SHA-256: `b83ff6a9b086a53ceda99b3f527eefda36ec49f69db392f84be51fdecb01e7c3`.

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

Initial sample status accuracy was 19/32, with 6/32 exact rows. The current
scores above include stricter temporal and conditional-policy proof requirements;
they are not claimed to improve every metric over earlier provisional runs.
Independent training examples, Unicode normalization, scope guards and grounded
source edges were evaluated during development. Pure-ML training expansion introduced portability/negation
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

Current blocker counts (overlap is possible): `{'POLICY_CONDITION_UNKNOWN': 421, 'NO_PRIMARY_PROFILE_PROOF': 465, 'NO_SUPPORTED_STEPS': 73, 'INCOMPLETE_WITHOUT_FINDING': 73, 'RETAINED_ARCHIVE_PRESENCE_UNKNOWN': 22, 'MISSING_REQUIRED_VERIFICATION': 83, 'COPY_COVERAGE_UNPROVEN': 112, 'FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION': 25, 'UNVERIFIED_MUTATION_AFTER_OBSERVATION': 48, 'SCOPE_ALIGNMENT_UNKNOWN': 1, 'NO_LINKED_RESOURCE_PROOFS': 3, 'UNSUPPORTED_SCOPED_STATE': 1, 'UNRESOLVED_PROCESS_PRECONDITION': 1, 'NO_STATE_PROOF': 1}`.

Conditional policy facts are now evaluated explicitly. Unknown retention periods,
attachment exclusivity, required reference context or restore-block capability
are not assumed from category names. Unknown conditions block destructive actions
and can reduce provisional sample recall; this limitation needs grounded evidence
or extraction improvements, rather than weakening proof requirements. A complete
obligation ledger and process/dependency analysis are retained in diagnostics.

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
