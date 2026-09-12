# Resolucao guiada — explicit_barriers

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `GFX-BAR-VALID` | `starter/core/barriers.cpp` | `can_transition` |
| `GFX-BAR-APPLY` | `starter/core/barriers.cpp` | `apply_barrier` |
| `GFX-BAR-TICK` | `starter/core/barriers.cpp` | `next_state` |

## Baseline

```powershell
cd days/2026-09-09/graphics/explicit_barriers/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** FAIL.


## GFX-BAR-VALID

### Onde colocar (GFX-BAR-VALID)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/barriers.cpp` |
| Funcao | `can_transition` |
| Substituir | corpo sob `TODO [GFX-BAR-VALID]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `GFX-BAR-VALID` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `GFX-BAR-VALID`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
if (from == ResourceState::Undefined && to == ResourceState::CopyDst) return true;
if (from == ResourceState::CopyDst && to == ResourceState::ShaderRead) return true;
return from == to;
```

### Por que funciona?
Materializa o contrato numerico de `GFX-BAR-VALID` usado pelo render.

### Verifique
Baseline parcial; `GFX-BAR-VALID` PASS.

### Checkpoint
- [ ] `GFX-BAR-VALID` PASS


## GFX-BAR-APPLY

### Onde colocar (GFX-BAR-APPLY)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/barriers.cpp` |
| Funcao | `apply_barrier` |
| Substituir | corpo sob `TODO [GFX-BAR-APPLY]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `GFX-BAR-APPLY` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `GFX-BAR-APPLY`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
if (!can_transition(r.state, to)) return false;
r.state = to;
return true;
```

### Por que funciona?
Materializa o contrato numerico de `GFX-BAR-APPLY` usado pelo render.

### Verifique
Baseline parcial; `GFX-BAR-APPLY` PASS.

### Checkpoint
- [ ] `GFX-BAR-APPLY` PASS


## GFX-BAR-TICK

### Onde colocar (GFX-BAR-TICK)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/core/barriers.cpp` |
| Funcao | `next_state` |
| Substituir | corpo sob `TODO [GFX-BAR-TICK]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `GFX-BAR-TICK` falha e a cena visual fica incompleta.

### Algoritmo / trace
1. Leia o PEDAGOGY-TEST de `GFX-BAR-TICK`.
2. Execute o Caso 1 no papel.
3. Cole o bloco abaixo no starter.

### Escreva o codigo

```cpp
if (s == ResourceState::Undefined) return ResourceState::CopyDst;
if (s == ResourceState::CopyDst) return ResourceState::ShaderRead;
return ResourceState::Present;
```

### Por que funciona?
Materializa o contrato numerico de `GFX-BAR-TICK` usado pelo render.

### Verifique
Baseline parcial; `GFX-BAR-TICK` PASS.

### Checkpoint
- [ ] `GFX-BAR-TICK` PASS


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
