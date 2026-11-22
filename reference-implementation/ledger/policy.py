"""The policy file (ledger.yml): which paths are how hard to undo, and what each level requires."""
import re
import subprocess
from pathlib import Path

import yaml

LEVELS = ["easy", "hard", "cannot_undo"]  # ordered: the later, the deeper the audit


def glob_to_regex(pattern: str) -> re.Pattern:
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


class Policy:
    def __init__(self, data: dict):
        self.records_dir = data.get("records_dir", "records")
        self.ignore = [glob_to_regex(p) for p in data.get("ignore", [])]
        self.default = data.get("default_reversibility", "easy")
        self.rules = [(glob_to_regex(r["path"]), r["level"]) for r in data.get("reversibility", [])]
        self.required = data.get("required_checks", {})
        self.zero_edit = data.get("zero_edit", "warn")  # warn | fail
        for level in [self.default] + [lvl for _, lvl in self.rules]:
            if level not in LEVELS:
                raise ValueError(f"unknown reversibility level '{level}' (use one of {LEVELS})")

    @classmethod
    def load(cls, root) -> "Policy":
        path = Path(root) / "ledger.yml"
        if not path.is_file():
            raise SystemExit(f"no policy file at {path}")
        return cls(yaml.safe_load(path.read_text(encoding="utf-8")) or {})

    @classmethod
    def load_from_base(cls, root, base: str):
        """Return (policy, source). The gate reads ledger.yml as it is on the BASE branch, so a pull request
        cannot loosen its own rules. Only if the base has no policy yet (first adoption) does it fall back
        to the policy in this branch, and it says so."""
        out = subprocess.run(["git", "-C", str(root), "show", f"{base}:./ledger.yml"], capture_output=True,
                             text=True, encoding="utf-8")
        if out.returncode == 0:
            return cls(yaml.safe_load(out.stdout) or {}), f"read from {base}, not from this branch"
        return cls.load(root), (f"WARNING: no ledger.yml on {base}; using the one in this branch "
                                "(acceptable for first adoption only)")

    def ignored(self, path: str) -> bool:
        return any(rx.match(path) for rx in self.ignore)

    def level_for(self, path: str) -> str:
        for rx, level in self.rules:
            if rx.match(path):
                return level
        return self.default

    def level_for_paths(self, paths) -> str:
        levels = [self.level_for(p) for p in paths] or [self.default]
        return max(levels, key=LEVELS.index)

    def required_checks(self, level: str) -> list:
        return list(self.required.get(level, ["consistency"]))
