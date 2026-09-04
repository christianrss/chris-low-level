# Testes guiados - MiniObjdump

## Teste 1 - reconhece o formato do próprio alvo

Compile `test_target`. Execute `miniobjdump test_target`. Em Linux espere `Format: ELF`; em Windows, `Format: PE`.

## Teste 2 - encontra seção de código

A saída deve conter `.text`. Este é um teste de integração entre parser de headers e resolução de nomes de seção.

## Teste 3 - arquivo inválido

Crie um arquivo com 64 bytes zero. O programa deve retornar erro, não crashar nem ler fora do buffer.

## Teste 4 - regressão de decoder

Escolha bytes curtos que o decoder já conhece, por exemplo `90 C3` (`NOP`, `RET`). Extraia a função de decode para que possa ser chamada em um teste unitário. Depois fixe a saída esperada.

## Próximo passo de qualidade

Quando ModR/M for implementado, adicione uma tabela de casos de instrução/bytes esperados e compare também com `objdump` ou `dumpbin` como referência externa, sem usar essas ferramentas na implementação.

## Cobertura pedagógica auditada

Os IDs abaixo precisam ter um critério de verificação antes de o módulo ser considerado concluído.

- `OBJDUMP-U16-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `OBJDUMP-U32-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `OBJDUMP-PARSE-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.

Arquivos de teste automatizado presentes no starter:
- `starter/tests/test_target.c`
- `starter/tests/integration_test.py`
