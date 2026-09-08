# Resolução guiada passo a passo — Set-associative cache simulator

Edite `starter/src/cache.cpp`.

### TODO D6-CACHE-DECODE
Em `access(address)`:
```cpp
auto block=address/line_size_;
auto set_index=block%sets_.size();
auto tag=block/sets_.size();
```

### TODO D6-CACHE-HIT
Varra ways do set. Se valid && tag igual: `++hits_`, atualize `last_used=++tick_`, retorne true.

### TODO D6-CACHE-EVICT
No miss, `++misses_`. Prefira invalid; se todas válidas, escolha menor `last_used`. Grave valid/tag/tick.

Trace: line=64, sets=2. addr0=0 -> block0 set0 tag0. addr128 -> block2 set0 tag1. Em direct-mapped, segundo expulsa primeiro.
Execute CMake/CTest. Teste compara direct versus 2-way em sequência de conflito.
