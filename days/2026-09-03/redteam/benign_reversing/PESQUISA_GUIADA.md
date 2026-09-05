# Pesquisa guiada — reversing benigno e regras YARA

## Fontes
- YARA documentation: strings, conditions e rule syntax.
- System V AMD64 ABI / Microsoft x64 ABI conforme o binário gerado.
- ELF ou PE/COFF specification para o formato produzido no seu host.

## Termos
`YARA strings condition`, `compiler generated assembly calling convention`, `printable ASCII extraction binary`.

## Perguntas
1. Como localizar o marcador benigno no binário sem executá-lo?
2. Como a transformação de `verify_code` aparece em assembly?
3. Quais argumentos chegam em quais registradores na ABI do host?
4. Por que uma regra YARA muito genérica produz falso positivo?
5. Qual é a diferença entre indicador estático e comportamento dinâmico?

Use somente o `lab_target` fornecido/compilado por você. Não introduza malware real neste exercício.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
