# Pesquisa guiada
Leia documentação/conteúdo conceitual do V8 apenas para comparar arquitetura: parser, bytecode interpreter, optimizing compiler e deoptimization. Não copie código do V8.

Pesquise:
- `V8 Ignition bytecode interpreter`
- `V8 TurboFan optimizing compiler`
- `recursive descent parser operator precedence`
- `stack based virtual machine bytecode`

Responda:
1. Por que `x + y * 2` não pode ser compilado lendo tokens estritamente da esquerda para a direita?
2. Qual a diferença entre token, AST e bytecode?
3. O que o instruction pointer representa?
4. Por que `Sub` precisa fazer `a-b`, não `b-a`, embora `b` seja retirado da stack primeiro?
5. O que precisaremos adicionar antes de suportar closures?

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
