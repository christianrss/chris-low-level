# Resolucao guiada

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

## Solução final
A implementação comentada/limpa está em `solutions/src/sum_x86_64.S`. Não use a solução antes de fazer o teste falhar e tentar o loop.


## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `ASM-SUM-01` — `starter/src/sum_x86_64.S` → `solutions/src/sum_x86_64.S`.
