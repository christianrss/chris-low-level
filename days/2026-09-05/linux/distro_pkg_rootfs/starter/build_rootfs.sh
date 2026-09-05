#!/bin/sh
set -eu
ROOT=${1:?usage: build_rootfs.sh ROOT}

# TODO [LINUX-ROOTFS-BUILD-03]: criar diretórios FHS mínimos de forma idempotente
# for d in bin etc proc sys dev tmp var/lib/chris-pkg; do
#     mkdir -p "$ROOT/$d"
# done
