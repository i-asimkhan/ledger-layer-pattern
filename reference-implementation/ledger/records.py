"""Ledger records: Markdown files with YAML front matter, plus the change hash."""
import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

_FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def now() -> str:
    """UTC timestamp. LEDGER_FIXED_TIME pins it, so demo output is reproducible."""
    return os.environ.get("LEDGER_FIXED_TIME") or datetime.now(timezone.utc).isoformat(timespec="seconds")


def change_hash(root: Path, covers: list) -> str:
    """Hash of the covered files as they stand now (line endings normalised), so drift is detectable."""
    lines = []
    for rel in sorted(covers):
        f = Path(root) / rel
        if f.is_file():
            digest = hashlib.sha256(f.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        else:
            digest = "missing"
        lines.append(f"{rel}\0{digest}")
    return sha256_text("\n".join(lines))


class Record:
    def __init__(self, path: Path, meta: dict, body: str):
        self.path, self.meta, self.body = Path(path), meta, body

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @classmethod
    def load(cls, path) -> "Record":
        m = _FRONT.match(Path(path).read_text(encoding="utf-8").replace("\r\n", "\n"))
        if not m:
            raise ValueError(f"{path}: record has no YAML front matter")
        return cls(path, yaml.safe_load(m.group(1)) or {}, m.group(2))

    def save(self) -> None:
        head = yaml.safe_dump(self.meta, sort_keys=False, allow_unicode=True).rstrip()
        self.path.write_text(f"---\n{head}\n---\n{self.body}", encoding="utf-8", newline="\n")


def load_all(records_dir: Path) -> list:
    if not Path(records_dir).is_dir():
        return []
    return [Record.load(p) for p in sorted(Path(records_dir).glob("*.md"))]


def find(records_dir: Path, rid: str) -> Record:
    for rec in load_all(records_dir):
        if rec.id == rid or rec.path.name.startswith(rid):
            return rec
    raise SystemExit(f"no record '{rid}' in {records_dir}")
