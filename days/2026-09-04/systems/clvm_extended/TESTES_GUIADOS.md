# Testes guiados — CLVM extended

## Caso 1 — assembler (CLVM-EXT-01)

1. `python tools/assemble.py programs/add2.asm add2.clvm`
2. Esperado: linha `wrote ... checksum=0x...` sem erro.

## Caso 2 — CALL/RET (CLVM-EXT-02)

1. Rodar `clvm add2.clvm` → stdout `8`, exit 0.
2. `clvm bad_ret.clvm` → stderr contém `return stack underflow`, exit ≠ 0.

## Caso 3 — memória (CLVM-EXT-03)

1. Montar e rodar `mem_demo.asm` → `42`.
2. `bad_mem.asm` → `memory out of bounds`.

## Caso 4 — loop/cmp (CLVM-EXT-04)

1. Montar e rodar `max_loop.asm`.
2. Stdout:
```text
0
1
2
3
1
```

## Regressão

`arithmetic.asm` → `38`.

## Integração

`ctest --test-dir build_ci -C Release` (solutions) deve PASS; starter deve FAIL até os TODOs.

## Debug

`clvm add2.clvm --trace` (solutions) mostra `call_depth`.
