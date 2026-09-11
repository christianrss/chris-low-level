# Teoria passo a passo — GPU timer query (simulação headless)

Este laboratório é em **Python**.

## 1. O que estamos construindo

APIs gráficas expõem timer queries. Este lab simula begin/end com perf_counter e guarda laps por nome — testável sem GPU.

## 2. Por que este módulo existe neste dia

Por quê estudar isso agora? Porque o contrato numérico do teste fixa o vocabulário
do resto do dia — sem o paper-trace, o código “quase certo” passa no olho e falha
no assert.

## 3. Formato / contrato de dados (wire)

| Passo | Resultado |
|-------|-----------|
| begin_query("draw") | handle **0** (primeiro) |
| end_query(0) | ms ≥ 0.0 |
| lap_times() | contém chave "draw" |

VISUAL-01 (relatório): lap draw > 0 ms quando houver trabalho real entre begin/end.

## 4. Trace numérico (valores dos testes)

Siga no papel **antes** de abrir o editor. Estes números são os do Caso 1.

```text
h = begin_query("draw")  # 0
ms = end_query(h)        # >= 0
laps["draw"] == ms
```

## 5. Algoritmo (ordem obrigatória)

1. begin: aloca handle, guarda (name, t0).
2. end: pop start, ms=(now-t0)*1000, guarda em _laps.
3. lap_times: cópia do dict.

## 6. Invariantes

- A saída é determinística para a mesma entrada do teste.
- Erros de pré-condição falham **agora** (retorno negativo, `Err`, `false`, exceção),
  não um default silencioso.
- O valor que o assert compara é o da seção de trace — não um sinônimo.

## 7. Bugs que o teste rejeita

- Sempre retornar handle −1.
- Não gravar lap.
- end sem pop (vazamento de starts).

## 8. Lab versus produção

GL_TIME_ELAPSED / D3D timestamp queries; aqui clock de CPU proxy.

## Modelo mental

handle → (nome, t0) → lap ms.

## Por quê headless?

CI sem GPU; o contrato de estados ainda treina a API de query.

## Por quê handle sequencial?

Teste afirma h==0 no primeiro begin.

## Invariante

Após end, handle some de _starts e aparece em _laps.

## Ligação

Dia 07 raster labs; este foca telemetria, não pixels.

## Benchmark

Meça ms de um sleep curto entre begin/end.


## Por quê — síntese

### Por quê estas invariantes?
Cada `TODO [ID]` isola uma propriedade que quebra silenciosamente se ignorada.

### Por quê medir?
O `BENCHMARK_GUIADO.md` pede a métrica `ms do lap draw (3 corridas)` — mesmo que o ambiente
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

Neste módulo `graphics/gpu_timer_query`, o fluxo de dados não é abstrato: cada função do starter
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
"""GPU timer query simulation (headless)."""

from __future__ import annotations

import time


class GpuTimerSim:
    def __init__(self) -> None:
        self._next = 0
        self._starts: dict[int, tuple[str, float]] = {}
        self._laps: dict[str, float] = {}

    def _clock(self) -> float:
        return time.perf_counter()

    def begin_query(self, name: str) -> int:
        # PEDAGOGY-SOLUTION: GFX-GPU-TIMER-01
        h = self._next
        self._next += 1
        self._starts[h] = (name, self._clock())
        return h

    def end_query(self, handle: int) -> float:
        # PEDAGOGY-SOLUTION: GFX-GPU-LAP-02
        name, t0 = self._starts.pop(handle)
        ms = (self._clock() - t0) * 1000.0
        self._laps[name] = ms
        return ms

    def lap_times(self) -> dict[str, float]:
        # PEDAGOGY-SOLUTION: GFX-GPU-BENCH-03
        return dict(self._laps)
```

## Fechamento teórico

Antes de abrir o editor: (1) valor do Caso 1 no papel; (2) arquivo + função;
(3) o que **não** mudar. Por quê essa trava? Porque “compilar até passar”
sem o número no papel produz soluções que quebram no próximo fixture.
