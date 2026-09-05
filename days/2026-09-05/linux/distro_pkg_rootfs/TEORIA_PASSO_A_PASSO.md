# Teoria passo a passo — Linux distro: pacote próprio + rootfs reproduzível

Uma distribuição Linux não é apenas “um kernel”. Ela precisa de **userspace**, layout de diretórios, metadados de pacotes e uma forma reproduzível de montar a árvore que será usada no boot. Hoje usamos um formato educacional simples: um arquivo `manifest.json` mais um diretório `payload/`.

O instalador trabalha contra um `--root`, nunca contra `/`. Isso permite testar sem privilégios. O manifest contém `name`, `version` e uma lista de arquivos. Para cada arquivo, o gerenciador resolve o caminho relativo dentro do rootfs, cria diretórios pais e copia bytes do payload. O banco local fica em `var/lib/chris-pkg/installed.json` dentro do rootfs.

O script `build_rootfs.sh` cria a hierarquia mínima `bin etc proc sys dev tmp var/lib/chris-pkg`. Em um boot real, `proc`, `sys` e `dev` seriam montados durante early userspace/PID 1; hoje eles são apenas pontos de montagem.

Referência temporal: em 5 de setembro de 2026, kernel.org lista Linux 7.2.3 como stable. O laboratório não depende dessa versão, mas ela é a referência atual para a futura trilha de build do kernel.
