"""Run the ingestion milestone's actual participant-input acceptance checks."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ghostgraph.contract import read_csv
from ghostgraph.evidence import EvidenceStore


def inspect(root):
    dataset = root / "dataset"
    assert len(read_csv(dataset / "deletion_requests.csv")) == 518
    assert len(read_csv(dataset / "sample_deletion_requests.csv")) == 32
    store = EvidenceStore(dataset, root / ".ghostgraph" / "extraction").load()
    assert len(store.manifest) == 94
    assert len(store.observations) > 1000
    assert {r["format"] for r in store.coverage} == {".json", ".sql", ".log", ".txt", ".pdf", ".png"}
    assert all(r["observations"] + r["scopes"] > 0 for r in store.coverage if r["format"] in {".json", ".sql", ".log", ".txt"})
    for obs in store.observations:
        assert obs.locator and obs.state and obs.system and obs.resource
        assert obs.available >= store.citation_times[obs.evidence_id]
    print(json.dumps(store.summary(), indent=2))
    return store


if __name__ == "__main__": inspect(Path(__file__).resolve().parents[2])
