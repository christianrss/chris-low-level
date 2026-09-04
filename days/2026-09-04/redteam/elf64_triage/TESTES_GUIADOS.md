# Testes guiados — ELF64 triage

Rode primeiro:

```bash
python starter/tests/test_ascii_strings.py
python starter/tests/test_elf64.py
```

Leia os fixtures como especificação executável do subset suportado.

Adicione casos para header truncado, magic errada, classe 32-bit e big-endian. Todo input inválido deve falhar de forma controlada, nunca por acesso fora do buffer.
