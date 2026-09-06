# Testes guiados — zlib/gzip containers

## Por que testar estes containers?

Header errado ou checksum com endian invertido produz blobs que *parecem* comprimidos mas são rejeitados por decoders reais. Os testes transformam o RFC em asserts executáveis.

## Como rodar

```powershell
cmake --build days/2026-09-06/tooling/zlib_gzip_containers/starter/build --config Release
ctest --test-dir days/2026-09-06/tooling/zlib_gzip_containers/starter/build -C Release --output-on-failure
```

Arquivo: `starter/test_zlib.cpp`.

---

## Teste 1 — Adler conhecido (`COMP-ZLIB-01`)

**Invariante:** `adler32("Wikipedia") == 0x11E60398`.

1. Monte `vector` a partir da string.
2. Chame `adler32`.
3. `REQUIRE` igualdade com `0x11e60398u`.

Se falhar: confira `s1=1` e módulo 65521 (TEORIA §3).

## Teste 2 — zlib CMF/FLG (`COMP-ZLIB-02`)

**Invariante:** pacote com `cmf==0x78` e FCHECK válido.

1. `zlib_compress({'z','l','i','b'})`.
2. `REQUIRE(pkt.cmf == 0x78)`.
3. `REQUIRE(((pkt.cmf << 8) + pkt.flg) % 31 == 0)`.

## Teste 3 — zlib round-trip + Adler (`COMP-ZLIB-03`)

**Invariante:** decompress(blob(compress(p))) == p.

1. Serialize com `zlib_blob_from_packet`.
2. `zlib_decompress`.
3. Compare bytes com o payload original.

Corrupir o trailer Adler (flip bit) deve lançar — exercício mental / extensão.

## Teste 4 — gzip CRC round-trip (`COMP-ZLIB-04`)

**Invariante:** magic `1F 8B` e round-trip.

1. `gzip_compress(payload)`.
2. `REQUIRE(gz[0]==0x1F && gz[1]==0x8B)`.
3. `gzip_decompress(gz) == payload`.

## Como depurar

- Hexdump dos 2 primeiros e 4/8 últimos bytes do blob.
- Compare Adler BE vs CRC LE conscientemente.
- Rode o mesmo payload no gabarito `solutions/` se o starter discordar do RFC.

## Cobertura pedagógica auditada

- `COMP-ZLIB-01` — Adler conhecido
- `COMP-ZLIB-02` — CMF/FLG
- `COMP-ZLIB-03` — decompress + Adler
- `COMP-ZLIB-04` — gzip CRC32 roundtrip

Marcadores `PEDAGOGY-TEST: COMP-ZLIB-*` em `starter/test_zlib.cpp` / `solutions/test_zlib.cpp`.
