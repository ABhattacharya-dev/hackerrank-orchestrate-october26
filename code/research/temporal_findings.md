# Temporal corroboration findings

Timestamps propose targets; they do not bind a resource to a customer. The table below is evaluation-only. No sample labels enter the matcher.

| Case | Candidate resource | Delta seconds | Stage | Independent proof / reason |
| --- | --- | ---: | --- | --- |
| case_01 | account_001 | -17 | weak_candidate | time proximity only; no independent subject corroboration |
| case_02 | account_002 | +303 | weak_candidate | time proximity only; no independent subject corroboration |
| case_06 | account_006 | -220 | corroborated_derived | evidence_57 strong subject in record; evidence_57 source_resource_id child-to-source |
| case_07 | account_007 | -81 | weak_candidate | time proximity only; no independent subject corroboration |
| case_08 | account_008 | +298 | weak_candidate | time proximity only; no independent subject corroboration |
| case_10 | account_010 | +37 | weak_candidate | time proximity only; no independent subject corroboration |
| case_18 | account_5193 | +179 | weak_candidate | time proximity only; no independent subject corroboration |
| case_20 | account_5193 | +179 | weak_candidate | time proximity only; no independent subject corroboration |

Within ±300 seconds, the full input has 118 unique-candidate cases and two multiple-candidate cases, but zero independently corroborated matches. Expanding to 360 seconds includes the 303-second example; it cannot retroactively make it a five-minute match. The sole corroborated public 360-second candidate uses a search record’s explicit source-resource relationship, which the frozen engine already follows. No account checks are recovered by admitting it again.

Missing account targets cannot be assigned from a worker resource ID plus timing even when independent snapshots show that ID absent: absence establishes state of the target, not ownership by this request. This independence distinction is the limiting evidence gap, not serialization. Anonymous analytics lookups with null subject/lookup fields have the same attribution gap. An LLM cannot legitimately fill an absent ownership fact without a cited relation.
