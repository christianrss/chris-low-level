# Pesquisa guiada — legacy BIOS boot sector

## Fontes
- Intel SDM: estado inicial/real mode, como contexto.
- Documentação histórica de BIOS interrupts, especialmente vídeo INT 10h.
- Referências de MBR/boot sector sobre assinatura `0x55AA`.

## Termos
`x86 BIOS boot sector 0x7c00`, `boot signature 55 aa offset 510`, `BIOS int 10 teletype`.

## Perguntas
1. Por que o setor precisa ter exatamente 512 bytes neste laboratório?
2. Em quais offsets ficam `0x55` e `0xAA`?
3. O que BIOS fornece e o que ainda não é um sistema operacional?
4. Qual a diferença entre bytes gerados pelo builder e o source NASM equivalente?

Não assuma que BIOS legado representa UEFI moderno; o módulo é um primeiro degrau histórico/arquitetural.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
