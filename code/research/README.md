# GhostGraph V3 experimental research

Branch: experiment/evidence-linkage-v3; base: submission-freeze-verified (3b942ac).
The protected CSV, source ZIP, dataset and root instructions must remain unchanged.
Production remains in the original checkout. No V3 code is enabled in main.py.

Run from this experimental checkout:

```bash
PYTHONPATH=code python3 -m unittest discover -s code/tests -v
python3 code/research/run.py
```

The runner writes predictions/diagnostics only under ignored .ghostgraph/v3 and
Markdown research reports. It does not write output.csv or code.zip. Labels are
loaded solely by evaluation; no canonical answer is available to linkage.py or
the experimental auditor. coverage.md describes all 518 unlabeled requests and
never assigns hidden truth. The fresh current-mode mismatch report is also
written to code/evaluation/mismatch_report.md, replacing the outdated report only
on this branch.

## Evidence stages and changes

- Direct: time-eligible unique subject in a record or explicit catalog.
- Corroborated derived: explicit structured source/copy relation, or temporal
  worker candidate with separate direct/structured/catalog ownership proof.
  An explicit unique subject identifier within the worker event can identify a
  target but does not prove its resulting state.
- Weak: time proximity, status agreement, resource type or unique nearest event
  without independent ownership. Never admitted to prediction.
- Rejected: future/out-of-request event, unavailable workflow timestamp,
  ambiguous subject, conflicting action assignment or foreign subject reference.

Graph propagation records a chain of source IDs/locators and its availability.
Child-to-source edges model the existing baseline rule; reverse copy edges are
the new C hypothesis. Shared contextual references and undocumented schema
semantics remain a false-link risk, even with stable-reference/contact-owner
checks. This is why new synthetic capability alone is insufficient for promotion.

B and C found only a redundant already-grounded public source relationship; they
recover no new legitimate missing ownership links. No participant record gives a
structured reverse edge that improves predictions. D audits the existing planner
but makes no new verification-generation change: missing expected checks cannot
be restored without their ownership/state/citation prerequisites. It is an
explicit no-op control, not an invented new technique. F combines B+C with the
existing planner. E is NOT RUN because no configured hosted review/vision key and
model are available. No credentials were requested merely to force an optional
experiment. review.py defines a bounded proposal schema and validation gate;
there is no claim of a completed LLM integration, measured accuracy or token cost.

## Independent tests

15 new tests supplement the 115 frozen tests (130 total, all passing): nearby
requests, multiple actions, successful worker versus surviving replica, primary
absence versus replica presence, foreign temporal association, reassigned email,
future worker/report timestamps, retained records/tombstone, archive inventory,
multilingual negation, reverse foreign/future copy links, global assignment
collision and invented/future/wrong-locator model proposals. Expectations are
independently authored, not copied from public output.

## Promotion decision

Reject promotion: A/B/C/D/F remain 9/32 exact rows, 29/32 statuses and 159/193 exact
steps; full predictions have zero structural violations but no row changes.
Additional code has no measured accuracy benefit and does not meet the meaningful
improvement gate. Hosted AI review remains unmeasured. No new competition package
is generated, and neither the frozen artifacts nor main implementation is replaced.
See results.md for all metrics, window counts, timings, usage and risks.

The baseline's known uncertainty, including prediction-only restoration capability
reasoning, is not newly certified by this research. No hidden accuracy is claimed.
