# Testes guiados — hid_report_fuzz

## Caso 1 — `RT-HID-MAGIC-01`

`python starter/test_hid_fuzz.py` — relatório de 8 bytes passa `validate_hid_boot_length`.

## Caso 2 — tamanho inválido

Buffer de 7 bytes deve retornar `False` em MAGIC-01.

## Caso 3 — `RT-HID-BOUNDS-02`

Seis usages em bytes 2..7 → `count_nonzero_key_slots == 6`.

## Caso 4 — `RT-HID-STRINGS-03`

Tecla A (`0x04`) → lista contém `usage:0x04`.

## Debug

| Sintoma | Causa | Ação |
|---------|-------|------|
| MAGIC sempre True | não checou `len==8` | compare com fixture `report_short.raw` |
| BOUNDS -1 | passou buffer curto | valide MAGIC antes |
