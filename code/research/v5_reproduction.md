# V5 reproduction verification

A temporary source-only root was assembled with the proposed README/code and supplied dataset copied unchanged. No extraction cache or baseline output was copied. The documented `python3 code/main.py --mode predict` succeeded, internally ran the complete official-contract validator (including known resource and citation cutoff checks), and reproduced the frozen CSV byte for byte. Exactly 518 rows, zero full structural violations, unchanged ten non-deletion decisions. All 144 tests passed from this temporary root.

Actual clean-cache CLI: 16.495s, 5 learned calls, 143 classification cache hits. Model/provider: ghostgraph-intent-hybrid-word-char-logreg-v5-selective / local scikit-learn. API cost $0; local token units inapplicable. Unresolved evidence cases: 490; this is prediction reproducibility, not strict certification success.

Output SHA256: `61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891`.

Runtime dependencies were already installed at pinned versions; no fresh dependency download or independent machine was claimed. Versions: {"numpy": "2.3.5", "scipy": "1.17.0", "scikit-learn": "1.8.0", "joblib": "1.5.3", "threadpoolctl": "3.6.0"}. OS tools Tesseract and pdftotext were available; setup instructions remain in README.

The proposed ZIP was extracted into a second empty root, supplied the dataset only, then the same CLI and tests were rerun successfully. Archive CRC, exact membership and exclusions are checked by code/package.py and the external verification script. The ZIP checksum is recorded outside the ZIP in proposals/README.md to avoid a self-reference. Protected root code.zip and output.csv are never written by this procedure.

Structured hosted session traces were unavailable locally; agent-trace.zip was not manufactured. The exact engineering assistant model identifier was not exposed by authoritative runtime metadata, so complete model-name logging compliance cannot be claimed.
