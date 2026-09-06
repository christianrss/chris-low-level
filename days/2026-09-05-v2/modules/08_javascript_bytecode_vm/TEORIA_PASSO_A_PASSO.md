# Teoria passo a passo

## 1. VM de bytecode
A VM mantém `ip` (instruction pointer), stack e programa. Cada instrução altera estado. Branches são o primeiro passo para sair de uma sequência linear e expressar `if`, loops e controle de fluxo.

## 2. JZ
`JZ target` remove uma condição da stack. Se ela for zero, `ip` vira `target`; caso contrário, avança uma instrução. O erro clássico é sobrescrever `ip` e depois incrementá-lo novamente.

## 3. JMP
`JMP target` é salto incondicional. O target precisa ser interpretado com a mesma convenção usada pelo assembler/programa de teste.

## 4. Trace
Para depurar uma VM, trace `ip`, instrução atual e snapshot da stack. Isso transforma bugs de controle de fluxo em uma sequência observável.

## 5. Evolução
Com branches estáveis podemos adicionar call frames, locals, exceptions, bytecode verifier, inline cache e JIT educacional.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.

## O quê

Este módulo ensina o conceito central do laboratório v2 com foco operacional no `starter/`.

## Como

Siga os `TODO [ID]` no starter; use a resolução para localizar arquivo/função e o que substituir.

| Etapa | Ação |
|-------|------|
| 1 | Ler README e mapa de TODOs |
| 2 | Implementar no starter |
| 3 | Rodar testes |

## Por que

Sem teoria mínima o aluno não conecta o exercício ao sistema maior.

## Por que (design)

O formato v2 compacta o dia 05; ainda assim cada módulo precisa de O quê/Como/Por quê verificáveis.

## Por que (qualidade)

O checker unificado exige ≥120 linhas, diagrama/tabela e ≥3 seções Por quê.

## Invariantes

- Cada TODO tagueado aparece em starter, solução, testes e resolução.
- Placement (Onde colocar) por ID.

## Bugs comuns

| Sintoma | Causa | Debug |
|---------|-------|-------|
| teste FAIL | stub não substituído | abra a âncora TODO |
| parse errado | ordem de campos | compare com solutions |

## Trace manual

No papel: anote entrada → transformação → saída esperada do primeiro teste do módulo.
