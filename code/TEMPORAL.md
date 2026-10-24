# Milestone 3 — temporal reconstruction acceptance

## Objective and implemented engine

`ghostgraph/temporal.py` reconstructs one resource at a requested cutoff and
returns aggregate state, a scoped witness where defensible, all retained scope
states/source references, and explicit uncertainty reasons. The audit engine
stores this explanation in each case's `temporal_ledger`. Original observations
remain unchanged. This milestone does not certify full submission correctness.

## Explicit precedence rules

1. Admit direct observations only when both observation time and availability
   time are at or before audit_at (inclusive). Late capture cannot backdate a fact.
   Trace-linked identifiers are unavailable before the latest contributing trace
   context; catalog-derived observations are unavailable before their link event.
2. Preserve physical replica/table scopes. For logical readbacks, retain collector
   origins separately instead of assuming two collectors queried the same store.
   Origin alone does not prove distinct physical replicas either: differing
   unaligned logical-source states produce SCOPE_ALIGNMENT_UNKNOWN.
3. Within each scope, the latest observed time supersedes earlier observations.
   Export/availability recency is an eligibility condition, not a state-precedence
   rule. SQL row updated_at is not snapshot time; declared snapshot_scope/header
   capture supplies observed time, while manifest capture supplies availability.
4. At equal observed time, differing direct states produce CONFLICT, irrespective
   of parser quality. Quality scores cannot conceal contradictory facts. Input
   permutations yield the same sorted conflict explanation. UNKNOWN at a later
   time cannot silently reuse an earlier definite state.
5. A directly observed positive copy in an explicit scope is not cleared by an
   absence in another scope. A later observation of that same replica can clear
   its own copy. An absent primary or one unsuccessful lookup cannot establish
   universal absence. Scoped ABSENT may be retained as a witness for provisional
   checks while aggregate state remains UNKNOWN/COPY_COVERAGE_UNPROVEN.
6. Universal absence requires explicit trusted coverage metadata. Ordinary
   participant record fields cannot inject the reserved _covers_all_copies flag.
   SQL absence lookup requires a matching independently linked resource/category
   and an explicit exhaustive snapshot scope. Generic/partial exports are not
   automatically exhaustive. Other clean states describe the known scopes; they
   do not independently certify full audit coverage or unknown copies.
7. Reported operation results never become direct resulting-state observations.
   A plausible mutation claim after a scope's last readback invalidates certainty
   (UNVERIFIED_MUTATION_AFTER_OBSERVATION), without proving either deletion or
   restoration. A later direct readback can supersede a claim for that scope.
   If other scopes remain older than the claim, uncertainty remains. Future claims
   are excluded; missing claim time yields explicit uncertainty. Same-time claims
   do not outweigh a direct point-in-time observation.
8. With no eligible observation, incomparable states or unresolved contradictions,
   retain UNKNOWN/CONFLICT internally. Unknown is not an allowed submission enum;
   strict export refuses those cases. Provisional candidate statuses and scoped
   checks are explicitly not certifications of aggregate deletion.

Known scoped states are carried forward only as the latest available evidence;
this is not a guarantee against unseen changes. Reported writes and source-scope
ambiguity can invalidate that assumption. Scope alignment and copy coverage must
be supplied by defensible evidence, not inferred from filenames or success flags.

## Executed edge-case acceptance

All 55 software tests passed, including 17 dedicated temporal tests plus existing
end-to-end audit/identity/replication tests. No failures, errors or skips.

- Future observation and late-captured earlier event both excluded.
- Later export of an older observation cannot defeat a newer actual observation.
- Equal-time contradictions survive differing quality scores and input order.
- Primary absence cannot clear replica presence, and vice versa.
- A later snapshot clears its own replica only; unknown coverage remains explicit.
- Single unscoped absence does not establish aggregate absence.
- Claimed delete success cannot establish absence; claimed restore success cannot
  establish presence. Both can invalidate older certainty pending readback.
- Repeated same-resource/user queries before, at and after a change return
  independent, repeatable cutoff results; direct recreation changes later state.
- SQL snapshot time is distinct from row-update and export times.
- A future trace identifier cannot link an earlier readback to a subject.
- A newer unknown scoped observation does not silently restore old certainty.

Commands:

```bash
PYTHONPATH=code python3 -m unittest discover -s code/tests -p test_temporal.py -v
python3 code/evaluation/verify.py
python3 code/evaluation/reproduce.py
```

Full predictor regression and cold-directory reproduction executed. The candidate
is byte-identical across warm/cold runs of this version. Stricter temporal guards
now diagnose 457 unresolved full cases; strict export exits 2 and writes no final
output.csv. Public status accuracy remains 29/32; exact row accuracy is 7/32.
The reduction from earlier exact-row scores reflects guarded scope/chronology
conclusions rather than hidden-label substitution. Current detailed metrics and
actual usage are in evaluation/evaluation_report.md and usage_report.md.

## Corrections and remaining risks

The previous ledger discarded lower-quality contradictory observations and used
lexical tie-breaking as though it resolved truth. It could conflate collector
origins, use export time for snapshot state, and retain old certainty after a
reported write. These paths now have explicit uncertainty and tests. A first
permutation test also exposed unstable conflict reference order; sorting now
includes state. An earlier source-link test expected unqualified scoped absence;
it now verifies linkage while expecting the required coverage uncertainty.

Physical scope alignment, exhaustive copy coverage and unsupported state evidence
remain unresolved in many real cases. The engine deliberately does not invent
these facts. The milestone exit criterion is met for the repeatable temporal and
replication acceptance tests; full submission readiness remains blocked.
