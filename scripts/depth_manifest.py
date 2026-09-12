"""Small YAML loader for repository contracts.

PyYAML is used when available. The fallback intentionally supports only
the mappings, lists and scalar values used by this repository's contract
files, keeping validation runnable in a stock Python CI environment.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def _strip_comment(line: str) -> str:
    quote: str | None = None
    for index, char in enumerate(line):
        if char in ("'", '"'):
            quote = None if quote == char else (char if quote is None else quote)
        if char == "#" and quote is None and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    return line.rstrip()


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if (value[0:1], value[-1:]) in {(('"', '"')), (("'", "'"))}:
        return value[1:-1]
    low = value.lower()
    if low in {"true", "false"}:
        return low == "true"
    if low in {"null", "none", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [_scalar(part) for part in inner.split(",")]
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        out: dict[str, Any] = {}
        if not inner:
            return out
        for part in inner.split(","):
            key, raw_item = part.split(":", 1)
            out[_key(key)] = _scalar(raw_item)
        return out
    return value


def _key(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _fallback_load(text: str) -> Any:
    rows: list[tuple[int, str]] = []
    for raw in text.splitlines():
        clean = _strip_comment(raw)
        if not clean.strip() or clean.lstrip().startswith("---"):
            continue
        rows.append((len(clean) - len(clean.lstrip(" ")), clean.strip()))

    def parse(index: int, indent: int) -> tuple[Any, int]:
        is_list = rows[index][1].startswith("- ")
        out: Any = [] if is_list else {}
        while index < len(rows):
            current_indent, content = rows[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ValueError(f"unexpected indentation near: {content}")
            if is_list:
                if not content.startswith("- "):
                    break
                item = content[2:].strip()
                if item.startswith("{") and item.endswith("}"):
                    out.append(_scalar(item))
                    index += 1
                    continue
                if ":" in item:
                    key, raw_value = item.split(":", 1)
                    parsed_key = _key(key)
                    entry: dict[str, Any] = {parsed_key: _scalar(raw_value)}
                    index += 1
                    if index < len(rows) and rows[index][0] > indent:
                        child, index = parse(index, rows[index][0])
                        if isinstance(child, dict):
                            entry.update(child)
                        elif entry[parsed_key] is None:
                            entry[parsed_key] = child
                        else:
                            raise ValueError(f"invalid list mapping near: {item}")
                    out.append(entry)
                    continue
                out.append(_scalar(item))
                index += 1
                continue

            if content.startswith("- ") or ":" not in content:
                break
            key, raw_value = content.split(":", 1)
            key = _key(key)
            value = _scalar(raw_value)
            index += 1
            if value is None and index < len(rows) and rows[index][0] > indent:
                value, index = parse(index, rows[index][0])
            out[key] = value
        return out, index

    if not rows:
        return {}
    parsed, consumed = parse(0, rows[0][0])
    if consumed != len(rows):
        raise ValueError(f"could not parse YAML near: {rows[consumed][1]}")
    return parsed


def load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) if yaml is not None else _fallback_load(text)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a top-level mapping")
    return data
