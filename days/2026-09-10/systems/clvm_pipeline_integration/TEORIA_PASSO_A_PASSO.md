# Teoria passo a passo — Pipeline CLVM: disasm + peephole + verify

Este laboratório é em **Python**.

## 1. O que estamos construindo

Capstone systems: junta disassembler, peephole `PUSH 0; ADD`→noop, e verificação de stack no mesmo bytecode.

## 2. Por que este módulo existe neste dia

Por quê estudar isso agora? Porque o contrato numérico do teste fixa o vocabulário
do resto do dia — sem o paper-trace, o código “quase certo” passa no olho e falha
no assert.

## 3. Formato / contrato de dados (wire)

| Bytes | Listing |
|-------|---------|
| `01 01  01 02  02  08` | PUSH 1, PUSH 2, ADD, HALT |
| peephole in: `01 00 02 01 05 08` | PUSH 0, ADD, PUSH 5, HALT |
| peephole out | `01 05 08` (PUSH 5, HALT) |

Opcodes: PUSH=0x01 (+imm), ADD=0x02, HALT=0x08.

## 4. Trace numérico (valores dos testes)

Siga no papel **antes** de abrir o editor. Estes números são os do Caso 1.

```text
disasm([01,1, 01,2, 02, 08]) → ["PUSH 1","PUSH 2","ADD","HALT"]
fold PUSH0+ADD → bytes([0x01,5,0x08])
verify_stack(code) → True
```

## 5. Algoritmo (ordem obrigatória)

1. disasm: avance pc conforme tamanho do opcode.
2. peephole: remova padrão PUSH 0 / ADD.
3. verify: simule altura de stack sem underflow.

## 6. Invariantes

- A saída é determinística para a mesma entrada do teste.
- Erros de pré-condição falham **agora** (retorno negativo, `Err`, `false`, exceção),
  não um default silencioso.
- O valor que o assert compara é o da seção de trace — não um sinônimo.

## 7. Bugs que o teste rejeita

- Esquecer immediates no disasm.
- Não remover o par PUSH0+ADD.
- verify que ignora underflow.

## 8. Lab versus produção

Compiladores reais fazem peephole em IR; aqui é bytecode linear.

## Modelo mental

bytes → texto → bytes otimizados → ok/fail de stack.

## Por quê apagar PUSH 0 + ADD?

x+0=x; o imediato 0 é morto.

## Por quê verify separado?

Disasm pode listar programa inválido; verify protege a VM.

## Invariante

Após peephole, semântica aritmética do Caso 1 preserva PUSH 5 HALT.

## Ligação

Dia 08 disasm/peephole; Dia 09 trace profiler.

## Paper-trace

Escreva as 4 linhas do disasm antes de codar.


## Por quê — síntese

### Por quê estas invariantes?
Cada `TODO [ID]` isola uma propriedade que quebra silenciosamente se ignorada.

### Por quê medir?
O `BENCHMARK_GUIADO.md` pede a métrica `1e4 disasm+peep` — mesmo que o ambiente
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

Neste módulo `systems/clvm_pipeline_integration`, o fluxo de dados não é abstrato: cada função do starter
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
"""CLVM pipeline: disasm → peephole → verify."""
from __future__ import annotations

PUSH, ADD, HALT = 0x01, 0x02, 0x08


def disasm(code: bytes) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-CLVM-DIS-01
    out: list[str] = []
    i = 0
    while i < len(code):
        op = code[i]
        if op == PUSH:
            out.append(f"PUSH {code[i+1]}")
            i += 2
        elif op == ADD:
            out.append("ADD")
            i += 1
        elif op == HALT:
            out.append("HALT")
            i += 1
        else:
            return []
    return out


def peephole(code: bytes) -> bytes:
    # PEDAGOGY-SOLUTION: CAP-CLVM-PEEP-02
    out = bytearray()
    i = 0
    while i < len(code):
        if i + 3 <= len(code) and code[i] == PUSH and code[i+1] == 0 and code[i+2] == ADD:
            i += 3
            continue
        out.append(code[i])
        i += 1
    return bytes(out)


def verify_stack(code: bytes) -> bool:
```

## Fechamento teórico

Antes de abrir o editor: (1) valor do Caso 1 no papel; (2) arquivo + função;
(3) o que **não** mudar. Por quê essa trava? Porque “compilar até passar”
sem o número no papel produz soluções que quebram no próximo fixture.
