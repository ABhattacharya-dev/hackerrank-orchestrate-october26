# V5.1 controlled production release

Approved source:4015ede, experiment/intent-safety-v5.1. Protected baseline:3b942ac, submission-freeze-verified. Production release tag:submission-v5.1. This is a selective source promotion, with unchanged competition predictions; it is not another model experiment.

## Scope and provenance

Runtime authorization, engine integration, normal CLI, packaging logic and all156 tests are exactly the approved candidate's Python source. Production modules import no research runtime logic. Three duplicate historical implementation snapshots and their superseded round-two runner were not promoted; proposed ZIP archives and proposal metadata were not merged. Useful V5/V5.1 reports, fixed probes/evaluators and compatibility imports remain. Genuine experimental Git branches/history and the append-only root transcript are preserved.

Differences from the proposed V5.1 source ZIP are release documentation/labels, actual release-run evaluation/usage headlines, historical-report notices and this report. There are no inference, policy, evidence, identity, citation-selection or serialization changes. The repository-only release_manifest.md records exact final artifact hashes and ZIP acceptance without a self-referential ZIP hash inside the ZIP.

## Executed release checks

- Fresh Python virtual environment: pinned requirements installed successfully and pip check reports no broken requirements. Python3.12 with pdftotext and English Tesseract is required; no paid API key/model service is needed.
- Main-checkout suite:156 tests pass. Clean-source suite:156 tests pass, retaining the original144 and12 independent CLI/integration tests. Test expectations are unchanged from the approved candidate.
- Public32:9 exact rows/sequences,29 correct statuses,159/193 exact matching steps; precision97.55%, recall82.38%, F189.33%, field accuracy79.05%, canonical citation accuracy78.67%. No regression.
- Full518: exact sorted request IDs, zero official-contract structural violations, no changed rows or operations/citations. Predictions regenerated only under ignored/temporary paths and compared byte for byte with the protected CSV.
- Clean extraction-cache normal CLI exits0, reproducing CSV SHA256:61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891. Runtime also succeeds with the entire research directory removed.
- Final source archive must pass CRC/exclusions, exact member/source comparison, deterministic repack, extracted-ZIP normal prediction and all156 tests before production is published. Actual final package results are recorded in the repository release_manifest.md.

The six pre-existing sample-only structural violations in three public cases remain documented; they are not the518 submission rows. Do not claim structural validity for every hypothetical input or strict certification success. Main's original output.csv is never rewritten during promotion.

## Actual release-run usage

Provider:local scikit-learn. Learned model:ghostgraph-intent-hybrid-word-char-logreg-v5-selective. Authorization layer:authorization-scope-v5.1. Training remains296 authored examples; public answers are evaluator-only, never predictor input or training. Full clean-source prediction:5 learned inference calls,143 classification cache hits,18.749s cold runtime;11 Tesseract and4 pdftotext invocations. Optional paid-model keys/selectors are absent in acceptance subprocesses. Hosted API calls/input tokens/output tokens/cost are0. API total and per-request token/cost averages are0; local sklearn token units are inapplicable and CPU/OCR cost is unpriced. Development-wide cumulative model calls were not instrumented; these are actual per-run counts.

## Remaining uncertainty and rollback

Pending/unfulfilled requester consent produces NOT_APPLICABLE with internal consent diagnostics; classifier uncertainty blocks export, and authorized ambiguous ownership remains an evidence problem. Bounded grammar and multilingual coverage are not universal consent proofs. Strict evidence certification still exits2 with490 unresolved cases and produces no certified artifact. Public exact accuracy is9/32 and hidden accuracy is unknown. No Output CSV score improvement is claimed.

Original artifacts remain at submission-freeze-verified and reversible checkpoint release-v5.1-pre-promotion, with local byte-preserved backup. Original code.zip SHA256:a0547f21fad274cf6b85b8bf3d6a4a88535cef9950108dcc605bb71226e6ddad. Original output.csv SHA256:61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891. A failed gate prevents publishing and preserves/restores the frozen submission rather than shipping a broken release.

Root log.txt is preserved append-only, including the real authorization and release steps. Hosted structured traces and exact engineering-assistant runtime model metadata are unavailable locally; no historical metadata was rewritten and no traces or identifiers were invented.
