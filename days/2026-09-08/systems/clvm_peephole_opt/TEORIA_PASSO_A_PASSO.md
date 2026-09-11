# Teoria passo a passo — peephole sobre bytecode CLVM

Este laboratório é em **C++**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

Depois do disassembler você vê `PUSH 0` seguido de `ADD`. Isso é identidade na pilha: somar zero não muda o topo. O otimizador apaga esses 6 bytes. Outro padrão: `PUSH a`, `PUSH b`, `ADD` vira um único `PUSH a+b` (11 bytes → 5).

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Padrão | Bytes | Efeito |
|--------|-------|--------|
| PUSH 0; ADD | `01 00 00 00 00 02` (6) | apagar |
| PUSH 2; PUSH 3; ADD | 5+5+1 = 11 | um PUSH 5 (`01 05 00 00 00`) |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
Caso 1: 01 00 00 00 00 02
  opcode 01, imm=0, próximo 02 (ADD) → match = 1
Caso 2: PUSH 2 + PUSH 3 + ADD
  a=2, b=3, soma=5
  saída: 01 05 00 00 00  (5 bytes)
  economizados: 11-5 = 6
Caso 3: o padrão PUSH0+ADD sozinho economiza 6 bytes (some inteiro).
```

## Algoritmo (ordem obrigatória)

1. `match_push0_add` exige 6 bytes, opcode PUSH, imm32 == 0, byte seguinte ADD.
2. `fold_const_add` exige dois PUSH e um ADD. Escreve PUSH da soma em LE.
3. `saved_bytes` varre e soma 6 para cada match (apagou 6, ou 11-5=6).

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Tratar PUSH 1 + ADD como identidade: o teste só aceita imm 0.
- Somar em big-endian: PUSH 2+3 escreveria `01 00 00 00 05` e `out[1]==5` falha.
- `saved_bytes` retornar 11: o teste espera 6 no padrão curto.

## Lab versus produção

Peephole de compilador (GCC `-fpeephole`) casa padrões de instruções, não de AST. Aqui o padrão é a ISA CLVM.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `systems/clvm_peephole_opt`, o fluxo de dados não é abstrato: cada função do starter
transforma um buffer ou um estado finito e devolve um valor que o teste compara
com igualdade estrita.

```text
entrada (fixture / literal do teste)
    → validação de limites (OOB / estado ilegal)
    → transformação (decode / fold / push / parse)
    → saída (string, código, ponteiro, probabilidade)
```

Por quê essa ordem? Se a validação vier depois da transformação, um buffer curto
gera leitura lixo e o assert falha com um número “quase certo”, difícil de depurar.

## Estruturas e papéis

| Peça | Papel | O que o teste fixa |
|------|-------|--------------------|
| buffer / stream | memória linear | bytes literais no caso |
| cursor / pc / head | progresso | avanço exatamente do size |
| estado / flags | FSM ou capacidade | transição ilegal rejeitada |
| retorno de erro | falha explícita | -1 / Err / false / throw |

## Trace estendido (mesmo caso, mais colunas)

Reescreva o Caso 1 da TEORIA com quatro colunas no papel:

```text
passo | cursor | lê | produz
------+--------+----+--------
(use os números já listados acima; não invente outro exemplo)
```

Se o cursor após o passo N não for o início do passo N+1, o listing ou o anel
desalinha e a string/valor diverge do assert.

## Invariantes reforçadas

1. Mesma entrada → mesma saída (determinismo).
2. Erro de formato não vira valor default silencioso.
3. Capacidade / size / transição ilegal falha **agora**.
4. O arquivo editado é só o citado na RESOLUCAO; o teste não se altera.

## Depuração dirigida

| Sintoma no teste | Hipótese #1 | O que imprimir |
|------------------|-------------|----------------|
| string/valor off-by-one | endianness ou size | hex do buffer e cursor |
| falha só no 2º caso | estado residual | reset entre casos |
| passe local, falha no runner | cwd / fixture path | path absoluto do fixture |

## Comparação com produção (detalhe)

Em ferramentas reais o mesmo contrato aparece com outros nomes: `objdump` (size
por opcode), `epoll` (anel de eventos), `softmax` em kernels CUDA (max-subtract).
Aqui o recorte é pequeno o bastante para caber no papel e grande o bastante para
o assert rejeitar o bug clássico.

## Trecho âncora do gabarito (só para conferir assinaturas)

Não copie cegamente. Use para confirmar nomes de funções e constantes:

```text
/* This source file must have a .cpp extension so that all C++ compilers
   recognize the extension without flags.  Borland does not know .cxx for
   example.  */
#ifndef __cplusplus
# error "A C compiler has been selected for C++."
#endif

#if !defined(__has_include)
/* If the compiler does not have __has_include, pretend the answer is
   always no.  */
#  define __has_include(x) 0
#endif


/* Version number components: V=Version, R=Revision, P=Patch
   Version date components:   YYYY=Year, MM=Month,   DD=Day  */

#if defined(__INTEL_COMPILER) || defined(__ICC)
# define COMPILER_ID "Intel"
# if defined(_MSC_VER)
#  define SIMULATE_ID "MSVC"
# endif
# if defined(__GNUC__)
#  define SIMULATE_ID "GNU"
# endif
  /* __INTEL_COMPILER = VRP prior to 2021, and then VVVV for 2021 and later,
     except that a few beta releases use the old format with V=2021.  */
# if __INTEL_COMPILER < 2021 || __INTEL_COMPILER == 202110 || __INTEL_COMPILER == 202111
#  define COMPILER_VERSION_MAJOR DEC(__INTEL_COMPILER/100)
#  define COMPILER_VERSION_MINOR DEC(__INTEL_COMPILER/10 % 10)
#  if defined(__INTEL_COMPILER_UPDATE)
#   define COMPILER_VERSION_PATCH DEC(__INTEL_COMPILER_UPDATE)
#  else
#   define COMPILER_VERSION_PATCH DEC(__INTEL_COMPILER   % 10)
#  endif
# else
#  define COMPILER_VERSION_MAJOR DEC(__INTEL_COMPILER)
#  define COMPILER_VERSION_MINOR DEC(__INTEL_COMPILER_UPDATE)
   /* The third version component from --version is an update index,
      but no macro is provided for it.  */
```

## Padrão PUSH 0 + ADD (6 bytes → 0)

```text
offset 0: 01 00 00 00 00   PUSH 0
offset 5: 02               ADD
```

Semanticamente: `x + 0 = x`. O match devolve 1; o otimizador pode apagar
os 6 bytes (ou marcar dead). **Por quê** 6? 5 do PUSH + 1 do ADD.

## Padrão PUSH a + PUSH b + ADD (11 → 5)

```text
01 | a0 a1 a2 a3 | 01 | b0 b1 b2 b3 | 02
```

Exemplo do teste: a=2, b=3 → s=5 → emit `01 05 00 00 00`.
Bytes economizados: 11 − 5 = **6**.

Trace numérico:

```text
a = 2 = 02 00 00 00 LE
b = 3 = 03 00 00 00 LE
s = 5 = 05 00 00 00 LE
out = [0x01, 0x05, 0x00, 0x00, 0x00]
out_len = 5
```

## Algoritmo de `saved_bytes`

Varre `i` de 0 até `len`:

1. Se `match_push0_add` em `i` → `saved += 6`, `i += 6`
2. Senão se janela 11 casa PUSH/PUSH/ADD → `saved += 6`, `i += 11`
3. Senão `i += 1` (não pular opcodes no meio)

**Por quê** não `i += size` genérico? Porque o peephole olha *padrões*
de bytes, não um decode completo — mas o tamanho dos padrões já embute
a ISA (5+1 e 5+5+1).

## Invariantes

- Match só retorna 1 se os bytes forem exatamente o padrão.
- Fold não escreve se `out_cap < 5`.
- Soma `a+b` em u32 (wrap modular, igual à VM i32 truncada no lab).

## Bugs comuns

| Sintoma | Causa |
|---------|-------|
| match em PUSH 1+ADD | esqueceu checar imm==0 |
| fold emite 11 bytes | copiou input em vez de PUSH s |
| saved=0 no teste | avançou `i` de 1 dentro do padrão |

## Lab vs produção

LLVM InstCombine / GCC peephole trabalham sobre IR SSA, não bytes crus.
Aqui o bytecode *é* a IR — igual a um assembler que otimiza antes de emitir.

## Checklist

- [ ] Hex `01 00 00 00 00 02` → match=1
- [ ] Hex PUSH2+PUSH3+ADD → out `01 05 00 00 00`
- [ ] Economiza 6 bytes no fold
