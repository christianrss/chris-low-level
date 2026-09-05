# Gabarito — Linux — Ciclo de Vida de Driver

Respostas esperadas (consulte `solutions/` para código completo).

1. device_open retorna 0 na primeira vez, -1 se já aberto.
2. device_release zera is_open; I/O retorna -1 se fechado.
3. Trace imprime [kmod-trace] em open/write/read/release.
4. Rubrica de review cobre register_chrdev e unregister no exit.
