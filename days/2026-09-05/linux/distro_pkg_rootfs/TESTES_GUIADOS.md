# Testes guiados

### Caso 1: `python starter/test_pkg.py` — deve falhar com TODOs abertos; imprime `OK linux package` na solution.
### Caso 2: `sh starter/test_rootfs.sh` — valida idempotência do builder (duas execuções).
### Caso 3: **Regressão path traversal:** manifest com `../escape` → `ValueError`.
### Caso 4: **Regressão arquivo ausente:** manifest lista `bin/missing` → `FileNotFoundError` e rollback (nenhum arquivo copiado, banco ausente).
### Caso 5: **Rollback transacional:** se a segunda cópia falha, a primeira também é revertida.
### Caso 6: Valide `solutions/` com os mesmos comandos após implementar.

## LINUX-ROOTFS-BUILD-03

Invariante protegida pelo teste com `PEDAGOGY-TEST: LINUX-ROOTFS-BUILD-03`.

## LINUX-PKG-INSTALL-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: LINUX-PKG-INSTALL-02`.

## LINUX-PKG-PARSE-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: LINUX-PKG-PARSE-01`.
## Execução real (opcional)

**Pré-requisitos:** Linux, `bash`, permissão para criar diretórios temporários.

```bash
python scripts/run_real_env_checklist.py --module linux/distro_pkg_rootfs --day 2026-09-05
```
