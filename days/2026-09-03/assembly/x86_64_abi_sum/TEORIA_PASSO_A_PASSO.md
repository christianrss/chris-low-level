# Teoria passo a passo — Assembly x86-64 e ABI System V AMD64

## 1. O que estamos construindo

Uma função `asm_sum_u64(const uint64_t* values, size_t count)` em Assembly que soma um array de inteiros sem sinal de 64 bits, respeitando a ABI System V AMD64 usada em Linux/macOS.

## 2. Por que ABI importa mais que opcode

A ISA diz *o que* cada instrução faz. A ABI diz *como* funções cooperam: quais registradores recebem argumentos, quem preserva o quê, onde está o retorno e como alinhar a stack.

Sem ABI, C e Assembly não se entendem.

## 3. Contrato desta função

```text
uint64_t asm_sum_u64(const uint64_t* values, size_t count);
```

| Papel | Registrador | Valor na entrada |
|-------|-------------|------------------|
| 1º arg (ponteiro) | RDI | endereço de `values[0]` |
| 2º arg (contagem) | RSI | `count` |
| retorno | RAX | soma modular 2^64 |

`uint64_t` ocupa 8 bytes; avançar o ponteiro soma 8 ao endereço.

## 4. Diagrama do loop

```text
RDI --> | v0 | v1 | v2 | ... |
         ^8B  ^8B  ^8B

RAX = 0
se RSI==0 -> ret
.loop:
  RAX += *RDI
  RDI += 8
  RSI -= 1
  se RSI!=0 -> .loop
ret
```

## 5. Exemplo numérico

`values = {1, 2, 3, 5, 8, 13}`, `count = 6`:

```text
RAX: 0 -> 1 -> 3 -> 6 -> 11 -> 19 -> 32
```

Overflow modular: `{UINT64_MAX, 1}` → `0` (como em C).

## 6. Como funciona internamente

1. `xor %rax,%rax` — acumulador zerado.
2. `test %rsi,%rsi` / `je .done` — lista vazia retorna 0 sem ler memória.
3. `add (%rdi),%rax` — load+add implícito.
4. `add $8,%rdi` — próximo elemento.
5. `dec %rsi` / `jne .loop` — controle de iteração.
6. `ret` — caller lê RAX.

Caller-saved: não precisamos salvar RDI/RSI/RAX neste exercício simples.

## 7. Invariantes

- `count == 0` ⇒ não acessar `values`.
- Cada iteração consome exatamente um `uint64_t`.
- Soma é modular 2^64, igual a `uint64_t` em C.
- RAX ao retornar contém o resultado; não depender de outros registradores.

## 8. Complexidade

- Tempo: O(n) onde n = `count`.
- Espaço: O(1) além do array de entrada.
- Uma iteração ≈ 1 load + 1 add + ajustes de ponteiro/contador.

## 9. Bugs comuns

- Usar `(%rdi)` com incremento de 1 em vez de 8.
- Esquecer caso `count == 0` (lê lixo ou trap).
- Confundir Windows x64 (RCX, RDX...) com System V (RDI, RSI...).
- Não preservar callee-saved se a função crescer e chamar outras rotinas.
- Comparar performance com C otimizado (-O3 -mavx2) sem inspecionar o assembly gerado.

## 10. Comparação com produção

| Este exercício | libc / compiler |
|----------------|-----------------|
| loop escalar manual | vetorização AVX2/AVX-512 automática |
| sem alinhamento explícito | `movdqu` vs `movdqa` conforme alinhamento |
| uma função isolada | LTO, inlining, PLT |

`objdump -d` na versão C revela se o compilador desenrolou ou vetorizou o loop.

## 11. Passo a passo guiado

1. Implemente retorno 0 (`xor rax; ret`) — teste `count=0` passa.
2. Adicione o loop completo (`ASM-SUM-01`).
3. Teste vetor `{1,2,3,5,8,13}` → 32.
4. Teste overflow `{UINT64_MAX, 1}` → 0.
5. Benchmark honesto vs C (documente limitações).

## 12. Como saber se está correto

```text
assembly ABI tests passed
```

Saída de `ctest` ou executável de teste sem falha de `assert`.
## 13. Stack frame futuro (preview)

Quando a função chamar `printf` ou outra libc, precisará alinhar RSP em 16 bytes antes de `call`:

```text
push %rbp
mov %rsp, %rbp
...
call helper
leave
ret
```

Este exercício isola o loop para não misturar ABI de chamada com aritmética de ponteiro.

## 14. Tabela de registradores callee-saved vs caller-saved

| Registrador | Quem preserva | Uso típico |
|-------------|---------------|------------|
| RBX, RBP, R12-R15 | callee | variáveis long-lived |
| RAX, RCX, RDX, RSI, RDI, R8-R11 | caller | temporários, args |

## 15. Checklist antes de entregar

- [ ] `count=0` não lê memória
- [ ] incremento de ponteiro é +8
- [ ] testes de overflow modular passam
- [ ] comentário no `.S` referencia `ASM-SUM-01`

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
