# Resolução guiada passo a passo — SPSC ring buffer

Edite `starter/src/spsc.cpp`.

Baseline:
```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

### TODO D6-SPSC-PUSH
Localize `bool SpscRing::push(int value)`. Leia `head_` relaxed, calcule:
```cpp
const auto next = (head + 1) % storage_.size();
```
Depois leia `tail_` com acquire:
```cpp
if (next == tail_.load(std::memory_order_acquire)) return false;
```
Agora grave o slot e só então publique:
```cpp
storage_[head] = value;
head_.store(next, std::memory_order_release);
return true;
```
Trace com storage=5 e capacidade lógica 4: head 0→1→2→3→4; próximo de 4 seria 0. Se tail ainda for 0, a fila está cheia.

### TODO D6-SPSC-POP
Localize `bool SpscRing::pop(int& out)`. Leia tail relaxed. Se for igual ao head adquirido, vazio:
```cpp
if (tail == head_.load(std::memory_order_acquire)) return false;
```
Leia antes de publicar tail:
```cpp
out = storage_[tail];
tail_.store((tail + 1) % storage_.size(), std::memory_order_release);
return true;
```

### TODO D6-SPSC-SIZE
`size_approx()` é observacional, não sincronização. Tire snapshots:
```cpp
auto h=head_.load(std::memory_order_acquire);
auto t=tail_.load(std::memory_order_acquire);
return h >= t ? h-t : storage_.size()-t+h;
```

Teste final deve imprimir `chris-spsc tests passed`. No debugger observe `head`, `tail`, `next` e o slot atual.
Se a ordem sai 1,3,2, procure avanço do índice antes da leitura/escrita.
