# Testes guiados

1. `python3 starter/test_pkg.py` deve falhar enquanto os TODOs estiverem abertos.
2. Depois de implementar parser + install, deve imprimir `OK linux package`.
3. `sh starter/test_rootfs.sh` deve imprimir `OK rootfs`.
4. Testes de regressão importantes: pacote válido, path traversal, arquivo ausente no payload, duas execuções do rootfs.
5. Para validar a referência final: execute os mesmos comandos dentro de `solutions/`.