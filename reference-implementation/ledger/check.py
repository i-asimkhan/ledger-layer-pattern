"""Step 3, the gate: a change passes only with a signed, audited record that still matches the code."""
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .audit import same_person
from .policy import Policy
from .records import Record, change_hash, load_all


@dataclass
class Finding:
    path: str
    record: str = ""
    problems: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def changed_files(root: Path, base: str) -> list:
    """Files changed on this branch relative to `base`, as paths relative to `root`."""
    out = subprocess.run(["git", "-C", str(root), "diff", "--name-only", "--relative", "--no-renames",
                          f"{base}...HEAD"], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"git diff against '{base}' failed: {out.stderr.strip()}\n"
                         "hint: the base branch and its history must be available. In GitHub Actions, "
                         "use the ledger action (it fetches them), or checkout with fetch-depth: 0.")
    return [p for p in out.stdout.splitlines() if p]


def verify_record(root: Path, policy: Policy, rec: Record):
    """Return (problems, warnings) for one record."""
    m, problems, warnings = rec.meta, [], []
    if not (m.get("attested_by") and m.get("attested_at")):
        problems.append("not attested by the builder")
    audit = m.get("audit") or {}
    if audit.get("status") != "pass":
        problems.append(f"not audited (audit status: {audit.get('status', 'pending')})")
    else:
        if same_person(audit.get("auditor"), m.get("attested_by")):
            problems.append("the auditor is the builder: nobody audits their own work")
        level = policy.level_for_paths(m.get("covers", []))  # current policy, not what the record claims
        checks = audit.get("checks") or {}
        for name in policy.required_checks(level):
            c = checks.get(name) or {}
            done = c.get("result") == "pass" if name == "consistency" else bool(c.get("done")) and bool(str(c.get("note", "")).strip())
            if not done:
                problems.append(f"'{level}' changes require the '{name}' check, and it is missing")
    if m.get("change_hash") != change_hash(root, m.get("covers", [])):
        problems.append("the record and the code have drifted: the change hash no longer matches")
    if m.get("drafted_by") != "human" and m.get("edited_by_builder") is False:
        (problems if policy.zero_edit == "fail" else warnings).append("the builder signed the drafted record with zero edits")
    return problems, warnings


def check(root: Path, base: str) -> list:
    """Check every changed file that needs a record. Returns a list of Findings.
    The policy comes from the base branch (see Policy.load_from_base), never from the change under test."""
    root = Path(root)
    policy, _ = Policy.load_from_base(root, base)
    records = sorted(load_all(root / policy.records_dir), key=lambda r: r.id, reverse=True)  # newest first
    cache, findings = {}, []
    for path in changed_files(root, base):
        if policy.ignored(path):
            continue
        rec = next((r for r in records if path in (r.meta.get("covers") or [])), None)
        if rec is None:
            findings.append(Finding(path, problems=["no Ledger record covers this file"]))
            continue
        if rec.id not in cache:
            cache[rec.id] = verify_record(root, policy, rec)
        problems, warnings = cache[rec.id]
        findings.append(Finding(path, rec.id, list(problems), list(warnings)))
    return findings
