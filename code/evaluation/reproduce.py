"""Check cold-cache output in a fresh directory with the same installed runtime."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def reproduce(root):
    expected=(root/'output.candidate.csv').read_bytes()
    with tempfile.TemporaryDirectory(prefix='ghostgraph-repro-') as folder:
        target=Path(folder)
        shutil.copytree(root/'code',target/'code',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(root/'dataset',target/'dataset')
        shutil.copy2(root/'README.md',target/'README.md')
        start=time.perf_counter()
        process=subprocess.run([sys.executable,str(target/'code/main.py'),'--allow-unresolved'],
                               cwd=target.parent,capture_output=True,text=True,timeout=180)
        if process.returncode:
            raise RuntimeError(process.stderr)
        actual=(target/'output.candidate.csv').read_bytes()
        assert actual==expected,'fresh-directory candidate differs'
        run=json.loads((target/'.ghostgraph/full_run.json').read_text())
        stats={'fresh_directory':True,'same_installed_runtime':True,'different_working_directory':True,
               'empty_extraction_cache':True,'byte_identical_candidate':True,
               'candidate_sha256':hashlib.sha256(actual).hexdigest(),
               'runtime_seconds':time.perf_counter()-start,'document_extraction':run['document_extraction'],
               'unresolved_cases':run['unresolved_cases'],'request_count':run['request_count']}
        (root/'.ghostgraph/reproducibility.json').write_text(json.dumps(stats,indent=2))
        print(json.dumps(stats,indent=2))
        return stats


if __name__=='__main__':reproduce(Path(__file__).resolve().parents[2])
