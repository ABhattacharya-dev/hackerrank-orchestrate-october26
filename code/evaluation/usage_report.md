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
