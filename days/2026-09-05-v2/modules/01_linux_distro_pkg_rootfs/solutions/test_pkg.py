# TESTS [LINUX-PKG-PARSE-01] [LINUX-PKG-INSTALL-02]
from pathlib import Path
from tempfile import TemporaryDirectory
import json, sys
sys.path.insert(0,str(Path(__file__).parent))
from chris_pkg import load_manifest, install_package
with TemporaryDirectory() as td:
    t=Path(td); pkg=t/'pkg'; (pkg/'payload/usr/share').mkdir(parents=True)
    (pkg/'payload/usr/share/hello.txt').write_text('hello')
    (pkg/'manifest.json').write_text(json.dumps({'name':'hello','version':'1.0','files':['usr/share/hello.txt']}))
    m=load_manifest(pkg/'manifest.json'); assert m['name']=='hello'
    root=t/'root'; install_package(pkg,root)
    assert (root/'usr/share/hello.txt').read_text()=='hello'
    db=json.loads((root/'var/lib/chris-pkg/installed.json').read_text()); assert db['hello']=='1.0'
    (pkg/'manifest.json').write_text(json.dumps({'name':'bad','version':'1','files':['../escape']}))
    try: load_manifest(pkg/'manifest.json'); raise AssertionError('unsafe path accepted')
    except ValueError: pass
print('OK linux package')
