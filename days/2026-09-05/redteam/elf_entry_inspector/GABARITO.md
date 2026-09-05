# Gabarito — Red Team — Inspector ELF64 Entry

Respostas esperadas (consulte `solutions/` para código completo).

1. parse_ident valida 16 bytes iniciais.
2. struct.unpack_from('<HHIQ', data, 16).
3. Fixture tem e_machine=62, e_entry=0x401000.
4. Truncado ou magic inválido → ValueError.
