# Teoria passo a passo — Worker transfer

Worker Threads permite paralelismo de JavaScript em V8 isolates separados. Mensagens normalmente usam structured
clone. Para `ArrayBuffer`, `postMessage(value,[buffer])` transfere ownership: o sender fica com buffer detached e o
worker recebe os bytes sem copiar o backing store.

Isso é diferente de `SharedArrayBuffer`, em que ambos observam a mesma memória e precisam de atomics para
coordenação.

O laboratório mede semântica, não performance absoluta: cria buffer determinístico, transfere ao worker, calcula
soma, devolve resultado e verifica que `byteLength` no sender vira 0 depois da transferência.
