# Exercícios — Gzip member parse

## Fácil

- **RS-GZ-01:** Rejeite `len < 10`, magic ≠ `1f8b`, CM ≠ 8.  
  **Aceite:** `caso_1_validate_fixed_header` PASS nos asserts de Truncated/BadMagic.

- **RS-GZ-01 (flags):** `flags & 0xE0 != 0` → `ReservedFlags`.  
  **Aceite:** flip dos bits reservados falha.

## Médio

- **RS-GZ-02:** Com `FLG_FNAME`, pule até NUL e retorne o offset seguinte.  
  **Aceite:** `caso_2` compara com `deflate_at` calculado no teste.

## Difícil

- **RS-GZ-03:** `parse_member` preenche `deflate_start`, `trailer_start`, CRC, ISIZE.  
  **Aceite:** `cargo test` completo no starter.

## Desafio

- **RS-GZ-CH-01:** Implemente skip de `FEXTRA` (XLEN) + teste manual com XLEN=4.  
  **Aceite:** documente hex; `deflate_payload_start` avança 2+4 além do fixo.
