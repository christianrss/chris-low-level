# Resolução guiada passo a passo — Distribuição Linux — Pacotes e Rootfs

## Mapa exato starter → resolução

- `LINUX-PKG-PARSE-01` → `starter/chris_pkg.py` (`load_manifest`)
- `LINUX-PKG-INSTALL-02` → `starter/chris_pkg.py` (`install_package`)
- `LINUX-ROOTFS-BUILD-03` → `starter/build_rootfs.sh`

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-05/linux/distro_pkg_rootfs/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto

Na raiz do repositório:

```bash
cd days/2026-09-05/linux/distro_pkg_rootfs/starter
python test_pkg.py
```

Saída esperada no baseline: `NotImplementedError` para `LINUX-PKG-PARSE-01` ou `LINUX-PKG-INSTALL-02`. Esse é o ponto de partida.

```bash
sh test_rootfs.sh
```

Com o TODO aberto, o script falha porque os diretórios FHS não existem.

## Exercício fácil — `LINUX-ROOTFS-BUILD-03`

### Arquivo

Abra `starter/build_rootfs.sh`. Descomente e complete o loop:

```sh
for d in bin etc proc sys dev tmp var/lib/chris-pkg; do
    mkdir -p "$ROOT/$d"
done
```

### Por que funciona?

`mkdir -p` cria a cadeia inteira (`var/lib/chris-pkg`) e não reclama se o diretório já existe. Duas execuções seguidas produzem o mesmo resultado — idempotência exigida por `test_rootfs.sh`.

### Verificação

```bash
sh test_rootfs.sh
```

Saída esperada: `OK rootfs`

## Exercício médio — `LINUX-PKG-PARSE-01`

### Arquivo

Abra `starter/chris_pkg.py`, localize `load_manifest`.

Substitua o corpo por:

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
    if not isinstance(item, str):
        raise ValueError("file path must be string")
    rel = Path(item)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe path: {item}")

return data
```

### Por que funciona?

- `json.loads` falha cedo se o arquivo não é JSON válido.
- Tipos errados viram `ValueError` com mensagens distintas — facilita debug nos testes.
- `Path(item).parts` decompõe `../escape` em `('..', 'escape')`; a presença de `..` bloqueia traversal sem depender de string hacks.
- Caminhos absolutos (`/etc/passwd`) são rejeitados por `is_absolute()`.

### Trace no papel

Manifest `{"name":"bad","version":"1","files":["../escape"]}`:

```text
rel = Path("../escape")
".." in ('..', 'escape') → ValueError
```

### Verificação parcial

```bash
python test_pkg.py
```

`test_rejects_path_traversal` passa; os outros ainda falham até `install_package`.

## Exercício difícil — `LINUX-PKG-INSTALL-02`

### Arquivo

No mesmo `chris_pkg.py`, localize `install_package`.

### Passo 1 — recarregar manifest e montar plano

```python
manifest = load_manifest(package_dir / "manifest.json")
plan: list[tuple[Path, Path]] = []

for item in manifest["files"]:
    src = package_dir / "payload" / item
    dst = root / item
    if not src.is_file():
        raise FileNotFoundError(src)
    plan.append((src, dst))
```

Validar `src` antes do loop de cópia garante que o plano inteiro é executável ou nenhum arquivo é escrito (exceto se você já copiou antes de validar — por isso validamos na montagem).

### Passo 2 — copiar com rollback

```python
installed: list[Path] = []
try:
    for src, dst in plan:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        installed.append(dst)

    db_path = root / "var/lib/chris-pkg/installed.json"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = (
        json.loads(db_path.read_text(encoding="utf-8"))
        if db_path.exists()
        else {}
    )
    db[manifest["name"]] = manifest["version"]
    db_path.write_text(
        json.dumps(db, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
except Exception:
    for dst in installed:
        if dst.exists():
            dst.unlink()
    raise

return manifest
```

### Por que funciona?

- `installed` registra apenas destinos copiados **nesta** execução.
- O banco só é gravado após todas as cópias — invariante transacional.
- `except` percorre `installed` de trás para frente ou em qualquer ordem: cada `unlink` remove o artefato parcial.
- Mesclar JSON existente preserva outros pacotes já instalados.

### Trace de rollback

`files: ["bin/ok", "bin/missing"]`, só `bin/ok` no payload:

```text
copia bin/ok → installed = [root/bin/ok]
FileNotFoundError em bin/missing
except: unlink root/bin/ok
db_path nunca foi escrito
```

## Rode os testes novamente

```bash
python test_pkg.py
sh test_rootfs.sh
```

Saída esperada:

```text
OK linux package
OK rootfs
```

## Como depurar se falhar

- **`unsafe path accepted`:** verifique `".." in rel.parts`, não só `startswith`.
- **`bin/ok` existe após rollback:** o `except` não está iterando `installed`, ou a cópia ocorre antes da validação de `src`.
- **`installed.json` ausente no happy path:** `db_path.parent.mkdir` faltando ou exceção silenciosa antes do write.
- **`KeyError` no banco:** você sobrescreveu o JSON em vez de mesclar.

Inspecione estado com prints temporários:

```python
print("plan", plan)
print("installed", installed)
```

Remova antes de entregar.

## Solução final comentada

Compare com `solutions/chris_pkg.py` e `solutions/build_rootfs.sh`. Você deve justificar: ordem validar→copiar→registrar, checagem de `src.is_file()`, e rollback no `except`.

## Relatório de resolução

| ID | Arquivo | Resultado esperado |
|----|---------|-------------------|
| LINUX-PKG-PARSE-01 | `chris_pkg.py` | JSON válido; paths absolutos e `..` → `ValueError` |
| LINUX-PKG-INSTALL-02 | `chris_pkg.py` | cópia + banco; rollback se `FileNotFoundError` |
| LINUX-ROOTFS-BUILD-03 | `build_rootfs.sh` | 7 diretórios FHS; idempotente em 2 execuções |

Critério de aceite: `python test_pkg.py` imprime `OK linux package` e `sh test_rootfs.sh` imprime `OK rootfs`. Se rollback falhar, revise se o banco é gravado **depois** do loop de cópia, não antes.
