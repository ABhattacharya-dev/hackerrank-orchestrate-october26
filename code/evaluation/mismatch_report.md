# Public-sample mismatch report

Generated from the actual full 32-case public evaluation. Reference answers are read only by evaluation. Reasons below describe present implementation gaps, not proof of dataset defects. Alternative valid citations still count wrong against exact public reference IDs.

| Metric | Result |
| --- | ---: |
| Case status accuracy | 87.5000% |
| Step precision | 96.5217% |
| Step recall | 57.5130% |
| Step F1 | 72.0779% |
| Field accuracy | 53.2198% |
| Canonical evidence citation accuracy | 58.6667% |
| Exact sequence accuracy | 6.2500% |
| Exact row accuracy | 6.2500% |

## Error impact and priorities

Status errors: 4; missing operations: 82; extra operations: 4; wrong states on aligned operations: 0; wrong citations on aligned operations: 0; relative ordering errors among shared steps: 0.

State/citation mismatches align on phase, system, resource and operation. Missing operations remain missing rather than being relabeled as wrong fields. Relative-order checks exclude omissions; omitted preceding steps can still change absolute step numbers and field/sequence scores. Exact step metrics use multiset matching including citations. Field accuracy counts all seven expected fields, including step_no, and treats missing steps as seven wrong fields. Evidence accuracy includes omitted expected cited steps as wrong; aligned-citation error counts alone are not a recall measure.

| Missing operation | Count |
| --- | ---: |
| VERIFY_RECORD_ABSENT | 23 |
| VERIFY_RECORD_PRESENT | 18 |
| VERIFY_RECORD_REDACTED | 10 |
| VERIFY_RECORD_ANONYMIZED | 7 |
| REPORT_EXPOSED_PII | 6 |
| REDACT_RECORD | 6 |
| REPORT_REMAINING_RECORD | 3 |
| DELETE_RECORD | 3 |
| BLOCK_RESTORE | 3 |
| VERIFY_RESTORE_BLOCKED | 3 |

1. Recover missing grounded identity/resource links and eligible primary/copy proofs before optimizing formatting or intent. Verification omissions dominate measured loss. Never infer absent account IDs from case/user suffixes.
2. Extract explicit retention, shared-context and restore capability facts where supplied. Unknown conditions remain blockers; adding blanket category assumptions would weaken policy correctness.
3. Review extra resources against their catalog and direct observations. Do not suppress supported findings solely because the public reference omits them.
4. Preserve deterministic output and consent guards. Selective inference saves model work; public audit-status scores do not justify replacing evidence reasoning with an LLM.

## Every remaining mismatched case

### case_01

Classification: predicted `INCOMPLETE`, reference `COMPLETE`. Incorrect: `True`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_001 ABSENT`; citation `evidence_54`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `INCOMPLETE_WITHOUT_FINDING`, `NO_LINKED_RESOURCE_PROOFS`, `NO_PRIMARY_PROFILE_PROOF`, `NO_SUPPORTED_STEPS`.

### case_02

Classification: predicted `INCOMPLETE`, reference `COMPLETE`. Incorrect: `True`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_002 ABSENT`; citation `evidence_54`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `INCOMPLETE_WITHOUT_FINDING`, `NO_LINKED_RESOURCE_PROOFS`, `NO_PRIMARY_PROFILE_PROOF`, `NO_SUPPORTED_STEPS`.

### case_03

Classification: predicted `COMPLETE`, reference `COMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_7566 ABSENT`; citation `evidence_94`. Temporal state is UNKNOWN; copy coverage or contradictory observations remain unresolved.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_9406 ANONYMIZED`; citation `evidence_94`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `MISSING_REQUIRED_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `UNVERIFIED_MUTATION_AFTER_OBSERVATION`.

### case_04

Classification: predicted `INCOMPLETE`, reference `COMPLETE`. Incorrect: `True`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_004 ABSENT`; citation `evidence_54`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_901 ANONYMIZED`; citation `evidence_56`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `INCOMPLETE_WITHOUT_FINDING`, `NO_LINKED_RESOURCE_PROOFS`, `NO_PRIMARY_PROFILE_PROOF`, `NO_SUPPORTED_STEPS`.

### case_07

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_REMAINING_RECORD support_platform/support_001 PRESENT`; citation `evidence_58`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION DELETE_RECORD support_platform/support_001 ABSENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_007 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_ABSENT support_platform/support_001 ABSENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

- `FINDING REPORT_REMAINING_RECORD object_storage/object_19 PRESENT`; citation `evidence_46`. Current grounded ledger supports a different or partial plan; review the reference state/citation against scoped evidence and the obligation ledger.
- `REMEDIATION DELETE_RECORD object_storage/object_19 ABSENT`; citation `(empty)`. Current grounded ledger supports a different or partial plan; review the reference state/citation against scoped evidence and the obligation ledger.
- `VERIFICATION VERIFY_RECORD_ABSENT object_storage/object_19 ABSENT`; citation `(empty)`. Current grounded ledger supports a different or partial plan; review the reference state/citation against scoped evidence and the obligation ledger.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_08

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_008 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`.

### case_09

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `REMEDIATION BLOCK_RESTORE backup_service/backup_4978 BLOCKED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_3960 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_4902 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RESTORE_BLOCKED backup_service/backup_4978 BLOCKED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_10

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_010 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`.

### case_11

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_REMAINING_RECORD search_service/search_052 PRESENT`; citation `evidence_03`. Temporal state is UNKNOWN; copy coverage or contradictory observations remain unresolved.
- `FINDING REPORT_EXPOSED_PII support_platform/support_864 PRESENT`; citation `evidence_03`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION DELETE_RECORD search_service/search_052 ABSENT`; citation `(empty)`. Temporal state is UNKNOWN; copy coverage or contradictory observations remain unresolved.
- `REMEDIATION REDACT_RECORD support_platform/support_864 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_9394 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_864 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `UNVERIFIED_MUTATION_AFTER_OBSERVATION`.

### case_12

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_2945 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_13

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_REMAINING_RECORD support_platform/support_4218 PRESENT`; citation `evidence_03`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION DELETE_RECORD support_platform/support_4218 ABSENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT support_platform/support_4218 ABSENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_4816 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `UNVERIFIED_MUTATION_AFTER_OBSERVATION`.

### case_14

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `REMEDIATION BLOCK_RESTORE backup_service/backup_3870 BLOCKED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_987 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RESTORE_BLOCKED backup_service/backup_3870 BLOCKED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `UNVERIFIED_MUTATION_AFTER_OBSERVATION`.

### case_15

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_1596 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_16

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_9528 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `POLICY_CONDITION_UNKNOWN`.

### case_17

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `REMEDIATION BLOCK_RESTORE backup_service/backup_3245 BLOCKED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_1797 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RESTORE_BLOCKED backup_service/backup_3245 BLOCKED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_6523 ABSENT`; citation `(empty)`. Temporal state is UNKNOWN; copy coverage or contradictory observations remain unresolved.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `FINDING_WITHOUT_FULL_REMEDIATION_AND_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `UNSUPPORTED_SCOPED_STATE`, `UNVERIFIED_MUTATION_AFTER_OBSERVATION`.

### case_18

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_EXPOSED_PII support_platform/support_5569 PRESENT`; citation `evidence_94`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION REDACT_RECORD support_platform/support_5569 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_5521 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_6645 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_5569 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_19

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_EXPOSED_PII support_platform/support_9553 PRESENT`; citation `evidence_01`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION REDACT_RECORD support_platform/support_9553 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_6793 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_9553 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `COPY_COVERAGE_UNPROVEN`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_20

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_5037 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_5569 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`.

### case_21

Classification: predicted `COMPLETE`, reference `COMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_6440 ABSENT`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_5335 ANONYMIZED`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`.

### case_22

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_4990 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_3482 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_23

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_410 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_4128 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`.

### case_24

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_7095 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: none.

### case_25

Classification: predicted `COMPLETE`, reference `COMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_3136 ABSENT`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_1895 ANONYMIZED`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`.

### case_26

Classification: predicted `COMPLETE`, reference `COMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_5684 ABSENT`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_4715 REDACTED`; citation `evidence_92`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_4566 ANONYMIZED`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `MISSING_REQUIRED_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `RETAINED_ARCHIVE_PRESENCE_UNKNOWN`.

### case_27

Classification: predicted `COMPLETE`, reference `COMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_3866 ABSENT`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_4707 REDACTED`; citation `evidence_92`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_4574 ANONYMIZED`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `MISSING_REQUIRED_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `RETAINED_ARCHIVE_PRESENCE_UNKNOWN`.

### case_28

Classification: predicted `COMPLETE`, reference `COMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_5482 ABSENT`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_2351 REDACTED`; citation `evidence_92`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_6077 ANONYMIZED`; citation `evidence_92`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `MISSING_REQUIRED_VERIFICATION`, `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`, `RETAINED_ARCHIVE_PRESENCE_UNKNOWN`.

### case_29

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_EXPOSED_PII support_platform/support_5281 PRESENT`; citation `evidence_92`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION REDACT_RECORD support_platform/support_5281 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_7012 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_3954 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_5281 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_30

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_EXPOSED_PII support_platform/support_6477 PRESENT`; citation `evidence_92`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION REDACT_RECORD support_platform/support_6477 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_4163 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_1707 PRESENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_REDACTED support_platform/support_6477 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `NO_PRIMARY_PROFILE_PROOF`, `POLICY_CONDITION_UNKNOWN`.

### case_31

Classification: predicted `INCOMPLETE`, reference `COMPLETE`. Incorrect: `True`. Relative ordering incorrect: `False`.

Missing steps:

- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_4857 ABSENT`; citation `evidence_51`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_6909 PRESENT`; citation `evidence_51`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_REDACTED identity_service/tombstone_440 REDACTED`; citation `evidence_51`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `INCOMPLETE_WITHOUT_FINDING`, `NO_PRIMARY_PROFILE_PROOF`, `NO_SUPPORTED_STEPS`, `POLICY_CONDITION_UNKNOWN`.

### case_32

Classification: predicted `INCOMPLETE`, reference `INCOMPLETE`. Incorrect: `False`. Relative ordering incorrect: `False`.

Missing steps:

- `FINDING REPORT_EXPOSED_PII identity_service/tombstone_9178 PRESENT`; citation `evidence_51`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `REMEDIATION REDACT_RECORD identity_service/tombstone_9178 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_ABSENT account_service/account_8858 ABSENT`; citation `(empty)`. No eligible grounded resource entry in the current case ledger. Review identifier/catalog extraction and cutoff availability; this does not prove the resource is unrelated or absent.
- `VERIFICATION VERIFY_RECORD_PRESENT security_service/audit_record_7068 PRESENT`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.
- `VERIFICATION VERIFY_RECORD_REDACTED identity_service/tombstone_9178 REDACTED`; citation `(empty)`. Policy proof gaps: POLICY_CONDITION_UNKNOWN. Policy applicability is UNKNOWN; safe treatment cannot be assumed.

Extra steps:

None.

Wrong states: None on aligned operations.

Wrong evidence: None on aligned operations.

Diagnosed case gaps: `INCOMPLETE_WITHOUT_FINDING`, `NO_PRIMARY_PROFILE_PROOF`, `NO_SUPPORTED_STEPS`, `POLICY_CONDITION_UNKNOWN`.

## Structural acceptance

Generated sample rows passing: 24/32. Violations: 13 across 8 cases: case_01, case_02, case_04, case_09, case_14, case_17, case_31, case_32. All reference rows pass. This milestone's all-structural-checks exit condition is **not met**; the valid subset is diagnostic only.

## Selective AI experiment

Ablation uses the same fixed training corpus and English scope/ambiguity guards. Rules-only abstains on unhandled language. ML-only uses the learned probability at 0.5 without guards. Guarded eager and guarded selective share decisions; selective skips inference when scope guards decide. Expected ambiguity is abstention, and unhandled definite intents count incorrect in the all-item accuracy. Calls exclude fitting and include real predict_proba execution; no API tokens apply.

| Dataset / arm | Correct | Abstentions | False authorizations |
| --- | ---: | ---: | ---: |
| public / rules_only | 28/32 | 4 | 0 |
| public / ml_only | 31/32 | 0 | 0 |
| public / guarded_eager | 32/32 | 0 | 0 |
| public / guarded_selective | 32/32 | 0 | 0 |
| independent / rules_only | 8/24 | 17 | 0 |
| independent / ml_only | 23/24 | 0 | 1 |
| independent / guarded_eager | 24/24 | 1 | 0 |
| independent / guarded_selective | 24/24 | 1 | 0 |

- public: eager 32 model calls, selective 4; replay 32 cache hits and no additional inference calls.
- independent: eager 24 model calls, selective 16; replay 24 cache hits and no additional inference calls.

Public samples contain only deletion intents; this measures intent coverage, not the full audit verdict. The 24 independently authored probes were frozen before their first run and checked for exact training-text overlap. They include multilingual deletion/access/correction, implicit consent, cancellation, opt-out and uncertainty. Their small development-only design cannot establish multilingual generalization. Probe failures were not used to change model training. Actual probe texts, expected decisions and arm predictions are reproducible in `evaluation/ai_ablation.py`.

The optional vision extractor was not evaluated against a hosted model: both GHOSTGRAPH_VISION_API_KEY and GHOSTGRAPH_VISION_MODEL were absent. Five artifacts remain queued for semantic review. No vision calls, token costs or image-accuracy gains are claimed. Local discriminative inference remains a genuine participating AI component.

## Experiments and limitations

The M5 baseline at commit f54c83e scored 28/32 status, 2/32 exact sequences, 111/115 exact step precision and 111/193 recall. A proposed document reclassification replaced attachment treatment with shared-context redaction when a document mentioned an order reference. It added three extra steps with no recovered reference steps (111/118 precision, unchanged recall), and did not establish a stronger document-role proof, so it was reverted. The initial new document fixtures also exposed missing synthetic-manifest setup; those experimental fixtures were discarded with the rejected parser change. No passing test claim includes those failed runs.

The adopted change only gates inference and normalizes deduplication keys; the training examples, policy and temporal rules are unchanged. Full regression tests run after evaluator, rejected parser and selective-inference changes. Caching uses model/training hash plus canonical text and returns copies so callers cannot corrupt cached decisions. Deterministic scope outputs have probability null, not a fabricated ML confidence.

All errors above have a reproducible diagnosis, but many require better evidence extraction or authoritative linkage rather than output padding. Structural acceptance and final export remain blocked. No hidden-set accuracy is known.
