# GhostGraph final candidate-run usage report

This report describes the actual 518-request run that produced
`output.candidate.csv`; strict final `output.csv` remains blocked by
490 proof/coverage gaps. It is not a claim that a final
submission run succeeded. Development/evaluation runs and the engineering
assistant's own conversation usage are excluded; their provider billing is not
available to the application.

| Component | Provider / model | Actual final-run usage |
| --- | --- | ---: |
| Intent inference | local scikit-learn / ghostgraph-intent-hybrid-word-char-logreg-v4 | 375 inference calls |
| Intent cache | same content/model/training-hash cache | 143 cache hits |
| Intent training | independently authored source examples | 296 examples; 1 fit |
| OCR | local Tesseract English recognizer | 0 fresh calls |
| PDF text extraction | local Poppler pdftotext | 0 fresh calls |
| Extraction cache | content-hash cache | 15 hits |

The ML component genuinely executes. It is a supervised discriminative model,
not a hosted LLM. Generic deterministic English consent/scope guards complement
the learned model; model decisions are used for multilingual/implicit intent.
Request decision sources: `{'explicit erasure or completion/audit of prior erasure': 446, 'semantic ML inference': 62, 'limited scope preserving the account': 3, 'explicit non-deletion scope': 5, 'access/correction/portability without erasure': 2}`. Cached repeated
texts reuse the same validated classification. No public output label trains it.

- Requests processed: 518.
- Input API tokens: 0; output API tokens: 0; total API tokens: 0.
- Average API tokens/request: 0. Token units are **not applicable** to TF-IDF,
  logistic regression, Tesseract or PDF text extraction; zero does not mean the
  local components performed no computation.
- Estimated API cost: USD 0.00 total; USD 0.00/request. Per-model API totals are
  also zero because all components execute locally with no metered API calls.
- Local compute/storage cost is unpriced and excluded, rather than invented.
- Measured warm-cache runtime: 6.875 seconds,
  0.013272 seconds/request averaged across the run.
- Cold extraction reproducibility run: 19.435 seconds,
  11 OCR and
  4 PDF extraction calls;
  identical candidate bytes. This separate validation run is not added to the
  final candidate-run counts above.

Training corpus SHA-256: `c61f2d25b193fa6713c9367e592751a0e5e792a937db1a51cde4c127ec94d4d6`.
Request-file SHA-256: `78464850941b84baecf9fee586208752521c4521d0c15c76f741516eb7f700d2`.
Combined manifest/evidence/identity/policy/activity hash:
`3b7030520f221ca63031f36ab5b72c3a139bb100e599476d003489014cccad7e`.
Candidate SHA-256: `b83ff6a9b086a53ceda99b3f527eefda36ec49f69db392f84be51fdecb01e7c3`.

Prompts, training examples and response validation live in
`code/ghostgraph/intent.py`. All retries are zero for this local deterministic
inference path; exceptions fail the run rather than returning a fabricated result.
No credentials or secret values are stored in source, reports or logs.
