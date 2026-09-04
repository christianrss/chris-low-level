# Teoria passo a passo — Arena allocator

## 1. O problema que estamos resolvendo
`new`/`delete` e `malloc`/`free` são interfaces gerais. Um *arena allocator* resolve um problema mais restrito: reservar um bloco grande de memória e atender várias alocações pequenas movendo apenas um cursor (`offset`). Isso troca flexibilidade por simplicidade e previsibilidade.

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

## 3. Alinhamento
Um endereço satisfaz alinhamento `A` quando `endereco % A == 0`. No exercício aceitamos apenas alinhamentos que são potências de dois. Para esses valores, o arredondamento pode ser feito com máscara:

```text
mask = alignment - 1
aligned = (value + mask) & ~mask
```

Você não deve decorar isso sem verificar. No papel, use `value=13`, `alignment=8`: o próximo múltiplo de 8 é 16.

## 4. Por que alinhar o endereço real e não apenas offset?
`std::vector<std::byte>::data()` tem um endereço base. Se você arredondar somente `offset_`, você implicitamente supõe que `base` já está alinhado para todo alinhamento pedido. A implementação deste laboratório calcula `base + offset_`, alinha o endereço e converte de volta para offset.

## 5. Overflow e capacidade
Nunca faça apenas `aligned_offset + size > capacity` sem pensar em overflow. A forma usada no projeto é:

```text
if aligned_offset > capacity -> falha
if size > capacity - aligned_offset -> falha
```

## 6. Reset O(1)
Uma arena não precisa percorrer objetos para recuperar o espaço bruto. Neste laboratório, `reset()` apenas coloca `offset_ = 0`. Isso não chama destrutores de objetos C++ que você eventualmente tenha construído manualmente nessa memória — limitação importante para fases futuras.

## 7. Exercícios
- Fácil: detectar potência de dois e calcular alinhamento no papel.
- Médio: implementar `align_up`.
- Difícil: implementar `allocate` com validação e exaustão.
- Desafio: benchmark arena versus várias alocações no heap e discutir quando a comparação é justa ou injusta.
