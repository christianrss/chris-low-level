# Resolução guiada passo a passo

## Parte A - parser do manifest
Abra `starter/chris_pkg.py` e localize `load_manifest(path: Path)`. O TODO é `LINUX-PKG-PARSE-01`. Primeiro leia o JSON, depois valide tipos e só então valide caminhos.

```python
data = json.loads(path.read_text(encoding="utf-8"))
if not isinstance(data.get("name"), str) or not data["name"]:
    raise ValueError("invalid package name")
if not isinstance(data.get("version"), str) or not data["version"]:
    raise ValueError("invalid package version")
files = data.get("files")
if not isinstance(files, list):
    raise ValueError("files must be a list")
```

Agora percorra `files`. Para cada item, construa `Path(item)` e rejeite `is_absolute()` ou `".." in rel.parts`. Rode `python3 starter/test_pkg.py`. Neste ponto o teste ainda deve falhar na instalação; isso é esperado.

## Parte B - instalação
Ainda em `starter/chris_pkg.py`, implemente `install_package()`. Chame `load_manifest()` antes de criar qualquer arquivo. Monte uma lista `plan` de pares `(src, dst)` e confirme que todas as fontes existem. Só depois execute as cópias e atualize `installed.json`. Esse passo corresponde a `LINUX-PKG-INSTALL-02`.

## Parte C - rootfs
Abra `starter/build_rootfs.sh`. Substitua `LINUX-ROOTFS-BUILD-03` por:

```sh
for d in bin etc proc sys dev tmp var/lib/chris-pkg; do
    mkdir -p "$ROOT/$d"
done
```

Rode `sh starter/test_rootfs.sh`. O teste executa o builder duas vezes e verifica os diretórios.

## Debug
Se o teste de pacote falhar, imprima temporariamente `manifest`, `src` e `dst`. Se um caminho inseguro for aceito, examine `Path(item).parts`. Remova prints de debug ao finalizar.

## Mapa de consistência auditada
- `LINUX-PKG-PARSE-01` - starter -> resolução -> teste -> solution.
- `LINUX-PKG-INSTALL-02` - starter -> resolução -> teste -> solution.
- `LINUX-ROOTFS-BUILD-03` - starter -> resolução -> teste -> solution.
