# Pesquisa guiada — hash chains, Merkle tree e PoW educacional

## Fontes
- NIST FIPS 180-4 para SHA-256.
- Bitcoin whitepaper, seções de timestamp server, proof-of-work e Merkle tree, apenas como referência conceitual.

## Termos
`SHA-256 canonical serialization`, `Merkle tree duplicate odd leaf`, `hash chain tamper detection`, `proof of work leading zero bits`.

## Perguntas
1. Por que a serialização precisa ser canônica antes do hash?
2. O que muda no Merkle root se uma transação muda?
3. Por que cada bloco inclui o digest anterior?
4. Como dificuldade baseada em zeros é apenas uma simplificação do conceito de target?
5. Por que este laboratório não deve ser tratado como blockchain de produção?

Não reutilize código de criptomoedas reais. Este módulo é local, determinístico e educacional.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
