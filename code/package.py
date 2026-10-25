"""Deterministic source-only submission archive with explicit exclusions."""

from pathlib import Path
import zipfile


# Historical snapshots remain in Git for audit, not in the submission runtime.
RESEARCH_ARCHIVE_ONLY = {'v5_round1.py', 'v5_round2_evaluated.py',
                         'v5_round2_integrated.py', 'v5_evaluate_round2.py'}


def package(root, destination=None):
    files=[root/name for name in ['README.md','AGENTS.md','problem_statement.md','agent_trace_instructions.md']]
    files += [p for p in (root/'code').rglob('*') if p.is_file()
              and p.suffix in {'.py','.md','.txt','.toml'}
              and not (p.parent.name=='research' and p.name in RESEARCH_ARCHIVE_ONLY)
              and not any(part in {'__pycache__','.venv','venv','node_modules','.git'} for part in p.parts)]
    required={'README.md','code/main.py','code/AGENTS.md','code/ARCHITECTURE.md',
              'code/evaluation/evaluation_report.md','code/evaluation/usage_report.md',
              'code/ghostgraph/authorization.py'}
    names={p.relative_to(root).as_posix() for p in files}
    assert required<=names, 'missing required source/reports'
    destination=Path(destination) if destination is not None else root/'code.zip'
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(files):
            name=path.relative_to(root).as_posix()
            assert not name.startswith('dataset/')
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,path.read_bytes())
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist())==names
    print(f'Packaged {len(files)} source/documentation files into {destination}')
    return destination


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='explicit proposed archive path; default code.zip')
    args=parser.parse_args()
    package(Path(__file__).resolve().parents[1],args.output)
