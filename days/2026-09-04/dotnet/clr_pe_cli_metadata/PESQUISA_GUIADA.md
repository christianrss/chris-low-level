# Pesquisa guiada
Fonte normativa: ECMA-335, principalmente Partition II para metadata. Para o contêiner PE, consulte a especificação PE/COFF da Microsoft.

Procure por:
- `ECMA-335 Partition II metadata physical layout`
- `PE COFF optional header data directories CLR runtime header`
- `IMAGE_COR20_HEADER metadata`

Responda:
1. Qual a diferença entre RVA e file offset?
2. Qual data directory aponta para o CLR Runtime Header?
3. O que `BSJB` identifica?
4. Por que `VirtualSize` e `SizeOfRawData` não devem ser confundidos?
5. Por que um parser seguro verifica truncamento antes de ler qualquer inteiro?

Não use `System.Reflection` para responder o exercício: queremos aprender o formato físico.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
