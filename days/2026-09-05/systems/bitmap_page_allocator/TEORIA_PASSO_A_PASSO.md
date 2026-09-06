# Teoria passo a passo — Systems — alocador bitmap de páginas

## 1. O problema que estamos resolvendo

Um kernel (ou runtime de baixo nível) precisa saber quais **páginas físicas ou lógicas** estão livres sem manter um ponteiro por página. Um bitmap compacta esse estado: 1 bit por página — `0` = livre, `1` = em uso. Este lab implementa alocação linear (primeira página livre) e liberação com detecção de double-free.

O padrão aparece em bootloaders, allocators de frame em kernels educacionais, pools de DMA e camadas abaixo de slab/buddy em sistemas reais.

## 2. Modelo mental

```text
page:  0  1  2  3  4  5  6  7 | 8  9 10 11 ...
byte0: [b0 b1 b2 b3 b4 b5 b6 b7] | byte1 ...
       ^bit0                    ^bit7
```

Para `N` páginas, o vetor de bytes tem tamanho `ceil(N/8)`:

```text
bytes = (page_count + 7) / 8
```

O construtor do starter já inicializa `bits_` com zeros — todas as páginas começam livres.

### Diagrama allocate/free

```text
  [TODAS LIVRES] --allocate()--> [PÁGINA 0 USADA]
        ^                              |
        +-------- free_page(0) ---------+
```

## 3. Mapeamento page → byte → bit (`SYS-PAGE-ALLOC-01`)

### O quê
Converter um índice de página em `(byte_index, bit_index)` dentro do vetor `bits_`, para o teste e para as operações de bit.

### Como
Função auxiliar `trace_page_to_bit(page)`:

```text
byte_index = page / 8
bit_index  = page % 8
```

### Por quê
Sem esse mapeamento explícito, `allocate`/`free` viram magia de máscaras. O assert `trace_page_to_bit(13) → byte 1, bit 5` prova que divisão e resto estão no sentido certo.

### Tabela de exemplos

| page | byte_index | bit_index | máscara `1 << bit_index` |
|-----:|-----------:|----------:|-------------------------:|
| 0    | 0          | 0         | 0x01                     |
| 7    | 0          | 7         | 0x80                     |
| 8    | 1          | 0         | 0x01                     |
| 13   | 1          | 5         | 0x20                     |

Trace manual para página 13: `13 / 8 = 1`, `13 % 8 = 5` — bit 5 do byte 1.

## 4. Operações bit a bit

### O quê
Consultar e alterar um único bit sem corromper os outros sete do mesmo byte.

### Como — consultar (`is_used`)

```cpp
(bits_[page / 8] & (1u << (page % 8))) != 0
```

### Como — setar livre/usada (`set_used`, `SYS-PAGE-FREE-02`)

```cpp
auto mask = static_cast<std::uint8_t>(1u << (page % 8));
if (used) bits_[page / 8] |= mask;
else       bits_[page / 8] &= ~mask;
```

### Por quê
`|=` / `&= ~mask` isolam o bit; `uint8_t` evita surpresa de promoção signed. Páginas fora de `[0, page_count_)`: `is_used` no gabarito retorna `true` (página inexistente = não alocável).

## 5. `allocate` — scan linear (`SYS-PAGE-ALLOC-01`)

### O quê
Devolver o menor índice livre, marcá-lo usado, ou `-1` se o bitmap estiver cheio.

### Como
Percorra `page` de `0` a `page_count_ - 1`:

1. Se `!is_used(page)`, marque usada com `set_used(page, true)` e retorne `page`.
2. Se nenhuma livre, retorne `-1` (OOM).

### Por quê
Ordem 0,1,2… é o contrato do teste e o comportamento clássico first-fit em frame allocator educacional. Complexidade O(n) por alocação — aceitável para lab pequeno; produção usa buddy/slab ou hint de próxima livre.

## 6. `free_page` — sem double-free (`SYS-PAGE-FREE-02`)

### O quê
Liberar uma página usada e rejeitar double-free / out-of-range sem corromper o bitmap.

### Como

```text
if page >= page_count_ → false
if !is_used(page)       → false  (já livre ou nunca alocada)
set_used(page, false)  → true
```

### Por quê
Retornar `false` em vez de assert permite que o runtime trate erro; o teste chama `free_page(1)` duas vezes e exige a segunda = `false`.

## 7. Invariantes do laboratório

| Invariante | Significado |
|------------|-------------|
| bit 0 = livre, bit 1 = usada | convenção do módulo |
| `allocate` nunca retorna página já usada | scan + set atômico no mesmo thread |
| `free_page` idempotente em falha | segunda liberação retorna false, não corrompe |
| OOM explícito | `-1` quando bitmap cheio |
| `page_count_` fixo após construção | sem resize dinâmico neste milestone |

## 8. Bugs clássicos de estudante

1. **`bit_index = page / 8`** — confundir com `page % 8`.
2. **Esquecer `static_cast<std::uint8_t>` na máscara** — shift em tipos signed pode surpreender.
3. **`allocate` retorna 0 mas `is_used(0)` false** — setou bit errado ou não chamou `set_used`.
4. **`free_page` sempre true** — não checa se página estava usada.
5. **Scan só até `bits_.size()`** — deve ir até `page_count_`; último byte pode ter bits fantasma se N não é múltiplo de 8.

## 9. Fragmentação e escala

O bitmap **não fragmenta memória física** — só rastreia ocupação. Fragmentação externa é problema de allocator de ordem superior. Em produção:

| Mecanismo | Quando |
|-----------|--------|
| Bitmap linear | poucas páginas, boot, pools fixos |
| Buddy allocator | potências de 2, coalescência |
| Slab | objetos de tamanho fixo (kernel) |
| Per-CPU cache | reduzir contenção em SMP |

## 10. Trace completo — alocador de 3 páginas

```text
PageAllocator alloc(3)   → bits_ = [0b00000000] (1 byte, 3 páginas lógicas)

allocate() → page 0, bits = 0b00000001
allocate() → page 1, bits = 0b00000011
allocate() → page 2, bits = 0b00000111
allocate() → -1 (OOM)

free_page(1) → true, bits = 0b00000101 (bit 1 limpo)
allocate()   → page 1, bits = 0b00000111
free_page(1) → false (double-free)
free_page(99) → false (out-of-range)
```

## 11. Relação com o portfólio

O arena allocator (Day 04) gerencia bytes dentro de um bloco; este módulo gerencia **unidades de página inteiras** com custo de metadado ~1/8 byte por página. A disciplina de invariantes + checagem de limites reaparece em todo código de sistemas.

## 12. Perguntas de verificação

1. Quantos bytes de bitmap para 10 páginas? (resposta: 2)
2. Por que `free_page` retorna `false` em double-free em vez de assert?
3. O que acontece se você usar `page / 8` como índice de bit?
4. Como o teste `trace_page_to_bit(13)` prova que você entendeu o mapeamento?

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
