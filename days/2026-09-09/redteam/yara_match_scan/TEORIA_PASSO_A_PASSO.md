# Teoria passo a passo — Scan estilo YARA (Python)

Este laboratório é em **Python**.

## 1. O que estamos construindo

Regras YARA misturam bytes fixos e wildcards. O lab parseia padrão `AA ??`, casa em offset e devolve lista de hits.

## 2. Por que este módulo existe neste dia

Por quê estudar isso agora? Porque o contrato numérico do teste fixa o vocabulário
do resto do dia — sem o paper-trace, o código “quase certo” passa no olho e falha
no assert.

## 3. Formato / contrato de dados (wire)

| Entrada | Saída |
|---------|-------|
| padrão parseado | `[0xAA, None]` (None = wildcard) |
| data com match @1 | `match_at(..., 1)` True |
| scan_all | `[1]` |

## 4. Trace numérico (valores dos testes)

Siga no papel **antes** de abrir o editor. Estes números são os do Caso 1.

```text
pat = [0xAA, None]
match_at(data, pat, 1) → True
scan_all(data, pat) → [1]
```

## 5. Algoritmo (ordem obrigatória)

1. parse: bytes hex; `??` → None.
2. match_at: para cada i, pat[i] is None ou == data[off+i].
3. scan_all: todos off onde match_at.

## 6. Invariantes

- A saída é determinística para a mesma entrada do teste.
- Erros de pré-condição falham **agora** (retorno negativo, `Err`, `false`, exceção),
  não um default silencioso.
- O valor que o assert compara é o da seção de trace — não um sinônimo.

## 7. Bugs que o teste rejeita

- Tratar ?? como 0.
- Off-by-one no fim do buffer.
- scan_all devolver bool.

## 8. Lab versus produção

YARA compila regras; aqui só o motor de bytes/wildcards.

## Modelo mental

máscara de bytes com buracos.

## Por quê None?

Sentinela de wildcard sem colidir com 0x00.

## Por quê offset 1 no teste?

Fixture posiciona o padrão fora do início.

## Invariante

len(pat) bytes a partir de off devem caber em data.

## Ligação

Dia 10 capstone_triage detecta magic ELF/PE/WASM.

## Segurança

Não ler além de len(data).


## Por quê — síntese

### Por quê estas invariantes?
Cada `TODO [ID]` isola uma propriedade que quebra silenciosamente se ignorada.

### Por quê medir?
O `BENCHMARK_GUIADO.md` pede a métrica `scan_all em 1MB sintético` — mesmo que o ambiente
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

Neste módulo `redteam/yara_match_scan`, o fluxo de dados não é abstrato: cada função do starter
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
"""YARA-style hex pattern scanner."""

from __future__ import annotations


def parse_hex_pattern(pat: str) -> list[int | None]:
    # PEDAGOGY-SOLUTION: RT-YARA-PARSE-01
    body = pat.strip("{} ").replace(" ", "")
    out: list[int | None] = []
    i = 0
    while i < len(body):
        if body[i:i+2] == "??":
            out.append(None); i += 2
        else:
            out.append(int(body[i:i+2], 16)); i += 2
    return out


def match_at(data: bytes, pattern: list[int | None], off: int) -> bool:
    # PEDAGOGY-SOLUTION: RT-YARA-MATCH-02
    if off + len(pattern) > len(data):
        return False
    for i, b in enumerate(pattern):
        if b is not None and data[off + i] != b:
            return False
    return True


def scan_all(data: bytes, pattern: list[int | None]) -> list[int]:
    # PEDAGOGY-SOLUTION: RT-YARA-TRIAGE-03
    return [i for i in range(len(data)) if match_at(data, pattern, i)]
```

## Fechamento teórico

Antes de abrir o editor: (1) valor do Caso 1 no papel; (2) arquivo + função;
(3) o que **não** mudar. Por quê essa trava? Porque “compilar até passar”
sem o número no papel produz soluções que quebram no próximo fixture.
