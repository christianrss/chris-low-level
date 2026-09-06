# Exercícios — Tooling — PNG IDAT pipeline

## Fácil

- **COMP-PNG-01** (`starter/png.cpp`): `png_chunk_crc` (CRC32 de type+data) e `png_chunk` (length/type/data/CRC BE).
  - **Aceite:** chunk IHDR com data 13 B tem tamanho 25; IEND vazio tem CRC `0xAE426082`.

## Médio

- **COMP-PNG-02** (`starter/png.cpp`): `build_ihdr` — 13 bytes, width/height BE.
  - **Aceite:** `ihdr.size()==13`, `ihdr[8]==8`, `ihdr[9]==0` para o fixture 3×2.
- **COMP-PNG-03** (`starter/png.cpp`): `filter_none_scanlines`.
  - **Aceite:** size `(width+1)*height`, primeiro byte 0, segundo = primeiro pixel.

## Difícil

- **COMP-PNG-04** (`starter/png.cpp`): `encode_png` / `decode_png` (signature + IHDR + IDAT zlib + IEND).
  - **Aceite:** `blob[0]==137 && blob[1]==80`; `decode_png(encode_png(img)).pixels == img.pixels`.

## Desafio

- **COMP-PNG-TOOL-01** (extensão): gravar o blob em disco e validar com um decoder externo (`pngcheck`, browser, ou Pillow).
  - **Aceite:** imagem 8×8 grayscale abre sem erro; dump de IHDR bate com width/height.
