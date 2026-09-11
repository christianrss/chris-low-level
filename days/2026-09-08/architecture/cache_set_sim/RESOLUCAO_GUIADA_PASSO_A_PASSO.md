# Resolucao guiada — cache_set_sim

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D6-CACHE-DECODE` | `starter/src/cache.cpp` | `l` |
| `D6-CACHE-HIT` | `starter/src/cache.cpp` | `CacheSim` |
| `D6-CACHE-EVICT` | `starter/src/cache.cpp` | `CacheSim` |


## Baseline

```powershell
cd days/2026-09-08/architecture/cache_set_sim/starter
cmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** FAIL.


## D6-CACHE-DECODE

### Onde colocar (D6-CACHE-DECODE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/cache.cpp` |
| Funcao | `l` |
| Substituir | corpo sob `TODO [D6-CACHE-DECODE]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-CACHE-DECODE` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-CACHE-DECODE` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```cpp
PEDAGOGY-SOLUTION: D6-CACHE-DECODE
 auto block=address/line_size_; auto si=block%sets_.size(); auto tag=block/sets_.size(); auto& set=sets_[si];
 // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-CACHE-DECODE`.

### Verifique
Rode o baseline; o caminho de `D6-CACHE-DECODE` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-CACHE-DECODE` PASS
- [ ] Nao alterei o teste

## D6-CACHE-HIT

### Onde colocar (D6-CACHE-HIT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/cache.cpp` |
| Funcao | `CacheSim` |
| Substituir | corpo sob `TODO [D6-CACHE-HIT]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-CACHE-HIT` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-CACHE-HIT` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```cpp
PEDAGOGY-SOLUTION: D6-CACHE-HIT
 for(auto& line:set) if(line.valid&&line.tag==tag){++stats_.hits;line.last_used=++tick_;return true;}
 ++stats_.misses;
 // 
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-CACHE-HIT`.

### Verifique
Rode o baseline; o caminho de `D6-CACHE-HIT` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-CACHE-HIT` PASS
- [ ] Nao alterei o teste

## D6-CACHE-EVICT

### Onde colocar (D6-CACHE-EVICT)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/cache.cpp` |
| Funcao | `CacheSim` |
| Substituir | corpo sob `TODO [D6-CACHE-EVICT]` |
| Nao mexer | assinatura, testes, outros TODOs |

### O problema
Sem este passo o assert de `D6-CACHE-EVICT` falha.

### Algoritmo / trace
Use o Caso ligado a `D6-CACHE-EVICT` em TESTES_GUIADOS / saida do teste.

### Escreva o codigo

```cpp
PEDAGOGY-SOLUTION: D6-CACHE-EVICT
 Line* victim=nullptr;
 for(auto& line:set) if(!line.valid){victim=&line;break;}
 if(!victim){victim=&set[0];for(auto& line:set) if(line.last_used<victim->last_used) victim=&line;}
 victim->valid=true;victim->tag=tag;victim->last_used=++tick_;return false;
}
```


### Por que funciona?
O bloco acima materializa o contrato numerico do teste para `D6-CACHE-EVICT`.

### Verifique
Rode o baseline; o caminho de `D6-CACHE-EVICT` deve passar sem quebrar TODOs anteriores.

### Checkpoint
- [ ] `D6-CACHE-EVICT` PASS
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
