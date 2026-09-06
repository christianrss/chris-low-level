# Exercícios — Compressed blob triage

## Fácil

- **RT-COMP-01 (gzip):** Detecte `1F 8B` e retorne `"gzip"`; buffer `<2` → `"unknown"`.  
  **Aceite:** `detect_compression_magic(gzip.compress(b"x")) == "gzip"`.

- **RT-COMP-01 (zlib):** Aceite segundo byte em `{0x01,0x5E,0x9C,0xDA}`.  
  **Aceite:** `zlib.compress(...)` → `"zlib"` e prefixo `b"\x78\x9c"` no teste.

## Médio

- **RT-COMP-03:** Regex ASCII imprimível com `min_len` parâmetro.  
  **Aceite:** `"SECRET_KEY=abc123"` em `extract_ascii_strings` do Caso 4 do teste.

## Difícil

- **RT-COMP-02:** `validate_size_limits` com corte compressed, ramo unknown, `safe_inflate_preview` e `except`.  
  **Aceite:** `python starter/test_blob_triage.py` → `OK blob triage` (big rejeitado, small aceito).

## Desafio

- **RT-COMP-CH-01:** Monte um buffer `unknown` de 100 bytes e um gzip cujo plaintext tenha 10_000 `A`. Documente a matriz `(max_compressed, max_uncompressed) → bool` para os pares (50, 5000), (200, 20000), (5000, 5000).  
  **Aceite:** asserts batem com a matriz; explique por que (200, 20000) passa e (5000, 5000) falha no gzip de 10k.
