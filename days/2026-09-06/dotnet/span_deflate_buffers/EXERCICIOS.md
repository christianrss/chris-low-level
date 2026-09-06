# Exercícios — Span deflate buffers

## Fácil

- **DN-SPAN-01 (tamanho):** Em `ReadStoredHeader`, rejeite `input.Length < 5` com `InvalidDataException`.  
  **Aceite:** span de 3 bytes no `Main` cai no `catch (InvalidDataException)`.

- **DN-SPAN-01 (BTYPE):** Extraia BTYPE com `(header >> 1) & 0x03` e exija `0`.  
  **Aceite:** header `0x01` do `BuildStoredBlock` passa; um header `0x03` (scratch) falha.

## Médio

- **DN-SPAN-03:** Valide `(ushort)(len ^ nlen) == 0xFFFF` após ler LE16.  
  **Aceite:** bloco canônico de `"LOWLEVEL"` passa; flip em `block[3]` → mismatch.

## Difícil

- **DN-SPAN-02:** `InflateStored` com Slice/CopyTo e check `dataOffset + length`.  
  **Aceite:** `dotnet run` em `starter/` imprime `OK deflate stored`.

## Desafio

- **DN-SPAN-CH-01:** Estenda o parser para rejeitar BFINAL=0 (multi-bloco) com mensagem clara, e documente o hex de um segundo stored block concatenado. Não precisa inflar o segundo bloco.  
  **Aceite:** teste manual: primeiro byte `0x00` (BFINAL=0, stored) → exceção documentada; `0x01` continua ok.
