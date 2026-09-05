# Pesquisa guiada — ECMA-48 / ANSI terminal state machine

## Fontes
- ECMA-48: control functions for coded character sets.
- Documentação de terminais VT100/xterm apenas para exemplos práticos de sequências.

## Termos
`ECMA-48 CSI parameters`, `ANSI escape state machine`, `CSI cursor movement erase display SGR`.

## Perguntas
1. Por que um parser incremental precisa manter estado entre bytes?
2. Qual a diferença entre ESC e CSI?
3. O que significa parâmetro omitido em movimentos de cursor?
4. Por que bytes normais devem continuar chegando à tela no estado Ground?
5. Como evitar que sequência incompleta corrompa o estado?

Implemente apenas o subset documentado no exercício; não tente suportar xterm inteiro no Day 01.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
