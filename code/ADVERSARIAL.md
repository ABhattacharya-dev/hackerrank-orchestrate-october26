# Milestone 7: adversarial testing and full-dataset acceptance

Objective: add genuinely new parser-to-CLI adversarial scenarios, exercise all
518 requests, validate every row and citation, and publish root output.csv only
when the complete contract is satisfied. Dependencies: earlier ingestion,
identity, temporal, policy, planner and exact output contract. Prior M5/M6
acceptance failures remain unresolved; this work does not bypass those gates.

## Concrete deliverables and acceptance tests

`tests/test_adversarial_pipeline.py` creates independent temporary datasets,
copies only the supplied policy, and runs the actual CLI pipeline through CSV,
JSON and SQL ingestion. No supplied evidence is mutated. These are new scenarios
with physical database identity, alias-cutoff transitions, real policy conditions,
export rejection and source/citation assertions; they are not renamed old fixtures.

1. Empty primary and populated regional replica use the **same SQL table name**
   but explicit different database IDs. The connector is still importing. The
   primary-success claim cannot clear the replica. Expected: INCOMPLETE, disable
   flow before delete, replica snapshot citation and two distinct copy scopes.
2. Historical email changes at the inclusive cutoff; conflicting observations
   arrive afterward, and a still-later capture describes an earlier absence.
   Expected: correct old/new alias lookup, earlier presence retained, equal-time
   conflict blocks export, later capture excluded from earlier proofs.
3. A fully redacted account tombstone, retained security/legal records, retained
   archive and active unsafe restore with explicit block capability. Expected:
   block restore only, preserve records, verify retained presence and redaction.
4. Repeated subject before/after direct-identifier redaction, with case IDs forcing
   reverse temporal execution order. Expected: earlier INCOMPLETE, later COMPLETE;
   reversing request input order cannot change results or contaminate caches.
5. Two customers share a historical address. Expected: ambiguous shared lookup
   plans no deletion; a unique grounded alias touches only its own account.
6. New French, Spanish and Korean negation requests with live personal data.
   Expected: NOT_APPLICABLE, no steps, no deletion authorized by mere data presence.
7. A manifest entry points to a missing artifact. Expected: documented MissingFile
   and strict refusal without creating final output.

The valid synthetic runs pass strict contract and source registry checks and
internal provenance/cutoff verification. Intentionally conflicting, ambiguous or
missing-evidence runs must refuse final output; these negative tests do not
contribute fabricated valid rows to the competition output.

## Actual results, failures and corrections

All seven new end-to-end tests passed; the full software regression ran **104
tests with zero failures, errors or skips**. Initially the replica test failed:
the adapter treated identical table names on two explicit databases as one scope,
turning valid replica presence into a conflict. It now uses an explicit
snapshot_scope.database_id together with the table and preserves that same scope
when deriving exhaustive-table absence. No physical identity is guessed from
filenames. Ambiguous duplicate snapshot system declarations fail detectably.
Existing participant evidence has no database_id extension, and its candidate
bytes remain unchanged. The correction is driven by new independent evidence
semantics, not public case labels.

`evaluation/full_acceptance.py` reruns software/public/full checks, checks the
exact CSV header, all 518 case keys, every strict step contract and citation,
and attempts strict publication to the real root output.csv path. It preserves
any existing destination on failure. It writes full_dataset_report.md with every
structural blocker and real application-run usage; JSON diagnostics remain ignored.

The actual full run produced 518 candidate rows with exact keys and ordering;
**420 rows pass strict structure, 98 fail with 171 violations**. The failures are
73 empty unsupported plans, 73 INCOMPLETE-without-finding errors for those same
cases, and 25 findings missing a full supported remedy/check sequence. All 729
cited steps match internal eligible ledger provenance. This does not certify
semantic coverage: **490 cases still have unresolved proof obligations**.
The strict root output.csv attempt therefore failed without writing a final file.
Cold extraction from a fresh source/data directory reproduces the candidate.

Final candidate usage: local scikit-learn hybrid word/character TF-IDF logistic
regression v5-selective, five learned inference calls, 370 deterministic scope
decisions, 143 classification cache hits for 518 requests. API input/output tokens
are zero; token units do not apply to these local components. Paid model calls are
zero, API cost USD 0.00; no paid model tariff applies. Local compute/storage is
unpriced, not asserted free. Validation-phase counts and OCR/PDF cache behavior
are separately recorded in full_dataset_report.md and usage_report.md. No
engineering-assistant token counts or runtime model identifiers are invented.

**Exit criterion NOT MET:** no valid complete root output.csv is available.
The provisional output.candidate.csv is retained and must not be relabeled.
Remaining risks are missing subject/resource links, policy condition facts,
copy coverage, unresolved capture/scope relationships and unsupported restore
capabilities. Missing evidence cannot be turned into fabricated findings or a
claim of COMPLETE to satisfy the CSV row count.

## Reproduce

```bash
python3 code/evaluation/full_acceptance.py
python3 code/evaluation/ai_ablation.py
python3 code/evaluation/planning_acceptance.py
python3 code/evaluation/reproduce.py
python3 code/evaluation/optimization_report.py
python3 code/evaluation/write_reports.py
python3 code/package.py
```

Full acceptance returns 2 for the documented blockers, 1 for software-test failure,
and 0 only after successful strict root export with zero violations and unresolved
cases. The Markdown reports contain actual results for source-code review.
