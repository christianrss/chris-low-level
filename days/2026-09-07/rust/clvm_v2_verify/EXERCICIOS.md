# Exercícios — CLVM v2 Rust

## Fácil

- **CLVM-RS-V2-POOL-02:** Implemente `encode_pool` para `["hi"]`.  
  **Aceite:** `cargo test caso_3` passa.

## Médio

- **CLVM-RS-V2-HEADER-01:** Parse `hello_v2.clvm`; rejeite magic/checksum.  
  **Aceite:** casos 1, 2, 6 verdes.

## Difícil

- **CLVM-RS-V2-PRINTS-03 + STACK-04:** `run_prints` + `verify_stack` OOB.  
  **Aceite:** `cargo test` completo no starter.

## Desafio

- **CLVM-RS-V2-CH-01:** Imagem com duas strings e dois `PRINTS`; stdout duas linhas.  
  **Aceite:** teste manual + `verify_stack` vazio.
