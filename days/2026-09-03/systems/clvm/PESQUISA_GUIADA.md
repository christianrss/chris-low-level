# Pesquisa guiada — bytecode VM e formato binário

## Fontes
- FNV-1a specification/reference para checksum educacional.
- Documentação de VMs stack-based (JVM/WebAssembly como contraste arquitetural, não como formato a copiar).
- Conceitos de endianness e binary file parsing.

## Termos
`stack virtual machine bytecode dispatch`, `FNV-1a 32 bit`, `relative branch bytecode`, `binary format magic version checksum`.

## Perguntas
1. Quais bytes pertencem ao header e quais ao code payload?
2. O checksum cobre exatamente qual região?
3. Como o assembler resolve labels em dois passes?
4. Como validar jump relativo para impedir sair do code segment?
5. Por que assembler, loader, validator e VM precisam concordar sobre o mesmo formato?

JVM/WASM são referências de engenharia; CLVM tem formato e opcodes próprios definidos no repositório.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
