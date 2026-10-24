# Milestone 1 — ingestion and provenance acceptance

## Objective and deliverables

Process every manifest artifact once; retain traceable observations and explicit failures/uncertainties. EvidenceStore provides CSV, SQL, JSON, text, log, PDF text and image OCR adapters, resource/identifier indexes, original global activity/audit rows and citation timestamps. Repeated load() on the same store is idempotent; one store is reused for all request audits. Content-hash document caches persist between runs.

## Executed acceptance results

- All 94 manifest entries have an outcome: 89 processed; 5 processed_unresolved; 0 parser failures.
- 2906 normalized observations and 116 SQL scopes retained. All observation locators, source hashes, system/resource IDs and timestamps were checked.
- 4317 original CSV activity/audit rows indexed by their original IDs and source filenames; claims remain distinct from direct state observations.
- All 32 software tests passed. After the final CSV-failure-report change, all 8 ingestion tests passed again.
- Synthetic tests exercise corrupt and missing artifacts, continued processing, partial-artifact rollback, CSV row provenance, repeated loads, configured-extractor escalation, absent vision configuration, and existing parser envelopes/path security.
- Public-sample predictor regression executed successfully; see the existing evaluator for metrics. This milestone does not certify final submission readiness.

## Explicit unresolved artifacts

| ID | Source | Status |
| --- | --- | --- |
| evidence_18 | evidence/documents/account_history_report_20260718.pdf | vision_not_configured |
| evidence_27 | evidence/documents/legal_retention_register_20260529.pdf | vision_not_configured |
| evidence_32 | evidence/images/backup_restore_console_20260429.png | vision_not_configured |
| evidence_42 | evidence/images/deleted_account_reference_20260310.png | vision_not_configured |
| evidence_46 | evidence/images/object_storage_browser_20260213.png | vision_not_configured |

These artifacts were read and text-extracted, but deterministic extraction did not establish unambiguous scoped resource state. Some catalog enrichment later supplies partial references; that does not resolve all artifact uncertainty. Empty SQL snapshots are processed scope evidence, not failures.

## Provenance and failure semantics

Each observation retains the public file_id, source path, line/row/table/document locator, availability and observation times, system/resource/category/state, original extracted fields and a source content hash. Derived catalog observations retain the supporting activity ID/time; their availability is no earlier than both file capture and catalog linkage. Original activity and identity-audit records retain their IDs and all CSV fields. trace(observation) returns the source locator/hash and fields.

Per-artifact exceptions yield failed outcomes with source and error class; partial observations and SQL scopes are rolled back before processing the next entry. Missing files and unsupported formats are explicit failures. Path escapes are fatal security errors. Global CSV failures are reported; strict application mode rejects ingestion failures. Outputs contain no raw exception strings that might reveal secrets. Unknown resource identifiers/states are retained as unresolved records rather than silently certified.

## Configured multimodal escalation

The optional OpenAI Responses adapter is in ghostgraph/vision.py. Set GHOSTGRAPH_VISION_API_KEY and GHOSTGRAPH_VISION_MODEL securely in the environment; HTTPS access to api.openai.com is required. No credentials or model are configured in this instance. Therefore zero remote vision calls were executed, and the five artifacts remain vision_not_configured. The live provider route is unverified; adapter contract tests use a test extractor, not a real model.

Vision requests are bounded by timeout/output length and preserve actual returned model/usage. Evidence is explicitly treated as untrusted data. Returned structured text and uncertainty are retained for review; they never automatically become certified resource states or bypass cutoff/identity rules. API errors and malformed responses remain visible as vision_failed. Existing Tesseract OCR is a local configured recognizer; it is distinct from semantic vision review.

## Reproduce

```bash
python3 code/evaluation/ingest.py
PYTHONPATH=code python3 -m unittest discover -s code/tests -v
```

Detailed current outcomes: .ghostgraph/ingestion_report.json (ignored local artifact; extraction text can contain participant data). Exit 1 means parser failure, while unresolved semantic artifacts remain explicit in the report even with exit 0. The exit criterion is met: every real manifest entry was processed with a detectable outcome and observations are traceable. Semantic ambiguity and final audit coverage remain subsequent work.
