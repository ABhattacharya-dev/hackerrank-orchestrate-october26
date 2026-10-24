"""Standalone schema/order/citation validator; no prediction or label lookup."""
import argparse
import csv
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ghostgraph.contract import FIELDS, read_csv, timestamp, validate_rows, resource_registry
from ghostgraph.evidence import EvidenceStore


def validate(output, requests, dataset, *, check_registry=False):
    with Path(output).open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('CSV header must be exactly: ' + ','.join(FIELDS))
        rows = list(reader)
    times = {r['file_id']: timestamp(r['captured_at']) for r in read_csv(dataset/'evidence_files.csv')}
    for filename, key in [('system_activity.csv','activity_id'),('user_audit_log.csv','audit_id')]:
        times.update({r[key]: timestamp(r['event_time']) for r in read_csv(dataset/filename)})
    pairs=None
    if check_registry:
        store=EvidenceStore(dataset,dataset.parent/'.ghostgraph/extraction').load()
        if store.failures:raise ValueError('source registry has ingestion failures')
        pairs=resource_registry(store)
    validate_rows(rows, read_csv(requests), times,known_resource_pairs=pairs)
    return len(rows)


def main():
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--requests', type=Path, default=root/'dataset/deletion_requests.csv')
    parser.add_argument('--check-registry',action='store_true',help='add source membership checks; syntactically valid absent-target IDs need not appear in captured rows')
    args = parser.parse_args()
    try:
        count = validate(args.output, args.requests, root/'dataset',check_registry=args.check_registry)
    except (AssertionError, ValueError, KeyError, TypeError, OSError) as exc:
        print('INVALID: ' + (str(exc) or 'output contract assertion failed'), file=sys.stderr)
        return 1
    print(f'VALID: {count} rows; schema, enums, numbering, ordering and citation availability checked. Semantic correctness is not certified.')
    return 0


if __name__ == '__main__': raise SystemExit(main())
