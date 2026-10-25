"""Source/ZIP acceptance with fresh cache and optional newly installed Python.

Writes only ignored verification files and temporary roots. Production artifacts
are compared, never overwritten. Run once on source, then on the proposed ZIP.
"""
import argparse,hashlib,json,os,shutil,subprocess,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def verify(python,archive=None):
    root=Path(tempfile.mkdtemp(prefix='ghostgraph-v51-acceptance-'))
    if archive:
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for name in z.namelist():
                p=Path(name)
                assert not p.is_absolute() and '..' not in p.parts
                assert not (p.parts[0]=='dataset' or p.suffix in {'.zip','.env','.jsonl','.sqlite'} or set(p.parts)&{'.git','.venv','__pycache__'})
            z.extractall(root)
    else:
        shutil.copytree(ROOT/'code',root/'code',ignore=shutil.ignore_patterns('__pycache__'))
        for name in ['README.md','AGENTS.md','problem_statement.md','agent_trace_instructions.md']:shutil.copy2(ROOT/name,root/name)
    shutil.copytree(ROOT/'dataset',root/'dataset')
    env=os.environ.copy()
    # Verification cannot accidentally enable an optional paid extraction adapter.
    for key in list(env):
        if key=='OPENAI_API_KEY' or key.startswith('GHOSTGRAPH_VISION'):env.pop(key)
    def run(args,**kw):return subprocess.run([str(python)]+args,cwd=root,env=env,capture_output=True,text=True,**kw)
    p=run(['code/main.py','--mode','predict']);assert p.returncode==0,(p.stdout,p.stderr)
    output=(root/'output.csv').read_bytes();assert output==(ROOT/'output.csv').read_bytes()
    usage=json.loads((root/'.ghostgraph/full_run.json').read_text())
    # Also run the production entry point with the entire research tree absent.
    research=root/'code/research';held=root/'research-disabled'
    if research.exists():research.rename(held)
    try:
        no_research=run(['code/main.py','--mode','predict','--output','no-research.csv'])
        assert no_research.returncode==0,no_research.stderr
        assert (root/'no-research.csv').read_bytes()==output
    finally:
        if held.exists():held.rename(research)
    env['PYTHONPATH']='code'
    tests=run(['-m','unittest','discover','-s','code/tests','-v']);assert tests.returncode==0,tests.stderr
    strict=run(['code/main.py','--mode','certify','--output','certified.csv'])
    assert strict.returncode==2 and not (root/'certified.csv').exists(),strict.stderr
    assert 'unresolved cases' in strict.stderr,strict.stderr
    cache=ROOT/'.ghostgraph/v51';cache.mkdir(parents=True,exist_ok=True)
    label='zip' if archive else 'source'
    (cache/(label+'_tests.txt')).write_text(tests.stderr)
    python_environment=json.loads(run(['-c','import sys,json; print(json.dumps(dict(executable=sys.executable,prefix=sys.prefix)))']).stdout)
    result=dict(root=str(root),python=str(python),python_environment=python_environment,archive=str(archive) if archive else None,
        crc='PASS' if archive else None,output_sha256=hashlib.sha256(output).hexdigest(),
        byte_identical=True,fresh_extraction_cache=True,normal_cli_exit=p.returncode,
        runtime_without_research=True,strict_exit=strict.returncode,strict_message=strict.stderr.strip(),
        tests=tests.stderr.split('----------------------------------------------------------------------')[-1].strip(),usage=usage,
        paid_key_available_to_cli=False)
    (cache/(label+'_acceptance.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='usage'},indent=2))

if __name__=='__main__':
    import sys
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python',type=Path,default=Path(sys.executable))
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args();verify(args.python.absolute(),args.archive.resolve() if args.archive else None)
