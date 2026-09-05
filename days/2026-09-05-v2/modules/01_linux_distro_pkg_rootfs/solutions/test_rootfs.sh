# TESTS [LINUX-ROOTFS-BUILD-03]
#!/bin/sh
set -eu
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
sh "$(dirname "$0")/build_rootfs.sh" "$TMP/root"
sh "$(dirname "$0")/build_rootfs.sh" "$TMP/root"
for d in bin etc proc sys dev tmp var/lib/chris-pkg; do test -d "$TMP/root/$d"; done
echo "OK rootfs"
