"""Report Milestone 5 structure separately from semantic readiness; never pad plans."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code'))
from evaluation.main import evaluate
from ghostgraph.contract import check_rows,read_csv,resource_registry,write_csv
from ghostgraph.evidence import EvidenceStore


def main():
    evaluate(ROOT)
    data=ROOT/'dataset';store=EvidenceStore(data,ROOT/'.ghostgraph/extraction').load()
    requests=read_csv(data/'sample_deletion_requests.csv')
    reference=read_csv(data/'sample_output.csv')
    candidate=read_csv(ROOT/'.ghostgraph/sample_predictions.csv')
    reference_errors=check_rows(reference,requests,store.citation_times)
    errors=check_rows(candidate,requests,store.citation_times,known_resource_pairs=resource_registry(store))
    blocked={e['case_id'] for e in errors}
    valid=[r for r in candidate if r['case_id'] not in blocked]
    selected_requests=[r for r in requests if r['case_id'] not in blocked]
    subset_errors=check_rows(valid,selected_requests,store.citation_times,known_resource_pairs=resource_registry(store))
    assert not reference_errors and not subset_errors
    write_csv(ROOT/'.ghostgraph/sample_structurally_valid_subset.csv',valid)
    # Full original request columns are kept; the subset cannot masquerade as a
    # complete 32-row sample submission or the final 518-row evaluation output.
    import csv
    with (ROOT/'.ghostgraph/sample_subset_requests.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(requests[0]));writer.writeheader();writer.writerows(selected_requests)
    report=dict(reference_rows=len(reference),reference_structural_violations=reference_errors,
                generated_rows=len(candidate),generated_structural_violations=errors,
                blocked_cases=sorted(blocked),valid_subset_rows=len(valid),valid_subset_violations=subset_errors,
                exit_criterion_met=not errors,
                namespace_note='Source registry is enforced for generated plans. Opaque absent-target reference IDs need not occur in captured rows; reference validation is structural, not semantic certification.')
    (ROOT/'.ghostgraph/planning_acceptance.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    return 2 if errors else 0

if __name__=='__main__':raise SystemExit(main())
