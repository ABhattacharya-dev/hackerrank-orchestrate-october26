"""Validate and reproduce the evaluated prediction submission, report actual usage."""
import hashlib,json,subprocess,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code'))
from evaluation.validate_output import validate

def main():
    count=validate(ROOT/'output.csv',ROOT/'dataset/deletion_requests.csv',ROOT/'dataset',check_registry=True)
    expected=(ROOT/'output.csv').read_bytes()
    with tempfile.TemporaryDirectory(prefix='ghostgraph-final-') as directory:
        clean=Path(directory);shutil.copytree(ROOT/'code',clean/'code',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'dataset',clean/'dataset')
        result=subprocess.run([sys.executable,str(clean/'code/main.py'),'--mode','predict'],cwd=clean.parent,capture_output=True,text=True)
        if result.returncode:raise RuntimeError(result.stderr)
        actual=(clean/'output.csv').read_bytes()
        if actual!=expected:raise AssertionError('cold prediction output differs')
        cold=json.loads((clean/'.ghostgraph/full_run.json').read_text())
    report=dict(rows=count,official_structural_violations=0,byte_identical=True,sha256=hashlib.sha256(expected).hexdigest(),cold_extraction=cold['document_extraction'],high_assurance_certified=False)
    (ROOT/'.ghostgraph/final_submission.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
