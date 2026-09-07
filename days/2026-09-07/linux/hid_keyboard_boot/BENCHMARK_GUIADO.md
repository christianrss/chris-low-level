# Benchmark guiado — HID boot keyboard

## Escopo

Pipeline userspace — benchmark opcional de throughput do ring buffer, não de latência USB real.

## Hipótese

Push+read de 32 `InputEvent` de 24 bytes deve completar em microssegundos; o custo domina em `memcpy` de 24 bytes por evento, não na lógica de índice circular.

## Protocolo opcional

```bash
cd starter/build
# Após implementar TODOs — loop 1M ciclos push/read no teste estendido
```

## Resultados observados

| Métrica | Valor típico (userspace, MSVC/GCC -O2) |
|---------|----------------------------------------|
| 32× push + 32× read (768 bytes) | < 5 µs |
| map_events press+release (1 tecla) | < 200 ns |
| Overhead evdev real (estimativa) | syscall + copy_to_user ~300 ns/evento |

**Conclusão:** neste lab, valide **corretude de diff e FIFO**, não latência USB. Hardware exige VM Linux + `evtest` — fora do escopo mínimo.

## Correlacionar com kernel

Se um relatório HID chega a 1 kHz, ring de 32 eventos cobre ~32 ms de atraso máximo antes de overflow — dimensionamento típico em drivers embarcados.
