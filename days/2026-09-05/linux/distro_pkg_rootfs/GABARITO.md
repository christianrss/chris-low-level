# Gabarito — Distribuição Linux — Pacotes e Rootfs

Respostas esperadas (consulte `solutions/` para código completo).

1. load_manifest retorna dict validado; ValueError em paths inseguros.
2. install_package copia payload, atualiza installed.json só no final.
3. Rollback remove arquivos copiados se FileNotFoundError ocorrer.
4. build_rootfs.sh cria bin, etc, proc, sys, dev, tmp, var/lib/chris-pkg.
