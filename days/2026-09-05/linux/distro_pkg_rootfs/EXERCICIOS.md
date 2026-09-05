# Exercícios — Distribuição Linux — Pacotes e Rootfs

Quatro níveis de dificuldade alinhados aos TODOs do módulo.

## Fácil
- **LINUX-PKG-PARSE-01:** Implemente `load_manifest()` validando JSON, `name`, `version` e lista `files`.

## Médio
- **LINUX-PKG-PARSE-01:** Rejeite caminhos absolutos e componentes `..` no manifest.

## Difícil
- **LINUX-PKG-INSTALL-02:** Implemente `install_package()` com rollback transacional se um arquivo do payload faltar.

## Expert
- **LINUX-ROOTFS-BUILD-03:** Complete `build_rootfs.sh` idempotente e documente como adicionar hashes por arquivo.
