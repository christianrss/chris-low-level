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

## Debug
Se read/write falhar, inspecione `is_open`, `length` e `n`. Se houver overflow, confirme o limite antes do `memcpy`.

## Mapa de consistência auditada
- `KMOD-MODEL-OPEN-01` - starter -> resolução -> teste -> solution.
- `KMOD-MODEL-IO-02` - starter -> resolução -> teste -> solution.
- `KMOD-SOURCE-REVIEW-03` - starter -> resolução -> teste -> solution.
