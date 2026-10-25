# V5.1 proposed release checksums and acceptance

Recommendation: promote the V5.1 Code ZIP after review; do not promote V5 as-is because its ambiguous-intent output bug remains there. No automatic merge or replacement of protected artifacts is performed. CSV accuracy is unchanged.

Branch: experiment/intent-safety-v5.1. Parent V5:08e975b. Protected tag:submission-freeze-verified (3b942ac). Exact final commit is available in branch history; no commit/archive self-hash is embedded in the archive.

| Artifact | SHA256 |
|---|---|
| proposals/code-v51.zip | `ab0c7e15ffb5e3529e3366a16a999406b665c46501146ab10729b6cb681a204a` |
| output.csv | `61c7563f3ffa04edb7ab18532f9d31b49fe316c52a5d013f80412e0b458a9891` |
| code.zip | `a0547f21fad274cf6b85b8bf3d6a4a88535cef9950108dcc605bb71226e6ddad` |
| proposals/code-v5.zip | `556dcb65abcdd7d76692e3b73967bf6efab56e91e957e3198fae929eb0e581f1` |
| code/ghostgraph/authorization.py | `b1fa786858b2b158dd0578252c3ffac4795e0c64a4b0316d01fee5cab2fdbdd9` |

Final proposed archive:87 source/documentation files, valid CRC, deterministic byte-identical repack, every member matches the evaluated source. Three duplicate historical implementations and their round-two runner are omitted from the ZIP but retained in Git. Dataset, secrets/credential files, environments, caches and nested archives are excluded. Source inventory and secret-pattern checks passed.

Fresh virtual environment `/tmp/ghostgraph-v51-venv`: pinned requirements installed and pip check passed. Final extracted ZIP ran the real CLI from an empty extraction cache with no paid keys/selectors: exit0,518 rows, zero official full structural violations and byte-identical frozen CSV. The runtime also passed with the entire research tree removed. All156 tests passed; original frozen115 and V5144 suites were separately rerun successfully. All public metrics remain unchanged (9/32 exact,29/32 statuses,159/193 exact steps); six pre-existing sample-only structural violations remain documented and are not the full submission rows.

Final extracted-archive measured prediction runtime:16.477s; learned local model calls:5; classification cache hits:143; OCR invocations:11; pdftotext invocations:4. Hosted/API calls and API tokens/cost:0. Local token units are inapplicable; local compute cost is unpriced. These are per-run measurements, not invented aggregate development usage.

Strict certification exits2 with490 unresolved cases and no certified CSV. Authorized missing/ambiguous ownership can still block output on new inputs; bounded language guards are not a universal consent proof. This is a Code ZIP-only readiness recommendation, not certification or hidden-accuracy success. See code/evaluation/v51_review.md for interpretation, independent CLI tests, initial failures/corrections and comparative ratings.

Reproduce the final archive acceptance from this checkout:

```bash
python3 code/evaluation/v51_acceptance.py --python /path/to/fresh/venv/bin/python --archive proposals/code-v51.zip
```

The code archive itself needs only the documented dependencies and supplied dataset for inference/tests; Git history is needed only for the optional historical three-source comparison. Structured hosted traces and exact engineering-model metadata remain unavailable locally; no traces or identifiers were fabricated. Root log.txt is preserved separately.
