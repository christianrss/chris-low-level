# Testes guiados - reversing benigno

Todos os testes usam somente dados próprios do laboratório.

## Teste 1 - extrator encontra uma string longa

Use `b"\x00HELLO_LOW_LEVEL\x00"`. O resultado deve conter o texto e o offset `1`.

## Teste 2 - limite mínimo

Com `minimum=5`, `b"ABCD\x00ABCDE\x00"` deve retornar somente `ABCDE`.

## Teste 3 - bytes não imprimíveis quebram a sequência

`b"ABC\x01DEF"` não deve ser tratado como uma única string.

## Teste 4 - arquivo vazio

`extract_ascii_strings(b"")` deve retornar uma lista vazia.

## Por que isto importa para reversing?

Parsers binários vivem de limites e classificação de bytes. Esses testes treinam a mesma disciplina que você usará ao implementar PE/ELF parsing, hex view e disassembly.
