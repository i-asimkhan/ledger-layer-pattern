"""Steps 2 and 4: the builder attests; a different person audits."""
from pathlib import Path

from .policy import Policy
from .records import Record, change_hash, now, sha256_text


def same_person(a, b) -> bool:
    return bool(a) and bool(b) and str(a).strip().lower() == str(b).strip().lower()


def attest(root: Path, rec: Record, by: str) -> Record:
    """The builder signs. 'edited by builder' is computed, not self-reported: did the body change?"""
    rec.meta["change_hash"] = change_hash(root, rec.meta.get("covers", []))
    rec.meta["edited_by_builder"] = sha256_text(rec.body) != rec.meta.get("draft_body_hash")
    rec.meta["attested_by"] = by
    rec.meta["attested_at"] = now()
    rec.meta["status"] = "attested"
    rec.meta["audit"] = {"auditor": None, "date": None, "status": "pending", "checks": {}}  # re-attesting resets audit
    rec.save()
    return rec


def audit(root: Path, policy: Policy, rec: Record, auditor: str, explain_back: str = "", stress: str = "",
          status: str = "pass") -> Record:
    """Record an audit. Refuses an audit by the builder, and refuses 'pass' when required checks are missing."""
    if not rec.meta.get("attested_by"):
        raise SystemExit("this record has not been attested by the builder yet")
    if same_person(auditor, rec.meta["attested_by"]):
        raise SystemExit("nobody audits their own work: the auditor must not be the builder")
    covers = rec.meta.get("covers", [])
    consistent = change_hash(root, covers) == rec.meta.get("change_hash")
    checks = {"consistency": {"done": True, "result": "pass" if consistent else "fail"}}
    if explain_back.strip():
        checks["explain_back"] = {"done": True, "note": explain_back.strip()}
    if stress.strip():
        checks["stress"] = {"done": True, "note": stress.strip()}
    if status == "pass":
        if not consistent:
            raise SystemExit("cannot pass: the code no longer matches the record (change hash differs)")
        level = policy.level_for_paths(covers)
        missing = [c for c in policy.required_checks(level) if c not in checks]
        if missing:
            raise SystemExit(f"cannot pass: '{level}' changes also need: {', '.join(missing)}")
    rec.meta["audit"] = {"auditor": auditor, "date": now(), "status": status, "checks": checks}
    rec.meta["status"] = "accepted" if status == "pass" else "attested"
    rec.save()
    return rec
