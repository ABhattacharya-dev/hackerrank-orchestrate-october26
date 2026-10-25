from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.v5_intent import AuthorizationIntent
from research.v5_probes import DEVELOPMENT
from research.v4_intent import PROBES
ROOT=Path(__file__).resolve().parents[2]
def decision(r):return None if r['low_confidence'] or r.get('ambiguous') else r['authorized']
def main():
    model=AuthorizationIntent()
    for dataset,probes in [('development',DEVELOPMENT),('known_v4',PROBES)]:
        failures=[]
        for name,text,expected in probes:
            r=model.classify(text)
            if decision(r)!=expected:failures.append(dict(id=name,text=text,expected=expected,predicted=decision(r),reason=r['decision_source']))
        print(dataset,len(probes)-len(failures),'/',len(probes),json.dumps(failures,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
