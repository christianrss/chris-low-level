# CLVM bytecode verifier — Dia 2026-09-07 (N2)

Checksum (Dia 01) prova integridade dos bytes. Este lab prova **forma**: opcodes conhecidos, saltos no range, pilha sem underflow conservador.

## TODOs

- `CLVM-VFY-BRANCH-01` — alvo de JMP/JZ/CALL/JNZ ∈ `[0, code_size]`
- `CLVM-VFY-STACK-01` — walk com `STACK_EFFECT`; detectar underflow

## Teste

```powershell
cd solutions
python tests/integration_test.py
```

## Portar

Atualize `projects/chris-vm/tools/verify_clvm.py` se melhorar a lógica.
