# Exercícios — Tooling — zlib/gzip containers

## Fácil

- **COMP-ZLIB-01** (`starter/adler32.cpp`): implemente Adler-32 (mod 65521, `s1=1`).
  - **Aceite:** `adler32("Wikipedia") == 0x11E60398`.

## Médio

- **COMP-ZLIB-02** (`starter/zlib_wrap.cpp`): `zlib_compress` + `zlib_blob_from_packet` com CMF/FLG, stored e Adler BE.
  - **Aceite:** `cmf==0x78` e `((cmf<<8)+flg)%31==0`.
- **COMP-ZLIB-03** (`starter/zlib_wrap.cpp`): `zlib_decompress` validando header e Adler.
  - **Aceite:** round-trip do payload `{'z','l','i','b'}`.

## Difícil

- **COMP-ZLIB-04** (`starter/crc32.cpp`, `starter/gzip_wrap.cpp`): CRC IEEE + gzip header/trailer LE.
  - **Aceite:** magic `1F 8B` e `gzip_decompress(gzip_compress(p))==p`.

## Desafio

- **COMP-ZLIB-TOOL-01** (extensão): parsear gzip com `FNAME` (flag bit 3) até o NUL, sem quebrar o subset atual nos testes.
  - **Aceite:** round-trip de um `.gz` gerado por `gzip` do sistema com nome de arquivo.
