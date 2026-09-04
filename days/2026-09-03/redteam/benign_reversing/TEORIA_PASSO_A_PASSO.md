# Red Team / Reverse Engineering seguro - do C ao assembly

## Limite de segurança do laboratório

Use somente `lab_target`, que é um programa benigno criado dentro deste pacote. O objetivo é compreender binários, assembly e debugging. Não há malware, persistência, evasão ou ataque a terceiros.

## O que você precisa entender antes de começar

### Código-fonte, compilador e executável

O arquivo `.c` é texto para humanos. O compilador transforma esse texto em instruções de máquina e metadados de um executável PE no Windows ou ELF no Linux.

### Análise estática e dinâmica

- estática: examinar o arquivo sem executá-lo;
- dinâmica: executar sob um debugger e observar estado em tempo real.

As duas abordagens se complementam.

### Registradores e calling convention

Um processador x86-64 possui registradores como RAX, RBX, RCX, RDX, RSP, RBP e RIP. `RIP` aponta para a instrução atual/seguinte. `RSP` aponta para o topo da stack.

A convenção de chamada define onde argumentos e retornos ficam. Em Windows x64, os quatro primeiros argumentos inteiros/ponteiros normalmente usam RCX, RDX, R8 e R9. Em System V AMD64 (Linux), usam RDI, RSI, RDX, RCX, R8 e R9. O retorno inteiro normalmente vem em RAX.

### Stack frame

Funções podem reservar espaço na stack para variáveis locais e salvar estado. Em builds sem otimização, é comum encontrar padrões com `push rbp`, `mov rbp, rsp` em ambientes que preservam frame pointer. Otimizações podem mudar completamente esse formato.

### Strings

Strings ASCII ficam como sequências de bytes imprimíveis terminadas por zero. Procurá-las é uma técnica inicial de triagem. Neste laboratório você constrói seu próprio extrator de strings em Python.

### YARA

YARA descreve padrões para identificar arquivos. Aqui a regra detecta somente o nosso binário educacional por strings controladas. Isso ensina o formato sem depender de malware real.

### O alvo benigno

`verify_code` transforma cada byte da entrada:

```text
transformed = (input[i] XOR 0x2A) + i
```

Depois compara com uma tabela constante. A tarefa não é força bruta; é reconstruir a lógica ao ler o fonte, o assembly e o estado do debugger.

## Passo a passo guiado

1. Compile `solutions/src/lab_target.c` em Debug e Release e compare os binários.
2. Rode com uma entrada errada para entender o comportamento externo.
3. Use seu `ascii_strings.py` e localize `LOWLEVEL-REVERSING-LAB-V1`, `accepted` e `rejected`.
4. No Linux, compare com `objdump -d`; no Windows, use `dumpbin /disasm` se disponível.
5. Em x64dbg/Visual Studio Debugger/WinDbg, abra somente o `lab_target` do laboratório.
6. Coloque breakpoint em `main` e, se os símbolos estiverem disponíveis, em `verify_code`.
7. Observe os argumentos conforme a calling convention do seu sistema.
8. Acompanhe o loop e identifique XOR, soma do índice e comparação.
9. Escreva em pseudocódigo o que o assembly faz antes de olhar o fonte da solução.
10. Complete a regra YARA educacional.

## Exercícios

- Fácil: construir o extrator ASCII.
- Médio: identificar no assembly o loop de comparação e os registradores usados.
- Difícil: reconstruir `verify_code` em pseudocódigo a partir do assembly.
- Desafio: explicar por que Debug e Release produzem assembly diferente mesmo implementando a mesma lógica.
