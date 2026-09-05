# Teoria passo a passo — Arena allocator

## 1. O problema que estamos resolvendo

`new`/`delete` e `malloc`/`free` são interfaces gerais. Um *arena allocator* resolve um problema mais restrito: reservar um bloco grande de memória e atender várias alocações pequenas movendo apenas um cursor (`offset`). Isso troca flexibilidade por simplicidade e previsibilidade.

Em produção, arenas aparecem em compiladores (AST nodes por função), parsers (tokens por arquivo), jogos (frame allocator), servidores HTTP (request scope) e kernels (slab/zone temporária). O padrão comum é: **muitas alocações pequenas com lifetime igual ou menor que um escopo conhecido**.

## 2. Modelo mental

Imagine um vetor de bytes de 1024 posições. `offset_` começa em zero. Uma alocação de 7 bytes ocupa uma faixa; antes da próxima alocação, o endereço pode precisar ser arredondado para satisfazer um alinhamento de 8, 16, 32 bytes etc.

```text
storage_: [........................................................]
           ^ base
           ^ offset inicial = 0

allocate(7, 8)
           [#######]
                  ^ próximo cursor lógico

allocate(32, 32)
                  .....padding.....[################################]
```

### Diagrama de estados

```text
  [CRIADA] --allocate()--> [PARCIALMENTE USADA] --reset()--> [VAZIA]
                |                                              ^
                +-- bad_alloc se cheia ------------------------+
```

## 3. Alinhamento

Um endereço satisfaz alinhamento `A` quando `endereco % A == 0`. No exercício aceitamos apenas alinhamentos que são potências de dois. Para esses valores, o arredondamento pode ser feito com máscara:

```text
mask = alignment - 1
aligned = (value + mask) & ~mask
```

### Tabela de exemplos manuais

| value | alignment | mask | value+mask | aligned |
|------:|----------:|-----:|-----------:|--------:|
| 0     | 8         | 7    | 7          | 0       |
| 13    | 8         | 7    | 20         | 16      |
| 16    | 8         | 7    | 23         | 16      |
| 17    | 8         | 7    | 24         | 24      |
| 0     | 32        | 31   | 31         | 0       |
| 33    | 32        | 31   | 64         | 64      |

Você não deve decorar isso sem verificar. No papel, use `value=13`, `alignment=8`: o próximo múltiplo de 8 é 16.

## 4. Por que alinhar o endereço real e não apenas offset?

`std::vector<std::byte>::data()` tem um endereço base. Se você arredondar somente `offset_`, você implicitamente supõe que `base` já está alinhado para todo alinhamento pedido. A implementação deste laboratório calcula `base + offset_`, alinha o endereço e converte de volta para offset.

```text
base = 0x1001 (não múltiplo de 16)
offset_ = 0
pedido: allocate(8, 16)

ERRADO: aligned_offset = align_up(0, 16) = 0  -> endereço 0x1001 (desalinhado)
CERTO:  aligned_addr = align_up(0x1001, 16) = 0x1010 -> offset = 15
```

## 5. Overflow e capacidade

Nunca faça apenas `aligned_offset + size > capacity` sem pensar em overflow. A forma usada no projeto é:

```text
if aligned_offset > capacity -> falha
if size > capacity - aligned_offset -> falha
```

### Trace de exaustão

Arena com capacidade 64, `offset_=60`, pedido `allocate(8, 8)`:

```text
aligned_offset = 60
size = 8
capacity - aligned_offset = 4
8 > 4 -> std::bad_alloc
```

## 6. Reset O(1)

Uma arena não precisa percorrer objetos para recuperar o espaço bruto. Neste laboratório, `reset()` apenas coloca `offset_ = 0`. Isso não chama destrutores de objetos C++ que você eventualmente tenha construído manualmente nessa memória — limitação importante para fases futuras.

## 7. Invariantes do laboratório

| Invariante | Significado |
|------------|-------------|
| `0 <= offset_ <= storage_.size()` | cursor nunca ultrapassa capacidade |
| cada `allocate` retorna endereço alinhado | `reinterpret_cast<uintptr_t>(ptr) % alignment == 0` |
| `alignment` é potência de dois não nula | rejeitado com `invalid_argument` |
| `size > 0` | alocação de tamanho zero é erro |
| após `reset`, todas as alocações anteriores são inválidas | uso após reset é UB |

## 8. Bugs clássicos de estudante

1. **Testar `alignment` com `% 2 == 0`**: 6 passa, mas não é potência de dois.
2. **Esquecer `value != 0` em `is_power_of_two`**: zero retorna true incorretamente.
3. **Somar `aligned_offset + size` sem checar overflow de `size_t`**.
4. **Retornar ponteiro sem avançar `offset_`**: duas alocações sobrepõem memória.
5. **Assumir que `reset` destrói objetos**: vazamento de recursos se você usou placement new.

## 9. Comparação com produção

| Aspecto | Arena deste lab | `malloc`/`free` | Bump allocator em jogo | LLVM BumpPtrAllocator |
|---------|-----------------|-----------------|------------------------|----------------------|
| Liberação individual | não | sim | não | não |
| Reset em lote | O(1) | N chamadas free | O(1) por frame | O(1) por escopo |
| Alinhamento arbitrário | potências de 2 | sim (via align) | sim | sim |
| Thread-safety | não | depende | por thread | por instância |
| Fragmentação interna | padding por alinhamento | pode fragmentar heap | mínima | mínima |

## 10. Quando usar arena vs heap

Use arena quando:
- o lifetime de todas as alocações termina juntos;
- o pico de memória é previsível;
- você quer evitar contenção no allocator global.

Evite arena quando:
- objetos precisam de lifetime independente;
- tamanhos são imprevisíveis e podem exceder a capacidade;
- destrutores e RAII precisam rodar por objeto.

## 11. Exemplo manual completo

Arena capacidade 32, alinhamento padrão 8:

```text
allocate(5, 8)  -> offset 0..5, próximo aligned 8
allocate(3, 8)  -> offset 8..11, próximo 16
allocate(10, 16)-> padding 16..16, bytes 16..26, próximo 32
allocate(1, 8)  -> bad_alloc (não cabe)
reset()
allocate(20, 8) -> offset 0..20, OK
```

## 12. Relação com o restante do portfólio

Este módulo prepara o terreno para allocators de página (bitmap), pools fixos e estruturas de kernel onde liberar byte a byte seria proibitivo em hot path. A disciplina de **invariantes + overflow + alinhamento** reaparece em quase todo código de sistemas.

## 13. Perguntas de verificação

Antes de implementar, responda no caderno:
1. Por que `13` alinhado a `8` vira `16` e não `8`?
2. O que acontece se dois threads chamam `allocate` sem lock?
3. Por que benchmark arena vs `new[]` em loop pode ser injusto se o loop também mede destruição?
