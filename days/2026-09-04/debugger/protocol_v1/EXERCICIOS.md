# Exercícios — Debug protocol v1

## Fácil

- **D2-DBG-APPEND-U16** e **D2-DBG-APPEND-U32:** serialize inteiros little-endian em `protocol.cpp`.
- **D2-DBG-READ-U16** e **D2-DBG-READ-U32:** reconstrua valores a partir de bytes.

## Médio

- **D2-DBG-FNV1A:** implemente hash FNV-1a 32-bit sobre payload.
- Calcule manualmente hash de payload `{0x01}` e compare com implementação.

## Difícil

- **D2-DBG-ENCODE:** monte header+payload respeitando limite de 1 MiB.
- **D2-DBG-DECODE:** valide magic, version, tamanho exato e checksum antes de retornar packet.

## Desafio

- Rode benchmark de 300k encode/decode com payload 64 B; registre packets/s.
- Escreva extensão v2 com MAC — quais campos mudariam sem quebrar v1?
