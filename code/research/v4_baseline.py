"""V4 evaluation-only baseline, never writes protected artifacts."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import run
from evaluation.main import metrics
from ghostgraph.contract import read_csv
ROOT=Path(__file__).resolve().parents[2]
def main():
    cache=ROOT/'.ghostgraph/v4';cache.mkdir(parents=True,exist_ok=True)
    for tag,file in [('sample','sample_deletion_requests.csv'),('full','deletion_requests.csv')]:
        rows,ds,u=run(ROOT,ROOT/'dataset'/file,cache/(tag+'.csv'),allow_unresolved=True,tag='v4_'+tag,mode='predict')
        data=dict(rows=rows,diagnostics=ds,usage=u)
        if tag=='sample':data['metrics']=metrics(rows,read_csv(ROOT/'dataset/sample_output.csv'))
        (cache/(tag+'.json')).write_text(json.dumps(data,indent=2))
        print(tag,data.get('metrics',{}).get('counts',{}))
if __name__=='__main__':main()
