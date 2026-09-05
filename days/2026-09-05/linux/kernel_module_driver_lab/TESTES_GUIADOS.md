# Testes guiados

### Caso 1: Compile e execute `test_device_model` em starter/ (falha até implementar TODOs).
### Caso 2: Ative trace: `device_set_trace(1)` imprime `[kmod-trace]` no stderr.
### Caso 3: **Double-open:** segundo `device_open` retorna -1.
### Caso 4: **I/O fechado:** `device_read` após `device_release` retorna -1.
### Caso 5: Revise `chris_char.c` com `REVIEW_RUBRIC.md` (KMOD-SOURCE-REVIEW-03).
### Caso 6: Valide solutions/ com os mesmos asserts.

## KMOD-MODEL-OPEN-01

Invariante protegida pelo teste com `PEDAGOGY-TEST: KMOD-MODEL-OPEN-01`.

## KMOD-MODEL-IO-02

Invariante protegida pelo teste com `PEDAGOGY-TEST: KMOD-MODEL-IO-02`.
## Execução real (opcional)

**Pré-requisitos:** Linux com headers do kernel, `build-essential`, VM recomendada.

```bash
python scripts/run_real_env_checklist.py --module linux/kernel_module_driver_lab --day 2026-09-05
```

Correlacione `device_set_trace(1)` no userspace com `dmesg` após `insmod`.
