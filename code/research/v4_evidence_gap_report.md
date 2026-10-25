# V4 original-source evidence gap report

Frozen prediction baseline reproduced without writing protected artifacts: 29/32 statuses, 9/32 exact rows, 159/193 exact steps. There are 34 missing operations and 4 extras. Canonical labels are evaluation-only, not proof that the cited source supports its answer.

## Method and scope

Read every manifest text/SQL/JSON/log artifact directly and extracted all supplied PDF/image text with the existing deterministic tools. For every unmatched target, compared exact original JSON record paths or source lines against normalized observations, capture/event times, cutoff-specific identities, ledger links and treatment. The original object-browser screenshot relevant to extra findings was visually reviewed; screenshot-wide co-occurrence is not treated as ownership. SQL empty-table/schema semantics were inspected separately from target-ID occurrence. No V3 temporal association was rerun.

## Classification counts

- PARSER_LOSS: 0 missing operations.
- NORMALIZATION_LOSS: 0 missing operations.
- SOURCE_STRUCTURE_LOSS: 0 missing operations.
- IDENTITY_RELATIONSHIP_LOSS: 0 missing operations.
- STATE_RECONSTRUCTION_ERROR: 0 missing operations.
- POLICY_ERROR: 0 missing operations.
- OUTPUT_CONVENTION_ERROR: 0 missing operations.
- SOURCE_DOES_NOT_SUPPORT_PROOF: 34 missing operations.

## Research matrix: every unmatched operation

| Case | Missing/extra operation | Target | Original artifact / locator | Normalized evidence | Subject linkage | Policy | Classification / confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| case_01 | missing_steps / VERIFY_RECORD_ABSENT | account_001 | evidence_54 evidence/databases/customer_accounts_failover_replica_20260902.sql artifact: no target ID; inspect snapshot schema/scope | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_02 | missing_steps / VERIFY_RECORD_ABSENT | account_002 | evidence_54 evidence/databases/customer_accounts_failover_replica_20260902.sql artifact: no target ID; inspect snapshot schema/scope | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_03 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_9406 | evidence_94 evidence/logs/resource_lookup_trace_20260926_103856.log line:42 | evidence_94 line:43 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_04 | missing_steps / VERIFY_RECORD_ABSENT | account_004 | evidence_54 evidence/databases/customer_accounts_failover_replica_20260902.sql artifact: no target ID; inspect snapshot schema/scope | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_04 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_901 | evidence_56 evidence/records/customer_analytics_report_20260907.json json:/records/0 | evidence_56 records/0 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_07 | missing_steps / VERIFY_RECORD_ABSENT | account_007 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_07 | extra_steps / REPORT_REMAINING_RECORD | object_19 | evidence_46 evidence/images/object_storage_browser_20260213.png artifact: no target ID; inspect snapshot schema/scope | evidence_46 document:catalog-reference PRESENT eligible no subject overlap | grounded ledger link | DELETE | OUTPUT_CONVENTION_ERROR / medium |
| case_07 | extra_steps / DELETE_RECORD | object_19 | No manifest target occurrence; no verification citation supplied | evidence_46 document:catalog-reference PRESENT eligible no subject overlap | grounded ledger link | DELETE | OUTPUT_CONVENTION_ERROR / medium |
| case_07 | extra_steps / VERIFY_RECORD_ABSENT | object_19 | No manifest target occurrence; no verification citation supplied | evidence_46 document:catalog-reference PRESENT eligible no subject overlap | grounded ledger link | DELETE | OUTPUT_CONVENTION_ERROR / medium |
| case_08 | missing_steps / VERIFY_RECORD_ABSENT | account_008 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_09 | missing_steps / VERIFY_RECORD_ABSENT | account_3960 | evidence_06 evidence/logs/structured_service_events_eu_west_20260918.log line:86 | evidence_06 line:86 ABSENT FUTURE subject-linked | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_09 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_4902 | evidence_06 evidence/logs/structured_service_events_eu_west_20260918.log line:28 | evidence_06 line:28 PRESENT FUTURE subject-linked | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_10 | missing_steps / VERIFY_RECORD_ABSENT | account_010 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_17 | extra_steps / VERIFY_RECORD_ABSENT | account_6523 | evidence_67 evidence/logs/resource_lookup_trace_20260310_061801.log line:2 | evidence_67 line:3 ABSENT eligible subject-linked | grounded ledger link | DELETE | OUTPUT_CONVENTION_ERROR / medium |
| case_18 | missing_steps / VERIFY_RECORD_ABSENT | account_5521 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_18 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_6645 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_20 | missing_steps / VERIFY_RECORD_ABSENT | account_5037 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_20 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_5569 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_21 | missing_steps / VERIFY_RECORD_ABSENT | account_6440 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/account_service/profile_lookups/5 | evidence_92 service_exports/account_service/profile_lookups/5 ABSENT eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_21 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_5335 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/analytics_platform/profiles/5 | evidence_02 snapshots/3/records/0 ANONYMIZED FUTURE no subject overlap; evidence_92 service_exports/analytics_platform/profiles/5 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_22 | missing_steps / VERIFY_RECORD_ABSENT | account_4990 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_23 | missing_steps / VERIFY_RECORD_ABSENT | account_410 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_23 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_4128 | evidence_02 evidence/records/customer_data_snapshot_bundle_20260917.json json:/snapshots/8/records/2 | evidence_02 snapshots/8/records/2 PRESENT FUTURE subject-linked | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_24 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_7095 | evidence_02 evidence/records/customer_data_snapshot_bundle_20260917.json json:/snapshots/8/records/3 | evidence_02 snapshots/8/records/3 PRESENT FUTURE subject-linked | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_25 | missing_steps / VERIFY_RECORD_ABSENT | account_3136 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/account_service/profile_lookups/0 | evidence_92 service_exports/account_service/profile_lookups/0 ABSENT eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_25 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_1895 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/analytics_platform/profiles/0 | evidence_02 snapshots/3/records/1 ANONYMIZED FUTURE no subject overlap; evidence_92 service_exports/analytics_platform/profiles/0 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_26 | missing_steps / VERIFY_RECORD_ABSENT | account_5684 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/account_service/profile_lookups/4 | evidence_02 snapshots/0/records/0 PRESENT FUTURE subject-linked; evidence_92 service_exports/account_service/profile_lookups/4 ABSENT eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_26 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_4566 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/analytics_platform/profiles/2 | evidence_02 snapshots/3/records/2 ANONYMIZED FUTURE no subject overlap; evidence_92 service_exports/analytics_platform/profiles/2 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_27 | missing_steps / VERIFY_RECORD_ABSENT | account_3866 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/account_service/profile_lookups/1 | evidence_02 snapshots/10/records/0 PRESENT FUTURE subject-linked; evidence_92 service_exports/account_service/profile_lookups/1 ABSENT eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_27 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_4574 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/analytics_platform/profiles/3 | evidence_02 snapshots/3/records/3 ANONYMIZED FUTURE no subject overlap; evidence_92 service_exports/analytics_platform/profiles/3 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_28 | missing_steps / VERIFY_RECORD_ABSENT | account_5482 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/account_service/profile_lookups/3 | evidence_92 service_exports/account_service/profile_lookups/3 ABSENT eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_28 | missing_steps / VERIFY_RECORD_ANONYMIZED | analytics_6077 | evidence_92 evidence/records/service_resource_export_20260915_114455.json json:/service_exports/analytics_platform/profiles/6 | evidence_02 snapshots/3/records/4 ANONYMIZED FUTURE no subject overlap; evidence_92 service_exports/analytics_platform/profiles/6 ANONYMIZED eligible no subject overlap | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_29 | missing_steps / VERIFY_RECORD_ABSENT | account_7012 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_29 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_3954 | evidence_02 evidence/records/customer_data_snapshot_bundle_20260917.json json:/snapshots/8/records/8 | evidence_02 snapshots/8/records/8 PRESENT FUTURE subject-linked | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_30 | missing_steps / VERIFY_RECORD_ABSENT | account_4163 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_30 | missing_steps / VERIFY_RECORD_PRESENT | audit_record_1707 | evidence_02 evidence/records/customer_data_snapshot_bundle_20260917.json json:/snapshots/8/records/9 | evidence_02 snapshots/8/records/9 PRESENT FUTURE subject-linked | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_31 | missing_steps / VERIFY_RECORD_ABSENT | account_4857 | evidence_51 evidence/records/customer_data_snapshot_bundle_20260915.json artifact: no target ID; inspect snapshot schema/scope | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |
| case_32 | missing_steps / VERIFY_RECORD_ABSENT | account_8858 | No manifest target occurrence; no verification citation supplied | none | not established | unresolved | SOURCE_DOES_NOT_SUPPORT_PROOF / high |

## Exact source findings

### case_01 / account_001 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3343` activity_3342 DELETE_RECORD 2026-08-20T16:41:43Z; eligible=True, subject overlap=False; `Deletion worker reported the requested operation as completed. Target resource: account_001.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_02 / account_002 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3377` activity_3376 DELETE_RECORD 2026-08-22T07:30:03Z; eligible=True, subject overlap=False; `Deletion worker completed some internal work but could not confirm the final state. Target resource: account_002.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_03 / analytics_9406 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_94 `evidence/logs/resource_lookup_trace_20260926_103856.log:line:42`: `2026-09-26T09:54:09Z level=DEBUG service=analytics_platform trace_id=rb-095409-021 event=analytics_profile_read_started resource_id=analytics_9406 lookup_key=null`
- evidence_94 `evidence/logs/resource_lookup_trace_20260926_103856.log:line:43`: `2026-09-26T09:54:09Z level=INFO service=analytics_platform trace_id=rb-095409-021 event=analytics_profile_read_completed resource_id=analytics_9406 customer_reference=null email=null phone=null email_hash=null audience_cohort=general_shopper`
- Original activity `system_activity.csv:row:3853` activity_3852 ANONYMIZE_RECORD 2026-09-15T10:31:16Z; eligible=True, subject overlap=False; `Policy action completed for analytics_9406.`. A claim naming a target supplies neither ownership nor resulting state.

### case_04 / account_004 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_04 / analytics_901 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_56 `evidence/records/customer_analytics_report_20260907.json:json:/records/0`: `{"resource_id": "analytics_901", "user_id": null, "email": null, "phone": null, "email_hash": null}`
- Original activity `system_activity.csv:row:3464` activity_3463 ANONYMIZE_RECORD 2026-08-27T08:47:41Z; eligible=True, subject overlap=False; `Deletion worker reported the requested operation as completed. Target resource: analytics_901.`. A claim naming a target supplies neither ownership nor resulting state.

### case_07 / account_007 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3591` activity_3590 DELETE_RECORD 2026-09-01T19:28:39Z; eligible=True, subject overlap=False; `Deletion worker reported the requested operation as completed. Target resource: account_007.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_08 / account_008 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3555` activity_3554 DELETE_RECORD 2026-08-31T13:48:58Z; eligible=True, subject overlap=False; `Deletion worker reported the requested operation as completed. Target resource: account_008.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_09 / account_3960 / VERIFY_RECORD_ABSENT

Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.

- evidence_06 `evidence/logs/structured_service_events_eu_west_20260918.log:line:86`: `2026-09-16T08:57:34Z {"severity":"INFO","logger":"account_service","service":"account_service","instance":"account-7","pod":"account-3cbd","region":"eu-west-1","trace_id":"tr-1463969","resource_id":"account_3960","event":"profile_lookup_completed","rows":"0","http_status":"404","duration_ms":"67"}`
- Original activity `system_activity.csv:row:3704` activity_3703 DELETE_RECORD 2026-09-07T07:55:18Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_3960 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.

### case_09 / audit_record_4902 / VERIFY_RECORD_PRESENT

Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.

- evidence_06 `evidence/logs/structured_service_events_eu_west_20260918.log:line:28`: `2026-09-16T08:52:59Z {"severity":"DEBUG","logger":"security_service","service":"security_service","instance":"security-5","pod":"security-c548","region":"ap-south-1","trace_id":"tr-9028396","resource_id":"audit_record_4902","event":"audit_record_read_completed","integrity_check":"passed","rows":"1"}`

### case_10 / account_010 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3596` activity_3595 DELETE_RECORD 2026-09-02T10:08:37Z; eligible=True, subject overlap=False; `Deletion worker reported the requested operation as completed. Target resource: account_010.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_18 / account_5521 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3733` activity_3732 DELETE_RECORD 2026-09-09T09:52:26Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_5521 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_18 / audit_record_6645 / VERIFY_RECORD_PRESENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_20 / account_5037 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3735` activity_3734 DELETE_RECORD 2026-09-09T10:14:55Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_5037 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_20 / audit_record_5569 / VERIFY_RECORD_PRESENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_21 / account_6440 / VERIFY_RECORD_ABSENT

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/account_service/profile_lookups/5`: `{"observed_at": "2026-09-15T09:31:19Z", "profile": null, "resource_id": "account_6440", "status_code": 404}`
- Original activity `system_activity.csv:row:3662` activity_3661 DELETE_RECORD 2026-09-05T11:01:53Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_6440 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.

### case_21 / analytics_5335 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/3/records/0`: `{"resource_id": "analytics_5335", "user_id": null, "email": null, "phone": null, "email_hash": null}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/analytics_platform/profiles/5`: `{"customer_reference": null, "email": null, "email_hash": null, "observed_at": "2026-09-15T09:34:42Z", "phone": null, "resource_id": "analytics_5335"}`
- Original activity `system_activity.csv:row:3666` activity_3665 ANONYMIZE_RECORD 2026-09-05T11:31:34Z; eligible=True, subject overlap=False; `Policy action completed for analytics_5335.`. A claim naming a target supplies neither ownership nor resulting state.

### case_22 / account_4990 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3574` activity_3573 DELETE_RECORD 2026-09-01T09:12:11Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_4990 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_23 / account_410 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3663` activity_3662 DELETE_RECORD 2026-09-05T11:10:55Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_410 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_23 / audit_record_4128 / VERIFY_RECORD_PRESENT

Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/8/records/2`: `{"resource_id": "audit_record_4128", "subject_reference": "user_23", "event_name": "account_deletion_reviewed"}`

### case_24 / audit_record_7095 / VERIFY_RECORD_PRESENT

Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/8/records/3`: `{"resource_id": "audit_record_7095", "subject_reference": "user_24", "event_name": "account_deletion_reviewed"}`

### case_25 / account_3136 / VERIFY_RECORD_ABSENT

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/account_service/profile_lookups/0`: `{"observed_at": "2026-09-15T09:31:40Z", "profile": null, "resource_id": "account_3136", "status_code": 404}`
- Original activity `system_activity.csv:row:3598` activity_3597 DELETE_RECORD 2026-09-02T10:48:27Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_3136 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.

### case_25 / analytics_1895 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/3/records/1`: `{"resource_id": "analytics_1895", "user_id": null, "email": null, "phone": null, "email_hash": null}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/analytics_platform/profiles/0`: `{"customer_reference": null, "email": null, "email_hash": null, "observed_at": "2026-09-15T09:58:44Z", "phone": null, "resource_id": "analytics_1895"}`
- Original activity `system_activity.csv:row:3603` activity_3602 ANONYMIZE_RECORD 2026-09-02T11:31:08Z; eligible=True, subject overlap=False; `Policy action completed for analytics_1895.`. A claim naming a target supplies neither ownership nor resulting state.

### case_26 / account_5684 / VERIFY_RECORD_ABSENT

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/0/records/0`: `{"resource_id": "account_5684", "customer_reference": "user_26", "email": "almeida.mariana@gmail.com", "phone": "+55 21 90180-9087"}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/account_service/profile_lookups/4`: `{"observed_at": "2026-09-15T09:01:48Z", "profile": null, "resource_id": "account_5684", "status_code": 404}`
- Original activity `system_activity.csv:row:3601` activity_3600 DELETE_RECORD 2026-09-02T11:08:43Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_5684 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.

### case_26 / analytics_4566 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/3/records/2`: `{"resource_id": "analytics_4566", "user_id": null, "email": null, "phone": null, "email_hash": null}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/analytics_platform/profiles/2`: `{"customer_reference": null, "email": null, "email_hash": null, "observed_at": "2026-09-15T11:29:16Z", "phone": null, "resource_id": "analytics_4566"}`
- Original activity `system_activity.csv:row:3604` activity_3603 ANONYMIZE_RECORD 2026-09-02T11:31:24Z; eligible=True, subject overlap=False; `Policy action completed for analytics_4566.`. A claim naming a target supplies neither ownership nor resulting state.

### case_27 / account_3866 / VERIFY_RECORD_ABSENT

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/10/records/0`: `{"resource_id": "account_3866", "customer_reference": "user_27", "email": "ananya-nair@gmail.com", "phone": "+91 97441 66195"}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/account_service/profile_lookups/1`: `{"observed_at": "2026-09-15T09:59:48Z", "profile": null, "resource_id": "account_3866", "status_code": 404}`
- Original activity `system_activity.csv:row:3531` activity_3530 DELETE_RECORD 2026-08-30T10:57:28Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_3866 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.

### case_27 / analytics_4574 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/3/records/3`: `{"resource_id": "analytics_4574", "user_id": null, "email": null, "phone": null, "email_hash": null}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/analytics_platform/profiles/3`: `{"customer_reference": null, "email": null, "email_hash": null, "observed_at": "2026-09-15T10:07:38Z", "phone": null, "resource_id": "analytics_4574"}`
- Original activity `system_activity.csv:row:3534` activity_3533 ANONYMIZE_RECORD 2026-08-30T11:31:09Z; eligible=True, subject overlap=False; `Policy action completed for analytics_4574.`. A claim naming a target supplies neither ownership nor resulting state.

### case_28 / account_5482 / VERIFY_RECORD_ABSENT

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/account_service/profile_lookups/3`: `{"observed_at": "2026-09-15T11:07:16Z", "profile": null, "resource_id": "account_5482", "status_code": 404}`
- Original activity `system_activity.csv:row:3530` activity_3529 DELETE_RECORD 2026-08-30T10:46:13Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_5482 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.

### case_28 / analytics_6077 / VERIFY_RECORD_ANONYMIZED

State is normalized, but original scoped record has null/missing owner or lookup selector; no authoritative eligible subject relationship.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/3/records/4`: `{"resource_id": "analytics_6077", "user_id": null, "email": null, "phone": null, "email_hash": null}`
- evidence_92 `evidence/records/service_resource_export_20260915_114455.json:json:/service_exports/analytics_platform/profiles/6`: `{"customer_reference": null, "email": null, "email_hash": null, "observed_at": "2026-09-15T11:44:55Z", "phone": null, "resource_id": "analytics_6077"}`
- Original activity `system_activity.csv:row:3535` activity_3534 ANONYMIZE_RECORD 2026-08-30T11:31:53Z; eligible=True, subject overlap=False; `Policy action completed for analytics_6077.`. A claim naming a target supplies neither ownership nor resulting state.

### case_29 / account_7012 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3533` activity_3532 DELETE_RECORD 2026-08-30T11:06:57Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_7012 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_29 / audit_record_3954 / VERIFY_RECORD_PRESENT

Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/8/records/8`: `{"resource_id": "audit_record_3954", "subject_reference": "user_29", "event_name": "account_deletion_reviewed"}`

### case_30 / account_4163 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3466` activity_3465 DELETE_RECORD 2026-08-27T10:55:42Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_4163 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_30 / audit_record_1707 / VERIFY_RECORD_PRESENT

Original target records exist only in captures after audit_at; embedded earlier snapshot times do not make them available earlier.

- evidence_02 `evidence/records/customer_data_snapshot_bundle_20260917.json:json:/snapshots/8/records/9`: `{"resource_id": "audit_record_1707", "subject_reference": "user_30", "event_name": "account_deletion_reviewed"}`

### case_31 / account_4857 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3683` activity_3682 DELETE_RECORD 2026-09-06T10:45:58Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_4857 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

### case_32 / account_8858 / VERIFY_RECORD_ABSENT

No original manifest target record; empty snapshots may establish scoped absence for independently known IDs, not ownership or an invented target ID.

- Original activity `system_activity.csv:row:3686` activity_3685 DELETE_RECORD 2026-09-06T11:05:15Z; eligible=True, subject overlap=False; `Deletion worker submitted primary profile account_8858 to account_service.`. A claim naming a target supplies neither ownership nor resulting state.
No original target occurrence in the manifest artifacts. Generic worker target claims are not state/ownership proof and were not used to invent an edge.

## Canonical conventions and stop decision

Case-independent preservation rules remain: retain required security/legal records, preserve compliant tombstone references, block supported restore paths without deleting archives, and use empty citations on incomplete-case future checks. The main missing operations already have parser-normalized state or cannot be attributed/available at cutoff. No recoverable new scoped ownership fact was established. A filename, product similarity, list position or numeric suffix is not an authoritative relationship.

The object-storage extra is supported by the selected delivery-confirmation filename in the original browser image and an eligible explicit exclusive subject catalog link. Other file rows are unrelated; the extractor does not join their customers. Suppressing that justified finding to match a reference would be an unsupported convention shortcut. The extra absent-account check likewise has an independent baseline ledger link and is not removed merely to improve precision.

No production parser or policy correction is justified by this matrix. Stop speculative observation/vision integration rather than invent relationships. The optional vision adapter limitation is real, but its currently queued text proposals cannot fill absent or future source facts. Tier-B validation design and independent source-boundary tests are reported separately; no unmeasured model assertion enters the ledger.
