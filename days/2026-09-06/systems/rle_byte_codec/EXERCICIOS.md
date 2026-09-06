# Exercícios — RLE byte codec

## Fácil

- **COMP-RLE-01 (parcial — header):** Em `starter/rle.cpp`, faça `encode_rle` escrever magic `CHRLE` (5 bytes) + `orig_len` LE32 e retornar `true` com payload vazio de runs (só para input vazio).  
  **Aceite:** input `{}` → buffer exatamente 9 bytes `43 48 52 4C 45 00 00 00 00`.

- **COMP-RLE-01 (runs):** Complete a varredura `(count, byte)` com teto 255.  
  **Aceite:** 10 zeros → hex `… 0A 00`; `ctest` Caso 1 ainda falha só no decode.

## Médio

- **COMP-RLE-02:** Implemente validação de magic + expansão de pares em `decode_rle`.  
  **Aceite:** round-trip de `"ABCD"`; `enc[0]='X'` → `decode_rle` retorna `false` (Caso 3).

## Difícil

- **COMP-RLE-03:** Garanta `return out.size() == len` e que o loop nunca leia além do buffer (`p + 1 < size`).  
  **Aceite:** buffer com `len=6` e um único par `(3,'A')` → `false`; suite oficial imprime `OK rle`.

## Desafio

- **COMP-RLE-CH-01:** Escreva um gerador que, para N∈{1,255,256,512}, produza N bytes iguais e verifique que o encode emite `ceil(N/255)` pares e o decode reconstrói N.  
  **Aceite:** asserts passam para os quatro N; documente o hex do caso N=256 (dois pares `FF xx` + `01 xx`).
