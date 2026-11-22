"""Command line: ledger draft | attest | audit | check"""
import argparse
from pathlib import Path

from . import audit as audit_mod
from . import check as check_mod
from . import draft as draft_mod
from .policy import Policy
from .records import find


def cmd_draft(a):
    root = Path(a.root)
    policy = Policy.load(root)
    files = a.files or [p for p in check_mod.changed_files(root, a.base) if not policy.ignored(p)]
    if not files:
        raise SystemExit("no files to cover: pass --files, or make a change relative to --base")
    rec = draft_mod.draft(root, policy, files, a.title, a.spec or "")
    print(f"drafted {rec.path.relative_to(root).as_posix()}  (reversibility: {rec.meta['reversibility']})")
    print("next: edit the record so it is true, then run: ledger attest", rec.id, "--by <your name>")


def cmd_attest(a):
    root = Path(a.root)
    rec = audit_mod.attest(root, find(root / Policy.load(root).records_dir, a.id), a.by)
    flag = "yes" if rec.meta["edited_by_builder"] else "NO (flagged for the auditor)"
    print(f"attested {rec.id} by {a.by}; edited by builder: {flag}")


def cmd_audit(a):
    root = Path(a.root)
    policy = Policy.load(root)
    rec = audit_mod.audit(root, policy, find(root / policy.records_dir, a.id), a.auditor,
                          a.explain_back or "", a.stress or "", a.status)
    print(f"audited {rec.id} by {a.auditor}: {rec.meta['audit']['status']}")


def cmd_check(a):
    _, source = Policy.load_from_base(Path(a.root), a.base)
    print(f"policy: {source}")
    findings = check_mod.check(Path(a.root), a.base)
    if not findings:
        print("gate: no changed files need a record. PASS")
        return 0
    for f in findings:
        tag = "PASS" if f.ok else "FAIL"
        print(f"{tag}  {f.path}" + (f"  (record {f.record})" if f.record else ""))
        for p in f.problems:
            print(f"      - {p}")
        for w in f.warnings:
            print(f"      ! warning: {w}")
    failed = sum(not f.ok for f in findings)
    print(f"gate: {'FAIL' if failed else 'PASS'} ({failed} of {len(findings)} changed file(s) not covered by a signed, audited record)"
          if failed else f"gate: PASS ({len(findings)} changed file(s) covered by signed, audited records)")
    return 1 if failed else 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="ledger", description="Ledger layer and audit gate (reference implementation)")
    p.add_argument("--root", default=".", help="project root (where ledger.yml lives)")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("draft", help="draft a record for a change")
    d.add_argument("--title", required=True)
    d.add_argument("--files", nargs="*", help="files the record covers (default: files changed vs --base)")
    d.add_argument("--base", default="main")
    d.add_argument("--spec", help="link or id of the spec or story")
    d.set_defaults(func=cmd_draft)

    t = sub.add_parser("attest", help="the builder signs the record")
    t.add_argument("id")
    t.add_argument("--by", required=True, help="the builder's name")
    t.set_defaults(func=cmd_attest)

    u = sub.add_parser("audit", help="a different person audits the record")
    u.add_argument("id")
    u.add_argument("--auditor", required=True)
    u.add_argument("--explain-back", help="short note: what the builder explained, in their own words")
    u.add_argument("--stress", help="short note: what stress or adversarial testing was run, and the result")
    u.add_argument("--status", choices=["pass", "needs-changes"], default="pass")
    u.set_defaults(func=cmd_audit)

    c = sub.add_parser("check", help="the gate: fail if a changed file lacks a signed, audited record")
    c.add_argument("--base", default="main", help="branch to compare against")
    c.set_defaults(func=cmd_check)

    a = p.parse_args(argv)
    return a.func(a) or 0


if __name__ == "__main__":
    raise SystemExit(main())
