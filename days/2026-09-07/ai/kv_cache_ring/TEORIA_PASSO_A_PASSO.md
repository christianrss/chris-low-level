# Teoria passo a passo — KV cache circular (D5-KV)

## 1. O que estamos construindo

Um **ring buffer** Python puro que simula o núcleo de um **KV cache** de atenção autoregressiva: slots fixos, posição lógica monotônica, eviction determinística e leitura por janela com detecção de **stale read**. Sem PyTorch, sem GPU — só listas e tags lógicos.

TODOs do lab: `D5-KV-APPEND` (gravar K/V + tag), `D5-KV-WINDOW` (ler intervalo validado), `D5-KV-RESET` (limpar ownership).

## 2. Por quê KV cache antes de kernels

Na inferência token-a-token, cada passo de atenção precisa das **keys** e **values** de todos os tokens anteriores. Recalcular o prefixo inteiro a cada novo token é \(O(n^2)\) em comprimento de sequência. Cachear K/V transforma o custo incremental em \(O(n)\) por token — o mesmo raciocínio que vLLM, FlashAttention e paged attention exploram com layouts mais ricos.

## 3. Ring buffer e tag lógico

```text
capacity = 4
logical positions escritas: 10  11  12  13
physical slots:               2   3   0   1
                              ↑ slot 0 agora pertence a p=13; p=9 foi evictado
```

Mapeamento físico: `slot = logical_position % capacity`. Isso **não basta**: após eviction, o slot pode conter bytes de outra posição. Por isso guardamos `positions[slot] = logical_position` — um **tag lógico** que prova ownership.

| Campo | Papel |
|-------|-------|
| `keys[slot]`, `values[slot]` | par K/V armazenado |
| `positions[slot]` | tag lógico ou `None` |
| `next_position` | próximo `p` esperado em `append` |
| `capacity` | tamanho fixo do ring |

## 4. Append sequencial (`D5-KV-APPEND`)

### O quê
`append(position, key, value)` grava K/V no slot circular e avança o cursor lógico. Só aceita `position == next_position` (append contíguo).

### Como
1. Rejeite `position != self.next_position` → `ValueError("non-contiguous position")`.
2. Calcule `slot = position % capacity`.
3. Escreva **juntos**: `keys[slot]`, `values[slot]`, `positions[slot] = position`.
4. Incremente `next_position += 1`.

### Por quê
Append contíguo espelha geração autoregressiva: token 0, depois 1, depois 2… Sem essa regra, o aluno poderia “preencher buracos” e mascarar eviction. Gravar o tag no mesmo passo da escrita K/V evita janela onde o slot tem valor novo mas tag antigo.

### Trace manual — capacity=3

```text
append(0,"k0","v0") → slot=0, positions=[0,None,None], next=1
append(1,"k1","v1") → slot=1, positions=[0,1,None], next=2
append(2,"k2","v2") → slot=2, positions=[0,1,2], next=3
append(3,"k3","v3") → slot=0 EVICT p=0, positions=[3,1,2], next=4
```

### Invariantes
- `next_position` conta quantas posições lógicas foram commitadas (não modulo capacity).
- Após append de `p`, `positions[p % capacity] == p`.
- Eviction é determinística: posição `p - capacity` deixa de ser legível.

### Bugs comuns
- Incrementar `next_position` antes de gravar tag → janela inconsistente.
- Aceitar `position` arbitrário → teste de contiguidade falha silenciosamente.
- Esquecer `positions[slot]` → stale read retorna K/V errado sem erro.

## 5. Leitura por janela (`D5-KV-WINDOW`)

### O quê
`window(start, end)` devolve `[(key, value), ...]` para posições lógicas `[start, end)`. Falha se alguma posição foi evictada.

### Como
1. Valide `start >= 0`, `end >= start`, `end <= next_position`; senão `ValueError("invalid window")`.
2. Para cada `p` em `range(start, end)`:
   - `slot = p % capacity`
   - Se `positions[slot] != p` → `KeyError(f"position {p} was evicted")`
   - Caso contrário, append `(keys[slot], values[slot])`
3. Retorne lista na ordem crescente de `p`.

### Por quê
Checar só “slot não é None” permitiria ler K/V de outra posição que reutilizou o slot — bug clássico de ring buffer. Comparar tag lógico é o invariante mínimo de correção antes de falar em page tables ou GPU.

### Trace manual — após trace da seção 4

```text
window(1, 4) → p=1 ok, p=2 ok, p=3 ok → [("k1","v1"),("k2","v2"),("k3","v3")]
window(0, 1) → p=0: slot=0 tem positions[0]=3 ≠ 0 → KeyError evicted
window(0, 5) → end > next_position → ValueError invalid window
```

### Invariantes
- Janela vazia (`start == end`) retorna `[]` se bounds válidos.
- Ordem de saída segue ordem lógica, não ordem física dos slots.
- Posição evictada nunca retorna par silenciosamente.

### Bugs comuns
- Retornar `keys[slot]` sem comparar tag → falso positivo após wrap.
- Usar `range(end)` em vez de `range(start, end)`.
- Permitir `end > next_position` → lê posições nunca escritas.

## 6. Reset (`D5-KV-RESET`)

### O quê
`reset()` descarta todo ownership e reinicia geração na posição lógica 0.

### Como
```text
positions ← [None] * capacity
keys      ← [None] * capacity
values    ← [None] * capacity
next_position ← 0
```

### Por quê
Em produção, reset acontece ao trocar de conversa, batch ou sessão. Sem limpar tags, um `append(0, ...)` após reset poderia ler tag residual e passar testes intermitentes.

### Invariantes
- Após reset, `next_position == 0` e todas as tags são `None`.
- Reset não altera `capacity`.

### Bugs comuns
- Zerar só `next_position` → stale tags sobrevivem.
- Recriar objeto em vez de limpar listas → API do teste que inspeciona `c.positions` falha.

## 7. Fluxo mental

```text
append(p,k,v) ──► slot=p%cap ──► grava K,V,tag ──► next++
                      │
                      ▼ (wrap)
                 evict p-cap

window(s,e) ──► para cada p: tag ok? ──► sim: (K,V) / não: KeyError
reset()     ──► limpa tudo ──► next=0
```

## 8. Complexidade

| Operação | Tempo | Espaço |
|----------|-------|--------|
| `append` | O(1) | O(1) extra |
| `window(s,e)` | O(e−s) | O(e−s) saída |
| `reset` | O(capacity) | O(1) extra |

## 9. Comparação com produção

| Este lab | Produção (LLM) |
|----------|----------------|
| Uma sequência, um par K/V | Batch × heads × head_dim |
| Tag inteiro por slot | Slot maps, block tables (paged attention) |
| Eviction por wrap | Políticas de janela, sliding window, quantização |
| Python lists | Tensores GPU, kernels fused |

O transferível é **ownership lógico + detecção de eviction**, não o layout exato da VRAM.

## 10. Passo a passo guiado (ordem dos TODOs)

1. `D5-KV-APPEND` — `append` em `starter/kv_cache.py`.
2. `D5-KV-WINDOW` — `window` com validação de tag.
3. `D5-KV-RESET` — `reset` completo.
4. `python starter/test_kv_cache.py` → `chris-kv-cache tests passed`.

## 11. Como saber se está correto

- Caso 1: capacity=3, quatro appends → `next_position==4`.
- Caso 2: `window(1,4)` retorna três pares na ordem k1..k3.
- Caso 3: `window(0,1)` após wrap → `KeyError`.
- Caso 4: após `reset()`, `next_position==0` e `positions==[None]*capacity`.

## 12. Invariantes globais do módulo

- API fixa: não renomeie métodos nem mude assinaturas.
- `capacity <= 0` no construtor continua lançando `ValueError("capacity")`.
- Mensagens de erro do teste dependem dos textos acima.

## 13. Por quê este módulo existe

Isolar o **contrato de correção** do KV cache — tag lógico, append contíguo, janela validada — antes de empilhar batch, heads e kernels. Cada `TODO [ID]` protege uma falha que, em inferência real, vira resposta errada ou vazamento de contexto entre sessões.
