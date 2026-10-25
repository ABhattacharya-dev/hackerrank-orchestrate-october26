"""Cold-copy reproducibility of the unpromoted combination; no protected writes."""
import json,shutil,tempfile,subprocess,sys,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SCRIPT='''import sys,json
from pathlib import Path
r=Path(sys.argv[1]);sys.path.insert(0,str(r/'code'))
from ghostgraph.contract import read_csv,check_rows,resource_registry,write_csv
from ghostgraph.evidence import EvidenceStore
from ghostgraph.identity import IdentityIndex
from ghostgraph.intent import IntentClassifier
from research.linkage import temporal_candidates
from research.auditor import ResearchAuditor
from collections import defaultdict
s=EvidenceStore(r/'dataset',r/'.ghostgraph/extraction').load()
if s.failures:raise RuntimeError(s.failures)
i=IdentityIndex(r/'dataset',s);q=read_csv(r/'dataset/deletion_requests.csv');links=defaultdict(list)
for c in temporal_candidates(s,i,q,360):links[c['case_id']].append(c)
m=IntentClassifier();a=ResearchAuditor(s,i,m,graph_enabled=True,temporal_links=links)
rows=[a.audit(x)[0] for x in sorted(q,key=lambda x:x['case_id'])]
errors=check_rows(rows,q,s.citation_times,known_resource_pairs=resource_registry(s))
if errors:raise RuntimeError(errors)
(r/'experimental_rows.json').write_text(json.dumps(rows))
write_csv(r/'experimental_output.csv',rows)
print(json.dumps(dict(rows=len(rows),calls=m.calls,cache_hits=m.cache_hits,extraction=dict(s.extraction_stats))))
'''
def main():
    expected=json.loads((ROOT/'.ghostgraph/v3/F_full_rows.json').read_text())
    start=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='ghostgraph-v3-cold-') as directory:
        target=Path(directory)
        shutil.copytree(ROOT/'code',target/'code',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'dataset',target/'dataset')
        p=subprocess.run([sys.executable,'-c',SCRIPT,str(target)],cwd=target.parent,capture_output=True,text=True,timeout=180)
        if p.returncode:raise RuntimeError(p.stderr)
        rows=json.loads((target/'experimental_rows.json').read_text())
        if rows!=expected:raise AssertionError('cold experimental predictions differ')
        actual=(target/'experimental_output.csv').read_bytes()
        if actual!=(ROOT/'output.csv').read_bytes():raise AssertionError('combination unexpectedly differs from protected baseline')
        report=dict(cold_cache=True,fresh_source_copy=True,different_cwd=True,byte_identical_to_baseline=True,sha256=hashlib.sha256(actual).hexdigest(),runtime_seconds=time.perf_counter()-start,usage=json.loads(p.stdout))
    (ROOT/'.ghostgraph/v3/reproducibility.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
