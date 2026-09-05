# Teoria passo a passo — CPU toy (fetch/decode/execute)

## 1. O que estamos construindo

Uma CPU arquitetural mínima: estado (registradores, PC, memória) + transições por `step()`. Cada ciclo busca um opcode em `memory[PC]`, decodifica operandos e altera o estado.

Não imitamos x86. Construímos um modelo mental comparável depois com RISC-V e com decoders reais.

## 2. Por que começar tão pequeno

Antes de lidar com prefixos, ModR/M e micro-op fusion, precisamos dominar:

- como o PC avança byte a byte;
- como imediatos little-endian ocupam múltiplos bytes;
- como LOAD/STORE conectam CPU e RAM;
- como saltos absolutos alteram o fluxo.

## 3. Codificação de instruções (tabela de offsets)

```text
opcode | mnemônico | operandos (bytes após opcode)
-------|-----------|------------------------------
0x00   | NOP       | (nenhum)
0x01   | HALT      | (nenhum)
0x10   | MOVI      | dst:u8, imm16:le
0x20   | ADD       | dst:u8, src:u8
0x30   | STORE     | src:u8, addr:u16:le
0x31   | LOAD      | dst:u8, addr:u16:le
0x40   | JNZ       | src:u8, target:u16:le (absoluto)
```

Diagrama de um programa `MOVI R0,5` + `HALT`:

```text
PC:  0    1    2    3    4
    [10][00][05][00][01]
     |   |   |----|   HALT
     |   R0  imm16=5
    MOVI
```

## 4. Exemplo numérico — soma R0+R1

Programa:

```text
10 00 05 00    MOVI R0, 5
10 01 07 00    MOVI R1, 7
20 00 01       ADD  R0, R1
01             HALT
```

Execução:

```text
passo 1: R0=5,  PC=4
passo 2: R1=7,  PC=8
passo 3: R0=12, PC=11
passo 4: halted
```

STORE de `0x1234` no endereço `0x0100` grava `34 12` (little-endian de 16 bits).

## 5. Como funciona internamente `step()`

```text
fetch opcode -> switch(op)
  MOVI: fetch reg, fetch imm16, escreve regs[dst]
  ADD:  fetch dst, fetch src, regs[dst] += regs[src] (mod 2^16)
  ...
  HALT: halted_=true, return false
return true  // continua executando
```

`fetch8`/`fetch16` validam limites e incrementam PC automaticamente.

## 6. Invariantes

- `pc_ < memory_.size()` antes de cada fetch.
- Índice de registrador ∈ {0,1,2,3}; outros valores lançam exceção.
- LOAD/STORE exigem `addr+1 < memory_.size()`.
- JNZ salta para endereço absoluto, não relativo.
- Após HALT, `step()` retorna `false`.

## 7. Complexidade

- `step()`: O(1) — no máximo alguns bytes lidos.
- `run()` com limite `L`: O(L) passos.
- Memória fixa: O(1) espaço extra além do programa.

## 8. Bugs comuns

- Esquecer `return true` após o `switch` (CPU “morre” silenciosamente).
- Tratar imediato como big-endian.
- JNZ com target relativo em vez de absoluto.
- STORE com ordem de bytes invertida.
- `default` que retorna `true` em opcode desconhecido (mascara erro).

## 9. Comparação com produção

| Toy CPU | CPU real (x86-64 / ARM) |
|---------|-------------------------|
| opcodes fixos simples | tamanho variável, prefixos |
| 4 registradores | dezenas + SIMD |
| memória flat byte[] | MMU, cache, TLB |
| JNZ absoluto | PC-rel, predição de branch |

O ciclo fetch-decode-execute é o mesmo; a complexidade do decode cresce.

## 10. Passo a passo guiado

1. Leia `starter/include/cpu.hpp` e a enum `Op`.
2. Implemente `MOVI` primeiro; rode testes — falha em `ADD` é esperado.
3. Adicione `ADD`, depois `STORE`/`LOAD`, depois `JNZ`.
4. Valide com `ctest --test-dir starter/build`.

## 11. Como saber se está correto

```text
100% tests passed
```

R0=12 no primeiro programa; R3=0x1234 e bytes `34 12` na RAM no segundo bloco de testes.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
