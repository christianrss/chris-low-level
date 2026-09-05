# Benchmark guiado — Kernel driver lifecycle

## Escopo

Este módulo modela lifecycle em userspace — **não há benchmark de desempenho obrigatório**. O foco é correção de estado e invariantes.

## Hipótese (referência)

Se portarmos o modelo para kernel real, o custo de `copy_from_user` domina writes pequenos; o lifecycle (`open`/`release`) é O(1) e irrelevante frente a cópia de dados.

## Protocolo opcional

Meça 1 milhão de ciclos open/write/read/release no binário userspace:

```bash
# wrapper de microbench opcional — não faz parte dos testes
```

## Resultados observados

| Métrica | Valor típico |
|---------|--------------|
| Ciclo open/write(3)/read(3)/release userspace | < 1 µs por ciclo |
| Overhead de syscall real (estimativa) | ~100–500 ns + cópia |

**Conclusão:** neste lab, valide **corretude de estado**, não latência. Benchmark de driver real exige hardware/VM dedicada — fora do escopo Day 03.
