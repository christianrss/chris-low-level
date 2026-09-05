# Resolução guiada passo a passo — Linux — Ciclo de Vida de Driver

## Mapa exato starter → resolução

| TODO ID | Arquivo starter |
|---------|-----------------|
| `KMOD-MODEL-OPEN-01` | `starter/device_model.c` → `device_open` |
| `KMOD-MODEL-IO-02` | `starter/device_model.c` → `device_write`, `device_read` |
| `KMOD-SOURCE-REVIEW-03` | `starter/chris_char.c` (revisão de código, não compila no CI) |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-TEST: ID` em `test_device_model.c` e `PEDAGOGY-SOLUTION: ID` em `solutions/`.

> Trabalhe em `days/2026-09-05/linux/kernel_module_driver_lab/starter/`. Consulte `solutions/` só após tentativa honesta.

---

## 0. Baseline — build e teste antes dos TODOs

```bash
cd days/2026-09-05/linux/kernel_module_driver_lab/starter
cmake -S . -B build
cmake --build build
./build/test_device_model
```

**Esperado antes dos TODOs:** o programa compila, mas falha nos `assert` (open retorna -1, read/write falham). Isso confirma que o esqueleto está correto e só falta implementar.

---

## TODO `KMOD-MODEL-OPEN-01` — `device_open`

### Arquivo
Abra `starter/device_model.c` e localize:

```cpp
int device_open(Device* dev) {
    // TODO [KMOD-MODEL-OPEN-01]
    device_trace("open", dev);
    return -1;
}
```

### Código
Substitua o corpo (mantenha o trace **depois** de marcar aberto):

```cpp
int device_open(Device* dev) {
    if (dev->is_open) {
        return -1;
    }
    dev->is_open = 1;
    device_trace("open", dev);
    return 0;
}
```

### Por que funciona?
- **O quê:** garantir no máximo um "handle" lógico aberto por vez.
- **Como:** `is_open` é o guard; segundo `open` vê `1` e retorna erro sem alterar estado.
- **Por quê:** drivers reais precisam decidir explicitamente se permitem reentrância; este lab modela device **não reentrante**, como muitos dispositivos de hardware.

### Verificação manual
```text
device_open(&dev)  → 0, is_open=1
device_open(&dev)  → -1, is_open ainda 1
```

### Checkpoint
Recompile e rode `./build/test_device_model`. Os asserts das linhas 16–17 devem passar; read/write ainda falham.

---

## TODO `KMOD-MODEL-IO-02` — `device_write`

### Arquivo
Mesmo arquivo, função `device_write`:

```cpp
int device_write(Device* dev, const void* src, size_t count) {
    // TODO [KMOD-MODEL-IO-02]
```

### Código

```cpp
int device_write(Device* dev, const void* src, size_t count) {
    if (!dev->is_open) {
        return -1;
    }
    if (count > sizeof dev->buffer) {
        count = sizeof dev->buffer;
    }
    memcpy(dev->buffer, src, count);
    dev->length = count;
    device_trace("write", dev);
    return (int)count;
}
```

### Por que funciona?
- **O quê:** copiar bytes do caller para o buffer interno de 64 bytes.
- **Como:** rejeita I/O se fechado; trunca `count` para não estourar `buffer`.
- **Por quê:** no kernel, `copy_from_user` também valida tamanho — overflow em driver é vulnerabilidade clássica.

---

## TODO `KMOD-MODEL-IO-02` — `device_read`

### Código

```cpp
int device_read(Device* dev, void* dst, size_t count) {
    if (!dev->is_open) {
        return -1;
    }
    if (count > dev->length) {
        count = dev->length;
    }
    memcpy(dst, dev->buffer, count);
    device_trace("read", dev);
    return (int)count;
}
```

### Por que funciona?
- Só lê até `length` bytes válidos (o que foi escrito).
- Após `device_release`, `is_open` é 0 → próximo `read` retorna -1 (teste linha 23).

### Checkpoint
```bash
./build/test_device_model
```

**Esperado:** `OK kmod model`

Com trace:
```bash
# no código, device_set_trace(1) já está no main
./build/test_device_model 2>&1
```

Saída esperada no stderr:
```text
[kmod-trace] open open=1 len=0
[kmod-trace] write open=1 len=3
[kmod-trace] read open=1 len=3
[kmod-trace] release open=0 len=3
```

---

## TODO `KMOD-SOURCE-REVIEW-03` — Revisão de `chris_char.c`

### O quê
Não há compilação no Windows. Leia `starter/chris_char.c` e preencha a rubrica em `REVIEW_RUBRIC.md`.

### Como
1. Abra `starter/chris_char.c` lado a lado com `solutions/chris_char.c`.
2. Para cada linha da rubrica, marque 0/1/2.
3. Responda as 4 perguntas de review no Relatório de resolução.

### Por quê?
Código kernel exige `copy_to_user`, cleanup em `module_exit`, e `MODULE_LICENSE`. Revisar código **sem executar** treina leitura como em code review de equipe.

### Lacunas intencionais no starter (para você notar)
| Item | Presente? | Nota |
|------|-----------|------|
| `module_init` / `module_exit` | Sim | `misc_register` / `misc_deregister` |
| `read` / `write` em fops | **Não** | Só open/release |
| `copy_to_user` | **Não** | Buffer kernel ausente |
| Double-open no kernel | N/A | Modelado só em userspace |

### Evidência esperada
Checklist preenchido + correlação trace userspace ↔ fluxo mental do módulo.

---

## Debug — falhas comuns

| Mensagem / sintoma | Causa provável | Correção |
|--------------------|----------------|----------|
| `assert(device_open(&dev) == 0)` falha | Ainda retorna -1 | Implementar OPEN-01 |
| `assert(device_write(...) == 3)` falha | Não checa `is_open` ou não atualiza `length` | Revisar IO-02 |
| `memcmp` falha após read | `read` copia mais que `length` | Truncar `count` com `dev->length` |
| Trace mostra `open=0` no write | Trace antes de setar `is_open` | Ordem: setar flag → trace |

---

## Validação final

```bash
cmake --build build
./build/test_device_model
python ../../../../scripts/pedagogy_check_unified.py --day 2026-09-05
```

**Esperado:** `OK kmod model` e pedagogy check PASS para este módulo.

---

## Relatório de resolução

| Campo | Preencher |
|-------|-----------|
| TODOs concluídos | KMOD-MODEL-OPEN-01, KMOD-MODEL-IO-02, KMOD-SOURCE-REVIEW-03 |
| Testes que falharam primeiro | |
| Bug mais difícil | |
| Tempo estimado | |
| O que aprendi | |

### Template

```
Aluno:
Módulo: linux/kernel_module_driver_lab
Data:

1. TODOs: KMOD-MODEL-OPEN-01, KMOD-MODEL-IO-02, KMOD-SOURCE-REVIEW-03
2. Primeira falha: [ex.: open sempre -1]
3. Correção aplicada: [ex.: guard is_open em device_open]
4. Rubrica chris_char: [notas 0-2 por critério]
5. Evidência: OK kmod model + trace stderr
```
