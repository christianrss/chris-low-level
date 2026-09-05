#!/bin/sh
set -eu
ROOT=${1:?usage: build_rootfs.sh ROOT}
for d in bin etc proc sys dev tmp var/lib/chris-pkg; do mkdir -p "$ROOT/$d"; done
