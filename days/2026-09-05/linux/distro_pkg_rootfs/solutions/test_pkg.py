import tempfile, json
from pathlib import Path
from chris_pkg import load_manifest, install_package
with tempfile.TemporaryDirectory() as td:
    t=Path(td); pkg=t/'pkg'; (pkg/'payload/bin').mkdir(parents=True)
    (pkg/'payload/bin/hello').write_text('hello\n')
    (pkg/'manifest.json').write_text(json.dumps({'name':'hello','version':'1.0.0','files':['bin/hello']}))
    m=load_manifest(pkg/'manifest.json'); assert m['name']=='hello'
    root=t/'root'; install_package(pkg,root)
    assert (root/'bin/hello').read_text()=='hello\n'
    db=json.loads((root/'var/lib/chris-pkg/installed.json').read_text()); assert db['hello']=='1.0.0'
    (pkg/'manifest.json').write_text(json.dumps({'name':'x','version':'1','files':['../escape']}))
    try: load_manifest(pkg/'manifest.json'); raise AssertionError('unsafe path accepted')
    except ValueError: pass
print('OK pkg')
