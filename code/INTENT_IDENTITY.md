# Milestone 2 — intent and historical identity acceptance

## Objective and implementation

Separate deletion authorization from access, correction, marketing opt-out,
recovery, denial and hypothetical procedure questions. Retain grounded current
and historical aliases without merging unrelated people.

The actual AI component is local supervised word/character TF-IDF plus balanced
logistic regression (ghostgraph-intent-hybrid-word-char-logreg-v4), fitted from
independently authored multilingual examples. Every uncached request executes
inference. Generic English scope guards handle explicit consent/denial and
non-deletion categories; the learned model decides multilingual/implicit cases.
Unicode/contraction normalization, a version/training-hash/text cache and bounded
uncertainty handling are implemented. Probabilities are not calibrated certainty.
No external model credentials are required. Training never reads public answers.
The task description and training examples are submitted in ghostgraph/intent.py.

Cancellation of a request to erase, explicit refusal to delete and hypothetical
how-to questions no longer become authorization merely because they contain
'delete'. Explicit undecided wording is marked ambiguous and blocks planning.
Low-confidence cases remain diagnosed; strict export refuses unresolved cases.
No unconstrained model constructs final CSV or step JSON.

IdentityIndex accepts the global EvidenceStore. It builds a separate cached
ownership/provenance index for each audit cutoff using eligible current snapshots,
audit old/new values, explicit catalog links and structured resource observations
that co-locate exactly one stable subject reference with actual contact fields.
Document-wide co-occurrence, names, ID suffixes and later evidence cannot create
identity edges. Original audit/activity/file IDs, locators and availability times
are retained; explain(email, cutoff) returns per-alias proof chains.

Old email, phone and supplied hash values remain retrieval aliases after a change;
that is necessary to discover stale copies. Shared aliases are excluded from
unique linkage; a shared request identifier is ambiguous and blocks all deletion
planning. Explicit foreign stable references override shared contact matches;
reassigned resources and foreign-owner dependency edges cannot contaminate the
subject graph. Repeated requests reuse eligible indexes, never a timeless verdict.
Unknown ownership interval boundaries are not invented. A snapshot is not used
as proof of every earlier historical field value.

## Executed acceptance

- All 32 public requests passed intent classification without low-confidence flags.
- All 32 resolved to a unique stable subject through eligible evidence; every
  emitted alias had at least one source proof available by that case's cutoff.
- All 38 software tests passed, zero failures/errors/skips.
- Independent tests cover access/correction/recovery/marketing opt-out, negated
  deletion, cancellation, hypothetical questions, undecided wording, multilingual
  positives and negatives, old/new emails, hashes, duplicate names, alias reuse,
  shared phones, future links, repeated resolution, conflicting stable references,
  reassigned resources, foreign dependencies and refusal to plan for ambiguity.
- Full predictor/sample regression and strict-export verification ran. Existing
  audit coverage blockers remain; intent/identity acceptance is not full deletion
  status or final-submission correctness. Public samples lack NOT_APPLICABLE
  examples, making independent negative-intent tests essential.

## Commands and provenance review

```bash
python3 code/evaluation/intent_identity.py
PYTHONPATH=code python3 -m unittest discover -s code/tests -v
```

Machine-readable acceptance flags are in ignored
.ghostgraph/intent_identity_acceptance.json. Per-case identity proof chains are
in ignored diagnostic files from the application. They may contain participant
identifiers and must remain outside source archives and conversation logs.

## Failures corrected and remaining risks

Earlier guards treated cancellation/how-to wording as direct erasure consent.
Identity ambiguity could still create provisional plans; traversal could follow
foreign-owner dependencies. These paths now have explicit guards and regression
tests. Identity provenance formerly depended only on snapshots/audits; eligible
structured resource/catalog links now supplement it with source explanations.

The local classifier is small and its language/generalization coverage is finite;
unrecognized subtle ambiguity can still require review. Temporal eligibility
and unique identifier ownership prevent unsupported merges but can leave genuine
links unresolved when evidence is insufficient. No claim is made that all global
resource ownership or the earlier 335 audit coverage gaps have been resolved.
The stated milestone exit criterion is met for executed public and adversarial
acceptance cases; full submission readiness remains separate.
