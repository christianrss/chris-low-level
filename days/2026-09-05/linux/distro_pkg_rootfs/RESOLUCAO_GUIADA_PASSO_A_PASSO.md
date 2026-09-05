# Resolução guiada passo a passo — Linux distro: pacote próprio + rootfs reproduzível

## Parte A — parser do manifest
Abra `starter/chris_pkg.py` e localize `load_manifest()`.

1. Leia JSON com `Path.read_text(encoding="utf-8")`.
2. Valide que `name` e `version` são strings não vazias e que `files` é lista.
3. Rejeite caminhos absolutos e qualquer componente `..`.
4. Retorne o dicionário validado.

Substitua o TODO `LINUX-PKG-PARSE-01` pelo bloco:
```python
data = json.loads(path.read_text(encoding="utf-8"))
if not isinstance(data.get("name"), str) or not data["name"]:
    raise ValueError("invalid package name")
if not isinstance(data.get("version"), str) or not data["version"]:
    raise ValueError("invalid package version")
files = data.get("files")
if not isinstance(files, list):
    raise ValueError("files must be a list")
for item in files:
    rel = Path(item)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe path: {item}")
return data
```
Execute `python starter/test_pkg.py`. O parser válido deve avançar; o teste de instalação ainda deve falhar.

## Parte B — instalação transacional mínima
Ainda em `starter/chris_pkg.py`, localize `install_package()`.

1. Chame `load_manifest()` antes de tocar no rootfs.
2. Para cada caminho, resolva `payload/<rel>` e `<root>/<rel>`.
3. Exija que a origem exista e seja arquivo.
4. Crie o diretório pai e copie com `shutil.copy2`.
5. Atualize `var/lib/chris-pkg/installed.json` **depois** das cópias.

Use:
```python
manifest = load_manifest(package_dir / "manifest.json")
for item in manifest["files"]:
    src = package_dir / "payload" / item
    dst = root / item
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

db_path = root / "var/lib/chris-pkg/installed.json"
db_path.parent.mkdir(parents=True, exist_ok=True)
db = json.loads(db_path.read_text()) if db_path.exists() else {}
db[manifest["name"]] = manifest["version"]
db_path.write_text(json.dumps(db, indent=2, sort_keys=True)+"\n")
```

## Parte C — rootfs por shell
Abra `starter/build_rootfs.sh` e substitua `LINUX-ROOTFS-BUILD-03` por um loop que crie os diretórios exatos:
```sh
for d in bin etc proc sys dev tmp var/lib/chris-pkg; do
    mkdir -p "$ROOT/$d"
done
```
Rode duas vezes; a segunda execução deve continuar com exit code 0. Isso demonstra **idempotência**.

## Mapa de consistência auditada
- `LINUX-PKG-PARSE-01` — starter → resolução → teste → solution.
- `LINUX-PKG-INSTALL-02` — starter → resolução → teste → solution.
- `LINUX-ROOTFS-BUILD-03` — starter → resolução → teste → solution.
