# Testes guiados - CLVM

## Por que testar esta VM?

Uma VM interpreta bytes que controlam fluxo de execução. Um erro de tamanho, salto ou pilha pode virar leitura fora do limite ou comportamento incorreto. Os testes servem para transformar regras do formato em invariantes executáveis.

## Teste 1 - assembler + loader + VM (integração)

**Invariante:** `arithmetic.asm` deve montar, carregar e imprimir `38`.

1. Compile `solutions/`.
2. Use `tools/assemble.py` para gerar `arithmetic.clvm` dentro do diretório de build.
3. Execute `clvm arithmetic.clvm`.
4. Capture `stdout`.
5. Falhe o teste se a saída, removendo espaços finais, não for `38`.

Esse teste atravessa quatro componentes: parser de assembly, serializer, loader e interpretador.

## Teste 2 - checksum corrompido (negativo/regressão)

1. Gere um arquivo válido.
2. Inverta um bit do último byte sem recalcular o checksum.
3. Execute a VM.
4. O processo deve terminar com erro e mencionar `checksum mismatch`.

Se no futuro alguém remover a validação de checksum, este teste falhará.

## Teste 3 - divisão por zero

Monte `PUSH 7; PUSH 0; DIV; HALT`. A VM deve recusar a operação sem crash.

## Teste 4 - salto inválido

Crie um bytecode cujo `JMP` aponte para fora do código. A VM deve detectar o destino inválido.

## Como depurar um teste quebrado

Use `--trace` e acompanhe `pc`, opcode e stack. Se a falha ocorrer antes da execução, coloque breakpoint em `clvm_parse`. Se ocorrer em branch, observe o valor de `pc` antes e depois de `checked_jump`.

## Cobertura pedagógica auditada

Os IDs abaixo precisam ter um critério de verificação antes de o módulo ser considerado concluído.

- `CLVM-VM-ARITH-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `CLVM-VM-JUMP-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `CLVM-C-FNV-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `CLVM-C-HEADER-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `CLVM-PY-FNV-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `CLVM-ASM-LABELS-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.

Arquivos de teste automatizado presentes no starter:
- `starter/tests/integration_test.py`
