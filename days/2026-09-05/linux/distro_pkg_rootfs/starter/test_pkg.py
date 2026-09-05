// Test cases (TESTES_GUIADOS.md):
// Caso 1: `python starter/test_pkg.py` — deve falhar com TODOs abertos; imprime `OK linux 
// Caso 2: `sh starter/test_rootfs.sh` — valida idempotência do builder (duas execuções).
// Caso 3: **Regressão path traversal:** manifest com `../escape` → `ValueError`.
// Caso 4: **Regressão arquivo ausente:** manifest lista `bin/missing` → `FileNotFoundError
// Caso 5: **Rollback transacional:** se a segunda cópia falha, a primeira também é reverti
// Caso 6: Valide `solutions/` com os mesmos comandos após implementar.
# PEDAGOGY-TEST: LINUX-PKG-PARSE-01: manifest válido e rejeição de path traversal
# PEDAGOGY-TEST: LINUX-PKG-INSTALL-02: instalação, banco e rollback transacional
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent))
from chris_pkg import install_package, load_manifest


def test_happy_path() -> None:
    with TemporaryDirectory() as td:
        base = Path(td)
        pkg = base / "pkg"
        (pkg / "payload/usr/share").mkdir(parents=True)
        (pkg / "payload/usr/share/hello.txt").write_text("hello", encoding="utf-8")
        (pkg / "manifest.json").write_text(
            json.dumps(
                {
                    "name": "hello",
                    "version": "1.0.0",
                    "files": ["usr/share/hello.txt"],
                }
            ),
            encoding="utf-8",
        )

        manifest = load_manifest(pkg / "manifest.json")
        assert manifest["name"] == "hello"

        root = base / "root"
        install_package(pkg, root)
        assert (root / "usr/share/hello.txt").read_text(encoding="utf-8") == "hello"

        db = json.loads(
            (root / "var/lib/chris-pkg/installed.json").read_text(encoding="utf-8")
        )
        assert db["hello"] == "1.0.0"


def test_rejects_path_traversal() -> None:
    with TemporaryDirectory() as td:
        pkg = Path(td) / "pkg"
        pkg.mkdir()
        (pkg / "manifest.json").write_text(
            json.dumps({"name": "bad", "version": "1", "files": ["../escape"]}),
            encoding="utf-8",
        )
        try:
            load_manifest(pkg / "manifest.json")
            raise AssertionError("unsafe path accepted")
        except ValueError:
            pass


def test_missing_payload_file_rolls_back() -> None:
    with TemporaryDirectory() as td:
        base = Path(td)
        pkg = base / "pkg"
        (pkg / "payload/bin").mkdir(parents=True)
        (pkg / "payload/bin/ok").write_text("ok", encoding="utf-8")
        (pkg / "manifest.json").write_text(
            json.dumps(
                {
                    "name": "broken",
                    "version": "1.0",
                    "files": ["bin/ok", "bin/missing"],
                }
            ),
            encoding="utf-8",
        )

        root = base / "root"
        try:
            install_package(pkg, root)
            raise AssertionError("missing file should abort install")
        except FileNotFoundError:
            pass

        assert not (root / "bin/ok").exists()
        db_path = root / "var/lib/chris-pkg/installed.json"
        assert not db_path.exists()


if __name__ == "__main__":
    test_happy_path()
    test_rejects_path_traversal()
    test_missing_payload_file_rolls_back()
    print("OK linux package")