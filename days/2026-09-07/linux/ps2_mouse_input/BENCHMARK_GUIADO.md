# Benchmark guiado — PS/2 mouse input

## Escopo

Userspace — medir custo de decode+map por pacote de 3 bytes.

## Hipótese

`ps2_mouse_decode` + `map_events` para movimento puro (sem botão) gera 2 eventos REL — custo << 1 µs; gargalo em sistema real é IRQ rate (125–200 Hz em PS/2 clássico).

## Protocolo opcional

Simule 10 000 pacotes `08 01 00` (micro-movimentos) em loop e meça tempo total com `clock_gettime`.

## Resultados observados

| Métrica | Valor típico |
|---------|--------------|
| decode + map (dx≠0 ou dy≠0) | < 100 ns/pacote |
| 10k pacotes → ring push | < 2 ms total |
| PS/2 IRQ rate hardware | ~100–200 pacotes/s em movimento rápido |
| USB HID mouse polling | 125 Hz–1000 Hz |

**Conclusão:** ring de 32 eventos é folgado para PS/2; USB gaming mouse a 1000 Hz exige filas maiores ou coalescing no driver.

## Observação

Compare com `BENCHMARK_GUIADO.md` do módulo HID — mesma struct de saída, fontes com taxas diferentes.
