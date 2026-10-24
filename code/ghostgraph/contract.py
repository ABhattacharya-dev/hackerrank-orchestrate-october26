"""Official output vocabulary, deterministic serialization, and strict validation."""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

GROUPS = {
    "FINDING": [("REPORT_REMAINING_RECORD", "PRESENT"), ("REPORT_EXPOSED_PII", "PRESENT"),
                ("REPORT_ACTIVE_DATA_FLOW", "ACTIVE"), ("REPORT_RESTORE_RISK", "ACTIVE")],
    "REMEDIATION": [("DISABLE_DATA_FLOW", "DISABLED"), ("BLOCK_RESTORE", "BLOCKED"),
                    ("DELETE_RECORD", "ABSENT"), ("REDACT_RECORD", "REDACTED"),
                    ("ANONYMIZE_RECORD", "ANONYMIZED")],
    "VERIFICATION": [("VERIFY_RECORD_ABSENT", "ABSENT"), ("VERIFY_RECORD_PRESENT", "PRESENT"),
                     ("VERIFY_RECORD_REDACTED", "REDACTED"), ("VERIFY_RECORD_ANONYMIZED", "ANONYMIZED"),
                     ("VERIFY_DATA_FLOW_DISABLED", "DISABLED"), ("VERIFY_RESTORE_BLOCKED", "BLOCKED")],
}
OPERATIONS = {op: (phase, state, pi, oi) for pi, (phase, pairs) in enumerate(GROUPS.items())
              for oi, (op, state) in enumerate(pairs)}
FIELDS = ["case_id", "deletion_status", "steps_json"]
STEP_FIELDS = {"step_no", "phase", "system_id", "resource_id", "operation", "state", "evidence_id"}


def timestamp(value):
    """Reject missing or timezone-naive times instead of guessing availability."""
    if not value:
        raise ValueError("missing timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.timestamp()


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def step(operation, system, resource, evidence=""):
    phase, state, _, _ = OPERATIONS[operation]
    return dict(step_no=0, phase=phase, system_id=system, resource_id=resource,
                operation=operation, state=state, evidence_id=evidence)


def order_key(item):
    _, _, pi, oi = OPERATIONS[item["operation"]]
    return pi, oi, item["system_id"], item["resource_id"]


def ordered(steps):
    result = sorted(steps, key=order_key)
    for i, item in enumerate(result, 1):
        item["step_no"] = i
    return result


def validate_rows(rows, requests, citation_times, *, require_proofs=True):
    expected = {r["case_id"]: r for r in requests}
    assert len(expected) == len(requests), "duplicate request IDs"
    assert [r["case_id"] for r in rows] == sorted(expected), "output IDs/count/order differ"
    for row in rows:
        assert set(row) == set(FIELDS), "incorrect CSV columns"
        status = row["deletion_status"]
        assert status in {"COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"}
        steps = json.loads(row["steps_json"])
        assert isinstance(steps, list)
        if status == "NOT_APPLICABLE":
            assert steps == []
        elif require_proofs:
            assert steps, f'{row["case_id"]}: no supported steps'
        assert steps == sorted(steps, key=order_key)
        semantic = set()
        for i, item in enumerate(steps, 1):
            assert set(item) == STEP_FIELDS
            assert type(item["step_no"]) is int and item["step_no"] == i
            assert all(isinstance(item[k], str) for k in STEP_FIELDS - {"step_no"})
            assert item["system_id"] and item["resource_id"]
            assert (item["phase"], item["state"]) == OPERATIONS[item["operation"]][:2]
            key = item["phase"], item["operation"], item["system_id"], item["resource_id"]
            assert key not in semantic, "duplicate semantic step"
            semantic.add(key)
            cited = status == "COMPLETE" or item["phase"] == "FINDING"
            if status == "COMPLETE":
                assert item["phase"] == "VERIFICATION"
            if cited:
                assert item["evidence_id"] in citation_times, "unknown citation"
                assert citation_times[item["evidence_id"]] <= timestamp(expected[row["case_id"]]["audit_at"])
            else:
                assert item["evidence_id"] == ""
        if status == "INCOMPLETE" and require_proofs:
            assert any(s["phase"] == "FINDING" for s in steps), "incomplete without finding"


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, path)
