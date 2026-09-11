# Resolucao guiada — spsc_ring_buffer

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-SPSC-PUSH` | `starter/src/spsc.cpp` | `capacity` |
| `D6-SPSC-POP` | `starter/src/spsc.cpp` | `SpscRing` |
| `D6-SPSC-SIZE` | `starter/src/spsc.cpp` | `SpscRing` |


## Baseline

```powershell
cd days/2026-09-08/systems/spsc_ring_buffer/starter
cmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** FAIL.


## D6-SPSC-PUSH

### Onde colocar (D6-SPSC-PUSH)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/spsc.cpp` |
| Funcao | `capacity` |
| Substituir | corpo sob `TODO [D6-SPSC-PUSH]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-SPSC-PUSH` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-SPSC-PUSH` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```cpp
PEDAGOGY-SOLUTION: D6-SPSC-PUSH
 auto head=head_.load(std::memory_order_relaxed);
 auto next=(head+1)%storage_.size();
 if(next==tail_.load(std::memory_order_acquire)) return false;
 storage_[head]=value;
 head_.store(next,std::memory_order_release);
 return true;
}
bool SpscRing::pop(int& out){
 // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-SPSC-PUSH`.

### Verifique
Rode o baseline; o caminho de `D6-SPSC-PUSH` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-SPSC-PUSH` PASS
- [ ] Nao alterei o teste

## D6-SPSC-POP

### Onde colocar (D6-SPSC-POP)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/spsc.cpp` |
| Funcao | `SpscRing` |
| Substituir | corpo sob `TODO [D6-SPSC-POP]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-SPSC-POP` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-SPSC-POP` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```cpp
PEDAGOGY-SOLUTION: D6-SPSC-POP
 auto tail=tail_.load(std::memory_order_relaxed);
 if(tail==head_.load(std::memory_order_acquire)) return false;
 out=storage_[tail];
 tail_.store((tail+1)%storage_.size(),std::memory_order_release);
 return true;
}
std::size_t SpscRing::size_approx() const{
 // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-SPSC-POP`.

### Verifique
Rode o baseline; o caminho de `D6-SPSC-POP` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-SPSC-POP` PASS
- [ ] Nao alterei o teste

## D6-SPSC-SIZE

### Onde colocar (D6-SPSC-SIZE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/spsc.cpp` |
| Funcao | `SpscRing` |
| Substituir | corpo sob `TODO [D6-SPSC-SIZE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-SPSC-SIZE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-SPSC-SIZE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```cpp
PEDAGOGY-SOLUTION: D6-SPSC-SIZE
 auto h=head_.load(std::memory_order_acquire), t=tail_.load(std::memory_order_acquire);
 return h>=t ? h-t : storage_.size()-t+h;
}
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-SPSC-SIZE`.

### Verifique
Rode o baseline; o caminho de `D6-SPSC-SIZE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-SPSC-SIZE` PASS
- [ ] Nao alterei o teste

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco do TODO |
| off-by-one | size/indice | refaca o trace |
| 2o caso falha | estado residual | reset |

## Relatorio de resolucao

- TODOs concluidos:
- Comandos + saida:
- Invariantes:
- Edge cases:
- Benchmark: nao executado / preencher
