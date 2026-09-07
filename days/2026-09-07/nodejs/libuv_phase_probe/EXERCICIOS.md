# Exercícios — Node.js libuv phase probe

## Fácil — prever ordem parcial (`D5-NODE-PROBE`)

**Enunciado:** Antes de rodar, escreva ordem esperada de `sync`, `nextTick`, `promise`, `timeout`, `immediate`. Marque quais pares **não** têm ordem garantida.

**Arquivo-alvo:** caderno; compare com `await probe()`.

**Critério de aceite:** explica por que timer vs immediate não é fixo globalmente.

## Médio — implementar probe (`D5-NODE-PROBE`)

**Enunciado:** Implemente `probe` com barreira de dois callbacks macro. Valide asserts do teste manualmente.

**Arquivo-alvo:** `starter/probe.js`.

**Critério de aceite:** `e[0]==="sync"`; microtasks antes de macro no teste.

## Difícil — starvation limitada (`D5-NODE-BOUNDED`)

**Enunciado:** Implemente `boundedNextTick`. Meça quanto tempo leva `boundedNextTick(10000)` vs loop síncrono — por quê?

**Arquivo-alvo:** `starter/probe.js`.

**Critério de aceite:** retorna `limit`; `limit<0` lança.

## Desafio — trace monotônico

**Enunciado:** Extensão: log `[hrtime, tag]` em probe. Prove monotonicidade dos timestamps por callback (não ordem total entre fases).

**Arquivo-alvo:** extensão local em `probe.js`.

**Critério de aceite:** relatório com 3 observações sobre overhead de instrumentação.
