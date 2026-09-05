# Pesquisa guiada — ELF, PE/COFF e x86-64 decoding

## Fontes
- System V ABI / ELF specification.
- Microsoft PE/COFF specification.
- Intel SDM, volumes de instruction format/encoding.

## Termos
`ELF64 header section header string table`, `PE COFF optional header sections`, `x86 opcode ModRM immediate little endian`.

## Perguntas
1. Como validar magic antes de ler offsets?
2. Por que todo offset/tamanho vindo do arquivo é não confiável?
3. Qual a diferença entre file offset e virtual address?
4. Por que um decoder precisa garantir progresso mesmo para opcode desconhecido?
5. Como `INT3` e `LEAVE` são reconhecidos no subset deste laboratório?

Não copie `objdump`/LLVM. Compare a saída depois que o seu parser/decoder estiver funcional.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
