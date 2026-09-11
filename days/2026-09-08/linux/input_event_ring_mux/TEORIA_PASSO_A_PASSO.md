# Teoria passo a passo — ring buffer de input em C

Este laboratório é em **C**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

Teclado e mouse do Dia 07 viram o mesmo `InputEvent`. Sem mux, duas filas. Aqui um anel de 4 slots guarda `(source, type, value)` em ordem FIFO.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Campo | Tipo | Exemplo tecla | Exemplo mouse |
|-------|------|--------------|---------------|
| source | u8 | 1 | 2 |
| type | u16 | 1 (EV_KEY) | 2 (EV_REL) |
| value | i32 | 10 | -3 |
| RING_CAP | 4 | quinto push falha | |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
push source=1 value=10  → count=1 tail=1
push source=2 value=-3  → count=2
pop → source 1, value 10   (FIFO, não o mouse)
pop → source 2, value -3
4 pushes enchem; o 5º retorna -1 e count permanece 4.
```

## Algoritmo (ordem obrigatória)

1. push: se count==4, -1. Senão grave em slots[tail], tail=(tail+1)%4, count++.
2. pop: se count==0, -1. Leia slots[head], head=(head+1)%4, count--.
3. mux_push empacota source/type/value e chama push.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Incrementar tail sem módulo 4: no 4º evento `tail==4` estoura o array.
- Pop devolver o último (LIFO): o teste exige source 1 primeiro.
- Quinto push retornar 0: o teste exige -1 (anel cheio).

## Lab versus produção

No kernel, `evdev` usa um anel de `input_event` (24 bytes). Aqui o struct é menor, mas a aritmética head/tail/count é a mesma.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `linux/input_event_ring_mux`, o fluxo de dados não é abstrato: cada função do starter
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

## Layout do anel (`RING_CAP = 4`)

```text
slots[0..3]  head  tail  count
vazio:       0     0     0
após push A: slots[0]=A, head=0, tail=1, count=1
após push B: slots[1]=B, head=0, tail=2, count=2
pop → A:     head=1, tail=2, count=1
```

Trace do teste:

```text
mux_push(source=1, type=1, value=10) → count=1
mux_push(source=2, type=2, value=-3) → count=2
pop → source=1 value=10
pop → source=2 value=-3
encher 4 pushes → 5º retorna -1
```

## Fórmulas

```text
push: slots[tail] = ev; tail = (tail+1) % CAP; count++
pop:  *out = slots[head]; head = (head+1) % CAP; count--
cheio: count == CAP
vazio: count == 0
```

**Por quê** `% CAP`? Sem módulo, `tail` sai do array e você corrompe memória.
**Por quê** `count` além de head/tail? Distinguir cheio vs vazio quando
`head == tail` (ambos 0).

## Mux

`mux_push` monta `InputEvent{type,value,source}` e chama `ring_push`.
É a ponte entre HID/PS2 (Dia 07) e um único consumidor.

## Invariantes

- `0 <= head,tail < CAP`
- `0 <= count <= CAP`
- FIFO: ordem de pop = ordem de push

## Bugs comuns

- Esquecer `% RING_CAP` → OOB
- Incrementar count no pop → overflow lógico
- Aceitar 5º push → teste espera -1

## Lab vs evdev

No kernel, `evdev` usa filas por cliente com drops sob pressão.
Aqui a política é **fail hard** (-1) para forçar o aluno a ver capacidade.

## Checklist

- [ ] Desenhei head/tail após 2 pushes
- [ ] Sei que value=-3 é int32, não unsigned
- [ ] 5º push em CAP=4 falha
