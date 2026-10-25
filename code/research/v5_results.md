# Actual V5 measurements

Historical evaluations are not overwritten. Final results are post-feedback regression.

```json
{
  "first_heldout": {
    "baseline": {
      "confusion": {
        "authorized": {
          "authorized": 18,
          "rejected": 0,
          "defer": 0
        },
        "rejected": {
          "authorized": 12,
          "rejected": 7,
          "defer": 0
        },
        "defer": {
          "authorized": 3,
          "rejected": 0,
          "defer": 0
        }
      },
      "total": 40,
      "correct": 25,
      "false_authorizations": 15,
      "false_authorization_rate": 0.6818181818181818,
      "missed_authorizations": 0,
      "missed_authorization_rate": 0.0,
      "correct_rejections": 7,
      "negatives": 19,
      "failures": [
        "quote_translate",
        "quote_report",
        "conditional_unmet",
        "conditional_confirmation",
        "hypothetical_future",
        "hypothetical_question",
        "third_party_uncle",
        "third_party_observer",
        "delegated",
        "refusal",
        "cancellation",
        "temporary_pause",
        "temporary_deactivate",
        "es_refusal",
        "pt_refusal"
      ]
    },
    "v5": {
      "confusion": {
        "authorized": {
          "authorized": 17,
          "rejected": 1,
          "defer": 0
        },
        "rejected": {
          "authorized": 0,
          "rejected": 19,
          "defer": 0
        },
        "defer": {
          "authorized": 0,
          "rejected": 0,
          "defer": 3
        }
      },
      "total": 40,
      "correct": 39,
      "false_authorizations": 0,
      "false_authorization_rate": 0.0,
      "missed_authorizations": 1,
      "missed_authorization_rate": 0.05555555555555555,
      "correct_rejections": 19,
      "negatives": 19,
      "failures": [
        "third_party_self"
      ]
    }
  },
  "round2_prospective": {
    "metrics": {
      "baseline": {
        "confusion": {
          "authorized": {
            "authorized": 9,
            "rejected": 2,
            "defer": 1
          },
          "rejected": {
            "authorized": 7,
            "rejected": 2,
            "defer": 0
          },
          "defer": {
            "authorized": 2,
            "rejected": 1,
            "defer": 0
          }
        },
        "total": 24,
        "correct": 11,
        "false_authorizations": 9,
        "false_authorization_rate": 0.75,
        "missed_authorizations": 3,
        "missed_authorization_rate": 0.25,
        "correct_rejections": 2,
        "negatives": 9,
        "failures": [
          "self_but",
          "foreign_coworker",
          "foreign_landlord",
          "foreign_their",
          "foreign_another",
          "delegated_client",
          "scoped_invoices",
          "same_scope_conflict",
          "cancel_instruction",
          "quote_summary",
          "conditional_pending",
          "procedural_sequence",
          "fr_scope"
        ]
      },
      "round1": {
        "confusion": {
          "authorized": {
            "authorized": 8,
            "rejected": 4,
            "defer": 0
          },
          "rejected": {
            "authorized": 3,
            "rejected": 6,
            "defer": 0
          },
          "defer": {
            "authorized": 0,
            "rejected": 0,
            "defer": 3
          }
        },
        "total": 24,
        "correct": 17,
        "false_authorizations": 3,
        "false_authorization_rate": 0.25,
        "missed_authorizations": 4,
        "missed_authorization_rate": 0.3333333333333333,
        "correct_rejections": 6,
        "negatives": 9,
        "failures": [
          "self_modifiers",
          "self_active",
          "self_registered",
          "self_but",
          "foreign_landlord",
          "foreign_their",
          "foreign_another"
        ]
      },
      "v5": {
        "confusion": {
          "authorized": {
            "authorized": 12,
            "rejected": 0,
            "defer": 0
          },
          "rejected": {
            "authorized": 0,
            "rejected": 9,
            "defer": 0
          },
          "defer": {
            "authorized": 0,
            "rejected": 0,
            "defer": 3
          }
        },
        "total": 24,
        "correct": 24,
        "false_authorizations": 0,
        "false_authorization_rate": 0.0,
        "missed_authorizations": 0,
        "missed_authorization_rate": 0.0,
        "correct_rejections": 9,
        "negatives": 9,
        "failures": []
      }
    },
    "usage": {
      "baseline": {
        "calls": 6,
        "cache_hits": 0
      },
      "round1": {
        "calls": 1,
        "cache_hits": 0
      },
      "v5": {
        "calls": 1,
        "cache_hits": 0
      }
    },
    "runtime_seconds": 0.02062406799814198
  },
  "final": {
    "intent": {
      "development": {
        "rows": [
          {
            "id": "quoted_translation",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "quoted_own",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "forwarded",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "forwarded_own",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "conditional_wait",
            "expected": null,
            "category": "continuation",
            "baseline": true,
            "v5": null
          },
          {
            "id": "conditional_met",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "export_then",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "hypothetical",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "third_party",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "third_party_own",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "negation",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "scoped_negation",
            "expected": true,
            "category": "continuation",
            "baseline": false,
            "v5": true
          },
          {
            "id": "cancel",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "temporary",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "question",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "request_question",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "fr_negative",
            "expected": false,
            "category": "continuation",
            "baseline": null,
            "v5": false
          },
          {
            "id": "fr_positive",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "es_negative",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "ja_negative",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "marketing",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "correction",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "repeat",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "privacy_exception",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          }
        ],
        "metrics": {
          "baseline": {
            "confusion": {
              "authorized": {
                "authorized": 9,
                "rejected": 1,
                "defer": 0
              },
              "rejected": {
                "authorized": 7,
                "rejected": 5,
                "defer": 1
              },
              "defer": {
                "authorized": 1,
                "rejected": 0,
                "defer": 0
              }
            },
            "total": 24,
            "correct": 14,
            "false_authorizations": 8,
            "false_authorization_rate": 0.5714285714285714,
            "missed_authorizations": 1,
            "missed_authorization_rate": 0.1,
            "correct_rejections": 5,
            "negatives": 13,
            "failures": [
              "quoted_translation",
              "forwarded",
              "conditional_wait",
              "third_party",
              "negation",
              "scoped_negation",
              "cancel",
              "temporary",
              "question",
              "fr_negative"
            ]
          },
          "v5": {
            "confusion": {
              "authorized": {
                "authorized": 10,
                "rejected": 0,
                "defer": 0
              },
              "rejected": {
                "authorized": 0,
                "rejected": 13,
                "defer": 0
              },
              "defer": {
                "authorized": 0,
                "rejected": 0,
                "defer": 1
              }
            },
            "total": 24,
            "correct": 24,
            "false_authorizations": 0,
            "false_authorization_rate": 0.0,
            "missed_authorizations": 0,
            "missed_authorization_rate": 0.0,
            "correct_rejections": 13,
            "negatives": 13,
            "failures": []
          }
        },
        "runtime_seconds": 0.04085522799869068,
        "calls": {
          "baseline": 7,
          "v5": 2
        }
      },
      "observed40": {
        "rows": [
          {
            "id": "quote_translate",
            "expected": false,
            "category": "quoted",
            "baseline": true,
            "v5": false
          },
          {
            "id": "quote_report",
            "expected": false,
            "category": "quoted",
            "baseline": true,
            "v5": false
          },
          {
            "id": "quote_adopt",
            "expected": true,
            "category": "quoted",
            "baseline": true,
            "v5": true
          },
          {
            "id": "quote_plus_own",
            "expected": true,
            "category": "quoted",
            "baseline": true,
            "v5": true
          },
          {
            "id": "conditional_unmet",
            "expected": null,
            "category": "conditional",
            "baseline": true,
            "v5": null
          },
          {
            "id": "conditional_confirmation",
            "expected": null,
            "category": "conditional",
            "baseline": true,
            "v5": null
          },
          {
            "id": "conditional_confirmed",
            "expected": true,
            "category": "conditional",
            "baseline": true,
            "v5": true
          },
          {
            "id": "conditional_refund_met",
            "expected": true,
            "category": "conditional",
            "baseline": true,
            "v5": true
          },
          {
            "id": "polite_condition",
            "expected": true,
            "category": "conditional",
            "baseline": true,
            "v5": true
          },
          {
            "id": "procedural_export",
            "expected": true,
            "category": "export",
            "baseline": true,
            "v5": true
          },
          {
            "id": "procedural_after",
            "expected": true,
            "category": "export",
            "baseline": true,
            "v5": true
          },
          {
            "id": "hypothetical_future",
            "expected": false,
            "category": "hypothetical",
            "baseline": true,
            "v5": false
          },
          {
            "id": "hypothetical_question",
            "expected": false,
            "category": "hypothetical",
            "baseline": true,
            "v5": false
          },
          {
            "id": "actual_question",
            "expected": true,
            "category": "explicit",
            "baseline": true,
            "v5": true
          },
          {
            "id": "third_party_uncle",
            "expected": false,
            "category": "third_party",
            "baseline": true,
            "v5": false
          },
          {
            "id": "third_party_observer",
            "expected": false,
            "category": "third_party",
            "baseline": true,
            "v5": false
          },
          {
            "id": "third_party_self",
            "expected": true,
            "category": "third_party",
            "baseline": true,
            "v5": true
          },
          {
            "id": "delegated",
            "expected": null,
            "category": "third_party",
            "baseline": true,
            "v5": null
          },
          {
            "id": "refusal",
            "expected": false,
            "category": "negation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "negation_export",
            "expected": true,
            "category": "negation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "negation_invoice",
            "expected": true,
            "category": "negation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "cancellation",
            "expected": false,
            "category": "cancellation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "temporary_pause",
            "expected": false,
            "category": "deactivation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "temporary_deactivate",
            "expected": false,
            "category": "deactivation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "marketing_only",
            "expected": false,
            "category": "marketing",
            "baseline": false,
            "v5": false
          },
          {
            "id": "access",
            "expected": false,
            "category": "export",
            "baseline": false,
            "v5": false
          },
          {
            "id": "correction_only",
            "expected": false,
            "category": "correction",
            "baseline": false,
            "v5": false
          },
          {
            "id": "repeat_request",
            "expected": true,
            "category": "repeat",
            "baseline": true,
            "v5": true
          },
          {
            "id": "repeat_followup",
            "expected": true,
            "category": "repeat",
            "baseline": true,
            "v5": true
          },
          {
            "id": "implicit_right",
            "expected": true,
            "category": "implicit",
            "baseline": true,
            "v5": true
          },
          {
            "id": "fr_refusal",
            "expected": false,
            "category": "multilingual",
            "baseline": false,
            "v5": false
          },
          {
            "id": "fr_refusal_verb",
            "expected": false,
            "category": "multilingual",
            "baseline": false,
            "v5": false
          },
          {
            "id": "fr_erase",
            "expected": true,
            "category": "multilingual",
            "baseline": true,
            "v5": true
          },
          {
            "id": "es_refusal",
            "expected": false,
            "category": "multilingual",
            "baseline": true,
            "v5": false
          },
          {
            "id": "es_erase",
            "expected": true,
            "category": "multilingual",
            "baseline": true,
            "v5": true
          },
          {
            "id": "pt_refusal",
            "expected": false,
            "category": "multilingual",
            "baseline": true,
            "v5": false
          },
          {
            "id": "pt_erase",
            "expected": true,
            "category": "multilingual",
            "baseline": true,
            "v5": true
          },
          {
            "id": "ja_refusal",
            "expected": false,
            "category": "multilingual",
            "baseline": false,
            "v5": false
          },
          {
            "id": "ko_refusal",
            "expected": false,
            "category": "multilingual",
            "baseline": false,
            "v5": false
          },
          {
            "id": "de_erase",
            "expected": true,
            "category": "multilingual",
            "baseline": true,
            "v5": true
          }
        ],
        "metrics": {
          "baseline": {
            "confusion": {
              "authorized": {
                "authorized": 18,
                "rejected": 0,
                "defer": 0
              },
              "rejected": {
                "authorized": 12,
                "rejected": 7,
                "defer": 0
              },
              "defer": {
                "authorized": 3,
                "rejected": 0,
                "defer": 0
              }
            },
            "total": 40,
            "correct": 25,
            "false_authorizations": 15,
            "false_authorization_rate": 0.6818181818181818,
            "missed_authorizations": 0,
            "missed_authorization_rate": 0.0,
            "correct_rejections": 7,
            "negatives": 19,
            "failures": [
              "quote_translate",
              "quote_report",
              "conditional_unmet",
              "conditional_confirmation",
              "hypothetical_future",
              "hypothetical_question",
              "third_party_uncle",
              "third_party_observer",
              "delegated",
              "refusal",
              "cancellation",
              "temporary_pause",
              "temporary_deactivate",
              "es_refusal",
              "pt_refusal"
            ]
          },
          "v5": {
            "confusion": {
              "authorized": {
                "authorized": 18,
                "rejected": 0,
                "defer": 0
              },
              "rejected": {
                "authorized": 0,
                "rejected": 19,
                "defer": 0
              },
              "defer": {
                "authorized": 0,
                "rejected": 0,
                "defer": 3
              }
            },
            "total": 40,
            "correct": 40,
            "false_authorizations": 0,
            "false_authorization_rate": 0.0,
            "missed_authorizations": 0,
            "missed_authorization_rate": 0.0,
            "correct_rejections": 19,
            "negatives": 19,
            "failures": []
          }
        },
        "runtime_seconds": 0.03502968599786982,
        "calls": {
          "baseline": 12,
          "v5": 4
        }
      },
      "observed24": {
        "rows": [
          {
            "id": "self_modifiers",
            "expected": true,
            "category": "self_scope",
            "baseline": true,
            "v5": true
          },
          {
            "id": "self_active",
            "expected": true,
            "category": "self_scope",
            "baseline": true,
            "v5": true
          },
          {
            "id": "self_registered",
            "expected": true,
            "category": "self_scope",
            "baseline": true,
            "v5": true
          },
          {
            "id": "self_third_quote",
            "expected": true,
            "category": "self_scope",
            "baseline": true,
            "v5": true
          },
          {
            "id": "self_but",
            "expected": true,
            "category": "self_scope",
            "baseline": false,
            "v5": true
          },
          {
            "id": "foreign_coworker",
            "expected": false,
            "category": "third_party",
            "baseline": true,
            "v5": false
          },
          {
            "id": "foreign_landlord",
            "expected": false,
            "category": "third_party",
            "baseline": true,
            "v5": false
          },
          {
            "id": "foreign_their",
            "expected": false,
            "category": "third_party",
            "baseline": true,
            "v5": false
          },
          {
            "id": "foreign_another",
            "expected": false,
            "category": "third_party",
            "baseline": true,
            "v5": false
          },
          {
            "id": "delegated_client",
            "expected": null,
            "category": "third_party",
            "baseline": true,
            "v5": null
          },
          {
            "id": "scoped_invoices",
            "expected": true,
            "category": "negation",
            "baseline": false,
            "v5": true
          },
          {
            "id": "scoped_export",
            "expected": true,
            "category": "negation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "same_scope_conflict",
            "expected": null,
            "category": "negation",
            "baseline": false,
            "v5": null
          },
          {
            "id": "cancel_instruction",
            "expected": false,
            "category": "cancellation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "quote_summary",
            "expected": false,
            "category": "quoted",
            "baseline": true,
            "v5": false
          },
          {
            "id": "quote_endorse",
            "expected": true,
            "category": "quoted",
            "baseline": true,
            "v5": true
          },
          {
            "id": "conditional_pending",
            "expected": null,
            "category": "conditional",
            "baseline": true,
            "v5": null
          },
          {
            "id": "conditional_satisfied",
            "expected": true,
            "category": "conditional",
            "baseline": true,
            "v5": true
          },
          {
            "id": "procedural_sequence",
            "expected": true,
            "category": "export",
            "baseline": null,
            "v5": true
          },
          {
            "id": "polite_request",
            "expected": true,
            "category": "conditional",
            "baseline": true,
            "v5": true
          },
          {
            "id": "fr_scope",
            "expected": false,
            "category": "multilingual",
            "baseline": true,
            "v5": false
          },
          {
            "id": "es_scope",
            "expected": false,
            "category": "multilingual",
            "baseline": false,
            "v5": false
          },
          {
            "id": "fr_current",
            "expected": true,
            "category": "multilingual",
            "baseline": true,
            "v5": true
          },
          {
            "id": "ko_scope",
            "expected": false,
            "category": "multilingual",
            "baseline": false,
            "v5": false
          }
        ],
        "metrics": {
          "baseline": {
            "confusion": {
              "authorized": {
                "authorized": 9,
                "rejected": 2,
                "defer": 1
              },
              "rejected": {
                "authorized": 7,
                "rejected": 2,
                "defer": 0
              },
              "defer": {
                "authorized": 2,
                "rejected": 1,
                "defer": 0
              }
            },
            "total": 24,
            "correct": 11,
            "false_authorizations": 9,
            "false_authorization_rate": 0.75,
            "missed_authorizations": 3,
            "missed_authorization_rate": 0.25,
            "correct_rejections": 2,
            "negatives": 9,
            "failures": [
              "self_but",
              "foreign_coworker",
              "foreign_landlord",
              "foreign_their",
              "foreign_another",
              "delegated_client",
              "scoped_invoices",
              "same_scope_conflict",
              "cancel_instruction",
              "quote_summary",
              "conditional_pending",
              "procedural_sequence",
              "fr_scope"
            ]
          },
          "v5": {
            "confusion": {
              "authorized": {
                "authorized": 12,
                "rejected": 0,
                "defer": 0
              },
              "rejected": {
                "authorized": 0,
                "rejected": 9,
                "defer": 0
              },
              "defer": {
                "authorized": 0,
                "rejected": 0,
                "defer": 3
              }
            },
            "total": 24,
            "correct": 24,
            "false_authorizations": 0,
            "false_authorization_rate": 0.0,
            "missed_authorizations": 0,
            "missed_authorization_rate": 0.0,
            "correct_rejections": 9,
            "negatives": 9,
            "failures": []
          }
        },
        "runtime_seconds": 0.016812028996355366,
        "calls": {
          "baseline": 6,
          "v5": 1
        }
      },
      "continuation16": {
        "rows": [
          {
            "id": "audit_earlier",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "audit_inspect",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "audit_address",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "residual",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "retained_ref",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "limited_reference",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "inquiry_prior",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "foreign_audit",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "cancel_audit",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "conditional_audit",
            "expected": null,
            "category": "continuation",
            "baseline": true,
            "v5": null
          },
          {
            "id": "negative_scope",
            "expected": true,
            "category": "continuation",
            "baseline": true,
            "v5": true
          },
          {
            "id": "retention_not_consent",
            "expected": null,
            "category": "continuation",
            "baseline": true,
            "v5": null
          },
          {
            "id": "quoted_audit",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          },
          {
            "id": "future_audit",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "access_audit",
            "expected": false,
            "category": "continuation",
            "baseline": false,
            "v5": false
          },
          {
            "id": "retention_question",
            "expected": false,
            "category": "continuation",
            "baseline": true,
            "v5": false
          }
        ],
        "metrics": {
          "baseline": {
            "confusion": {
              "authorized": {
                "authorized": 7,
                "rejected": 0,
                "defer": 0
              },
              "rejected": {
                "authorized": 4,
                "rejected": 3,
                "defer": 0
              },
              "defer": {
                "authorized": 2,
                "rejected": 0,
                "defer": 0
              }
            },
            "total": 16,
            "correct": 10,
            "false_authorizations": 6,
            "false_authorization_rate": 0.6666666666666666,
            "missed_authorizations": 0,
            "missed_authorization_rate": 0.0,
            "correct_rejections": 3,
            "negatives": 7,
            "failures": [
              "inquiry_prior",
              "foreign_audit",
              "conditional_audit",
              "retention_not_consent",
              "quoted_audit",
              "retention_question"
            ]
          },
          "v5": {
            "confusion": {
              "authorized": {
                "authorized": 7,
                "rejected": 0,
                "defer": 0
              },
              "rejected": {
                "authorized": 0,
                "rejected": 7,
                "defer": 0
              },
              "defer": {
                "authorized": 0,
                "rejected": 0,
                "defer": 2
              }
            },
            "total": 16,
            "correct": 16,
            "false_authorizations": 0,
            "false_authorization_rate": 0.0,
            "missed_authorizations": 0,
            "missed_authorization_rate": 0.0,
            "correct_rejections": 7,
            "negatives": 7,
            "failures": []
          }
        },
        "runtime_seconds": 0.009104015000048093,
        "calls": {
          "baseline": 3,
          "v5": 0
        }
      }
    },
    "competition": {
      "sample": {
        "baseline": {
          "runtime_seconds": 0.9883422029961366,
          "calls": 4,
          "cache_hits": 0,
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
        "v5": {
          "runtime_seconds": 0.8921800980024273,
          "calls": 4,
          "cache_hits": 0,
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
          "changed_rows": [],
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
        }
      },
      "full": {
        "baseline": {
          "runtime_seconds": 5.104895841002872,
          "calls": 5,
          "cache_hits": 143,
          "violations": []
        },
        "v5": {
          "runtime_seconds": 6.580265769996913,
          "calls": 5,
          "cache_hits": 143,
          "violations": [],
          "changed_rows": []
        }
      }
    },
    "byte_identical": true
  }
}
```
