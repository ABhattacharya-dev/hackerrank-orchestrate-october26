# Actual three-source V5.1 regression measurements

Warm extraction-cache comparison; separate acceptance uses fresh caches. No hidden labels.

```json
{
  "frozen": {
    "sample": {
      "calls": 4,
      "cache_hits": 0,
      "runtime_seconds": 1.1687524590015528,
      "violations": [
        {
          "case_id": "case_01",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_01",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        },
        {
          "case_id": "case_02",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_02",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        },
        {
          "case_id": "case_04",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_04",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        }
      ],
      "unresolved": 30,
      "changed_vs_frozen": [],
      "metrics": {
        "counts": {
          "cases": 32,
          "status_correct": 29,
          "exact_sequences": 9,
          "exact_rows": 9,
          "predicted_steps": 163,
          "expected_steps": 193,
          "exact_step_matches": 159,
          "structural_step_matches": 159,
          "expected_fields": 1351,
          "field_matches": 1068,
          "expected_citations": 75,
          "canonical_citation_matches": 59,
          "ordering_errors": 0,
          "missing_steps": 34,
          "extra_steps": 4,
          "wrong_states": 0,
          "wrong_evidence": 0
        },
        "status_accuracy": 0.90625,
        "exact_row_accuracy": 0.28125,
        "exact_sequence_accuracy": 0.28125,
        "step_precision": 0.9754601226993865,
        "step_recall": 0.8238341968911918,
        "step_f1": 0.8932584269662921,
        "structural_step_precision": 0.9754601226993865,
        "structural_step_recall": 0.8238341968911918,
        "field_accuracy": 0.7905255366395263,
        "canonical_evidence_accuracy": 0.7866666666666666
      }
    },
    "full": {
      "calls": 5,
      "cache_hits": 143,
      "runtime_seconds": 8.0797240949978,
      "violations": [],
      "unresolved": 490,
      "changed_vs_frozen": []
    }
  },
  "v5": {
    "sample": {
      "calls": 4,
      "cache_hits": 0,
      "runtime_seconds": 1.0942574959990452,
      "violations": [
        {
          "case_id": "case_01",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_01",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        },
        {
          "case_id": "case_02",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_02",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        },
        {
          "case_id": "case_04",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_04",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        }
      ],
      "unresolved": 30,
      "changed_vs_frozen": [],
      "metrics": {
        "counts": {
          "cases": 32,
          "status_correct": 29,
          "exact_sequences": 9,
          "exact_rows": 9,
          "predicted_steps": 163,
          "expected_steps": 193,
          "exact_step_matches": 159,
          "structural_step_matches": 159,
          "expected_fields": 1351,
          "field_matches": 1068,
          "expected_citations": 75,
          "canonical_citation_matches": 59,
          "ordering_errors": 0,
          "missing_steps": 34,
          "extra_steps": 4,
          "wrong_states": 0,
          "wrong_evidence": 0
        },
        "status_accuracy": 0.90625,
        "exact_row_accuracy": 0.28125,
        "exact_sequence_accuracy": 0.28125,
        "step_precision": 0.9754601226993865,
        "step_recall": 0.8238341968911918,
        "step_f1": 0.8932584269662921,
        "structural_step_precision": 0.9754601226993865,
        "structural_step_recall": 0.8238341968911918,
        "field_accuracy": 0.7905255366395263,
        "canonical_evidence_accuracy": 0.7866666666666666
      }
    },
    "full": {
      "calls": 5,
      "cache_hits": 143,
      "runtime_seconds": 5.900770010994165,
      "violations": [],
      "unresolved": 490,
      "changed_vs_frozen": []
    }
  },
  "v51": {
    "sample": {
      "calls": 4,
      "cache_hits": 0,
      "runtime_seconds": 1.4489033420031774,
      "violations": [
        {
          "case_id": "case_01",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_01",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        },
        {
          "case_id": "case_02",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_02",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        },
        {
          "case_id": "case_04",
          "code": "NO_SUPPORTED_STEPS"
        },
        {
          "case_id": "case_04",
          "code": "INCOMPLETE_WITHOUT_FINDING"
        }
      ],
      "unresolved": 30,
      "changed_vs_frozen": [],
      "metrics": {
        "counts": {
          "cases": 32,
          "status_correct": 29,
          "exact_sequences": 9,
          "exact_rows": 9,
          "predicted_steps": 163,
          "expected_steps": 193,
          "exact_step_matches": 159,
          "structural_step_matches": 159,
          "expected_fields": 1351,
          "field_matches": 1068,
          "expected_citations": 75,
          "canonical_citation_matches": 59,
          "ordering_errors": 0,
          "missing_steps": 34,
          "extra_steps": 4,
          "wrong_states": 0,
          "wrong_evidence": 0
        },
        "status_accuracy": 0.90625,
        "exact_row_accuracy": 0.28125,
        "exact_sequence_accuracy": 0.28125,
        "step_precision": 0.9754601226993865,
        "step_recall": 0.8238341968911918,
        "step_f1": 0.8932584269662921,
        "structural_step_precision": 0.9754601226993865,
        "structural_step_recall": 0.8238341968911918,
        "field_accuracy": 0.7905255366395263,
        "canonical_evidence_accuracy": 0.7866666666666666
      }
    },
    "full": {
      "calls": 5,
      "cache_hits": 143,
      "runtime_seconds": 6.444269305997295,
      "violations": [],
      "unresolved": 490,
      "changed_vs_frozen": []
    }
  }
}
```
