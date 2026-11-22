"""Step 1, the Ledger: draft a record for a change. Offline template by default; providers are pluggable."""
import importlib
import re
from pathlib import Path

from .policy import Policy
from .records import Record, change_hash, load_all, sha256_text


def template_provider(files: dict) -> dict:
    """Offline drafter. `files` maps path -> number of lines (or None if the file is gone).
    A provider is any function with this signature that returns the four section texts."""
    listing = "\n".join(f"- `{p}` ({'removed' if n is None else f'{n} lines'})" for p, n in files.items())
    return {
        "context": f"This change touches {len(files)} file(s):\n\n{listing}\n\nTODO: say why the change is needed.",
        "decision": "TODO: state what was decided, in plain words.",
        "alternatives": "TODO: list the serious alternatives, with their pros and cons.",
        "consequences": "TODO: what becomes easier or harder, and what could go wrong.",
    }


def load_provider(spec):
    """`None` or 'template' -> the offline drafter. 'package.module:function' -> your own provider."""
    if not spec or spec == "template":
        return "template", template_provider
    module, _, func = spec.partition(":")
    return spec, getattr(importlib.import_module(module), func)


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "change"


def _next_id(records_dir: Path) -> str:
    ids = [int(r.id) for r in load_all(records_dir) if r.id.isdigit()]
    return f"{(max(ids) + 1) if ids else 1:04d}"


def draft(root: Path, policy: Policy, files: list, title: str, spec: str = "", provider_spec=None) -> Record:
    root = Path(root)
    name, provider = load_provider(provider_spec)
    sizes = {}
    for rel in files:
        f = root / rel
        sizes[rel] = len(f.read_text(encoding="utf-8", errors="replace").splitlines()) if f.is_file() else None
    sections = provider(sizes)
    body = (f"# {title}\n\n## Context\n\n{sections['context']}\n\n## Decision\n\n{sections['decision']}\n\n"
            f"## Alternatives considered\n\n{sections['alternatives']}\n\n## Consequences\n\n{sections['consequences']}\n")
    records_dir = root / policy.records_dir
    records_dir.mkdir(parents=True, exist_ok=True)
    rid = _next_id(records_dir)
    meta = {
        "id": rid,
        "title": title,
        "status": "proposed",
        "covers": sorted(files),
        "spec": spec or None,
        "reversibility": policy.level_for_paths(files),
        "change_hash": change_hash(root, files),
        "drafted_by": name,
        "draft_body_hash": sha256_text(body),
        "attested_by": None,
        "attested_at": None,
        "edited_by_builder": None,
        "audit": {"auditor": None, "date": None, "status": "pending", "checks": {}},
    }
    rec = Record(records_dir / f"{rid}-{_slug(title)}.md", meta, body)
    rec.save()
    return rec
