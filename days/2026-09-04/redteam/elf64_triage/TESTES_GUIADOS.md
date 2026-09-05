# Testes guiados — elf64_triage

Este arquivo é a ponte entre cada TODO real do `starter/` e a evidência que deve ficar verde. Não pule diretamente para `solutions/`.

## Baseline

A partir da pasta deste módulo:

```bash
python starter/tests/test_ascii_strings.py
python starter/tests/test_elf64.py
```

**Antes de implementar:** ambos falham com `NotImplementedError` antes da implementação.

## Mapa TODO → teste

### `D2-ELF-STRINGS`
- Arquivo: `starter/tools/ascii_strings.py`
- Validação: extrai runs ASCII com offset e respeita `minimum`.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-ELF-STRINGS`

### `D2-ELF-HEADER`
- Arquivo: `starter/tools/elf64.py`
- Validação: lê fixture ELF64 e rejeita truncado, magic, classe, endian e versão inválidos.
- Marcador no código de teste: `PEDAGOGY-TEST: D2-ELF-HEADER`

## Depois de concluir

Rode novamente o mesmo comando. Resultado esperado:

- ambos encerram com código 0 e mensagens de sucesso.
- Não remova/afrouxe asserts para “fazer passar”.
- Compare com `solutions/` somente depois de seu starter ficar verde.
- Acrescente pelo menos um edge case próprio e anote qual regressão ele detectaria.
