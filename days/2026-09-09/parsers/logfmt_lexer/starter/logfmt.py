"""logfmt key=value lexer."""

from __future__ import annotations

import shlex


def tokenize(line: str) -> list[str]:
    """TODO [PR-LOGFMT-LEX-01]: split tokens respecting quotes."""
    raise NotImplementedError("PR-LOGFMT-LEX-01")


def parse_kv(tok: str) -> tuple[str, str]:
    """TODO [PR-LOGFMT-KV-02]: parse key=value."""
    raise NotImplementedError("PR-LOGFMT-KV-02")


def parse_line(line: str) -> dict[str, str]:
    """TODO [PR-LOGFMT-ESC-03]: full line to dict."""
    raise NotImplementedError("PR-LOGFMT-ESC-03")
