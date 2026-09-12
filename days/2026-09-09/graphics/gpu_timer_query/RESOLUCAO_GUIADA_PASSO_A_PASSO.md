# Resolucao guiada — gpu_timer_query

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `GFX-TQ-BEGIN` | `starter/core/gpu_timer.cpp` | `GpuTimer::begin` |
| `GFX-TQ-END` | `starter/core/gpu_timer.cpp` | `GpuTimer::end` |
| `GFX-TQ-READ` | `starter/core/gpu_timer.cpp` | `GpuTimer::last_ms` |

## Baseline

```powershell
cd days/2026-09-09/graphics/gpu_timer_query/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** FAIL.


## GFX-TQ-BEGIN

### Onde colocar (GFX-TQ-BEGIN)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/gpu_timer.cpp` |
| Funcao | `GpuTimer::begin` |
| Substituir | corpo sob `TODO [GFX-TQ-BEGIN]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `GFX-TQ-BEGIN` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `GFX-TQ-BEGIN`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
running = true;
t0 = now_seconds;
(void)0;
```

### Por que funciona?
Materializa o contrato numerico de `GFX-TQ-BEGIN` usado pelo render.

### Verifique
Baseline parcial; `GFX-TQ-BEGIN` PASS.

### Checkpoint
- [ ] `GFX-TQ-BEGIN` PASS


## GFX-TQ-END

### Onde colocar (GFX-TQ-END)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/gpu_timer.cpp` |
| Funcao | `GpuTimer::end` |
| Substituir | corpo sob `TODO [GFX-TQ-END]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `GFX-TQ-END` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `GFX-TQ-END`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
if (!running) return;
last = (now_seconds - t0) * 1000.0;
running = false;
```

### Por que funciona?
Materializa o contrato numerico de `GFX-TQ-END` usado pelo render.

### Verifique
Baseline parcial; `GFX-TQ-END` PASS.

### Checkpoint
- [ ] `GFX-TQ-END` PASS


## GFX-TQ-READ

### Onde colocar (GFX-TQ-READ)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/gpu_timer.cpp` |
| Funcao | `GpuTimer::last_ms` |
| Substituir | corpo sob `TODO [GFX-TQ-READ]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `GFX-TQ-READ` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `GFX-TQ-READ`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
return last;
(void)0;
(void)0;
```

### Por que funciona?
Materializa o contrato numerico de `GFX-TQ-READ` usado pelo render.

### Verifique
Baseline parcial; `GFX-TQ-READ` PASS.

### Checkpoint
- [ ] `GFX-TQ-READ` PASS


## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | TODO intacto | cole o bloco |
| off-by-one | indices | refaca o trace |
| sem janela | backend errado | rode o `_sw` / `_gl` |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado
