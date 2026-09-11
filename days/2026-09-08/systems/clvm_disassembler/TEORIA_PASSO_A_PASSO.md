# Teoria passo a passo — disassembler CLVM em C

Este laboratório é em **C (bytecode)**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O verifier do Dia 07 diz se o programa é bem formado. O disassembler transforma os **mesmos bytes** em texto para você depurar o codegen. Sem tamanho por opcode, o `pc` come o imediato de um PUSH e o listing mente.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Opcode | Bytes | Exemplo |
|--------|-------|---------|
| PUSH `0x01` | 1 + imm32 little-endian | `01 2A 00 00 00` = PUSH 42 |
| JMP `0x09` / JZ `0x0A` / CALL `0x0B` / JNZ `0x13` | 1 + u16 LE | `09 0A 00` = JMP 10 |
| ADD `0x02`, HALT `0x08` | 1 | `02`, `08` |

Arquivo de fixture: `starter/fixtures/push42.clbc` contém exatamente `01 2A 00 00 00`.

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
bytes: 01 2A 00 00 00 02 08
pc=0 op=0x01 PUSH
  imm = 0x2A | 0x00<<8 | 0x00<<16 | 0x00<<24 = 42
  tamanho 5 → linha "PUSH 42"
pc=5 op=0x02 ADD tamanho 1 → "ADD"
pc=6 op=0x08 HALT tamanho 1 → "HALT"
pc=7 == len → para
listagem: ["PUSH 42", "ADD", "HALT"]
```

JMP isolado `09 0A 00`: offset = 0x0A | (0x00<<8) = 10. Linha `"JMP 10"`, size 3.
Opcode `0xFF` não está na tabela → retorno -1 (o teste exige falha, não a string `"???"`).

## Algoritmo (ordem obrigatória)

1. Se `data[offset] != 0x01` ou não há 5 bytes, `decode_push` retorna -1.
2. Monte o imm32 em little-endian (byte baixo primeiro). Não use `ntohl`.
3. Branch: opcodes 0x09, 0x0A, 0x0B, 0x13; offset u16 LE; size sempre 3.
4. `disassemble_all` chama um decodificador e faz `pc += size`. Opcode de 1 byte usa o nome da tabela.
5. Opcode fora da tabela aborta o listing inteiro.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- `PUSH 42` com size 1: o teste de `disassemble_all` vê a linha seguinte como `0x2A` e falha a string `"ADD"`.
- Interpretar o imm em big-endian: `01 2A 00 00 00` vira 704643072, não 42.
- Aceitar `0xFF` como `"UNK"`: o teste espera retorno negativo.

## Lab versus produção

Em produção (`objdump`, `llvm-objdump`) a tabela de tamanhos é a ISA. Aqui o subset é o da CLVM do Dia 03/07. O arquivo `.clbc` é o bytecode; o C é só o decodificador.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `systems/clvm_disassembler`, o fluxo de dados não é abstrato: cada função do starter
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
#ifdef __cplusplus
# error "A C++ compiler has been selected for C."
#endif

#if defined(__18CXX)
# define ID_VOID_MAIN
#endif
#if defined(__CLASSIC_C__)
/* cv-qualifiers did not exist in K&R C */
# define const
# define volatile
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
```

## Endianness e o caso PUSH 256

O Caso 1 usa `2A 00 00 00` (= 42). Isso mascara bugs de endianness porque o byte
baixo já é o valor. O Desafio usa `01 00 01 00 00`:

```text
bytes após opcode: 00 01 00 00
LE: 0x00 | (0x01<<8) | (0x00<<16) | (0x00<<24) = 256
BE errado:         0x00010000 = 65536
só byte[1]:        0  (errado)
```

**Por quê** o lab insiste em LE? Porque a ISA CLVM (Dia 03) e o verifier (Dia 07)
já fixaram little-endian. Trocar endian no disassembler quebra a paridade com a VM.

## Tabela completa de tamanhos (wire format)

| Opcode | Hex | Size | Operando |
|--------|-----|------|----------|
| PUSH | 0x01 | 5 | u32 LE |
| ADD/SUB/... | 0x02.. | 1 | — |
| HALT | 0x08 | 1 | — |
| JMP | 0x09 | 3 | u16 LE |
| JZ | 0x0A | 3 | u16 LE |
| CALL | 0x0B | 3 | u16 LE |
| JNZ | 0x13 | 3 | u16 LE |

Qualquer outro opcode → `disassemble_all` retorna **-1** (não `"UNK"`).

## Invariante do cursor `pc`

```text
pc_0 = 0
para cada instrução i:
  size_i = decode(code[pc_i])
  pc_{i+1} = pc_i + size_i
pc_final == len(code)
```

Se `size_PUSH` for 1, o próximo “opcode” é `0x2A` e a listagem vira lixo.
Se `size_JMP` for 1, o byte `0x0A` vira JZ solto.

## Relação com o verifier (Dia 07)

| Camada | Pergunta |
|--------|----------|
| Verifier | o programa é bem formado? |
| Disassembler | o que cada instrução *diz*? |

O verifier usa a **mesma** tabela de tamanhos. Se o C e o Python discordarem
no size de PUSH, um aceita e o outro rejeita o mesmo `.clbc`.

## Lab versus produção

`objdump -d` / `llvm-objdump` leem tabelas de ISA enormes e relocações.
Aqui o subset é didático: três decoders (`decode_push`, `decode_branch`,
walk linear). Em produção você geraria a tabela a partir de um `.td` (TableGen);
no lab você escreve o switch à mão para sentir o desalinhamento.

## Checklist antes de compilar

- [ ] Trace `01 2A 00 00 00` → imm=42, size=5 no papel
- [ ] Trace `09 0A 00` → JMP 10, size=3
- [ ] Trace programa 7 bytes → 3 linhas
- [ ] Sei que `0xFF` retorna negativo
