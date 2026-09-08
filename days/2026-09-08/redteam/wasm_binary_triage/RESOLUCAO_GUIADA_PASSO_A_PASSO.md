# Resolução guiada passo a passo — WASM binary triage

Edite `starter/wasm_triage.py`.

### TODO D6-WASM-ULEB
`read_u32_leb(data, offset)` mantém `value=0`, `shift=0`. Por no máximo 5 iterações:
```python
if offset >= len(data): raise ValueError("truncated ULEB128")
b=data[offset]; offset+=1
value |= (b & 0x7f) << shift
if b & 0x80 == 0: return value, offset
shift += 7
```
Depois do quinto byte ainda continuado, rejeite.

### TODO D6-WASM-HEADER
Em `parse_sections`, exija len>=8, magic e versão 1.

### TODO D6-WASM-SECTIONS
Cursor começa em 8. Leia `section_id`, depois ULEB payload size. Calcule end e verifique `end <= len(data)`.
Registre `{id, header_offset, payload_offset, payload_size}` e avance cursor=end.

Fixture: uma custom section id=0 com payload `abc` vira bytes `00 03 61 62 63`.
Execute `python starter/test_wasm_triage.py`. Nenhum arquivo externo é usado.
