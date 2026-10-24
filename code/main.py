"""GhostGraph CLI. Run from any directory; paths default to the checkout root."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

from ghostgraph.contract import read_csv, validate_rows, write_csv, resource_registry
from ghostgraph.engine import Auditor
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier, MODEL_NAME
from ghostgraph.intent import POSITIVE, NEGATIVE
from ghostgraph.vision import from_environment


def run(root, requests_path, output, *, allow_unresolved=False, tag="full"):
    started = time.perf_counter()
    dataset = root / "dataset"
    requests = read_csv(requests_path)
    required = {"case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"}
    if not requests or any(set(row) != required for row in requests):
        raise ValueError("request schema mismatch or empty requests")
    if len({r["case_id"] for r in requests}) != len(requests):
        raise ValueError("duplicate case IDs")
    store = EvidenceStore(dataset, root / ".ghostgraph" / "extraction", vision_extractor=from_environment()).load()
    report_path = root / ".ghostgraph" / "ingestion_report.json"
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text(json.dumps(store.ingestion_report(), indent=2))
    if store.failures and not allow_unresolved:
        raise ValueError("evidence ingestion failures; inspect .ghostgraph/ingestion_report.json")
    intent = IntentClassifier()
    auditor = Auditor(store, IdentityIndex(dataset, store=store), intent)
    pairs = [auditor.audit(r) for r in sorted(requests, key=lambda r: r["case_id"])]
    rows, diagnostics = map(list, zip(*pairs))
    unresolved = [d for d in diagnostics if d["issues"]]
    cache = root / ".ghostgraph"
    cache.mkdir(exist_ok=True)
    (cache / (tag + "_diagnostics.json")).write_text(json.dumps(diagnostics, indent=2))
    input_hashes = dict(store.hashes)
    for name in ["user_identities.csv", "user_audit_log.csv", "system_activity.csv", "deletion_rules.csv", "evidence_files.csv"]:
        input_hashes[name] = hashlib.sha256((dataset / name).read_bytes()).hexdigest()
    usage = {"provider": "local scikit-learn", "model": MODEL_NAME,
             "request_count": len(requests), "inference_calls": intent.calls,
             "cache_hits": intent.cache_hits, "input_tokens": 0, "output_tokens": 0,
             "unique_classifications": len(intent.cache), "scope_decisions": intent.scope_decisions,
             "token_units_applicable": False, "api_cost_usd": 0.0,
             "training_examples": len(POSITIVE) + len(NEGATIVE),
             "training_hash": intent.training_hash, "runtime_seconds": time.perf_counter() - started,
             "unresolved_cases": len(unresolved), "status_counts": dict(Counter(r["deletion_status"] for r in rows)),
             "input_hashes": input_hashes, "requests_hash": hashlib.sha256(Path(requests_path).read_bytes()).hexdigest(),
             "intent_decision_sources": dict(Counter(d["intent"]["decision_source"] for d in diagnostics)),
             "document_extraction": dict(store.extraction_stats),
             "ingestion": store.summary()}
    (cache / (tag + "_run.json")).write_text(json.dumps(usage, indent=2))
    if unresolved and not allow_unresolved:
        raise ValueError(f"{len(unresolved)} unresolved cases; no final output written. Inspect .ghostgraph/{tag}_diagnostics.json. --allow-unresolved writes a PROVISIONAL candidate only.")
    validate_rows(rows, requests, store.citation_times, require_proofs=not allow_unresolved,known_resource_pairs=resource_registry(store))
    write_csv(output, rows)
    summary = {k: usage[k] for k in ["request_count", "inference_calls", "cache_hits", "runtime_seconds", "unresolved_cases", "status_counts"]}
    print(json.dumps(summary))
    return rows, diagnostics, usage


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Evidence-backed temporal deletion audit; strict by default")
    parser.add_argument("--requests", type=Path, default=root / "dataset/deletion_requests.csv")
    parser.add_argument("--output", type=Path, help="defaults to output.csv in strict mode; output.candidate.csv with --allow-unresolved")
    parser.add_argument("--allow-unresolved", action="store_true", help="write explicitly provisional candidate despite diagnosed missing proofs")
    args = parser.parse_args()
    try:
        output = args.output or root / ("output.candidate.csv" if args.allow_unresolved else "output.csv")
        run(root, args.requests.resolve(), output.resolve(), allow_unresolved=args.allow_unresolved)
    except (ValueError, AssertionError) as exc:
        print("GhostGraph: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__": raise SystemExit(main())
