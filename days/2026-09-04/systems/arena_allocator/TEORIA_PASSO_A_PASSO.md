# Teoria passo a passo — Arena allocator

## 1. O problema de produção

`malloc`/`free` são gerais. Uma arena reserva um bloco e atende alocações movendo um cursor — previsível quando muitas alocações compartilham lifetime (AST, tokens, frame de jogo, request HTTP).

### O quê

`Arena`: `is_power_of_two`, `align_up`, `allocate(size, alignment)`, `reset()` O(1) sobre `vector<byte>`.

### Como

Alinhar o endereço real `base+offset_` (não só o offset); checar capacidade sem overflow (`size > cap - aligned_offset`); avançar cursor; reset zera `offset_`.

### Por quê

Alinhar só o offset assume `data()` já alinhado a qualquer A — falso. Soma `aligned+size` sem guard overflow → aceita alocação que ultrapassa o bloco. Reset sem disciplina = use-after-reset (UB).

## 2. Modelo mental

```text
storage_: [................................]
           ^ base   offset_=0
allocate(7,8) → [#######]  cursor avança (+padding se preciso)
```

## 3. Alinhamento (potência de 2)

```text
mask = A-1; aligned = (value + mask) & ~mask
```

| value | A | aligned |
|------:|--:|--------:|
| 13 | 8 | 16 |
| 17 | 8 | 24 |
| 33 | 32 | 64 |

## 4. Base real vs offset

```text
base=0x1001, offset=0, A=16
ERRADO: align_up(0,16)=0 → ptr 0x1001 desalinhado
CERTO:  align_up(0x1001,16)=0x1010 → offset 15
```

## 5. Overflow

```text
se aligned_offset > cap → bad_alloc
se size > cap - aligned_offset → bad_alloc
```

## 6. Invariantes

| Invariante | Significado |
|------------|-------------|
| `0 ≤ offset_ ≤ size` | cursor válido |
| ptr % A == 0 | alinhamento |
| A potência de 2 ≠ 0 | senão invalid_argument |
| size > 0 | zero rejeitado |
| após reset, ptrs velhos inválidos | UB se usados |

## 7. Bugs clássicos

1. `% 2 == 0` aceita 6.
2. Esquecer `value != 0` em power-of-two.
3. Overflow em `aligned+size`.
4. Retornar sem avançar `offset_`.
5. Assumir que reset chama destrutores.

## 8. Quando usar

Usar: lifetime em lote, pico previsível, evitar contenção no allocator global.  
Evitar: lifetimes independentes, RAII por objeto, tamanhos que explodem a capacidade.

## 9. Comparação

| | Arena lab | malloc | Bump jogo | LLVM BumpPtr |
|--|-----------|--------|-----------|--------------|
| Free individual | não | sim | não | não |
| Reset lote | O(1) | N frees | O(1)/frame | O(1)/escopo |
| Threads | não | depende | por thread | por instância |

## 10. Exemplo completo (cap 32, A=8)

```text
alloc(5,8) → 0..5, próximo 8
alloc(3,8) → 8..11, próximo 16
alloc(10,16) → 16..26
alloc(1,8) → bad_alloc
reset; alloc(20,8) → OK
```

## 11. Relação com o portfólio

Prepara bitmap page allocator, pools e hot paths de kernel onde free byte-a-byte é proibitivo. Invariantes + overflow + alinhamento reaparecem em quase todo código de sistemas.

## 12. Perguntas

1. Por que 13→16 e não 8?
2. Dois threads sem lock?
3. Benchmark arena vs `new[]` com destruição no loop — justo?

## Fundamentos adicionais (reforço Dia 01)

### O quê

Uma arena (bump allocator) entrega blocos contíguos com reset O(1), sem free individual.

### Como

Trabalhe com um exemplo numérico no papel antes de editar o starter: anote entradas, estado intermediário e saída esperada.

### Por quê

Sem o modelo mental no papel, o código vira tentativa-e-erro e os testes não ensinam o invariante.

### Por quê comparar com produção

Implementações reais (libc, kernels, VMs, GPUs) usam as mesmas ideias com mais camadas; este lab isola o núcleo.

### Por quê falhar de propósito no starter

O starter compila e o teste falha até o TODO existir — isso prova que o harness mede o comportamento certo.

### Trace manual

`	ext
entrada -> transformação -> invariante -> saída
` 

### Bugs comuns (módulo)

| Sintoma | Causa | Depuração |
|---------|-------|-----------|
| Teste falha após 'implementar' | Off-by-one / endian | Trace byte a byte |
| PASS sem entender | Copiou gabarito | Refaça o paper-trace |

