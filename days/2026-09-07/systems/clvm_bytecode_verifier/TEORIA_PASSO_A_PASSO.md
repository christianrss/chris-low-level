# Teoria â€” verifier CLVM (N2)

## 1. Por que este lab

Checksum prova integridade. Verifier prova **forma** do programa.

### Por que depois do codegen?

Imagens do N1 devem passar aqui â€” fecha o ciclo compileâ†’validate.

## 2. Dois tipos de confianÃ§a

| Camada | Pergunta |
|--------|----------|
| FNV | Bytes mudaram? |
| Verifier | Bytes sÃ£o bem formados? |

## 3. Efeito de pilha

`(pops, pushes)` por opcode. Walk conservador.

### Por que conservador?

CFG completo Ã© difÃ­cil; underflow no caminho seguido jÃ¡ pega bugs graves do codegen.

## 4. Boundaries e branches

Alvo âˆˆ `[0, len(code)]`.

### Por que range e nÃ£o sÃ³ boundaries?

Lab focado; boundary strict fica para depois.

## 5. LigaÃ§Ã£o Dia 01

`clvm_parse` = header. Verifier = code shape.

## 6. LigaÃ§Ã£o js2clvm

Falha no verifier â‡’ bug no lowering ou assemble.

## 7. STACK_EFFECT

Sincronizar com FORMAT.md.

## 8. Checklist

Header, opcodes, branches, depth.

## 9. Como testar

ok.clvm VALID; bad_checksum mismatch.

## 10. Diagrama

```text
.clvm â†’ header checks â†’ linear decode â†’ stack walk â†’ VALID/INVALID
```

## 11â€“30. ExpansÃ£o pedagÃ³gica

Portar para chris-vm. NÃ£o executar PRINT. Complementa rust-validator. Mensagens estÃ¡veis. FNV = assemble. Little-endian branches. Entry OOB Ã© header. Truncated PUSH. Unknown opcode. JMP segue alvo no walk. JZ fall-through. CALL segue alvo. RET encerra path. Depth>1024 erro. steps cap. fixtures no repo. Starter FAIL atÃ© TODOs. Solutions PASS. Documente limites. CI apÃ³s assemble. Compare com Dia 01 TEORIA checksum. PrÃ³ximo: N3 `%`. NÃ£o quebre v1. Evite parse duplo. Use pathlib. Testes em integration_test.py. Pedagogy markers. RelatÃ³rio no fim do lab.
- Nota pedagógica 63: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 64: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 65: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 66: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 67: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 68: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 69: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 70: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 71: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 72: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 73: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 74: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 75: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 76: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 77: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 78: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 79: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 80: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 81: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 82: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 83: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 84: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 85: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 86: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 87: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 88: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 89: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 90: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 91: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 92: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 93: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 94: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 95: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 96: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 97: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 98: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 99: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 100: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 101: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 102: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 103: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 104: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 105: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 106: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 107: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 108: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 109: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 110: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 111: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 112: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 113: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 114: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 115: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 116: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 117: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 118: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 119: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
- Nota pedagógica 120: relacione checksum Dia 01 com walk de pilha; documente limites do verifier.
