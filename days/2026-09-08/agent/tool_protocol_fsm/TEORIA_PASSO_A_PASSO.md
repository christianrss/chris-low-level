# Teoria passo a passo — FSM de protocolo de ferramenta

Este laboratório é em **Python**. Não é um esboço em Python com o mesmo nome.

## Por que este laboratório existe

O loop do Dia 07 percebe e verifica. Este Python (harness, não bytecode) só deixa a ferramenta andar IDLE → CALLING → WAITING → DONE ou ERROR.

Por quê começar pelo formato, e não pela API da linguagem? Porque o bug clássico
aqui é **desalinhamento**: o programa “funciona” no exemplo errado e falha no
assert do teste com um número diferente do esperado.

## Contrato de dados

| Campo | Papel neste lab |
|-------|-------------|
| formato | ver a tabela abaixo |
| teste | compara o número do trace, não a intenção |

| Estado | Evento | Próximo |
|--------|--------|---------|
| IDLE | call | CALLING |
| CALLING | sent | WAITING |
| WAITING | ok | DONE |
| WAITING | err | ERROR |

## Trace numérico (os mesmos valores do teste)

Siga no papel **antes** de abrir o editor. Os números abaixo são os do Caso 1,
não um espaço em branco para preencher depois.

```text
fsm.transition("call") == "CALLING"
trace anexa "call->CALLING"
transition("sent") → WAITING
handle_response(True, {"result": 1}) → state DONE
  payload_keys = ["result"]
validate_tool_call("search", {}) == True
segundo fsm: call, sent, handle_response(False, {}) → ERROR
evento fora da tabela → ValueError
```

## Algoritmo (ordem obrigatória)

1. transition consulta TRANSITIONS[(state, event)]. Se não houver, ValueError sem mudar estado.
2. handle_response chama transition("ok" ou "err") e devolve state + keys.
3. validate_tool_call exige name não vazio e args dict.

## Invariantes

- A saída é determinística para a mesma entrada.
- Tamanho consumido e texto/valor produzido mudam juntos: se o tamanho estiver
  errado, o próximo byte é lido como opcode e o teste vê outra string.
- Erro de formato falha **agora** (retorno negativo, `Err`, `false`, exceção),
  não um valor default silencioso.

## Bugs que o teste rejeita

- Aceitar call a partir de WAITING: a chave não existe, o teste do ERROR path não chega se você não recusar.
- validate("", {}) deve ser falso.

## Lab versus produção

O harness em projects/chris-agent-harness registra a mesma trilha. Aqui a evidência é o trace.

## Checklist antes de compilar

- [ ] Escrevi no papel o valor esperado do Caso 1 (está na seção de trace).
- [ ] Sei qual arquivo e qual função recebem o corpo novo.
- [ ] Sei o que **não** mudar (assinatura, nomes dos opcodes, capacidade do buffer).

Por quê não pular o trace? O teste compara bytes, não a intenção.

## Mecanismo interno (segunda camada)

Neste módulo `agent/tool_protocol_fsm`, o fluxo de dados não é abstrato: cada função do starter
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
"""Tool calling FSM — IDLE→CALLING→WAITING→DONE/ERROR."""

from __future__ import annotations

TRANSITIONS = {
    ("IDLE", "call"): "CALLING",
    ("CALLING", "sent"): "WAITING",
    ("WAITING", "ok"): "DONE",
    ("WAITING", "err"): "ERROR",
}


class ToolProtocolFSM:
    def __init__(self):
        self.state = "IDLE"
        self.trace: list[str] = []

    def transition(self, event: str) -> str:
        # PEDAGOGY-SOLUTION: AGT-TOOL-01
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise ValueError(key)
        self.state = TRANSITIONS[key]
        self.trace.append(f"{event}->{self.state}")
        return self.state

    def handle_response(self, ok: bool, payload: dict) -> dict:
        # PEDAGOGY-SOLUTION: AGT-TOOL-02
        self.transition("ok" if ok else "err")
        return {"state": self.state, "payload_keys": list(payload.keys())}

    def validate_tool_call(self, name: str, args: dict) -> bool:
        # PEDAGOGY-SOLUTION: AGT-TOOL-03
        return bool(name) and isinstance(args, dict)
```

## Grafo do protocolo de tool-call

```text
IDLE --call--> CALLING --sent--> WAITING --ok--> DONE
                                   |
                                   +--err--> ERROR
```

`TRANSITIONS` dict:

```text
(IDLE, call) → CALLING
(CALLING, sent) → WAITING
(WAITING, ok) → DONE
(WAITING, err) → ERROR
```

Trace:

```text
transition("call") → CALLING; trace ["call->CALLING"]
handle_response(True, {"x":1}) → state DONE, keys ["x"]
validate_tool_call("", {}) → False
validate_tool_call("search", {"q":"a"}) → True
```

**Por quê** FSM? Agentes que disparam tools sem estado viram
reentrância e double-submit. Aresta ilegal levanta `ValueError`.

## Invariantes

- Estado só muda via tabela
- Evento ilegal **não** altera `state` (exceção antes)
- `validate_tool_call` exige nome não-vazio e `dict`

## Bugs comuns

- Aceitar IDLE→DONE direto
- `handle_response` sem chamar `transition`
- Validar só `name` e ignorar tipo de `args`

## Lab vs produção

LangGraph / OpenAI tool protocol têm retries e timeouts.
Aqui o núcleo é a **máquina de estados** testável.

## Checklist

- [ ] IDLE→call→CALLING
- [ ] WAITING+err→ERROR
- [ ] aresta ilegal → ValueError
