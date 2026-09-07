# RESOLUÇÃO GUIADA — Graphics / resource state tracker

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-GFX-REGISTER` | `starter/src/state_tracker.cpp` | `Tracker::register_resource` |
| `D5-GFX-TRANSITION` | `starter/src/state_tracker.cpp` | `Tracker::transition` |
| `D5-GFX-FLUSH` | `starter/src/state_tracker.cpp` | `Tracker::flush` |

Header: `starter/include/state_tracker.hpp` (já completo — não edite enum/struct).

IDs: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` em `solutions/`, `PEDAGOGY-TEST: ID` em `starter/tests/test.cpp`.

## Baseline

```powershell
cd days/2026-09-07/graphics/resource_state_tracker/starter
cmake -B build -S .
cmake --build build
ctest --test-dir build --output-on-failure
```

**Esperado:** FAIL — registro duplicado não lança; transições retornam false; flush vazio.

---

## D5-GFX-REGISTER — mapa sem duplicatas

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/state_tracker.cpp` |
| **Função / âncora** | `TODO [D5-GFX-REGISTER]` em `register_resource` |
| **Substituir** | corpo com `(void)id;(void)s;` |
| **Não mexer** | `state_tracker.hpp`, outras funções |

### 1. O problema

Stub ignora parâmetros — teste espera exceção no segundo `register_resource("tex", ...)`.

### 2. Código completo

```cpp
void Tracker::register_resource(std::string id, State s) {
 if (states_.contains(id)) throw std::invalid_argument("duplicate resource");
 states_.emplace(std::move(id), s);
}
```

### 3. Por que funciona?

- `contains` rejeita ID antes de sobrescrever silenciosamente.
- `emplace` move string — evita cópia extra.

### 4. Verifique

Recompile e rode ctest — caso REGISTER passa; TRANSITION/FLUSH ainda falham.

---

## D5-GFX-TRANSITION — barrier e estado lógico

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/state_tracker.cpp` |
| **Função / âncora** | `TODO [D5-GFX-TRANSITION]` em `transition` |
| **Substituir** | `(void)id;(void)after;return false;` |
| **Não mexer** | `register_resource`, assinatura em `.hpp` |

### 1. O problema

Sempre retorna `false` — nenhuma barrier enfileirada; `flush` fica vazio.

### 2. Código completo

```cpp
bool Tracker::transition(const std::string& id, State after) {
 auto it = states_.find(id);
 if (it == states_.end()) throw std::out_of_range("resource");
 if (it->second == after) return false;
 pending_.push_back({id, it->second, after});
 it->second = after;
 return true;
}
```

### 3. Por que funciona?

- `before` capturado **antes** de mutar `it->second`.
- Retorno `false` em estado igual evita barrier redundante (terceira transição ShaderRead no teste).
- `out_of_range` alinha com `state()` para ID desconhecido.

### 4. Verifique

Após build, asserts de TRANSITION passam; FLUSH ainda pode falhar se pending não for drenado.

---

## D5-GFX-FLUSH — entregar lote e limpar

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/state_tracker.cpp` |
| **Função / âncora** | `TODO [D5-GFX-FLUSH]` em `flush` |
| **Substituir** | `return {};` |
| **Não mexer** | map `states_` — flush não apaga estados |

### 1. O problema

`flush` retorna vetor vazio — teste espera `size()==2` e segundo flush vazio.

### 2. Código completo

```cpp
std::vector<Barrier> Tracker::flush() {
 auto out = pending_;
 pending_.clear();
 return out;
}
```

### 3. Por que funciona?

- Cópia para `out` antes de `clear` — caller recebe snapshot estável.
- `states_` intacto — `state("tex")` continua `ShaderRead` após flush.

### 4. Verifique

```powershell
ctest --test-dir build --output-on-failure
```

**Esperado:** `chris-gfx-state tests passed`.

---

## Debug / depuração

| Sintoma | Ação |
|---------|------|
| duplicate não lança | confira `contains` antes de `emplace` |
| flush size 3 | transição idempotente retornou true |
| state errado | `it->second = after` ausente |
| segundo flush não vazio | `clear()` não chamado |

Breakpoint em `transition`: observe `pending_.size()` após cada chamada.

Trace manual: `Undefined→CopyDst→ShaderRead` = 2 barriers; terceira `ShaderRead` = false.

---

## Relatório de resolução

| Campo | Sua resposta |
|-------|----------------|
| Data | |
| Barriers retornadas no 1º flush | |
| Resultado 2º flush (deve ser 0) | |
| `state("tex")` final | |
| CTest | PASS / FAIL |

Comparativo CPU vs GPU: leia `docs/COMPARISON.md`.
