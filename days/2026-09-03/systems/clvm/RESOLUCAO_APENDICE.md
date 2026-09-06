# CLVM Dia 01 — apêndice opcional da resolução

> Material extra. O caminho obrigatório (com **Onde colocar** arquivo/função/substituir) está em `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`. Use este arquivo só para paper-trace e armadilhas de PC.

## Paper-trace de `countdown.asm`

Programa típico (resumo):

```text
PUSH 3
loop:
  DUP
  PRINT
  PUSH 1
  SUB
  DUP
  JZ end
  JMP loop
end:
  PRINT
  HALT
```

Arquivo real: `starter/programs/countdown.asm` — imprime `3\n2\n1\n0`.

### Tabela (n inicia em 3)

| passo | stack (topo→) | stdout | nota |
|-------|---------------|--------|------|
| PUSH 3 | 3 | | |
| DUP; PRINT | 3 | 3 | |
| PUSH 1; SUB | 2 | | |
| DUP; JZ end | 2 | | pop 2 ≠ 0 → não salta |
| JMP loop | 2 | | |
| … imprime 2, 1 | | 3 2 1 | |
| após SUB a partir de 1 | 0 | | |
| DUP; JZ end | 0 | | pop 0 → salta; sobra `0` |
| PRINT; HALT | | … 0 | imprime o zero restante |

### Armadilha clássica do PC relativo

Se você somar o deslocamento **antes** de consumir o i16, o destino fica 2 bytes errado — o assembler usou `next_pc = pc_do_JMP + 3`.

Se JZ não der pop quando a condição é falsa, a stack acumula lixo e o próximo DUP/PRINT quebra.

### Debug

```powershell
clvm countdown.clvm --trace
```

Compare `pc=` e a stack impressa com a tabela acima.

---

## Evolução (não é Dia 01)

LOAD/STORE, CALL/RET, EQ/LT/JNZ e ops de stack **não** fazem parte deste lab.

Continuidade: [`days/2026-09-04/systems/clvm_extended`](../../../2026-09-04/systems/clvm_extended/) e o capstone `projects/chris-vm`.

Opcodes `0x0B`+ no Dia 01 **não** existem; não implemente prévias de memória aqui.
