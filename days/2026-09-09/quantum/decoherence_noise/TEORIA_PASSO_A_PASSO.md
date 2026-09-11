# Teoria passo a passo — Canal de decoerência (Python)

Este laboratório é em **Python**.

## 1. O que estamos construindo

Estados quânticos ideais decaem sob ruído. O lab modela um canal simples: probabilidades normalizam, apply reduz coerência, trace tem comprimento fixo.

## 2. Por que este módulo existe neste dia

Por quê estudar isso agora? Porque o contrato numérico do teste fixa o vocabulário
do resto do dia — sem o paper-trace, o código “quase certo” passa no olho e falha
no assert.

## 3. Formato / contrato de dados (wire)

| Assert | Valor |
|--------|-------|
| p0+p1 | ≈ 1.0 |
| nxt[0] | < 1.0 após apply |
| len(trace) | 4 |

## 4. Trace numérico (valores dos testes)

Siga no papel **antes** de abrir o editor. Estes números são os do Caso 1.

```text
canal → (p0,p1) com p0+p1≈1
apply → nxt[0] < 1.0
trace → 4 amostras
```

## 5. Algoritmo (ordem obrigatória)

1. Construa o canal / vetor de probabilidade normalizado.
2. apply: mistura com ruído reduzindo a componente dominante.
3. trace: lista de comprimento 4 conforme contrato do teste.

## 6. Invariantes

- A saída é determinística para a mesma entrada do teste.
- Erros de pré-condição falham **agora** (retorno negativo, `Err`, `false`, exceção),
  não um default silencioso.
- O valor que o assert compara é o da seção de trace — não um sinônimo.

## 7. Bugs que o teste rejeita

- Não normalizar (soma ≠ 1).
- apply que não reduz nxt[0].
- trace com len ≠ 4.

## 8. Lab versus produção

Canais Kraus (depolarizing, amplitude damping) em simuladores; aqui um proxy pedagógico.

## Modelo mental

probabilidade clássica + ruído que 'esquenta' o estado.

## Por quê exigir soma 1?

Sem normalização o Born rule mente.

## Por quê nxt[0]<1?

Prova que o canal não é identidade.

## Invariante

Após canal válido, soma das probs ≈ 1.

## Ligação

Dia 10 capstone_measurement usa Born em amplitudes.

## Numérico

Use abs(p0+p1-1)<1e-9 como o teste.


## Por quê — síntese

### Por quê estas invariantes?
Cada `TODO [ID]` isola uma propriedade que quebra silenciosamente se ignorada.

### Por quê medir?
O `BENCHMARK_GUIADO.md` pede a métrica `1e5 apply` — mesmo que o ambiente
pule a medição, o aluno registra o protocolo.

### Por quê não alterar o teste?
O teste é o contrato. Ajuste o código até a saída igualar o caderno.

## Checklist antes de implementar

- [ ] Escrevi no papel o valor do Caso 1 (seção 4).
- [ ] Sei arquivo/função de cada TODO (`RESOLUCAO` / `TODO_MAP`).
- [ ] Sei o que **não** mudar (assinaturas, nomes públicos, capacidade fixa).

## Como saber se está correto

Rode os testes do `starter/` (esperado FAIL) e depois os de `solutions/` (PASS).
A string/número impresso deve bater com o trace caractere a caractere / bit a bit.

## Fluxo de dados (visão única deste módulo)

```text
entrada do Caso 1  →  transformação do algoritmo (seção 5)  →  valor do assert
       ↑                          ↑                                ↑
  paper-trace              código no starter                  TESTES_GUIADOS
```

Se qualquer seta divergir, pare: o bug está na seta, não no “conceito geral”.

## Tabela rápida TODO → propriedade

| Ordem | Propriedade protegida |
|-------|------------------------|
| 1º TODO | base do contrato (parse/init/open) |
| 2º TODO | transformação / estado intermediário |
| 3º TODO | agregação / export / verificação final |

Substitua na ordem da RESOLUCAO: pular o 1º faz o 2º mentir com dados lixo.

## O que não fazer

- Não reescrever o módulo em outra linguagem “porque é mais fácil”.
- Não alterar asserts para caber na sua saída.
- Não inventar um segundo exemplo no lugar do trace do Caso 1.
- Não copiar `solutions/` no começo — use a RESOLUCAO só ao travar.

## Fechamento

Releia o wire (seção 3) e o trace (seção 4). Risque no caderno a linha que você
calculou diferente do teste. Só então abra o arquivo do starter citado na
resolução e substitua o corpo da função nomeada.

## Mecanismo interno (segunda camada)

Neste módulo `quantum/decoherence_noise`, o fluxo de dados não é abstrato: cada função do starter
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
"""Simple decoherence noise channel."""

from __future__ import annotations


def depolarizing_channel(p0: float, p1: float, gamma: float) -> tuple[float, float]:
    # PEDAGOGY-SOLUTION: Q-DECO-CHANNEL-01
    mix = gamma / 2
    return (1 - gamma) * p0 + mix, (1 - gamma) * p1 + mix


def apply_noise_step(probs: list[float], gamma: float) -> list[float]:
    # PEDAGOGY-SOLUTION: Q-DECO-APPLY-02
    if len(probs) != 2:
        raise ValueError("2-level only")
    p0, p1 = depolarizing_channel(probs[0], probs[1], gamma)
    return [p0, p1]


def trace_decoherence(p0: float, steps: int, gamma: float) -> list[float]:
    # PEDAGOGY-SOLUTION: Q-DECO-TRACE-03
    cur = [p0, 1.0 - p0]
    trace = [cur[0]]
    for _ in range(steps):
        cur = apply_noise_step(cur, gamma)
        trace.append(cur[0])
    return trace
```

## Fechamento teórico

Antes de abrir o editor: (1) valor do Caso 1 no papel; (2) arquivo + função;
(3) o que **não** mudar. Por quê essa trava? Porque “compilar até passar”
sem o número no papel produz soluções que quebram no próximo fixture.
