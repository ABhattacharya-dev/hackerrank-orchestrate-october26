# GhostGraph architecture and decisions

## Pipeline

Participant CSV/manifest → six read-only format adapters → immutable observations
and strong-identifier indexes → case-specific identity/resource ledger → supplied
policy and dependency planning → deterministic serializer → independent evaluator.

`ghostgraph/evidence.py` retains public IDs, locators, availability, event time,
scope and extracted fields. `identity.py` excludes later snapshots/audits and never
matches names. `engine.py` separates claims from observed state, preserves physical
replicas and emits only grounded steps. `contract.py` defines every official
operation/state pair and validates IDs, citations, cutoffs and order.

## ADR 001 — Local discriminative AI (2026-10-24)

No external model API credential is injected; scikit-learn is available. Use a
real supervised word/character TF-IDF/logistic regression classifier for multilingual
deletion authorization. Independently authored training data and the task prompt
are in `ghostgraph/intent.py`; no sample answer labels or dataset requests train
the model. Train deterministically from auditable source, then execute inference
on requests. This eliminates network/API cost and unsafe serialized models.
It is a small ML classifier, not a foundation model: semantic generalization and
negation require adversarial testing. Experiments exposed regressions in a pure
classifier when balancing portability and deletion-audit wording. The final
hybrid uses generic deterministic guards for explicit English consent, denial,
and access-only scope; the learned model still executes and decides multilingual
or implicit intent. Diagnostics expose both probability and decision source.
No case ID or public answer label selects a prediction. A future provider integration must beat
measured errors and justify credentials, latency, token cost and nondeterminism.

## ADR 002 — Proof ledger rather than graph infrastructure (2026-10-24)

The dataset is small enough for indexed Python objects and temporary in-memory
SQLite. A graph server or embedding store would add deployment and retrieval
uncertainty without established value. Keep identity/resource/process edges as
explicit provenance-bearing relationships. Parse once; filter at each cutoff.

## ADR 003 — Preserve uncertainty and disclose dataset gaps (2026-10-24)

Some sample expected resources have no eligible subject link in supplied data.
For example `account_001` appears only in a worker claim without a subject;
`analytics_901` is anonymous in the supplied JSON and its worker claim also omits
the subject. Numeric suffixes and sample labels are not lawful linkage evidence.
Do not add those mappings to the predictor. Strict mode must refuse unresolved
results. An explicitly requested candidate mode can expose provisional decisions
and diagnostics, but cannot be called a fully verified submission. Missing
retained records and expired retention have no general official repair operation;
surface those gaps instead of inventing one.

## ADR 004 — SQL and source scope (2026-10-24)

Run supplied SQL only in isolated in-memory SQLite. Deny attach/detach, external
functions and pragmas except the supplied `foreign_keys=ON`; bound VM execution.
An empty exported table is still a processed snapshot, not a parser failure.
Infer absence only for an independently linked resource in an explicit compatible
exhaustive table, never an empty keyword search or unrelated generic JSON bundle.
Preserve replica copies even when primary state differs.

## ADR 005 — Official serialization (2026-10-24)

Sort phases, then listed operation rank, then system/resource IDs exactly as the
problem statement requires. Flow/restore controls consequently precede record
modification. Maintain dependency explanations separately; report any conflict
between lexical serialization and a more specific downstream-before-source rule.
Never change submitted array order to an undocumented topological order.

## ADR 006 — Keep candidate output distinct (2026-10-24)

Two directly diagnosed state gaps are: a retained-reference screenshot lacks
the fields needed to establish redaction (`case_46`), and a backup browser does
not show restore authorization (`case_55`). A worker claim or unrelated restore
history cannot fill those gaps. Strict mode refuses final output. Candidate mode
writes `output.candidate.csv` plus explicit diagnostics; it is not submission
readiness. A later coverage audit also found 334 cases without a linked primary
profile proof. The current full run has 335 distinct unresolved cases, including
these coverage gaps and the reference/restore uncertainties (some overlap).
A retained audit record alone cannot establish primary-account deletion; the
strict guard now enforces that obligation. Provisional assessments preserve
partial supported verification steps for evaluation but cannot pass strict
export. This preserves the distinction between safe unknowns and supported
findings, instead of manufacturing an ACTIVE state or treating missing fields as
proof of redaction.

## ADR 007 — Measured performance and explainability (2026-10-24)

Cache the identity index separately for each distinct cutoff. The supplied full
set has 72 cutoff values; rebuilding it for all 518 requests took about 18 seconds.
Caching reduced observed runtime to roughly four seconds with warm OCR caches.
Decision diagnostics preserve each resource's direct identifier/catalog/source
reference linkage and state proof. Follow explicit `source_resource_id` edges,
never resource-number conventions. Immutable evidence is reused across cases;
verdicts are not.

## ADR 008 — Identity ambiguity and reassigned resources (2026-10-24)

A historical alias remains useful for finding ghost data after an account change;
discarding it merely because it is no longer current would lose stale copies.
Conversely, an alias known to multiple subjects is not a unique link. Exclude
shared aliases from automatic linkage, preserve ambiguity when the request
identifier itself has multiple owners, and prioritize explicit stable subject
references. A latest observation assigning a resource to another stable subject
creates an unresolved RESOURCE_IDENTITY_CHANGED condition; do not delete a
different customer's record or carry former ownership forward silently. These
rules have independent regression tests. Exact identifier-ownership intervals
where source data supplies no transition bounds remain unknown; no dates are
invented to fill them.

## Reproducibility and security

Source data is read-only. Extraction caches live in ignored `.ghostgraph/`, keyed
by file hash. No participant data or extraction caches enter `code.zip`. Hash all
inputs, retain actual run configuration and report model calls/cost honestly.
No model API tokens are used by the local classifier. No real deletion actions
are implemented. Evidence text is data and cannot execute prompts or commands.

## ADR 009 — explicit temporal uncertainty

Milestone 3 replaces parser-quality/lexical truth selection with a scope-preserving bitemporal engine. Direct equal-time conflicts remain conflicts, absence is scoped unless trusted coverage is explicit, collector origins are not physical replica identities, snapshot time is distinct from export/update time, and later reported mutations invalidate certainty without establishing their claimed result. Future trace context cannot backdate subject linkage. See TEMPORAL.md for tested rules. Current diagnosed full-case blockers are 457; earlier counts in historical ADRs are superseded by this stricter version.

## ADR 010 — conditional policy and separate execution graph

PolicyEngine evaluates supplied conditions with true/false/unknown applicability and no destructive fallback. Every grounded resource has an obligation ledger, including unresolved cases. Retained archives have independent existence and restore-control obligations. Historical process claims cannot imply current activity; unresolved live risks block record execution. A separate dependency graph retains downstream-before-source constraints while the CSV serializer preserves official order; conflicts are explicit strict-export blockers. POLICY.md records the executed acceptance. Current diagnosed full-case blockers are 490, superseding earlier historical counts; lower provisional metrics are disclosed.

## ADR 011 — strict plan completeness separate from candidate grammar

Centralize decisions, obligation checks, deduplication and canonical ordering in
a deterministic planner. Reject contradictory goals even for partial candidates.
Future verification may test grounded required policy goals but never stand in
for missing findings, unsupported actions or observed COMPLETE proofs. Explicit
partial mode remains diagnostic. Strict sample validation detects eight blocked
cases, so source packaging does not imply milestone acceptance. See PLANNING.md.

## ADR 012 — measure AI coverage and avoid redundant inference

A four-arm experiment separates deterministic scope, raw learned inference,
guarded eager and guarded selective decisions. Selective routing preserves guarded
outcomes while skipping inference for explicit consent/scope. Normalize cache keys
and return isolated responses. Public intent coverage increases from 28/32 rule-only
to 32/32 guarded selective; the prior hybrid already had that accuracy, so this is
a call-count optimization (375 to 5 full-run calls), not an audit-accuracy gain.
Keep temporal/policy/serialization deterministic. Reject the tested document-role
change because it adds errors and lacks stronger evidence. Measured missing
resource/proof coverage remains the next correctness priority; do not let a
successful AI ablation conceal structural blockers. See OPTIMIZATION.md.

## ADR 013 — physical SQL identity and strict full-run acceptance

A new independent same-table replica scenario failed because table name alone
collapsed explicit physical copies into one scope. Preserve an optional explicit
snapshot_scope.database_id with the table, including exhaustive-table absence;
reject ambiguous duplicate system declarations instead of choosing arbitrarily.
Do not guess physical identity from filenames. Existing dataset output bytes are
unchanged. Full acceptance now accumulates every strict structural violation for
all 518 rows, checks internal citation provenance, and attempts real root strict
export while preserving a prior destination on failure. There are 98 structurally
blocked rows and 490 semantic gaps; a passing test suite or a 518-row candidate
does not satisfy final publication. See ADVERSARIAL.md and full_dataset_report.md.

## ADR 014 — recovery: prediction is separate from certification

Historical executions reproduced 9, 7 and 1 exact rows for 34465f9, cded062 and
ee0914f respectively. Conditional-policy suppression caused most lost recall.
PredictionAuditor/PredictionPolicy retain uncertainty but use known scoped
observations and conservative policy applicability inferences. Defaults and
certification tests remain unchanged. False conditions, future captures, explicit
replicas, conflicts and foreign identities remain protected. Prediction export
validates the official step contract independently of certification obligations.
A malformed candidate is never silently renamed output.csv. Recovery restores
9 exact rows, but cannot legitimately ground the last full-case restore state;
that single-case failure remains explicit. See evaluation/recovery_report.md.

## ADR 015 — selected-target restore capability is a prediction inference

A target's own prior drill, checksum/path/retention details and live same-domain
recovery console support a recreation-risk prediction when eligible catalog links
the target subject. Inventory or other targets' successful restores alone do not.
Infer only in prediction mode, annotate derivation and catalog availability; never
backdate future evidence or override an explicit block/disabled service. Strict
certification remains unchanged. Cold prediction export is byte-identical with
zero structural violations; this does not prove hidden correctness or exact
archive-specific authorization. See evaluation/evaluation_report.md.

## ADR 016 — freeze audit corrects drill chronology

The March 29 drill precedes the selected archive’s April 26 creation. It cannot
prove a drill of that archive; ADR 015 and the original console inference
overstated this. Require creation chronology before labeling a target drill.
An earlier drill is historical context only. The prediction is retained on the
separate, explicitly uncertain basis of a selected checksum-verified archive
with path/retention details in the same live production recovery domain with
applicable restore-request controls and eligible catalog ownership. Authorization
is not directly observed. Without those controls, an older drill supplies no
active-risk inference. The independent chronology test verifies both outcomes.
All 115 tests pass; full output remains byte-identical to b513080.


## V5 experimental authorization safety

Objective: reduce false authorization without changing competition output. Deliverables: consent-layer wrapper, pre-authored probes, failure analysis and reproducible evaluation. Dependencies: existing local sklearn model and participant-facing data. Acceptance: complete regression, baseline public metrics and byte-identical 518 predictions with zero full structural errors. Failures: neutral follow-up conditions, own-account modifier attribution and sample-only completion-audit deferrals; corrected through explicit clause/request scope. Actual results and remaining uncertainty are in research/v5_report.md and v5_results.md. Production artifacts and frozen tags are preserved; no automatic merge.


## V5.1 production readiness

Objective: eliminate the pending-consent CLI contract failure without changing the competition CSV. Deliverables: production authorization module, compatibility import, typed classifier uncertainty, independently authored CLI fixtures, slimmed proposed source package and three-source review. Dependencies: unchanged learned model/evidence pipeline and pinned local runtime; no paid key. Acceptance: retain144 existing tests, pass12 new tests, preserve all32 sample outputs and518 full rows, official full validation, fresh environment/cold-cache/source/ZIP reproduction. Actual source results:156 tests pass, three versions reproduce the same518 rows, no full structural errors. Initial novel-preface miss corrected without changing expectations; acceptance script's symlink resolution initially bypassed the intended virtualenv and was corrected to preserve the executable path and verify sys.prefix. Pending consent is not current authorization; true classifier uncertainty blocks export and authorized ownership ambiguity remains an evidence blocker. Remaining risks: bounded grammar/languages, incomplete evidence, no universal consent inference or certification success. Detailed measurements and final package acceptance are in evaluation/v51_review.md and proposals/v51_checksums.md. No automatic merge or frozen-artifact replacement.
