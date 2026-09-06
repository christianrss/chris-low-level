# Benchmark guiado — PNG IDAT pipeline

**Pergunta:** quanto custa encode+decode de um PNG grayscale mínimo (stored zlib) em função de width×height?

Protocolo:

1. Compile **Release**.
2. Imagens determinísticas **8×8** e **64×64** (pixels ` (x+y) & 0xFF `).
3. 5 aquecimentos; ≥30 medições de `encode_png` → `decode_png`.
4. Registre mediana (µs) e tamanho do blob (bytes).
5. Anote: stored + filter None ⇒ ratio ~1; o custo é framing+CRC+Adler+cópias.

**Experimento seguinte:** comparar um vs N IDATs fatiando o zlib em dois chunks (mesmo plaintext) — overhead de CRC duplicado.

## Resultados observados

Ambiente de referência: preencha após o lab.

| Métrica | Valor referência | Notas |
|---------|------------------|-------|
| encode+decode 8×8 median | ___ µs | fixture pequeno |
| encode+decode 64×64 median | ___ µs | |
| blob size 8×8 | ___ B | signature+chunks |
| blob size 64×64 | ___ B | |

Valores são ordem de grandeza — **rerode** e registre mediana após warm-up.
