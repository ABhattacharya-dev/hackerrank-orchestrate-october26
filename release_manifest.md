# GhostGraph V5.1 production release manifest

Release acceptance: PASS. Production tag: `submission-v5.1`; the tag identifies the final production commit. Approved candidate: `4015ede`. Frozen baseline: `submission-freeze-verified` at `3b942ac`. Reversible checkpoint: `release-v5.1-pre-promotion` at `3b942ac`. No frozen tag is modified.

| Artifact | SHA256 |
|---|---|
| Production code.zip | `1681ba4bd15187cc87512c4ba1cb10b03e1ac4fc2229d2632daf7723c63fd312` |
| Unchanged output.csv | `61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891` |
| Original frozen code.zip | `a0547f21fad274cf6b85b8bf3d6a4a88535cef9950108dcc605bb71226e6ddad` |

## Executed acceptance

- Fresh Python3.12 virtual environment: pinned requirements installed, pip check passed; no paid API key is required.
- All156 software tests pass in the production checkout, clean-source root and extracted final production ZIP.
- Public32:9/32 exact rows and29/32 correct statuses;159/193 exact matching steps,97.55% precision,82.38% recall,89.33% F1,79.05% field accuracy and78.67% canonical citation accuracy. No regression or claimed improvement in Output CSV accuracy.
- All518 rows are correctly keyed/sorted and pass official-contract validation with zero full-dataset structural violations. Every serialized operation and citation is unchanged: regenerated CSV is byte-identical to protected output.csv.
- Real normal CLI succeeds with an empty extraction cache in both source and final extracted ZIP; runtime also works with the entire research tree removed.
- Final archive:88 files; CRC/integrity, source member bytes, exclusions, secret-pattern scan and deterministic packaging checked. No dataset, credentials, caches, virtual environment, proposed archive, duplicate historical implementation or nested archive is included.
- Final ZIP learned model usage:5 local scikit-learn inference calls,143 classification cache hits,17.958s cold runtime;11 Tesseract and4 pdftotext invocations. No hosted model/API calls; API tokens/cost and per-request API averages are0. Local sklearn token units are inapplicable and CPU/OCR cost is unpriced.
- Strict certification remains distinct: exit2 with490 unresolved cases and no certified output. Six pre-existing sample-only structural violations are unchanged; they are not the518 submitted rows. Bounded language/consent parsing and incomplete evidence remain semantic limitations. No hidden accuracy or certification success is claimed.

## Changes from the proposed V5.1 package

All Python source and dependency pins are byte-identical to approved4015ede. Added only `code/evaluation/release_report.md`; updated release labels/architecture/progress/evaluation/usage documentation and historical report notices. Three superseded implementation snapshots and the old round-two runner remain in experimental Git history rather than production source. Proposed ZIPs were not merged. Details are in code/evaluation/release_report.md.

The original CSV/ZIP remain recoverable verbatim from the frozen tag/checkpoint and an ignored local byte-preserved backup. Root log.txt retains the complete existing byte prefix and appends only real promotion events. Hosted structured session traces and exact engineering-runtime model metadata remain unavailable; nothing was fabricated or retroactively rewritten.

The repository-only manifest is intentionally outside code.zip to avoid a self-referential ZIP checksum. The final root code.zip must equal the accepted staged ZIP byte for byte before the release is committed/tagged/pushed.
