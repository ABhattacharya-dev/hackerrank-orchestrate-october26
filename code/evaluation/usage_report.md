# V5 final prediction usage

Provider: local scikit-learn, frozen TF-IDF logistic regression with authorization-scope-v5-research-3 gates. Training: unchanged 296 authored examples. Full518 evaluation: 5 learned inference calls, 143 classification cache hits, 6.580s prediction evaluation excluding shared ingestion. Five genuine learned inferences participate in the workflow. No hosted AI or paid inference was used; API calls/tokens and API cost are zero. Local sklearn has no provider token units; local compute cost is unpriced, not asserted free.

The V4 comparison was actually replayed using local LinearSVC (32 alternative learned calls); it did not outperform the frozen model. No alternative weights or new LLM were adopted. Research benchmark runs and their individual call counts/runtimes are recorded in research/v5_results.md. These per-run counts must not be mistaken for a total across all development reruns; exact aggregate development inference counts were not instrumented. Clean package CLI usage is recorded separately in research/v5_reproduction.md.

No production CSV gain is claimed. This is a proposed Code ZIP-only quality improvement. Hosted session structured rollouts and exact engineering-runtime model metadata are unavailable locally; no trace files or identifiers were invented. Root log.txt preserves the actual append-only development transcript; a hosted-interface export is still needed for complete structured traces.

## Historical usage record below (not V5 headline)

# Actual final prediction-run usage

This is the 518-request prediction run that produced root output.csv, not the
older certification candidate. Provider: local scikit-learn. Model: ghostgraph-intent-hybrid-word-char-logreg-v5-selective.

| Measurement | Actual final-run value |
| --- | ---: |
| Requests | 518 |
| Learned local inference calls | 5 |
| Deterministic unique scope decisions | 370 |
| Intent classification cache hits | 143 |
| Unique normalized classifications | 375 |
| Training fits / authored examples | 1 / 296 |
| API input / output tokens | 0 / 0 |
| Paid model calls | 0 |
| API cost total / per request | USD 0.00 / USD 0.00 |
| Runtime seconds | 6.407435 |

Token units do not apply to local TF-IDF/logistic regression, Tesseract or PDF
extraction. No token estimate was invented. No paid provider tariff applies
because no paid API calls were made. CPU/storage cost is unpriced, not asserted
free. The actual classifier participates in multilingual/implicit intent; English
scope guards and cached repetitions avoid redundant inference. Training uses
296 authored source examples, never public output labels.

Warm-run document extraction: {'cache_hits': 15}.
Separate cold reproducibility validation: {'tesseract_calls': 11, 'pdftotext_calls': 4}.
Public evaluations, unit fixtures, earlier failed extraction attempts, cold
reproduction and engineering-assistant usage are separate validation/development
work and are excluded from final-run counts. Engineering-assistant billing and
exact runtime model metadata are not exposed and are not fabricated.

Restore-console inference is deterministic source extraction and rule evaluation,
not an unrecorded paid vision call. The supplied image was visually reviewed
during engineering; deployed extraction uses the reproducible local OCR path.

Final output SHA-256: 61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891.
Request SHA-256: 78464850941b84baecf9fee586208752521c4521d0c15c76f741516eb7f700d2.
Training SHA-256: c61f2d25b193fa6713c9367e592751a0e5e792a937db1a51cde4c127ec94d4d6.

This export passes the official structural contract but is not high-assurance
certification. All uncertainty remains available in local prediction diagnostics.
