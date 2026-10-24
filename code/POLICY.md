# Milestone 4 — policy, proof obligations and resurrection risk

## Objective and implementation

PolicyEngine reads all 15 rules from dataset/deletion_rules.csv. Both action and
condition are evaluated; an unknown condition never authorizes a destructive
fallback. Recognized conditions have explicit deterministic interpreters. Changed
or unsupported condition text is diagnosed, rather than silently receiving old
semantics. Missing, malformed or expired retention facts do not create DELETE
permission. DATA_FLOW controls additionally follow the root/problem contract,
because the CSV does not define a DATA_FLOW category.

The per-case obligation_ledger includes every grounded resource key, even when
its state or policy applicability is unresolved:

- identity_linkage and supporting public source references;
- category/source, rule_id, condition, applicability and raw policy_action;
- condition_facts with values and source locators, including catalog exclusivity;
- required_state, observed_state and the available scoped witness state;
- remediation_required (true, false or unknown), verification_obligations;
- preservation restrictions and explicit uncertainty/failure reasons.

Raw policy_action is the CSV declaration; treatment is the currently supported
applicable strategy, or null when facts are insufficient. Conditional obligations
remain unresolved until supported. Preserving a record temporarily while policy
is unknown is not certification of deletion or permanent retention permission.

## Supplied-category coverage

| Categories | Required treatment / condition facts |
| --- | --- |
| USER_PROFILE, SECONDARY_IDENTIFIER, SEARCH_INDEX_ENTRY, CACHE_ENTRY, USER_EXPORT, MARKETING_PROFILE | DELETE under the supplied Always condition |
| SUPPORT_MESSAGE | REDACT shared context, established by shared_context or supplied order reference; preserve shared conversation and other subjects' identifiers |
| SUPPORT_ATTACHMENT | DELETE only with explicit exclusivity/subject_count=1 or grounded catalog statement; unknown/multiple ownership cannot authorize deletion |
| ANALYTICS_PROFILE, PRODUCT_TELEMETRY | ANONYMIZE attributable records; verify already-anonymous records instead of dropping the obligation |
| EMAIL_DELIVERY_LOG | REDACT supplied subject-email presence or an actual email matching grounded subject identifiers; verify already-redacted state |
| SECURITY_AUDIT_LOG | RETAIN within a supplied retention window; end bound is inclusive; unknown/expired window has no inferred DELETE fallback |
| LEGAL_HOLD_RECORD | RETAIN with active-hold/window evidence; inactive/expired/unknown conditions require further policy resolution |
| BACKUP_ARCHIVE | RETAIN archive and separately block/verify restore access; known BLOCKED establishes blocking capability, otherwise explicit capability facts are required |
| ACCOUNT_TOMBSTONE | REDACT when account deletion/reference requirement is established; preserve stable internal reference and required record links |

A clean label cannot overrule exposed stored identifiers: purported ANONYMIZED
analytics with an email/hash/user reference, or REDACTED tombstones with prohibited
fields, produce POLICY_STATE_FACT_CONFLICT. Query/lookup subject metadata alone
is not treated as stored analytics attribution. Unsupported condition facts stay
unknown; ordinary categorical labels are not used to invent missing legal periods,
exclusive ownership or reference requirements.

Retained-record absence is an unmet verification obligation, not authorization to
invent a repair operation or delete other retained records. Backup verification
requires both VERIFY_RECORD_PRESENT and VERIFY_RESTORE_BLOCKED. A restore block
is not proof that archive data remains available: archive_present evidence is
checked independently. Stable-reference tombstones are never deleted as a
substitute for removing prohibited identifiers.

## Process state and dependencies

process_analysis uses eligible direct configuration observations and the temporal
engine's state at the cutoff. Sync/import/indexing/replication types are descriptive
labels from configuration fields; an event or connector name alone cannot prove
that the process is currently active. Historical activity is retained as claims,
separate from active_at_cutoff (true/false/unknown). A later disabled configuration
beats historical activation; a future activation does not affect an earlier audit.
Contradictory configuration/state is explicitly unknown. Restore risks use backup
controls; restore-related DATA_FLOW names still require disabling the process,
not an incorrectly selected archive control.

remediation_plan keeps an execution dependency graph separate from canonical CSV
serialization. Known flow/restore controls precede record changes. Explicit
source_resource_id/upstream_resource_id/replica_of edges require downstream
changes before source changes. Cycles or unresolved active-process preconditions
produce no claimed safe execution order. If a valid topological execution order
conflicts with mandated operation/system/resource sorting, the conflict is
recorded and strict export blocks it; final candidate arrays retain the exact
mandated ordering. No real deletion or remediation is executed.

## Executed acceptance results

- All 76 software tests passed, zero failures/errors/skips.
- The dedicated policy acceptance runner passed 21 tests: all 15 supplied
  categories have positive-condition fixtures using the actual unmodified CSV.
- The actual sample run contains 80 obligation entries across 11 categories
  (10 CSV categories plus DATA_FLOW). Every category is recognized and every
  entry contains the required ledger fields; retained/tombstone DELETE strategies
  are forbidden. Dependencies were checked for every claimed execution order.
- End-to-end custom case: erase only account_1, preserve required security audit,
  legal hold, archive and compliant tombstone; disable flow, block restore, then
  delete the profile, with retained-presence and redaction verification steps.
- Adversarial checks cover unknown/expired/malformed retention, inclusive end
  bounds, multi-owner attachments, clean labels hiding identifiers, historical
  disabled processes, future activation, unmitigated restore preconditions,
  dependency cycles and canonical-order conflicts.
- Full 518-case candidate regression and strict refusal executed. Fresh source,
  dataset copy and empty extraction cache reproduced identical candidate bytes.

Commands:

```bash
python3 code/evaluation/policy_acceptance.py
python3 code/evaluation/verify.py
python3 code/evaluation/reproduce.py
```

Detailed per-case ledgers, condition facts and process plans remain in ignored
.ghostgraph/ diagnostics. They may contain participant identifiers and must not be
copied into source archives or conversation logs. POLICY.md and test fixtures are
submitted source-visible documentation.

## Failures corrected and remaining risks

Earlier category-only treatment did not prove applicability and could omit
retained-archive presence checks. Earlier test fixtures did not explicitly declare
exhaustive absence where their policy assertion needed it; the fixtures now state
that assumption rather than weakening the temporal engine. Configuration booleans
from logfmt/SQLite are handled; actual source category, not a process name,
selects its required control. Active unresolved risks block record execution.

The stricter current ledger diagnoses 490 unresolved full cases. Many predicates
remain unknown in the present extraction; further grounded context may resolve
them. This is not proof that those inputs are defective. Public candidate status
accuracy is 28/32 (87.5%), and exact rows are 1/32 (3.125%); these are regression
measurements, not submission readiness. No sample labels feed policy decisions.
The milestone's category-coverage and retained-data safety criteria pass; the
full competition submission remains blocked.
