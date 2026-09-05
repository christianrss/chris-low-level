# Resolução guiada passo a passo — Linux kernel: lifecycle de char device + módulo real para revisão

## Parte A — `device_open`
Abra `starter/device_model.c`, função `device_open`.
```c
if (dev->is_open) return -1;
dev->is_open = 1;
return 0;
```
Isso implementa `KMOD-MODEL-OPEN-01`. Compile e rode; o teste de double-open deve passar, mas I/O ainda falhará.

## Parte B — read/write
Em `device_write`, primeiro valide estado, limite `count` ao tamanho do buffer, copie e atualize `length`.
```c
if (!dev->is_open) return -1;
if (count > sizeof dev->buffer) count = sizeof dev->buffer;
memcpy(dev->buffer, src, count);
dev->length = count;
return (int)count;
```
Em `device_read`:
```c
if (!dev->is_open) return -1;
if (count > dev->length) count = dev->length;
memcpy(dst, dev->buffer, count);
return (int)count;
```
Isso fecha `KMOD-MODEL-IO-02`.

## Parte C — revisão do módulo real
Abra `starter/chris_char.c`. NÃO execute `insmod` aqui. Localize: `module_init`, `module_exit`, `misc_register`, `misc_deregister` e `file_operations`. Para `KMOD-SOURCE-REVIEW-03`, escreva em `ANSWERS.md` qual recurso adquirido no init é liberado no exit e por que essa simetria importa.

Build do modelo portátil:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```
A solution deve passar 100%.

## Mapa de consistência auditada
- `KMOD-MODEL-OPEN-01` — starter → resolução → teste → solution.
- `KMOD-MODEL-IO-02` — starter → resolução → teste → solution.
- `KMOD-SOURCE-REVIEW-03` — starter → resolução → teste → solution.
