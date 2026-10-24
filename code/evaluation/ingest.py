"""Process all evidence once and persist explicit ingestion/provenance outcomes."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ghostgraph.evidence import EvidenceStore
from ghostgraph.vision import from_environment

if __name__=='__main__':
    root=Path(__file__).resolve().parents[2]
    vision=from_environment()
    store=EvidenceStore(root/'dataset',root/'.ghostgraph/extraction',vision_extractor=vision).load()
    report=store.ingestion_report()
    report['vision']={'configured':vision is not None,'calls':vision.calls if vision else 0,'usage':vision.usage if vision else []}
    path=root/'.ghostgraph/ingestion_report.json';path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report,indent=2))
    print(json.dumps({'manifest_entries':len(store.manifest),'outcomes':len(store.coverage),
        'failures':len(store.failures),'unresolved':len(store.unresolved),'observations':len(store.observations),
        'report':str(path)}))
    raise SystemExit(1 if store.failures else 0)
