# Teoria passo a passo — Resource state tracker (D5-GFX)

## 1. O que estamos construindo

Um **tracker de estados de recurso GPU** em C++ headless: registra texturas/buffers com estado lógico (`Undefined`, `CopyDst`, `ShaderRead`, `RenderTarget`, `Present`), enfileira **barriers** quando o estado muda e devolve o lote em `flush()`. Não executa Vulkan/D3D12 — simula a ordem lógica que um command stream real gravaria.

TODOs: `D5-GFX-REGISTER`, `D5-GFX-TRANSITION`, `D5-GFX-FLUSH`.

Módulo **GFX_VISUAL_EXEMPT**: laboratório CPU-only, sem janela Win32.

## 2. Por que estados explícitos existem

GPUs modernas (Vulkan, D3D12) não escondem coerência de cache. A aplicação declara **em qual layout/estado** uma imagem está antes de cada uso (copy, shader sample, render target, present). Omitir uma transição causa corrupção silenciosa ou validation layer error. Este lab comprime o conceito numa enum pequena para você praticar **ordem + barriers** sem driver.

## 3. Modelo de dados

### O quê

```cpp
enum class State { Undefined, CopyDst, ShaderRead, RenderTarget, Present };
struct Barrier { std::string id; State before, after; };
class Tracker {
  unordered_map<string, State> states_;
  vector<Barrier> pending_;
};
```

### Como

- `states_` — estado **lógico atual** por ID de recurso.
- `pending_` — barriers ainda não “submetidas” ao backend (flush entrega lote).

### Por quê

Separar estado lógico de fila pending espelha engines reais: você grava transições no command list e só no submit/barrier batch elas viram API calls. Atualizar `states_` na mesma chamada de `transition` evita calcular `before` obsoleto na transição seguinte.

### Diagrama — ciclo de vida de um recurso

```text
register(id, Undefined)
    │
    ▼
transition(CopyDst) ──► pending += {id, Undefined, CopyDst}
    │
    ▼
transition(ShaderRead) ──► pending += {id, CopyDst, ShaderRead}
    │
    ▼
flush() ──► retorna 2 barriers; pending limpo
```

## 4. Registro (`D5-GFX-REGISTER`)

### O quê

`register_resource(id, initial)` insere recurso com estado inicial.

### Como

```text
se states_.contains(id): throw invalid_argument("duplicate resource")
states_.emplace(move(id), s)
```

### Por quê

ID duplicado quebraria invariante “um estado por recurso” e geraria barriers com `before` ambíguo. APIs reais falham na criação duplicada ou exigem handle único.

### Invariantes

- Recurso deve existir antes de `transition`.
- Registro não gera barrier (estado inicial não é transição).

### Bugs comuns

- `operator[]` silencioso em vez de `emplace` + check.
- Permitir segundo `register` com mesmo id.

## 5. Transição (`D5-GFX-TRANSITION`)

### O quê

`transition(id, after) → bool`: se estado mudou, enfileira barrier e atualiza mapa; se `current == after`, retorna `false` (sem barrier redundante).

### Como

```text
it ← states_.find(id); se ausente: out_of_range
se it->second == after: return false
pending_.push_back({id, it->second, after})
it->second ← after
return true
```

### Por quê

Barriers redundantes desperdiçam CPU e podem inserir waits desnecessários na GPU. Retornar `false` permite ao caller pular batch. Atualizar `states_` **antes** do flush modela “estado conhecido pelo tracker após gravar comando”, não após GPU completar — correto para ordem lógica.

### Trace manual — `tex`

```text
register("tex", Undefined)
transition(CopyDst)     → true,  pending=[{tex,U,CopyDst}]
transition(ShaderRead)  → true,  pending+= {tex,CopyDst,ShaderRead}
transition(ShaderRead)    → false, pending inalterado
flush()                 → 2 barriers, pending=[]
state("tex")            → ShaderRead
```

### Tabela — enum educacional vs APIs

| Lab `State` | D3D12 (aprox.) | Vulkan (aprox.) |
|-------------|----------------|-----------------|
| Undefined | COMMON / invalid | UNDEFINED |
| CopyDst | COPY_DEST | TRANSFER_DST_OPTIMAL |
| ShaderRead | PIXEL_SHADER_RESOURCE | SHADER_READ_ONLY_OPTIMAL |
| RenderTarget | RENDER_TARGET | COLOR_ATTACHMENT_OPTIMAL |
| Present | PRESENT | PRESENT_SRC_KHR |

Vulkan exige também `srcStage`, `dstStage`, `access masks` — a enum do lab é **intencionalmente menor**.

### Invariantes

- `before` na barrier = estado imediatamente anterior à transição.
- Transição após `flush` parte do estado já atualizado.

### Bugs comuns

- Não atualizar `states_` até flush → segunda transição com `before` errado.
- Retornar `true` em transição idempotente.
- Esquecer `out_of_range` para id desconhecido.

## 6. Flush (`D5-GFX-FLUSH`)

### O quê

`flush() → vector<Barrier>` copia `pending_`, limpa fila, retorna lote.

### Como

```text
out ← pending_
pending_.clear()
return out
```

### Por quê

Segunda chamada deve retornar vazio — prova que barriers foram “consumidas”. Em backend real, cada barrier viraria `vkCmdPipelineBarrier` ou `ResourceBarrier` no command list.

### Invariantes

- Ordem FIFO das barriers preservada.
- `state(id)` após flush reflete últimas transições (mapa não é limpo).

## 7. Fluxo mental — frame típico

```text
register texture
transition CopyDst      (upload)
transition ShaderRead   (sample)
transition RenderTarget (draw)
transition Present      (swapchain)
flush → traduzir para API → GPU
```

## 8. Headless vs GPU real

| Aspecto | Este tracker (CPU) | GPU real |
|---------|-------------------|----------|
| Execução | C++ + CTest | driver + hardware |
| Sincronização | lista em RAM | fences, semaphores |
| Validação | asserts | validation layers |
| Visual | não requerido | swapchain / present |

Ver `docs/COMPARISON.md` para colunas Software/CPU vs OpenGL vs Vulkan/D3D12.

## 9. Complexidade

| Operação | Tempo |
|----------|-------|
| `register` | O(1) médio |
| `transition` | O(1) médio |
| `flush` | O(k) barriers pendentes |

## 10. Passo a passo guiado (ordem dos TODOs)

1. `D5-GFX-REGISTER` — `starter/src/state_tracker.cpp`.
2. `D5-GFX-TRANSITION` — barrier + update map.
3. `D5-GFX-FLUSH` — snapshot + clear.
4. Build CTest conforme `TESTES_GUIADOS.md`.

## 11. Como saber se está correto

- Registro duplicado lança exceção.
- Duas transições distintas + uma redundante → `flush().size()==2`.
- Segundo `flush()` vazio; `state("tex")==ShaderRead`.

## 12. Bugs comuns (checklist)

| Sintoma | Causa |
|---------|-------|
| flush retorna 3 | idempotente gerou barrier |
| state errado após flush | não atualizou map em transition |
| duplicate passa | falta check antes de emplace |
| pending não limpa | retornou referência interna |

## 13. Por quê este módulo existe

Resource barriers são a fronteira entre **lógica de engine** e **driver**. Cada TODO protege invariante que engines D3D12/Vulkan assumem: IDs únicos, ordem de transições e batch explícito.
