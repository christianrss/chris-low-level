# Exercícios — CHRLE em Rust

## Fácil

- **RS-RLE-01 (header):** Em `encode`, escreva `b"CHRLE"` e `len.to_le_bytes()`.  
  **Aceite:** `cargo test caso_1_encode_ten_zeros` passa o assert de magic/len.

- **RS-RLE-01 (run):** Agrupe zeros com `count=10`.  
  **Aceite:** bytes `[9]=10`, `[10]=0`.

## Médio

- **RS-RLE-02:** Rejeite buffer `< 9` e magic errada com `Truncated` / `BadMagic`.  
  **Aceite:** `caso_3` cobre magic flip e slice curto.

## Difícil

- **RS-RLE-02 + 03:** Decode completo + `round_trip_ok`.  
  **Aceite:** `cargo test` em `starter/` todo verde.

## Desafio

- **RS-RLE-CH-01:** Encode de 300 bytes iguais deve emitir dois runs (255+45). Documente o hex.  
  **Aceite:** teste manual `encode(&[7u8; 300])` → dois pares; round-trip true.
