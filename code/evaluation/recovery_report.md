> Final update: root output.csv now has 518 rows and zero official structural
> violations. Target-scoped console drill/checksum/domain inference resolves the
> last blocker in prediction mode. Public metrics remain 9/32 exact. See
> evaluation_report.md for current results. The recovery investigation below is
> preserved as historical evidence of the 1146bc7 baseline and its limitations.

# Accuracy recovery regression report

Checkpoint: recovery-checkpoint-a0437e3. Comparison copies under /tmp/ghostgraph-history use git archive of code and read-only participant dataset symlinks; no organizer data was accessed.

| Version | Status | Exact rows | Precision | Recall | Citations |
| --- | ---: | ---: | ---: | ---: | ---: |
| 34465f9 | 29/32 | 9/32 | 97.55% | 82.38% | 78.67% |
| cded062 | 29/32 | 7/32 | 98.06% | 78.76% | 76.00% |
| ee0914f | 28/32 | 1/32 | 97.14% | 52.85% | 58.67% |
| a0437e3 | 28/32 | 2/32 | 96.52% | 57.51% | 58.67% |
| Recovery prediction | 29/32 | 9/32 | 97.55% | 82.38% | 78.67% |

Recovery F1 89.33%; field accuracy 79.05%; exact sequence 28.12%. This recovers, but does not exceed, the initial 9/32 baseline. No hidden accuracy is known.

## Causes and requirement audit

A: Official enums, phases, ordering, citations/cutoffs, preservation and complete plans remain enforced. Equal-time conflicts, future evidence and foreign subject references remain protected.

B: Supplied snapshot scopes and positive replica observations justify known-copy state reconstruction. Typed security/legal records justify conservative preservation as a prediction, without inventing retention deadlines. Structured tombstone references support retaining stable links while removing direct identifiers. Backup restore-policy entries support proposed blocking; that is not evidence the action executed. Subject-scoped attachment records support a prediction of exclusive ownership, with explicit uncertainty.

C: Universal absence proof against hypothetical unseen copies and a mandatory primary-profile proof in every case are certification assumptions, not output-format rules. An operation claim after a readback creates uncertainty but cannot erase the readback as a prediction or establish the claimed state. These remain certification diagnostics.

| Restriction | Basis / effect |
| --- | --- |
| NO_PRIMARY_PROFILE_PROOF | Additional global coverage assumption; warnings preserved, not a reason to suppress otherwise supported predictions. |
| COPY_COVERAGE_UNPROVEN | Valid certification concern; suppresses absent checks for known scoped readbacks without evidence of another remaining copy. Prediction uses known scopes and preserves actual replicas. |
| POLICY_CONDITION_UNKNOWN | Conditional rules are official; demanding explicit boolean metadata for every retained record is extra. Prediction preserves records and records applicability assumptions separately. False or expired conditions are never overridden. |
| UNVERIFIED_MUTATION_AFTER_OBSERVATION | Appropriate uncertainty; a claim does not establish new state. Prediction carries eligible observations forward; certification still refuses. |
| NO_SUPPORTED_STEPS | Genuine contract limitation when a deletion prediction cannot contain any supported operations. Not bypassed. |
| MISSING_REQUIRED_VERIFICATION | Valid for applicable known resource goals. Kept; an archive policy entry is distinguished from a separately observed physical retained archive. |

No hidden truth exists for a statistical false-positive estimate of these warnings. The following public canonical disagreement counts are observable proxies, not proven semantic false-positive rates.
- NO_PRIMARY_PROFILE_PROOF: 29/32 cases warned; 10 of those have canonical COMPLETE. Warnings overlap.
- COPY_COVERAGE_UNPROVEN: 9/32 cases warned; 1 of those have canonical COMPLETE. Warnings overlap.
- POLICY_CONDITION_UNKNOWN: 19/32 cases warned; 4 of those have canonical COMPLETE. Warnings overlap.
- UNVERIFIED_MUTATION_AFTER_OBSERVATION: 5/32 cases warned; 1 of those have canonical COMPLETE. Warnings overlap.
- NO_SUPPORTED_STEPS: 5/32 cases warned; 4 of those have canonical COMPLETE. Warnings overlap.
- MISSING_REQUIRED_VERIFICATION: 4/32 cases warned; 4 of those have canonical COMPLETE. Warnings overlap.

## Lost operations traced to current code

Each row below was emitted in 34465f9 but omitted by a0437e3. Policy losses come from policy.py unknown-condition returns and engine.py treatment=None suppression; temporal losses come from temporal.py scoped-absence and post-observation-claim invalidation. Planner additionally inserts policy goal checks but cannot restore suppressed observations. Identity/capture changes remain justified where earlier linkage was ungrounded.

| Case | Lost operation | Resource | Current ledger reason |
| --- | --- | --- | --- |
| case_03 | VERIFY_RECORD_ABSENT | account_7566 | UNKNOWN |
| case_07 | REPORT_REMAINING_RECORD | support_001 | POLICY_CONDITION_UNKNOWN |
| case_07 | DELETE_RECORD | support_001 | POLICY_CONDITION_UNKNOWN |
| case_07 | VERIFY_RECORD_ABSENT | support_001 | POLICY_CONDITION_UNKNOWN |
| case_09 | BLOCK_RESTORE | backup_4978 | POLICY_CONDITION_UNKNOWN |
| case_09 | VERIFY_RESTORE_BLOCKED | backup_4978 | POLICY_CONDITION_UNKNOWN |
| case_11 | REPORT_REMAINING_RECORD | search_052 | UNKNOWN |
| case_11 | REPORT_EXPOSED_PII | support_864 | POLICY_CONDITION_UNKNOWN |
| case_11 | DELETE_RECORD | search_052 | UNKNOWN |
| case_11 | REDACT_RECORD | support_864 | POLICY_CONDITION_UNKNOWN |
| case_11 | VERIFY_RECORD_PRESENT | audit_record_9394 | POLICY_CONDITION_UNKNOWN |
| case_11 | VERIFY_RECORD_REDACTED | support_864 | POLICY_CONDITION_UNKNOWN |
| case_12 | VERIFY_RECORD_PRESENT | audit_record_2945 | POLICY_CONDITION_UNKNOWN |
| case_13 | REPORT_REMAINING_RECORD | support_4218 | POLICY_CONDITION_UNKNOWN |
| case_13 | DELETE_RECORD | support_4218 | POLICY_CONDITION_UNKNOWN |
| case_13 | VERIFY_RECORD_ABSENT | support_4218 | POLICY_CONDITION_UNKNOWN |
| case_13 | VERIFY_RECORD_PRESENT | audit_record_4816 | POLICY_CONDITION_UNKNOWN |
| case_14 | BLOCK_RESTORE | backup_3870 | POLICY_CONDITION_UNKNOWN |
| case_14 | VERIFY_RECORD_PRESENT | audit_record_987 | POLICY_CONDITION_UNKNOWN |
| case_14 | VERIFY_RESTORE_BLOCKED | backup_3870 | POLICY_CONDITION_UNKNOWN |
| case_15 | VERIFY_RECORD_PRESENT | audit_record_1596 | POLICY_CONDITION_UNKNOWN |
| case_16 | VERIFY_RECORD_PRESENT | audit_record_9528 | POLICY_CONDITION_UNKNOWN |
| case_17 | BLOCK_RESTORE | backup_3245 | POLICY_CONDITION_UNKNOWN |
| case_17 | VERIFY_RECORD_PRESENT | audit_record_1797 | POLICY_CONDITION_UNKNOWN |
| case_17 | VERIFY_RESTORE_BLOCKED | backup_3245 | POLICY_CONDITION_UNKNOWN |
| case_18 | REPORT_EXPOSED_PII | support_5569 | POLICY_CONDITION_UNKNOWN |
| case_18 | REDACT_RECORD | support_5569 | POLICY_CONDITION_UNKNOWN |
| case_18 | VERIFY_RECORD_REDACTED | support_5569 | POLICY_CONDITION_UNKNOWN |
| case_19 | REPORT_EXPOSED_PII | support_9553 | POLICY_CONDITION_UNKNOWN |
| case_19 | REDACT_RECORD | support_9553 | POLICY_CONDITION_UNKNOWN |
| case_19 | VERIFY_RECORD_PRESENT | audit_record_6793 | POLICY_CONDITION_UNKNOWN |
| case_19 | VERIFY_RECORD_REDACTED | support_9553 | POLICY_CONDITION_UNKNOWN |
| case_22 | VERIFY_RECORD_PRESENT | audit_record_3482 | POLICY_CONDITION_UNKNOWN |
| case_26 | VERIFY_RECORD_REDACTED | support_4715 | POLICY_CONDITION_UNKNOWN |
| case_27 | VERIFY_RECORD_REDACTED | support_4707 | POLICY_CONDITION_UNKNOWN |
| case_28 | VERIFY_RECORD_REDACTED | support_2351 | POLICY_CONDITION_UNKNOWN |
| case_29 | REPORT_EXPOSED_PII | support_5281 | POLICY_CONDITION_UNKNOWN |
| case_29 | REDACT_RECORD | support_5281 | POLICY_CONDITION_UNKNOWN |
| case_29 | VERIFY_RECORD_REDACTED | support_5281 | POLICY_CONDITION_UNKNOWN |
| case_30 | REPORT_EXPOSED_PII | support_6477 | POLICY_CONDITION_UNKNOWN |
| case_30 | REDACT_RECORD | support_6477 | POLICY_CONDITION_UNKNOWN |
| case_30 | VERIFY_RECORD_REDACTED | support_6477 | POLICY_CONDITION_UNKNOWN |
| case_31 | VERIFY_RECORD_PRESENT | audit_record_6909 | POLICY_CONDITION_UNKNOWN |
| case_31 | VERIFY_RECORD_REDACTED | tombstone_440 | POLICY_CONDITION_UNKNOWN |
| case_32 | REPORT_EXPOSED_PII | tombstone_9178 | POLICY_CONDITION_UNKNOWN |
| case_32 | REDACT_RECORD | tombstone_9178 | POLICY_CONDITION_UNKNOWN |
| case_32 | VERIFY_RECORD_PRESENT | audit_record_7068 | POLICY_CONDITION_UNKNOWN |
| case_32 | VERIFY_RECORD_REDACTED | tombstone_9178 | POLICY_CONDITION_UNKNOWN |

## Submission status and limitations

Prediction export has 518 rows, 2 strict structural violations: `[{'case_id': 'case_55', 'code': 'NO_SUPPORTED_STEPS'}, {'case_id': 'case_55', 'code': 'INCOMPLETE_WITHOUT_FINDING'}]`. Previously 171 violations across 98 cases. The sole remaining case has no eligible restore-state observation; its console proves an archive exists but not restore permission. A later restore log is ineligible. No active risk, deletion finding or COMPLETE decision is fabricated to fill that gap. Root output.csv is therefore not published; output.prediction.candidate.csv is the explicitly best-effort deliverable.

Other unrecovered sample checks include anonymous records without grounded ownership, missing absent-account identifiers, and unavailable earlier readbacks. Numeric suffixes, null trace lookups and sample labels cannot supply ownership. Extra object-storage findings have grounded catalog links and are not suppressed just to match labels. No further accuracy gain is claimed.

Strict mode remains the default, with its 490 unresolved cases and unchanged behavior. Prediction diagnostics also preserve 490 uncertainty-bearing cases; this is intentionally not a certification pass. The full run uses 5 local learned inference calls and 143 cache hits; zero paid API calls/input/output API tokens/cost, local token units not applicable and CPU cost unpriced. No AI-call optimization work was performed in recovery.
