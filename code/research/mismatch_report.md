# V3 current prediction mismatch report

Fresh frozen-prediction evaluation. Labels are used only by evaluation. Missing/extra steps align by phase/system/resource/operation; wrong-state/citation errors are separate. Zero relative ordering errors does not excuse missing steps or shifted step numbers.

- status_accuracy: 90.625000%
- exact_row_accuracy: 28.125000%
- step_precision: 97.546012%
- step_recall: 82.383420%
- step_f1: 89.325843%
- canonical_evidence_accuracy: 78.666667%
- field_accuracy: 79.052554%
- exact_sequence_accuracy: 28.125000%

## case_01

Status INCOMPLETE / reference COMPLETE; classification wrong: True; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_001 ABSENT citation=evidence_54; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: INCOMPLETE_WITHOUT_FINDING, NO_LINKED_RESOURCE_PROOFS, NO_PRIMARY_PROFILE_PROOF, NO_SUPPORTED_STEPS

## case_02

Status INCOMPLETE / reference COMPLETE; classification wrong: True; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_002 ABSENT citation=evidence_54; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: INCOMPLETE_WITHOUT_FINDING, NO_LINKED_RESOURCE_PROOFS, NO_PRIMARY_PROFILE_PROOF, NO_SUPPORTED_STEPS

## case_03

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_9406 ANONYMIZED citation=evidence_94; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: COPY_COVERAGE_UNPROVEN, PREDICTION_KNOWN_SCOPE_ABSENCE, UNVERIFIED_MUTATION_AFTER_OBSERVATION

## case_04

Status INCOMPLETE / reference COMPLETE; classification wrong: True; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_004 ABSENT citation=evidence_54; missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_901 ANONYMIZED citation=evidence_56; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: INCOMPLETE_WITHOUT_FINDING, NO_LINKED_RESOURCE_PROOFS, NO_PRIMARY_PROFILE_PROOF, NO_SUPPORTED_STEPS

## case_07

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_007 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
- REPORT_REMAINING_RECORD object_storage/object_19 PRESENT citation=evidence_46; supported ledger differs from canonical coverage; review state/citation or planning obligation.
- DELETE_RECORD object_storage/object_19 ABSENT citation=(empty); supported ledger differs from canonical coverage; review state/citation or planning obligation.
- VERIFY_RECORD_ABSENT object_storage/object_19 ABSENT citation=(empty); supported ledger differs from canonical coverage; review state/citation or planning obligation.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY

## case_08

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_008 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF

## case_09

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_3960 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_PRESENT security_service/audit_record_4902 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY, RETAINED_ARCHIVE_PRESENCE_UNKNOWN

## case_10

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_010 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF

## case_17

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
None.

Extra:
- VERIFY_RECORD_ABSENT account_service/account_6523 ABSENT citation=(empty); supported ledger differs from canonical coverage; review state/citation or planning obligation.

Wrong citations: []
Wrong states: []
Case uncertainty codes: COPY_COVERAGE_UNPROVEN, POLICY_CONDITION_UNKNOWN, PREDICTED_POLICY_APPLICABILITY, PREDICTED_RETENTION_APPLICABILITY, PREDICTION_KNOWN_SCOPE_ABSENCE, RETAINED_ARCHIVE_PRESENCE_UNKNOWN, UNSUPPORTED_SCOPED_STATE, UNVERIFIED_MUTATION_AFTER_OBSERVATION

## case_18

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_5521 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_PRESENT security_service/audit_record_6645 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY

## case_20

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_5037 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_PRESENT security_service/audit_record_5569 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF

## case_21

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_6440 ABSENT citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_5335 ANONYMIZED citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF

## case_22

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_4990 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF, PREDICTED_RETENTION_APPLICABILITY

## case_23

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_410 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_PRESENT security_service/audit_record_4128 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF

## case_24

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_PRESENT security_service/audit_record_7095 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes:

## case_25

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_3136 ABSENT citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_1895 ANONYMIZED citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF

## case_26

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_5684 ABSENT citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_4566 ANONYMIZED citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: MISSING_REQUIRED_VERIFICATION, NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY, RETAINED_ARCHIVE_PRESENCE_UNKNOWN

## case_27

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_3866 ABSENT citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_4574 ANONYMIZED citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: MISSING_REQUIRED_VERIFICATION, NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY, RETAINED_ARCHIVE_PRESENCE_UNKNOWN

## case_28

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_5482 ABSENT citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_ANONYMIZED analytics_platform/analytics_6077 ANONYMIZED citation=evidence_92; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: MISSING_REQUIRED_VERIFICATION, NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY, RETAINED_ARCHIVE_PRESENCE_UNKNOWN

## case_29

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_7012 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_PRESENT security_service/audit_record_3954 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY

## case_30

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_4163 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.
- VERIFY_RECORD_PRESENT security_service/audit_record_1707 PRESENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: NO_PRIMARY_PROFILE_PROOF, PREDICTED_POLICY_APPLICABILITY

## case_31

Status COMPLETE / reference COMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_4857 ABSENT citation=evidence_51; missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: PREDICTED_POLICY_APPLICABILITY, PREDICTED_RETENTION_APPLICABILITY

## case_32

Status INCOMPLETE / reference INCOMPLETE; classification wrong: False; relative ordering wrong: False.

Missing:
- VERIFY_RECORD_ABSENT account_service/account_8858 ABSENT citation=(empty); missing discovery/attribution: no eligible grounded ledger target.

Extra:
None.

Wrong citations: []
Wrong states: []
Case uncertainty codes: PREDICTED_POLICY_APPLICABILITY, PREDICTED_RETENTION_APPLICABILITY

Cases without mismatches: case_05, case_06, case_11, case_12, case_13, case_14, case_15, case_16, case_19.
