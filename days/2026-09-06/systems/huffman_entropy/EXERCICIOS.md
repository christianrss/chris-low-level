# Exercícios — Huffman entropy codec

## Fácil

- **COMP-HUF-01:** Em `starter/bit_io.cpp`, implemente `write_bit`, `flush` e `read_bit` MSB-first.  
  **Aceite:** `write_bits(0b1011, 4)` + `flush` → um byte `0xB0`; reader devolve 1,0,1,1 (`PEDAGOGY-TEST: COMP-HUF-01`).

## Médio

- **COMP-HUF-02:** Implemente `build_huffman_codes` com heap, caso de símbolo único e códigos alinhados à esquerda em 16 bits.  
  **Aceite:** para freqs de `AAAABB C`, `table` não vazia e todo `bit_length ≥ 1`.

- **COMP-HUF-03 (header):** Faça `encode_huffman` emitir `CHHUF` + LE32 + `n` + entradas (payload pode ser vazio temporariamente).  
  **Aceite:** primeiros 5 bytes == `CHHUF`; `n` bate com `table.size()`.

## Difícil

- **COMP-HUF-03 + COMP-HUF-04:** Complete bitstream no encode e trie+`BitReader` no decode.  
  **Aceite:** round-trip de `{'A','A','A','B','B','C'}`; `enc[0]='X'` → `decode_huffman` false; `ctest` imprime `OK huffman`.

## Desafio

- **COMP-HUF-CH-01:** Meça bits médios por símbolo (`total_bits / n`) no bloco de teste e mostre que é ≤ log2(|alfabeto|) e ≥ entropia empírica H = −Σ p log2 p (com tolerância de arredondamento de código inteiro).  
  **Aceite:** tabela impressa + desigualdades documentadas no relatório pessoal; input de um único símbolo tem média = 1.0 bit/símbolo neste lab.
