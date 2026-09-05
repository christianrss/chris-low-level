# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/` e localize os TODOs.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada etapa.
5. Só então compare com `solutions/`.

---

# Red Team / Reverse Engineering - laboratório benigno

Este laboratório cria o próprio alvo educacional para reversing. Não use software de terceiros.

## O que estudar

- stack frame e calling convention;
- passagem de argumentos;
- strings e constantes em PE/ELF;
- função de verificação e branches;
- comparação entre fonte, assembly e execução;
- criação de uma pequena ferramenta defensiva para extrair strings ASCII.

## Exercícios

### Fácil
Compile `lab_target` em Debug e Release. Compare tamanhos e símbolos.

### Médio
Abra o binário próprio com `objdump -d`, Visual Studio Disassembly, x64dbg ou Ghidra. Localize `verify_code()` e identifique:

1. onde o comprimento é testado;
2. onde cada byte da entrada é transformado;
3. qual branch leva a "accepted" e qual leva a "rejected".

### Difícil
Sem alterar o binário, reconstrua em pseudocódigo C a lógica de `verify_code()` a partir do assembly.

### Tooling defensivo
Complete `starter/tools/ascii_strings.py` para extrair strings imprimíveis de um binário próprio e compare com a versão de referência.

### YARA defensivo
A regra em `solutions/rules/lab_target.yar` serve apenas para reconhecer o binário educacional pelo texto de laboratório. Ela não é uma assinatura de malware.

## Segurança

O alvo apenas valida um código local e imprime resultado. Ele não acessa rede, não persiste, não injeta processos, não evade ferramentas e não coleta dados.

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-binary-toolkit` |
| O que levar | strings/YARA-style scanning |
| Testes a replicar | unit tests on fixtures |
| Milestone | MILESTONES.md — binary toolkit |
| Commit sugerido | `feat(toolkit): port reversing helpers from day01 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
