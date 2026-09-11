# Teoria passo a passo — softmax numericamente estável em C

Este laboratório é em **C**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

Softmax ingenuo `exp(x_i)/sum exp(x_j)` estoura em float32 quando x=1000. Subtrair o máximo não muda as probabilidades e deixa o maior exp igual a 1.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Entrada | max | exp(x-max) | papel |
|---------|-----|------------|-------|
| 1, 2, 3 | 3 | e^{-2}, e^{-1}, e^{0} | e^0 = 1 é o maior |
| soma | | e^{-2}+e^{-1}+1 | divide cada termo |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
xs = 1, 2, 3
m = 3
e1 = exp(-2) ≈ 0.135335
e2 = exp(-1) ≈ 0.367879
e3 = exp(0)  = 1
soma ≈ 1.503214
p2 ≈ 1/1.503214 ≈ 0.665241  > p0
soma das probabilidades = 1 (±1e-5)
log_softmax[i] = (x_i - m) - log(soma)
loss no alvo 2 = -log_softmax[2]
```

## Algoritmo (ordem obrigatória)

1. Ache o máximo.
2. Some exp(x_i - max).
3. Divida cada exp pela soma. Isso é `softmax_stable`.
4. log-softmax não divide: `(x_i - max) - log(soma)`.
5. cross-entropy no índice target é o negativo desse log.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- `expf(xs[i])` sem subtrair max: no teste {1,2,3} ainda passa, mas o algoritmo exigido é o estável (max==3).
- Esquecer a normalização: soma das saídas ≠ 1, assert de 1e-5 falha.
- loss no índice 0: o teste usa target 2, a classe do maior logit.

## Lab versus produção

PyTorch `softmax` e `log_softmax` usam o mesmo truque. Aqui o n máximo da loss é 8 (buffer na função).

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `ai/softmax_stable`, o fluxo de dados não é abstrato: cada função do starter
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

## Por quê subtrair o max?

`softmax(x)_i = exp(x_i) / Σ exp(x_j)`.
Se `x = [1000,1001,1002]`, `exp(1002)` overflowa em float32.
Estável:

```text
m = max(x)
y_i = exp(x_i - m)
p_i = y_i / Σ y
```

Trace do teste `xs={1,2,3}`:

```text
m = 3
exp(1-3)=exp(-2)≈0.135335
exp(2-3)=exp(-1)≈0.367879
exp(0)=1
sum≈1.503214
p≈[0.0900, 0.2447, 0.6652]
Σp = 1
p[2] > p[0]
```

## log-softmax e CE

```text
log_softmax_i = (x_i - m) - log(Σ exp(x_j - m))
CE = -log_softmax[target]
```

Para target=2: CE ≈ -log(0.6652) ≈ 0.4076

**Por quê** CE via log-softmax? Evita `log(softmax)` com underflow em p≈0.

## Invariantes

- Σ softmax = 1 (±1e-5)
- argmax(p) = argmax(x)
- n<=0 ou ponteiros nulos → -1

## Bugs comuns

- Softmax sem `-m` → NaN/Inf em logits grandes
- Dividir antes de somar
- CE com target fora de [0,n)

## Lab vs produção

PyTorch `torch.softmax` / `log_softmax` usam o mesmo truque em kernels CUDA.
O lab é o kernel em C cru.

## Checklist

- [ ] max=3; exp(-2), exp(-1), 1
- [ ] soma das probs = 1
- [ ] CE(target=2) = -log_softmax[2]
