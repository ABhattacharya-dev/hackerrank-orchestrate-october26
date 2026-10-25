# V6 candidate audit

Protected production:7a18c2e, submission-v5.1. Research branch:experiment/activity-assignment-v6. Production inference modules, output.csv and code.zip are unchanged. No canonical labels are read by v6_assignment.py; labels enter only reproduction/evaluation/report tooling.

## Independent source reproduction

All reviewer counts reproduce exactly:508 authorized full requests,342 without account_service steps;108 unique compatible candidates in the fixed [-120,+30] minute window, split73 INCOMPLETE/35 COMPLETE. Public13 unique candidates agree with all13 canonical IDs (evaluation only);57 unique candidates in the166 already-grounded full requests agree with all57 current account sets. All539 qualifying account DELETE_RECORD events have source deletion_worker, with270 SUCCESS,158 PARTIAL and111 FAILED results.

Mapping COMPLETE→SUCCESS, PARTIALLY_COMPLETE→PARTIAL, NOT_STARTED→FAILED is a lexical workflow-compatibility hypothesis, not an official causal mapping or a deletion-state fact. FAILED is compatible with an unsuccessful start attempt but does not prove a worker belongs to the request. Mapping was fixed from the review/source vocabularies, not optimized using canonical labels. Workflow claims and operation outcomes do not determine actual record state.

The supplied asymmetric window has no independent preregistration/provenance available in the repository. Whether the external reviewer tuned it against known public cases cannot be established. It is a development hypothesis, not held-out validation. V6 froze the supplied window and a five-window comparison grid before scoring, and did not search for an optimal public score.

## Window sensitivity

Unique means exactly one eligible event, not nearest event, one resource per subject, or a forced global one-to-one matching. Bounds require event≥requested_at, event≤audit_at and workflow report≤audit_at. Enforcing the first two bounds changes none of the reviewer counts in this dataset, but they remain required safeguards. Wider windows are less likely to appear unique, and can expose a false narrow singleton.

| Window | Status filter | Missing-account unique | Existing-account unique / agree | Public unique / agree |
|---|---|---:|---:|---:|
| five_minutes | False | 86 | 32 / 0 | 7 / 5 |
| five_minutes | True | 37 | 8 / 0 | 4 / 3 |
| half_hour | False | 13 | 8 / 0 | 7 / 7 |
| half_hour | True | 40 | 21 / 0 | 6 / 5 |
| wide_review | False | 14 | 8 / 8 | 8 / 8 |
| wide_review | True | 108 | 57 / 57 | 13 / 13 |
| two_hours | False | 14 | 8 / 8 | 6 / 6 |
| two_hours | True | 108 | 57 / 57 | 12 / 12 |
| one_day | False | 4 | 4 / 4 | 0 / 0 |
| one_day | True | 63 | 35 / 34 | 5 / 4 |

## Eight conflicting five-minute singletons

All eight status-compatible narrow-window singleton candidates disagree with the existing resource set. A disagreement is not itself proof that a customer cannot have multiple accounts, but it invalidates using narrow uniqueness as ownership proof. Existing edges are never removed.

| Case | Worker | Candidate | Grounded resource | Delta seconds |
|---|---|---|---|---:|
| case_51 | activity_3740 | account_5193 | account_3610 | 179 |
| case_90 | activity_3354 | account_9051 | account_9673 | -105 |
| case_269 | activity_2014 | account_5047 | account_7699 | 133 |
| case_292 | activity_1850 | account_731 | account_1125 | -134 |
| case_326 | activity_1602 | account_8264 | account_3785 | 284 |
| case_331 | activity_1563 | account_9523 | account_6814 | 153 |
| case_371 | activity_1236 | account_6093 | account_5896 | -207 |
| case_422 | activity_1000 | account_5754 | account_4087 | 147 |

## Provenance classes and candidate graph

The graph records directly evidenced existing relationships (`already_grounded` with separate source proofs), independently corroborated candidate relationships (`own` positive eligible references), weak time/status-only candidates, and rejected/conflicting candidates with explicit reasons. New weak relationships are never relabeled as direct evidence. The ordinary ledger's temporary discovery seed is replaced in diagnostics by an explicitly labeled research hypothesis; existing grounded resources delegate to the baseline ledger without replacement. No strict-certification code is changed or invoked with candidate edges.

B uses a unique status-compatible event plus bounds/foreign-owner/history/existing-assignment consistency checks. Absence of a contradiction is not positive ownership proof. C adds conservative bipartite collision rejection across contemporaneously eligible requests from different independently resolved subjects. It does not maximize a one-to-one assignment: such exclusivity is not established. Repeated same-subject requests can share an event; multiple events/resources remain unresolved rather than forced. Future peer requests/statuses and future identity snapshots cannot affect earlier collision checks. D additionally requires positive ownership corroboration before ordinary source-grounded state/policy planning. All108 new singleton candidates lack that corroboration;57 have corroboration only because they are already grounded controls. Eight of those controls are collision-rejected as event associations, while their actual existing resource edges remain in output.

Per-window candidate records, source event locators/times, eligibility, ownership proofs and B/C/D rejection reasons are enumerated in v6_edge_provenance.md and reproducibly generated .ghostgraph/v6/*_edges.json. No inference uses numeric suffixes, nearest-ID conventions, canonical resource labels or worker SUCCESS as a resulting-state observation.

## case_09: eligible state is not eligible ownership

Request cutoff:2026-09-16T09:00:00Z. The eligible activity_3703 (system_activity.csv row3704) identifies account_3960 as a worker target at2026-09-07T07:55:18Z,3882 seconds before reported_at. It contains no subject identifier. A full account snapshot really is eligible: evidence_93, evidence/databases/customer_data_inventory_20260916.sql, snapshot_scope row for account_service (line12) and table customer_profiles, captured2026-09-16T08:37:39Z. Its exhaustive lookup supports absence of that specified resource conditional on identifying the target; it does not supply the missing subject/account relationship. B/C use the worker correlation assumption to propose a future empty-citation account verification. D rejects the unsupported ownership inference.

The actual profile readback in evidence_06 line86 observes account_3960 absent at2026-09-16T08:57:34Z, but the file was captured2026-09-18T11:55:24Z: it is ineligible. The retained audit_record_4902 and its subject trace exist only in the same late file (readback line28, observed2026-09-16T08:52:59Z). Original-source identifier search finds no eligible record/catalog/worker reference identifying or proving presence of that audit resource. Its verification cannot be recovered without late-source use or inventing an ID. No late trace is used to tie the worker target to user_61. Citation clamping would not fix that ownership leak; it is not performed.

No supplied external prototype or provenance proving an untuned window is present. The reviewer counts are verified; the stronger ownership/generalization interpretation is not established.
