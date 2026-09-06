# Teoria passo a passo

## 1. Da linguagem ao CIL
C# normalmente compila para Common Intermediate Language (CIL), armazenado em assemblies. O CLR carrega metadados e executa/JIT-compila métodos. Hoje construímos um decoder minúsculo para visualizar o nível abaixo do C#.

## 2. Stream de opcodes
O decoder percorre um `byte[]` com índice `i`. Cada instrução registra offset, mnemonic e operand opcional. Alguns opcodes ocupam um byte; outros exigem operand.

## 3. `ldc.i4.s`, `add`, `ret`
`ldc.i4.s` (`0x1F`) consome um operando `int8` assinado. `add` (`0x58`) e `ret` (`0x2A`) não consomem operand adicional. O detalhe crítico é avançar `i` corretamente.

## 4. Bounds e sinal
Antes de ler o operand, cheque `i >= code.Length`. O cast para `sbyte` preserva valores negativos. Parsers de bytecode precisam tratar truncamento como erro, não como dado zero.

## 5. Próxima evolução
Depois podemos ler method bodies reais de PE/CLI metadata, construir stack-effect analysis e um interpretador educacional.

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
