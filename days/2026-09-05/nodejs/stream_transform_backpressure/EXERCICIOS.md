# Exercícios — Node streams

## Fácil — NODE-XFORM-01
Explique por que `chunk.toString('utf8')` falha quando `€` cruza chunks.

## Médio — NODE-XFORM-01
Implemente `_transform` e `_flush` até `assert.deepEqual(lines, ['a', '', 'b€', 'c'])`.

## Médio — NODE-BACKPRESSURE-02
Complete `runBackpressureDemo()` aguardando `drain` quando `write` retorna false.

## Difícil
Adicione teste com arquivo de 1 MiB e meça tempo com/sem respeitar backpressure.

## Desafio
Implemente Transform que conta linhas e emite número a cada 1000 linhas.

## Reflexão
Como backpressure se relaciona com `pipeline()` e `stream.promises`?
