"""Deterministic source-only submission archive with explicit exclusions."""

from pathlib import Path
import zipfile


def package(root):
    files=[root/name for name in ['README.md','AGENTS.md','problem_statement.md','agent_trace_instructions.md']]
    files += [p for p in (root/'code').rglob('*') if p.is_file()
              and p.suffix in {'.py','.md','.txt','.toml'}
              and not any(part in {'__pycache__','.venv','venv','node_modules','.git'} for part in p.parts)]
    required={'README.md','code/main.py','code/AGENTS.md','code/ARCHITECTURE.md',
              'code/evaluation/evaluation_report.md','code/evaluation/usage_report.md'}
    names={p.relative_to(root).as_posix() for p in files}
    assert required<=names, 'missing required source/reports'
    destination=root/'code.zip'
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
    print(f'Packaged {len(files)} source/documentation files into code.zip')
    return destination


if __name__=='__main__':package(Path(__file__).resolve().parents[1])
