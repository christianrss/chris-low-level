# Pesquisa guiada — Node/libuv

## Fontes primárias / técnicas

- [Node.js — Event loop](https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick) — ordem oficial.
- libuv design notes — fases poll/check/idle.
- Documentação `process.nextTick` vs `setImmediate`.

## Perguntas antes de implementar

1. Por que **não** assumir `setTimeout(0)` sempre antes de `setImmediate`?
2. Como recursão de `nextTick` causa **starvation** de I/O?
3. Quando preferir `setImmediate` a `process.nextTick` para fatiar CPU?
4. Onde microtasks (`Promise`) rodam relative ao nextTick queue?

## Investigação prática

1. Rode probe em duas versões Node (se disponível) — ordem timer/immediate mudou?
2. Implemente loop CPU 100% sem yield — observe latência de timer.
3. Leia issue/discussão sobre depreciação futura de nextTick — impacto em APIs?

## Depois da implementação

Documente simplificações do probe, invariante testado (micro antes de macro) e métrica operacional (ex.: latência p99 com/sem yield).
