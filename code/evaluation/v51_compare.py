"""Three-source regression comparison; public answers are evaluator-only.

Historical checkouts are copied by git archive, not modified. Warm extraction
caches may be reused here; separate ZIP acceptance checks use empty caches.
"""
import io,json,shutil,subprocess,sys,tarfile,tempfile,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def child(root,output):
    sys.path.insert(0,str(root/'code'))
    import main as application
    from ghostgraph.contract import read_csv,check_rows,resource_registry,write_csv
    from ghostgraph.evidence import EvidenceStore
    from ghostgraph.identity import IdentityIndex
    from ghostgraph.prediction import PredictionAuditor
    from evaluation.main import metrics
    store=EvidenceStore(root/'dataset',root/'.ghostgraph/extraction').load();assert not store.failures
    result={}
    for name,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]:
        q=read_csv(root/'dataset'/file);model=application.IntentClassifier()
        auditor=PredictionAuditor(store,IdentityIndex(root/'dataset',store),model);start=time.perf_counter()
        pairs=[auditor.audit(r) for r in sorted(q,key=lambda r:r['case_id'])];rows,ds=map(list,zip(*pairs))
        result[name]=dict(rows=rows,calls=model.calls,cache_hits=model.cache_hits,runtime_seconds=time.perf_counter()-start,
            violations=check_rows(rows,q,store.citation_times,known_resource_pairs=resource_registry(store)),
            unresolved=sum(bool(d['issues']) for d in ds))
        if name=='sample':result[name]['metrics']=metrics(rows,read_csv(root/'dataset/sample_output.csv'))
        write_csv(output.with_name(output.stem+'_'+name+'.csv'),rows)
    output.write_text(json.dumps(result,indent=2))

def main():
    cache=ROOT/'.ghostgraph/v51';cache.mkdir(parents=True,exist_ok=True);results={}
    for arm,ref in [('frozen','3b942ac'),('v5','08e975b'),('v51',None)]:
        stage=Path(tempfile.mkdtemp(prefix='v51-compare-'+arm+'-'))
        if ref:
            content=subprocess.check_output(['git','archive',ref,'code'],cwd=ROOT)
            with tarfile.open(fileobj=io.BytesIO(content)) as archive:archive.extractall(stage,filter='data')
        else:shutil.copytree(ROOT/'code',stage/'code',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'dataset',stage/'dataset')
        if (ROOT/'.ghostgraph/extraction').exists():
            shutil.copytree(ROOT/'.ghostgraph/extraction',stage/'.ghostgraph/extraction')
        output=cache/(arm+'.json')
        subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',str(stage),str(output)],check=True)
        results[arm]=json.loads(output.read_text())
    summary={}
    for arm,result in results.items():
        summary[arm]={name:{k:v for k,v in run.items() if k not in ['rows','metrics']} for name,run in result.items()}
        summary[arm]['sample']['metrics']={k:v for k,v in result['sample']['metrics'].items() if k!='mismatches'}
        for name in ['sample','full']:
            summary[arm][name]['changed_vs_frozen']=[r['case_id'] for r,b in zip(result[name]['rows'],results['frozen'][name]['rows']) if r!=b]
    summary['full_byte_identical_to_protected']={arm:(cache/(arm+'_full.csv')).read_bytes()==(ROOT/'output.csv').read_bytes() for arm in results}
    (cache/'comparison.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--child':child(Path(sys.argv[2]),Path(sys.argv[3]))
    else:main()
