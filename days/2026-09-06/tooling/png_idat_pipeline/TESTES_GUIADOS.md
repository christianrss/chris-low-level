# Testes guiados — PNG IDAT pipeline

## Por que testar este encoder?

Um byte errado no CRC, no endian do IHDR ou no filtro quebra viewers sem stack trace útil. Os asserts amarram a spec a um fixture 3×2 reproduzível.

## Como rodar

```powershell
cmake --build days/2026-09-06/tooling/png_idat_pipeline/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/png_idat_pipeline/starter/build -C Release --output-on-failure
```

Arquivo: `starter/test_png.cpp`.

Fixture:

```text
width=3 height=2 depth=8 color=0
pixels = 10 20 30 40 50 60
```

---

## Teste 1 — chunk length/type/CRC (`COMP-PNG-01`)

**Invariante:** `png_chunk("IHDR", ihdr).size() == 4+4+13+4`.

1. Construa IHDR (após COMP-PNG-02) ou data dummy de 13 B.
2. Empacote com `png_chunk`.
3. `REQUIRE` tamanho 25.

Extra manual: CRC de `"IEND"` == `0xAE426082`.

## Teste 2 — IHDR 13 bytes (`COMP-PNG-02`)

**Invariante:** layout fixo.

1. `build_ihdr(img)`.
2. `REQUIRE(size==13 && ihdr[8]==8 && ihdr[9]==0)`.
3. Confira hex BE width/height na TEORIA.

## Teste 3 — filter None (`COMP-PNG-03`)

**Invariante:** stride `width+1`.

1. `filter_none_scanlines(img)`.
2. `REQUIRE(size == (3+1)*2)`.
3. `REQUIRE(filtered[0]==0 && filtered[1]==10)`.

## Teste 4 — round-trip encode/decode (`COMP-PNG-04`)

**Invariante:** signature PNG + pixels idênticos.

1. `encode_png(img)` → `blob[0]==137`, `blob[1]==80`.
2. `decode_png(blob)`.
3. `REQUIRE` width/height/pixels iguais ao original.

## Como depurar

- Se CRC falha: dump type+data e compare com `crc32` isolado.
- Se pixels diferem: hexdump das scanlines filtradas antes do zlib.
- Se signature falha: confira os 8 bytes `{137,80,78,71,13,10,26,10}`.

## Cobertura pedagógica auditada

- `COMP-PNG-01` — chunk length/type/crc
- `COMP-PNG-02` — IHDR 13 bytes
- `COMP-PNG-03` — filter None scanlines
- `COMP-PNG-04` — roundtrip encode/decode

Marcadores `PEDAGOGY-TEST: COMP-PNG-*` em `starter/test_png.cpp` / `solutions/test_png.cpp`.
