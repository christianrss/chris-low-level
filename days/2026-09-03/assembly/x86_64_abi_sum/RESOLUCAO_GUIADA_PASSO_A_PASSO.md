# Resolucao guiada

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `ASM-SUM-01` | `starter/src/sum_x86_64.S` | `asm_sum_u64` — preservar ABI e loop de soma |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/assembly/x86_64_abi_sum/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

1. Abra `starter/src/sum_x86_64.S`. Comece zerando RAX com `xor %rax,%rax`.
2. Teste RSI. Se for zero, salte para o retorno. Isso evita ler memoria quando a lista esta vazia.
3. Dentro do loop, some `(%rdi)` em RAX. Os parenteses significam memoria apontada por RDI.
4. Some 8 a RDI, decremente RSI e repita enquanto RSI nao for zero.
5. Termine com `ret`; RAX ja contem o valor que C recebera.
6. Escreva primeiro o teste de vetor `{1,2,3,5,8,13}` esperando 32. So depois adicione zero elementos e overflow.
7. Compile e execute com CMake. Leia uma falha de `assert` como evidencia de que o contrato ABI ou o loop esta incorreto.
8. Benchmark: compare com C, mas nao conclua que Assembly e melhor apenas por um numero. O compilador pode vetorizar a versao C e sua Assembly escalar pode perder. Inspecione o assembly gerado antes de concluir.

## Etapa de código 1 - retorno neutro

Comece com a função que apenas retorna zero. Isso compila e prova que C consegue chamar o símbolo Assembly:

```asm
asm_sum_u64:
    xor %rax, %rax
    ret
```

O teste com `count=0` passa; o teste com valores reais ainda falha. Essa falha é desejada.

## Etapa de código 2 - loop real

```asm
asm_sum_u64:
    xor %rax, %rax
    test %rsi, %rsi
    je .done
.loop:
    add (%rdi), %rax
    add $8, %rdi
    dec %rsi
    jne .loop
.done:
    ret
```

Leia cada linha em termos da ABI: RDI e o ponteiro, RSI e a contagem e RAX e o retorno.

## Etapa de teste

```c
const uint64_t values[] = {1, 2, 3, 5, 8, 13};
assert(asm_sum_u64(values, 6) == 32);
assert(asm_sum_u64(values, 0) == 0);
```

Depois adicione overflow modular com `{UINT64_MAX, 1}` esperando zero.

## Etapa de depuração

| Falha | Hipótese | Verificação |
|-------|----------|-------------|
| soma errada em 6 elementos | incremento de ponteiro ≠ 8 | trace `RDI` no debugger |
| crash com count>0 | leitura antes de testar RSI | `test %rsi,%rsi` antes do loop |
| overflow test falha | soma em 128 bits acidental | use `add` 64-bit em RAX |

## Etapa de benchmark

Compare com loop C equivalente; documente flags e se o compilador vetorizou (ver `BENCHMARK_GUIADO.md`).

## Solução final
A implementação comentada/limpa está em `solutions/src/sum_x86_64.S`. Não use a solução antes de fazer o teste falhar e tentar o loop.


## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `ASM-SUM-01` — `starter/src/sum_x86_64.S` → `solutions/src/sum_x86_64.S`.

## Relatório de resolução

Checklist ao concluir:

- [ ] `ASM-SUM-01` implementado com contrato System V (RDI, RSI, RAX).
- [ ] Testes em `starter/tests/test_sum.c` passam (vetor, vazio, overflow).
- [ ] Loop inspecionado: `add $8,%rdi`, `dec %rsi`, `jne .loop`.
- [ ] Benchmark documentado com limitação C vetorizado vs Assembly escalar.

**Saída esperada:** `assembly ABI tests passed`.

**Depuração:** use GDB/LLDB em `asm_sum_u64` e confira registradores na entrada e após cada iteração.

**Arquivos starter editados:** `starter/src/sum_x86_64.S`.
## Etapa de depuração — quando o assert falha

Se a soma retornar lixo com `count>0`, inspecione com GDB:

```text
break asm_sum_u64
run
info registers rdi rsi rax
```

Confirme que RDI aponta para o primeiro `uint64_t` e RSI contém a contagem.

## Etapa de overflow

```c
const uint64_t ov[] = {UINT64_MAX, 1};
assert(asm_sum_u64(ov, 2) == 0);
```

Modularidade é parte do contrato — igual ao C unsigned.

## Perguntas de verificação

1. Por que `dec %rsi` e não `sub $1,%rsi`? (equivalente aqui)
2. O que acontece se o caller passar ponteiro NULL com count>0?
3. Como o compilador C com `-O3` poderia vencer sua versão escalar?
