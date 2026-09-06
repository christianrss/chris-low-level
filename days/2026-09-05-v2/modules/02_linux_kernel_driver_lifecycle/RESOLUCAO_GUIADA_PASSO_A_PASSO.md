## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| `KMOD-SOURCE-REVIEW-03` | `starter/chris_char.c` |
| `KMOD-MODEL-OPEN-01` | `starter/device_model.c` |
| `KMOD-MODEL-IO-02` | `starter/device_model.c` |

# Resolução guiada passo a passo

## Parte A - open/release
Abra `starter/device_model.c`, função `device_open`. Para `KMOD-MODEL-OPEN-01`:

```c
if (d->is_open) return -1;
d->is_open = 1;
return 0;
```

Compile e rode. O teste vai avançar até I/O.

## Parte B - write/read
Em `device_write`, rejeite dispositivo fechado, limite `n` a `sizeof d->buffer`, copie e atualize `d->length`. Em `device_read`, limite `n` a `d->length` e copie para `out`. Isso fecha `KMOD-MODEL-IO-02`.

Build:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

## Parte C - revisão real
Abra `starter/chris_char.c` e `starter/ANSWERS_TEMPLATE.md`. Não execute `insmod`. Para `KMOD-SOURCE-REVIEW-03`, registre que `misc_register(&chris_dev)` é desfeito por `misc_deregister(&chris_dev)`. Explique que init/exit simétricos evitam recursos registrados sobreviverem ao unload.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/chris_char.c` |
| **Função / âncora** | comentário `TODO [KMOD-SOURCE-REVIEW-03]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [KMOD-SOURCE-REVIEW-03]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |

## Debug
Se read/write falhar, inspecione `is_open`, `length` e `n`. Se houver overflow, confirme o limite antes do `memcpy`.

## Mapa de consistência auditada
- `KMOD-MODEL-OPEN-01` - starter -> resolução -> teste -> solution.
- `KMOD-MODEL-IO-02` - starter -> resolução -> teste -> solution.
- `KMOD-SOURCE-REVIEW-03` - starter -> resolução -> teste -> solution.
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)

### 4. Por que funciona

O stub no âncora TODO é substituído pelo comportamento testado.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.
