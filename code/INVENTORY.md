# Milestone 0 — participant-data inventory

Scope: all nine CSVs, 94 manifest evidence files, and all 32 public answers. Only participant-facing data was inspected. This reconnaissance milestone does not establish submission readiness.

## CSV schemas and actual-value profiles

| File | Rows | Fields |
| --- | ---: | --- |
| deletion_requests.csv | 518 | case_id, email, requested_at, reported_status, reported_at, audit_at, request_text |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| deletion_rules.csv | 15 | rule_id, data_category, condition, required_action |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| evidence_files.csv | 94 | file_id, file_path, origin, captured_at |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| output.csv | 0 | case_id, deletion_status, steps_json |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| sample_deletion_requests.csv | 32 | case_id, email, requested_at, reported_status, reported_at, audit_at, request_text |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| sample_output.csv | 32 | case_id, deletion_status, steps_json |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| system_activity.csv | 4011 | activity_id, event_time, event_type, source_system, target_system, resource_id, reported_result, details |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| user_audit_log.csv | 306 | audit_id, user_id, event_time, field_name, old_value, new_value |

Actual-value distributions (identifiers are summarized rather than copied into logs):

| user_identities.csv | 850 | user_id, name, email, phone, email_hash, updated_at |

Actual-value distributions (identifiers are summarized rather than copied into logs):

- `deletion_requests.csv.reported_status`: {'COMPLETE': 254, 'NOT_STARTED': 112, 'PARTIALLY_COMPLETE': 152}.
- `user_audit_log.csv.field_name`: {'phone': 92, 'email': 107, 'email_hash': 107}.
- `system_activity.csv.event_type`: {'INDEX_RECORD': 400, 'UPDATE_RECORD': 672, 'RETAIN_RECORD': 206, 'SEND_EMAIL': 368, 'SYNC_RECORD': 447, 'DELETE_RECORD': 890, 'ANONYMIZE_RECORD': 204, 'REFRESH_CACHE': 284, 'CREATE_EXPORT': 155, 'CHECK_DATA_FLOW': 89, 'CHECK_RESTORE_ACCESS': 28, 'REDACT_RECORD': 173, 'DISABLE_DATA_FLOW': 36, 'BLOCK_RESTORE': 36, 'RESTORE_BACKUP': 1, 'CLASSIFY_REQUEST': 10, 'LINK_RESOURCE_IDENTITY': 12}.
- `system_activity.csv.reported_result`: {'SUCCESS': 2914, 'FAILED': 721, 'PARTIAL': 376}.
- `deletion_rules.csv.required_action`: {'DELETE': 7, 'REDACT': 3, 'ANONYMIZE': 2, 'RETAIN': 3}.
- Evaluation requests have 517 distinct supplied emails and 72 audit cutoffs; do not cache a verdict solely by email.
- Identity snapshot: 850 stable user IDs. Current fields and audit old/new values are separate evidence, not a timeless union of identity ownership.

## Supplied deletion policy

| Category | Condition (verbatim) | Treatment |
| --- | --- | --- |
| USER_PROFILE | Always | DELETE |
| SECONDARY_IDENTIFIER | Always | DELETE |
| SEARCH_INDEX_ENTRY | Always | DELETE |
| CACHE_ENTRY | Always | DELETE |
| SUPPORT_MESSAGE | Conversation contains shared customer, agent, or order context that must be retained | REDACT |
| SUPPORT_ATTACHMENT | Attachment belongs only to the deletion subject | DELETE |
| ANALYTICS_PROFILE | Record is still attributable to a user | ANONYMIZE |
| PRODUCT_TELEMETRY | Record is still attributable to a user | ANONYMIZE |
| USER_EXPORT | Always | DELETE |
| MARKETING_PROFILE | Always | DELETE |
| EMAIL_DELIVERY_LOG | Log contains a user email address | REDACT |
| SECURITY_AUDIT_LOG | Record is within the supplied retention period | RETAIN |
| LEGAL_HOLD_RECORD | A supplied legal hold is active | RETAIN |
| BACKUP_ARCHIVE | Restore access can be blocked | RETAIN |
| ACCOUNT_TOMBSTONE | Account is deleted and only a stable internal user_id is needed to preserve references to retained records | REDACT |

Retention and legal-hold conditions require evidence of applicable dates/holds; no default legal period is supplied. A retained backup still requires safe restore controls. A tombstone may retain its stable user reference, while name/email/phone/email hash must be removed. Shared-context support messages require redaction; subject-only attachments require deletion.

## Evidence inventory and adapters

Manifest formats: {'.log': 26, '.json': 28, '.txt': 1, '.png': 11, '.sql': 24, '.pdf': 4}. Paths resolve relative to dataset/. Manifest origin/capture metadata identifies sources, not subjects.

Directories: databases/ (SQL), records/ (JSON and text), logs/, documents/ (PDF), images/ (PNG). All 94 paths were resolved and processed. Documents/images are business artifacts rather than explicit verdicts: statements, support attachments, compliance/retention records, and account/search/marketing/analytics/export/connector/backup/reference screens.

JSON has four top-level arrangements: service_exports by system and collection; snapshots with data_store/collection/captured_at and records; explicit observation records with recorded_at/system/resource_id/record_type/result/subject_reference; ordinary business records with collection/capture metadata. Nested profile:null or empty search hits are scoped readbacks; anonymous profiles can have every subject field null. Text handovers contain time | system | resource | category | result | subject rows.

Logs use logfmt, bracket/trace, pipe-separated, syslog, timestamp-plus-JSON and escaped cloud message envelopes. Start and completion lines must be joined by trace/request ID; interleaved lines and unrelated records are common. Cache misses/retries are not deletion proofs; operational success claims differ from actual readbacks.

SQL table names and number of files containing each:

- `backup_restore_entries`: 11.
- `connector_subscriptions`: 11.
- `customer_analytics_profiles`: 11.
- `customer_data_failover_replica`: 1.
- `customer_data_primary`: 11.
- `customer_data_read_replica`: 5.
- `customer_data_replica_ap_south`: 3.
- `customer_data_replica_eu_west`: 3.
- `customer_data_reporting_replica`: 2.
- `customer_exports`: 11.
- `customer_profiles`: 11.
- `customer_profiles_failover_replica`: 1.
- `customer_profiles_primary`: 1.
- `customer_search_documents`: 11.
- `search_documents_primary`: 1.
- `security_audit_records`: 11.
- `snapshot_scope`: 11.
- `support_records`: 11.

SQL variants include typed inventory tables (profiles, search, analytics, support, exports, connectors, backups and audit records), record_json snapshots with origin_system/collection_name, and primary/read/regional/reporting/failover replicas. snapshot_scope and completion timestamps delimit coverage. Empty exported tables are evidence of scoped absence only after subject/resource linkage and scope coverage are established. Never interpret primary absence as replica absence.

## Dependencies, ambiguities and citation conventions

- Intent comes first; access/correction/export/marketing opt-out alone is NOT_APPLICABLE. Public samples contain no negative-intent example.
- Request email → eligible current/historical identifiers → evidence content/trace links → scoped resource ledger → conditional policy → flow/restore controls and record treatment → verification. Do not map IDs by shared numeric suffix.
- Distinguish requested_at, reported_at, audit_at, identity update/event times, embedded observation times, and file capture/availability. Exclude later evidence; equal-time conflicts, alias reuse, shared names, stale replicas and restored copies need explicit rules.
- Cite public file_id, activity_id or audit_id; existence is insufficient: the source must support that resource/state by cutoff. COMPLETE uses cited verification only. INCOMPLETE findings are cited, while all proposed remediation and future verification use empty evidence_id. NOT_APPLICABLE has [].
- Serialize FINDING → REMEDIATION → VERIFICATION, then the operation order in problem_statement.md, then system_id/resource_id ascending; number steps after sorting. Dependency execution order may conflict with lexical canonical order: document the conflict instead of silently changing serialization.
- Root/problem report paths say evaluation/; README explicitly uses code/evaluation/ and packages README plus code. Keep reports under code/evaluation/. Root log.txt and the separate requested trace ZIP are distinct; no nested archive belongs in code.zip.
- Missing retained records have no universal repair operation; UNKNOWN is not an allowed final status. Anonymous or absent resources may lack a grounded subject link. Earlier baseline diagnostics are implementation coverage failures, not proof that all affected inputs are defective.
- Investigated citation ambiguity: sample case_09 names account/security verification with evidence_93, whose readback covers only a backup; the ordinary-log account observation is in a file captured after cutoff. Keep this discrepancy explicit.

## All 32 public answers reviewed

| Case | Status | Steps | Cited IDs |
| --- | --- | ---: | --- |
| case_01 | COMPLETE | 1 | evidence_54 |
| case_02 | COMPLETE | 1 | evidence_54 |
| case_03 | COMPLETE | 3 | evidence_94 |
| case_04 | COMPLETE | 2 | evidence_54, evidence_56 |
| case_05 | INCOMPLETE | 3 | evidence_54 |
| case_06 | INCOMPLETE | 4 | evidence_57 |
| case_07 | INCOMPLETE | 4 | evidence_58 |
| case_08 | INCOMPLETE | 4 | evidence_59 |
| case_09 | INCOMPLETE | 5 | evidence_93 |
| case_10 | INCOMPLETE | 4 | evidence_61 |
| case_11 | INCOMPLETE | 14 | evidence_03 |
| case_12 | INCOMPLETE | 5 | evidence_01 |
| case_13 | INCOMPLETE | 8 | evidence_03 |
| case_14 | INCOMPLETE | 5 | evidence_03 |
| case_15 | INCOMPLETE | 5 | evidence_01 |
| case_16 | INCOMPLETE | 7 | evidence_05 |
| case_17 | INCOMPLETE | 5 | evidence_01 |
| case_18 | INCOMPLETE | 14 | evidence_94 |
| case_19 | INCOMPLETE | 8 | evidence_01 |
| case_20 | INCOMPLETE | 8 | evidence_94 |
| case_21 | COMPLETE | 3 | evidence_92 |
| case_22 | INCOMPLETE | 8 | evidence_05 |
| case_23 | INCOMPLETE | 8 | evidence_92 |
| case_24 | INCOMPLETE | 7 | evidence_92 |
| case_25 | COMPLETE | 3 | evidence_92 |
| case_26 | COMPLETE | 6 | evidence_92 |
| case_27 | COMPLETE | 6 | evidence_92 |
| case_28 | COMPLETE | 6 | evidence_92 |
| case_29 | INCOMPLETE | 14 | evidence_92 |
| case_30 | INCOMPLETE | 14 | evidence_92 |
| case_31 | COMPLETE | 3 | evidence_51 |
| case_32 | INCOMPLETE | 5 | evidence_51 |

Sample status distribution: {'COMPLETE': 10, 'INCOMPLETE': 22}. All 32 sample rows passed schema/order/citation-availability validation. This is not semantic entailment validation or proof that the predictor reproduces them.

## Executed acceptance checks

- `python3 code/evaluation/validate_output.py --output dataset/sample_output.csv --requests dataset/sample_deletion_requests.csv`: 32 rows pass.
- Existing validator regression tests cover future citations, invalid phases/states/fields, missing/duplicate IDs and non-deletion steps; rejection of column order and step order is checked in this milestone.
- Root AGENTS.md and supplied dataset remain unchanged. All major formats and contracts are inventoried; model accuracy, extraction completeness and final submission readiness remain separate milestones.

## Field-level value coverage

Each entry is `field: distinct values / empty cells`; all cells were scanned. Empty and explicit JSON null are different representations.

- `deletion_requests.csv` — case_id: 518/0, email: 517/0, requested_at: 508/0, reported_status: 3/0, reported_at: 238/0, audit_at: 72/0, request_text: 375/0.
- `deletion_rules.csv` — rule_id: 15/0, data_category: 15/0, condition: 9/0, required_action: 4/0.
- `evidence_files.csv` — file_id: 94/0, file_path: 94/0, origin: 30/0, captured_at: 93/0.
- `output.csv` — case_id: 0/0, deletion_status: 0/0, steps_json: 0/0.
- `sample_deletion_requests.csv` — case_id: 32/0, email: 32/0, requested_at: 30/0, reported_status: 3/0, reported_at: 22/0, audit_at: 13/0, request_text: 32/0.
- `sample_output.csv` — case_id: 32/0, deletion_status: 2/0, steps_json: 32/0.
- `system_activity.csv` — activity_id: 4011/0, event_time: 4011/0, event_type: 17/0, source_system: 11/0, target_system: 19/0, resource_id: 3948/0, reported_result: 3/0, details: 4011/0.
- `user_audit_log.csv` — audit_id: 306/0, user_id: 196/0, event_time: 198/0, field_name: 3/0, old_value: 306/0, new_value: 306/0.
- `user_identities.csv` — user_id: 850/0, name: 847/0, email: 850/0, phone: 850/0, email_hash: 850/0, updated_at: 850/0.
