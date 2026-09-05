"""Gerenciador mínimo de pacotes para rootfs educacional."""

import json
import shutil
from pathlib import Path


def load_manifest(path: Path) -> dict:
    """Valida e retorna o manifest de um pacote.

    TODO [LINUX-PKG-PARSE-01]: validar JSON, campos obrigatórios e caminhos seguros.
    """
    raise NotImplementedError("LINUX-PKG-PARSE-01")


def install_package(package_dir: Path, root: Path) -> dict:
    """Instala payload no rootfs com rollback transacional em caso de falha.

    TODO [LINUX-PKG-INSTALL-02]: montar plano, copiar arquivos, atualizar banco
    apenas após sucesso; reverter cópias parciais se algo falhar.
    """
    raise NotImplementedError("LINUX-PKG-INSTALL-02")
