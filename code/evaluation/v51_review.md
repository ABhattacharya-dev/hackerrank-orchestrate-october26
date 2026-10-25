> Historical candidate assessment, retained as development evidence. Production promotion and final acceptance are documented in `code/evaluation/release_report.md` and the root `release_manifest.md`; proposal paths below refer to the experimental branch.

# V5.1 production-readiness and Code ZIP promotion review

## Decision

Recommend V5.1 for a reviewed **Code ZIP-only promotion**, with source and extracted-archive acceptance verified; exact checksums are in proposals/v51_checksums.md. Do not merge or overwrite the protected artifacts automatically. There is no measured Output CSV accuracy gain. Protected reference: `3b942ac`, tag `submission-freeze-verified`; V5 reference: `08e975b`; proposed branch: `experiment/intent-safety-v5.1`.

## Reproduced blocker and official-contract interpretation

A fresh fictional CLI dataset supplied a directly linked present profile and this separate request: “If the replacement device arrives, erase my membership. It has not arrived; do not act yet.” V5 exited2 with `NO_SUPPORTED_STEPS` and `INCOMPLETE_WITHOUT_FINDING`, writing no CSV. The same real CLI now exits0 with `fictional_00,NOT_APPLICABLE,[]`; no policy finding is invented and no resource plan is generated. The internal result retains low-confidence/pending-consent flags, `CONSENT_UNRESOLVED` and `CONSENT_NOT_ESTABLISHED`.

The problem statement requires determining whether the person actually requested deletion before reconstructing evidence. NOT_APPLICABLE is for a request that does not presently authorize deletion; INCOMPLETE is for supported resource/policy findings plus remediation and future verification. The contract has no consent-pending status. The following is our explicit operational interpretation of that contract, not an official new rule or a claim that ambiguous language can always be resolved:

| Situation | Prediction behavior | Internal meaning |
|---|---|---|
| Explicit unfulfilled condition | NOT_APPLICABLE,[] | No current consent; condition/approval pending; re-evaluate when independently authorized |
| Hypothetical/informational/quoted instruction | NOT_APPLICABLE,[] | Not an actual current requester instruction |
| Claimed but unverified third-party authority | NOT_APPLICABLE,[] | Present authority is not established; representative claim is not proof |
| Explicit undecided/contradictory requester consent | NOT_APPLICABLE,[] | Current consent unresolved, not permanent refusal |
| Classifier uncertainty about an unfamiliar instruction | Export blocked, existing destination preserved | CLASSIFICATION_UNRESOLVED; no guessed consent or guessed non-applicability |
| Authorized deletion with ambiguous resource ownership | Evidence diagnostics retained; unsupported export blocked | Authorization stays true; do not relabel non-applicable or invent findings |
| Authorized deletion and proven remaining profile | INCOMPLETE with finding/remediation/verification | Actual evidence-backed resource violation |

A pending semantic-consent row is a non-authorization decision at this evaluation time, not permission to execute deletion later. Strict certification remains more conservative and can reject unresolved consent diagnostics. Genuine model ambiguity, provider failure and resource uncertainty are not silently mapped to NOT_APPLICABLE. A truly authorized case with no representable supported finding/verification is still a known representational limitation: ordinary export fails rather than fabricate a compliant row. We have not solved all incomplete-evidence cases.

## Production integration

Runtime consent gates now live in `code/ghostgraph/authorization.py`. `code/main.py` imports that production module; `code/research/v5_intent.py` is a compatibility import. Production code imports no research modules and the normal CLI is tested with the entire research directory removed. The unchanged local learned classifier and authored training corpus stay in `ghostgraph/intent.py`. No changes were made to evidence parsing, identity, temporal reconstruction, supplied policy or planning logic. Engine edits are limited to authorization handling and a typed classifier-uncertainty failure; CLI edits collect those failures in `full_blocked_cases.json` before refusing export.

A new pre-authored sentence-structure test initially failed: an actual instruction after a topical preface was deferred. The expected authorization was preserved. A bounded grammatical preface rule now handles `regarding`/`concerning`/`as for`/`with regard or respect to`, while full-clause refusal, conditional, quotation and ownership checks still apply. Independent counterexamples test those scopes. No weights, thresholds, sample IDs or probe-string lookup were added. This correction used test feedback and is not fresh held-out validation.

## Software and independent CLI tests

Frozen source:115 tests pass. V5 source:144 tests pass. V5.1 retains those144 tests unchanged and adds12, for156 passing tests. Historical tests were rerun using their actual Git-exported source trees, not simulated class substitutions.

The new fixture is entirely fictional, with explicit user/email linkage, a directly observed profile and a real policy file. Nineteen ordinary CLI request texts cover six authorized actions and thirteen requests without present authority. Every exported row is checked using the official checker, including phase/operation/state, numbering, resource registry, evidence existence and cutoff, remediation/verification pairing and ordering. Authorized fixture plans assert exact operations, citations and resources. Additional tests cover blocked ambiguous identity, fault-injected classifier uncertainty with preservation of an existing output, and runtime import boundaries. Three foreign-language CLI examples include French/Japanese non-deletion and Spanish deletion; three examples do not establish broad language accuracy.

Acceptance does not consist only of classifier assertions: real subprocess CLI inference and serialization run against the fictional evidence. No new fixture string exactly overlaps the authored model-training corpus. Existing samples/V5 probes remain observed regression; the independent new test expectations were fixed before the integration correction and were not changed to fit output. The novel-preface failure and fix are disclosed above.

## Three-source competition regression

| Metric | Frozen | V5 | V5.1 |
|---|---:|---:|---:|
| exact public rows | 9 | 9 | 9 |
| correct public statuses | 29 | 29 | 29 |
| exact canonical steps | 159 | 159 | 159 |
| step_precision | 97.55% | 97.55% | 97.55% |
| step_recall | 82.38% | 82.38% | 82.38% |
| step_f1 | 89.33% | 89.33% | 89.33% |
| field_accuracy | 79.05% | 79.05% | 79.05% |
| canonical_evidence_accuracy | 78.67% | 78.67% | 78.67% |
| exact_sequence_accuracy | 28.12% | 28.12% | 28.12% |
| Full518 structural violations | 0 | 0 | 0 |
| Full rows changed vs protected CSV | 0 | 0 | 0 |
| Public sample rows changed | 0 | 0 | 0 |

The six pre-existing sample-only structural violations (unsupported empty predictions in three public cases) remain identical in all three source versions. They are not the submitted full518 rows. Do not claim zero violations for arbitrary/sample requests or strict certification success. All ten current NOT_APPLICABLE full requests remain unchanged. No hidden labels or hidden accuracy are claimed.

## Retained intent robustness

- development: frozen 14/24, V5.1 24/24; V5.1 false authorizations 0, misses 0. These are observed regression results.
- observed40: frozen 25/40, V5.1 40/40; V5.1 false authorizations 0, misses 0. These are observed regression results.
- observed24: frozen 11/24, V5.1 24/24; V5.1 false authorizations 0, misses 0. These are observed regression results.
- continuation16: frozen 10/16, V5.1 16/16; V5.1 false authorizations 0, misses 0. These are observed regression results.

Known V4 probes remain32/32 (frozen21/32). The honest first-held-out V5 result remains39/40, not the later observed40/40. Round-two prospective24 was24/24 before further public-regression changes. The V5 reports retain those chronology and confusion matrices; do not relabel any rerun as unseen.

## Qualitative assessment

These are engineering ratings, not numerical judge scores or hidden-accuracy estimates.

| Dimension | Frozen | V5 | V5.1 |
|---|---|---|---|
| Authorization safety | Weak on known adversarial consent probes | Substantially safer classifier; pending-consent CLI blocker | Improved end-to-end; explicit pending/model/ownership distinctions; bounded language limitations remain |
| Maintainability | Modular stable pipeline; broad intent guard | Runtime depends on research file; duplicate snapshots packaged | Production authorization module, thin compatibility shim, fewer archived implementations |
| Reproducibility | Verified frozen output | Verified full output and source ZIP | Three-source equality, fresh dependency environment, cold-cache/source/ZIP acceptance, runtime without research |
| Competition accuracy | 9/32 exact,29/32 statuses | Identical | Identical; no CSV score improvement claimed |
| Code ZIP readiness | Valid artifact with known intent weakness | Do not promote as-is: ambiguous-intent export bug | Recommended reviewed replacement after matching archive acceptance; no automatic promotion |

The proposed archive excludes three historical implementation snapshots plus their round-two runner. They remain in Git. Reports, useful fixed probes, final evaluator, new end-to-end tests and reproducible implementation are retained. More files/test counts are not themselves evidence of scoring improvement.

## Reproduction, usage and limitations

Fresh environment dependencies installed from the pinned requirements and `pip check` passed. Source CLI acceptance used Python prefix `/tmp/ghostgraph-v51-venv`. Fresh extraction-cache prediction took21.555s, with5 local learned calls,143 classification cache hits,11 Tesseract and4 pdftotext invocations. API keys/optional paid vision selectors were removed from the verification subprocess environment. Runtime without any research directory reproduced the same output.

Strict certification exits2 with490 unresolved cases and creates no certified output; this remains an evidence limitation. Classifier uncertainty can prevent a full export on new texts; it never fabricates findings. Regex speech-act parsing, multilingual coverage and unverified representative authority remain limited. Further blinded externally authored testing would improve confidence.

CSV SHA256: `61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891`. Protected ZIP SHA256: `a0547f21fad274cf6b85b8bf3d6a4a88535cef9950108dcc605bb71226e6ddad`. Runtime authorization source SHA256: `b1fa786858b2b158dd0578252c3ffac4795e0c64a4b0316d01fee5cab2fdbdd9`. The proposed ZIP checksum is recorded outside its own archive in proposals/v51_checksums.md to avoid self-reference.

Hosted structured session traces and authoritative exact engineering-model metadata remain unavailable locally. The actual append-only root transcript is preserved; no trace or model identifier was fabricated. This limits transcript completeness, not the verified runtime code package.

Commands actually executed: Git-source three-arm comparison, all original/new unit suites, `python3 -m venv`, pinned `pip install`, `pip check`, real conditional CLI before/after, clean-source CLI with/without research, and strict certification. ZIP acceptance/checksum results are recorded with the proposed archive.

## Extracted proposed archive acceptance

The extracted proposed source ZIP passed CRC and the same156-test suite in the freshly installed virtual environment (prefix `/tmp/ghostgraph-v51-venv`). The normal prediction CLI exited0 with an empty extraction cache and reproduced all518 frozen rows byte for byte;5 local learned calls,143 cache hits, cold runtime17.560s. The same package ran without its research directory. Paid-model keys/selectors were absent. Strict certification independently exited2 with490 unresolved cases and produced no certified artifact. These are actual executed checks, not inferred from source inspection.

Final source documentation is repackaged deterministically and the final archive is checked again. Source exclusions include dataset, environments, caches, credentials and nested archives; known secret-pattern scan and file inventory review found no included secrets. The final external checksum record identifies the exact proposed ZIP and tested output. Installation and verification are same-machine fresh-venv tests, not a claim of independent-host or cross-platform validation.
