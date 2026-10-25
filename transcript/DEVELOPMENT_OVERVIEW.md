# GhostGraph: development overview

## Executive overview

GhostGraph audits whether a customer authorized deletion and whether the relevant data reached its required state at a case-specific cutoff. It separates workflow claims from observed records, discovers surviving copies and recreation paths, preserves policy-required records, and generates ordered findings, remediation plans and verification checks.

The user established the objectives, evidence restrictions, acceptance criteria and release decisions. The agent implemented the software and selected concrete algorithms: indexed Python evidence objects, isolated SQLite snapshot parsing, local word/character TF-IDF logistic regression for selective intent inference, historical identifier resolution, a temporal resource ledger, CSV-driven policy evaluation and deterministic serialization. It generates plans; it never executes external deletions.

This retrospective covers the original recorded development and later research. Production remains `7a18c2e`, tagged `submission-v5.1`. V6 occurred afterward and was rejected; it is not part of the released implementation.

## Engineering methodology

The user's delegation was explicit:

> **You own the engineering decisions. I own the project objectives.**

The agent could choose libraries, revise architecture and execute milestones autonomously, while the user specified invariants and intervened when evidence or measured performance contradicted progress claims. This was delegation of implementation, not attribution of agent-written code to the user.

Acceptance required executable tests, public-sample comparisons, independent counterexamples and reproducible artifacts. Passing software tests did not establish canonical accuracy. Source capture times, resource ownership and preservation obligations constrained inference. Experimental branches kept rejected changes separate; production promotion required explicit authorization. Public answers were evaluation fixtures, not training data or prediction lookups. Public and full request sets were evaluated separately. The [source index](MILESTONE_INDEX.md) supplies exact timestamps, original section headings and Git references for each grouping below.

## Development milestones

### 1. Requirements and the first runnable baseline

**Objective:** Turn the challenge into an executable, auditable system.

**User's technical direction:** Extend root instructions without replacing them; prioritize evidence, temporal correctness and exact outputs over presentation.

**Agent implementation:** Created `code/AGENTS.md`, then implemented the CLI, local classifier, evidence adapters, ledger, evaluator and packaging.

**Technical decisions:** The agent chose lightweight Python and auditable local ML rather than infrastructure or a credential-dependent service.

**Failure analysis and corrections:** Empty starter entry points initially exited successfully without doing work. Subsequent implementation required real assertions; early normalization, document-boundary and classifier problems were corrected.

**Measured outcome:** The logged first implementation passed 26 tests and matched 9/32 public rows, but strict export refused 335 unresolved cases. It was provisional, not submission-ready.

**Source references:** [“Establish GhostGraph instructions,” 2026-10-24T17:51:18.554285+00:00](../log.txt#L36); [implementation results, 18:35:35.208860+00:00](../log.txt#L302); commit `34465f9`.

### 2. Inventory, ingestion and provenance

**Objective:** Parse the global evidence once without losing source identity.

**User's technical direction:** Inspect actual schemas, policies, snapshots and all public answers; make every manifest outcome detectable.

**Agent implementation:** Added inventory documentation, explicit ingestion outcomes, transactional rollback and indexed observations with file/activity/audit IDs, locators, capture times and content hashes.

**Technical decisions:** Structured parsers handled CSV, SQL and JSON; text extraction/OCR handled documents and images. Semantic vision remained an optional review adapter.

**Failure analysis and corrections:** Malformed rows exposed incomplete exception handling; partial facts now rolled back rather than appearing complete.

**Measured outcome:** All 94 artifacts were processed: 89 processed, five unresolved, zero parser failures and 2,906 traceable observations; 32 tests passed. Hosted vision was not executed.

**Source references:** [“Milestone 1 ingestion and provenance,” 2026-10-24T18:47:44.681627+00:00](../log.txt#L404); commit `f3ee29d`; [ingestion report](../code/INGESTION.md).

### 3. Consent and historical identity

**Objective:** Identify authorized requests and their defensible subject relationships.

**User's technical direction:** Distinguish deletion from export, correction, marketing and refusal; resolve changed identifiers without cross-user contamination.

**Agent implementation:** Combined learned intent inference with scope guards and built cutoff-specific identity indexes from snapshots, audit transitions, catalogs and structured records.

**Technical decisions:** Full identifiers and stable references could support links; names, suffixes and document-wide co-occurrence could not. Shared aliases remained ambiguous.

**Failure analysis and corrections:** Cancellation wording and foreign dependency references could incorrectly authorize or propagate a plan; guards and provenance checks addressed these paths.

**Measured outcome:** All 32 public intents and subject resolutions passed; 38 tests passed. Because public samples contained no non-deletion cases, this did not establish negative-intent robustness.

**Source references:** [“Milestone 2 intent and historical identity,” 2026-10-24T18:55:01.214603+00:00](../log.txt#L439); commit `1530f59`; [identity acceptance](../code/INTENT_IDENTITY.md).

### 4. Time and replica reconstruction

**Objective:** Reconstruct resource state independently at each `audit_at`.

**User's technical direction:** Exclude future evidence, preserve replicas and distinguish successful operation claims from actual absence.

**Agent implementation:** Added a reducer separating observation time from availability, maintaining scoped histories, equal-time conflicts and uncertainty explanations.

**Technical decisions:** Parser quality could not override contradictions; collector origins were not automatically physical replicas.

**Failure analysis and corrections:** Snapshot precedence and future trace-link leakage required correction. Stricter coverage rules also suppressed previously emitted verification steps.

**Measured outcome:** All 55 tests passed, including 17 temporal tests. Historical comparison nevertheless showed exact rows falling from 9/32 to 7/32 and unresolved full cases rising to 457.

**Source references:** [“Milestone 3 temporal reconstruction,” 2026-10-24T19:08:45.462115+00:00](../log.txt#L475); commit `cded062`; [recovery comparison](../code/evaluation/recovery_report.md).

### 5. Conditional policy and resurrection risk

**Objective:** Apply deletion obligations while preserving required records.

**User's technical direction:** Drive treatment from `deletion_rules.csv`, including retained security/legal records, tombstones and unsafe restore paths.

**Agent implementation:** Built conditional policy evaluation, per-resource obligation ledgers, process histories and dependency-aware internal remediation plans.

**Technical decisions:** DELETE, REDACT, ANONYMIZE and RETAIN had distinct required states; execution dependencies remained separate from mandated CSV ordering.

**Failure analysis and corrections:** Missing predicate facts blocked many operations. Later recovery traced substantial recall loss to treating unavailable condition metadata as grounds for globally suppressing otherwise supported predictions.

**Measured outcome:** Seventy-six tests passed, with focused coverage of all 15 policy categories. Public exact rows declined to 1/32; 490 full cases remained unresolved.

**Source references:** [“Milestone 4 policy and resurrection risk,” 2026-10-24T19:43:10.941433+00:00](../log.txt#L515); commit `ee0914f`; [policy documentation](../code/POLICY.md).

### 6. Deterministic planning, AI ablations and adversarial acceptance

**Objective:** Generate exact plans and test the complete pipeline.

**User's technical direction:** Enforce operation/state enums, citations, ordering and consecutive numbering; measure errors and create independent scenarios.

**Agent implementation:** Centralized planning, contradiction checks and evaluation alignment. Compared rule-only, raw ML, guarded eager and selective inference; added on-disk adversarial CLI fixtures.

**Technical decisions:** Deterministic code constructed JSON. Selective routing reduced full-run learned calls from 375 to five without changing candidate bytes.

**Failure analysis and corrections:** A document-role experiment added three erroneous operations and was reverted. A replica fixture exposed merged physical databases sharing table names; explicit database IDs corrected scope handling.

**Measured outcome:** Tests increased through 90, 97 and 104; exact rows reached only 2/32. Full validation still found 171 violations across 98 cases, so publication remained blocked.

**Source references:** [planner acceptance, 2026-10-24T20:58:35.663163+00:00](../log.txt#L559); [full-run acceptance, 2026-10-25T00:15:30.958488+00:00](../log.txt#L656); commits `f54c83e`, `e2aa599`, `a0437e3`.

### 7. Historical regression recovery

**Objective:** Explain declining canonical coverage instead of assuming newer code was better.

**User's technical direction:**

> Do not assume newer code is automatically better.

**Agent implementation:** Reproduced historical versions in isolated comparison copies, traced lost operations and separated competition prediction from strict certification.

**Technical decisions:** Official schema requirements remained mandatory; extra certification assumptions stayed diagnostic rather than suppressing every prediction. Eligible scoped observations and conservative preservation inferences were restored.

**Failure analysis and corrections:** Conditional-policy suppression and universal copy-coverage demands explained much of the loss. Future evidence, explicit conflicts and foreign identities remained excluded.

**Measured outcome:** With 107 tests passing, exact rows recovered from 2 to 9/32 and matching steps from 111 to 159/193. Full structural errors fell from 171 to two; 490 certification uncertainties remained.

**Source references:** [“Accuracy recovery V2,” 2026-10-25T00:32:08.341047+00:00](../log.txt#L698); commit `1146bc7`; [regression report](../code/evaluation/recovery_report.md).

### 8. Restore blocker and factual freeze audit

**Objective:** Resolve the last submission blocker without fabricating restore state.

**User's technical direction:** Inspect the actual console, reject future restore events and distinguish inventory from executable restoration capability. The subsequent user audit challenged a drill preceding archive creation.

**Agent implementation:** Added a prediction-only, provenance-bearing restore-risk inference and counterfactual tests.

**Technical decisions:** Selected-archive details, applicable live controls and eligible catalog linkage supported an uncertain operational-domain prediction—not directly observed archive authorization.

**Failure analysis and corrections:** The initial summary incorrectly described the March 29 drill as target-specific despite April 26 archive creation. The freeze audit corrected this and added chronology regression coverage.

**Measured outcome:** Tests rose from 114 to 115; 518 rows passed full structural validation. Correcting the reasoning left CSV bytes and 9/32 exact public performance unchanged.

**Source references:** [restore blocker, 2026-10-25T00:45:03.259574+00:00](../log.txt#L1010); [freeze audit, 00:54:55.921539+00:00](../log.txt#L1263); commits `b513080`, `3b942ac`; architecture ADR016.

### 9. V3/V4 linkage and original-source research

**Objective:** Recover missing evidence without importing weak relationships.

**User's technical direction:** Use isolated experiments, inspect original sources and require measurable generalizable improvement.

**Agent implementation:** Tested temporal candidates, structured relationships and scoped original-JSON validation. V4 audited 34 missing operations and compared the frozen intent model with LinearSVC.

**Technical decisions:** Time proximity proposed candidates, not ownership. Model assertions could not validate themselves or bypass source scope and cutoff checks.

**Failure analysis and corrections:** A validator briefly created false novelty by misassigning a legal-service scope. Correcting it left zero novel facts. Hosted model review was NOT RUN.

**Measured outcome:** V3/V4 left prediction bytes unchanged and were rejected. Their separate research suites passed 130/133 tests. Both intent estimators scored 21/32 with 11 false authorizations, motivating authorization-specific work.

**Source references:** [V3, 2026-10-25T01:23:00.640758+00:00](../log.txt#L1370); [V4, 02:49:10.510640+00:00](../log.txt#L1703); commits `9e6c3e2`, `eb06bdc`; [V3 results](https://github.com/ABhattacharya-dev/hackerrank-orchestrate-october26/blob/9e6c3e2/code/research/results.md) and [V4 results](https://github.com/ABhattacharya-dev/hackerrank-orchestrate-october26/blob/eb06bdc/code/research/v4_experiment_results.md).

### 10. V5 authorization safety

**Objective:** Reduce false authorization while preserving competition output.

**User's technical direction:** Separate actual instructions from quotations, hypotheses, conditions and third-party requests; preserve separately authorized actions despite unrelated negation.

**Agent implementation:** Added a consent/speech-act layer over the unchanged learned classifier and authored development/prospective tests before implementation changes.

**Technical decisions:** Clause-level scope and requester attribution preceded learned fallback; diagnostics retained uncertainty.

**Failure analysis and corrections:** Blanket condition handling initially affected 144 full requests. Later public auditing found six erroneous deferrals despite unchanged full CSV bytes; continuation and retention-scope corrections restored public results.

**Measured outcome:** First held-out performance improved 25→39/40, with false authorizations 15→0 and one miss. A subsequent prospective set improved 11→24/24. Final 144 tests passed; later reruns were observed regression, not fresh held-out evidence.

**Source references:** [V5 implementation, recorded 2026-10-25T05:03:01.394444+00:00](../log.txt#L2129); commit `08e975b`; [detailed chronology](../code/research/v5_report.md).

### 11. V5.1 integration and authorized production promotion

**Objective:** Turn classifier safety into a valid end-to-end release.

**User's technical direction:**

> Do not automatically equate every unknown with INCOMPLETE.

**Agent implementation:** Reproduced the real CLI's invalid `INCOMPLETE,[]` consent result, moved authorization into the production package and added 12 integration tests.

**Technical decisions:** Unfulfilled or undecided consent maps to NOT_APPLICABLE with diagnostics; classifier uncertainty blocks export. Authorized ambiguous ownership remains an evidence problem.

**Failure analysis and corrections:** Novel sentence structure exposed another missed instruction. A verification helper also dereferenced the virtualenv executable into base Python; preserving its path and checking `sys.prefix` corrected the claimed environment test.

**Measured outcome:** All 156 tests passed with unchanged public/full predictions. After explicit user approval, selective promotion excluded superseded prototypes and proposal ZIPs; cold extracted-ZIP reproduction passed and `7a18c2e` was released.

**Source references:** [V5.1 repair, 2026-10-25T05:24:25.660861+00:00](../log.txt#L2324); [promotion, 05:44:27.916646+00:00](../log.txt#L2540); commits `4015ede`, `7a18c2e`; [release manifest](../release_manifest.md).

### 12. Post-release V6 assignment experiment

**Objective:** Test an external activity-assignment hypothesis without changing production.

**User's technical direction:**

> If the experiment increases raw step recall but relies on unjustified ownership, reject it.

**Agent implementation:** Reproduced the reviewer's 108 unique candidates and 57/57 grounded matches; tested uniqueness, collision rejection, ownership corroboration and placebo schedules.

**Technical decisions:** Worker outcomes never proved absence; eligible state evidence did not establish ownership. Future captures remained excluded.

**Failure analysis and corrections:** Two apparent gains were forbidden account-only COMPLETE upgrades and were blocked. Unrelated-singleton controls still defeated weak assignment; none of the 108 new targets had independent ownership corroboration.

**Measured outcome:** Guarded weak matching reached 10/32 exact and 165/193 steps, but the corroborated variant stayed at baseline. All 173 research tests passed; promotion was rejected. These tests are not the release's 156-test count.

**Source references:** [V6 final rejection, 2026-10-25T07:10:44.340402+00:00](../log.txt#L3019); commit `fcb820a`; [V6 results](../code/research/v6_assignment_results.md). These entries exist in the original pre-editorial log, after the production log ended.

## Final engineering decisions

Certification retained unresolved proof obligations; competition prediction exposed assumptions while independently enforcing the official output contract. Neither mode permits invented evidence. Deterministic JSON construction kept policy reasoning, citations, ordering and numbering outside unconstrained model output.

Ownership required source relationships rather than shared names, numeric suffixes or temporal uniqueness. Capture eligibility applied to identity inference as well as final citations. V5.1 was selected for demonstrated authorization robustness and valid integration, not higher CSV accuracy. V3/V4 offered no defensible prediction gain; V6's apparent gain depended on unsupported attribution. The validated release therefore remained frozen.

## Verified final results

The authoritative [release manifest](../release_manifest.md) identifies `7a18c2e` / `submission-v5.1`:

| Measure | Released result |
|---|---:|
| Sorted prediction rows | 518 |
| Full-dataset structural violations | 0 |
| Passing V5.1 software tests | 156 |
| Exact public rows | 9/32 |
| Correct public statuses | 29/32 |
| Exact matching canonical steps | 159/193 |
| Step precision / recall / F1 | 97.55% / 82.38% / 89.33% |
| Local learned inference calls / classification cache hits | 5 / 143 |
| Unresolved strict-certification cases | 490 |

The learned model genuinely participates; hosted API calls and API cost are zero. Local token units are inapplicable and CPU/OCR cost is unpriced. Six pre-existing sample-only structural errors remain distinct from the valid 518-row submission. Public regression metrics are not hidden evaluation scores or a certification pass.

## Limitations and provenance

This is an editorial retrospective, not an original conversation transcript. `log.txt` preserves verbatim user prompts but summarizes agent responses/actions; it is not a complete structured rollout. Engineering-runtime model identifiers were unavailable when logged; missing traces are not reconstructed. The application classifier and its measured usage are separately auditable.

V5 explicitly records late persistence: entry timestamps must not be treated as recovered task-start times. Superseded claims—especially restore chronology and intermediate sample regressions—remain visible rather than silently repaired in history. This editorial task neither reran evaluations nor regenerated submission/trace archives. The [source index](MILESTONE_INDEX.md) and [integrity audit](INTEGRITY_AUDIT.md) distinguish preserved production history, genuine later research and append-only documentation entries.
