# Teoria passo a passo

## 1. Streams em Node
Streams permitem processar dados incrementalmente. `Transform` recebe chunks, produz outros chunks e mantém estado entre chamadas. Nosso `LineTransform` precisa lidar com linhas que atravessam fronteiras de chunk.

## 2. UTF-8 e chunk boundaries
Um caractere multibyte como `€` pode chegar dividido. `StringDecoder` guarda bytes incompletos e só devolve texto válido quando há bytes suficientes. Concatenar `chunk.toString()` ingenuamente pode corromper caracteres.

## 3. Buffer lógico de linha
`this.pending` guarda o fragmento que ainda não terminou em `\n`. A cada `_transform`, combine pending + texto decodificado, separe linhas completas e retenha a cauda. `_flush` entrega o restante no fim do stream.

## 4. Backpressure
Em Writable, `write()` retornar `false` significa que o buffer interno passou do limite de pressão. O produtor deve parar e aguardar `drain`. Ignorar isso pode aumentar memória e latência. O arquivo `backpressure_demo.js` existe de verdade no starter/solution para observar esse mecanismo.

## 5. Relação com libuv
O stream é uma abstração JS construída sobre event loop e I/O assíncrono. A trilha futura desce para libuv, handles, requests e filas do event loop.

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
