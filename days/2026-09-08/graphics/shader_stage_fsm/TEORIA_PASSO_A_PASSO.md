# Teoria passo a passo — máquina de estados de shader em C++

Este laboratório é em **C++**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

Um shader não salta de rascunho para GPU pronta. A ordem é EDIT → COMPILE → LINK → READY, com volta para EDIT em falha. Pular READY direto do EDIT é ilegal — o teste mede isso.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| De | Para | Legal? |
|----|------|--------|
| EDIT (0) | COMPILE (1) | sim |
| EDIT | READY (3) | não |
| COMPILE | LINK (2) ou EDIT | sim |
| LINK | READY | sim |
| READY | EDIT | sim |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
estado inicial s=0 (EDIT)
can(0,1)=1
can(0,3)=0
apply 1 → s=1, retorno 0
apply 3 a partir de COMPILE → retorno -1, s continua 1
illegal(0,3)=1
```

## Algoritmo (ordem obrigatória)

1. shader_can consulta a tabela. Qualquer outro par retorna 0.
2. shader_apply só escreve *stage se can for 1.
3. shader_illegal é o inverso de can.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Permitir EDIT→READY: o segundo assert (can==0) falha.
- apply ilegal alterar o estágio: o teste exige que s permaneça COMPILE.
- illegal retornar 0 para EDIT→READY: o último assert falha.

## Lab versus produção

No driver, glCompileShader e glLinkProgram são as arestas. Este lab testa a tabela sem contexto OpenGL.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `graphics/shader_stage_fsm`, o fluxo de dados não é abstrato: cada função do starter
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

## Grafo de estados (lab)

```text
EDIT ──compile──► COMPILE ──link──► LINK ──ready──► READY
  ▲                  │                              │
  └──────edit────────┘                              │
  ▲                                                 │
  └────────────────────edit─────────────────────────┘
```

Tabela `shader_can`:

| from | to | ok? |
|------|----|-----|
| EDIT | COMPILE | 1 |
| COMPILE | LINK | 1 |
| COMPILE | EDIT | 1 |
| LINK | READY | 1 |
| READY | EDIT | 1 |
| EDIT | READY | **0** |
| LINK | COMPILE | **0** |

Trace do teste:

```text
EDIT → COMPILE : can=1, apply=0, stage=COMPILE
EDIT → READY   : can=0, apply=-1, stage inalterado
illegal(EDIT,READY)=1
```

**Por quê** FSM? Em APIs reais (D3D12/Vulkan) recurso fora do estado certo
é UB ou device-loss. O lab compacta isso em inteiros.

## Invariantes

- `apply` só muda `*stage` se `can==1`
- Aresta ilegal **não** altera estado (teste verifica)
- `illegal` é o complemento de `can`

## Bugs comuns

- Permitir EDIT→READY “porque está pronto mentalmente”
- `apply` setar estado mesmo quando can=0
- Esquecer COMPILE→EDIT (reabrir shader)

## Lab vs produção

PSO / shader modules têm pipelines longos (compile → reflect → link → cache).
Aqui 4 estados bastam para treinar a **disciplina de transição**.

## Checklist

- [ ] EDIT→COMPILE sim; EDIT→READY não
- [ ] apply ilegal retorna -1
- [ ] estado permanece EDIT após aresta ilegal
