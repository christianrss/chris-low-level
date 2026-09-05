# SOLVES [LINUX-PKG-PARSE-01]
# SOLVES [LINUX-PKG-INSTALL-02]
# SOLVES [LINUX-ROOTFS-BUILD-03]
import json, shutil
from pathlib import Path

def load_manifest(path: Path):
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("name"),str) or not data["name"]: raise ValueError("invalid package name")
    if not isinstance(data.get("version"),str) or not data["version"]: raise ValueError("invalid package version")
    files=data.get("files")
    if not isinstance(files,list): raise ValueError("files must be a list")
    for item in files:
        rel=Path(item)
        if rel.is_absolute() or ".." in rel.parts: raise ValueError(f"unsafe path: {item}")
    return data

def install_package(package_dir: Path, root: Path):
    manifest=load_manifest(package_dir/"manifest.json")
    for item in manifest["files"]:
        src=package_dir/"payload"/item; dst=root/item
        if not src.is_file(): raise FileNotFoundError(src)
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
    db_path=root/"var/lib/chris-pkg/installed.json"; db_path.parent.mkdir(parents=True,exist_ok=True)
    db=json.loads(db_path.read_text()) if db_path.exists() else {}
    db[manifest["name"]]=manifest["version"]
    db_path.write_text(json.dumps(db,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return manifest
