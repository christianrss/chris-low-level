# Testes — verifier

## CLVM-VFY-BRANCH-01

Branch OOB deve gerar erro (após implementar). Fixture ok não tem branch inválido.

## CLVM-VFY-STACK-01

### Caso 1: `fixtures/ok.clvm` → VALID
### Caso 2: `fixtures/bad_checksum.clvm` → checksum mismatch

Esperado: `clvm_bytecode_verifier tests passed`.
