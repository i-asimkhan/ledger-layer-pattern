#!/usr/bin/env python3
"""A scripted 60-second walkthrough on the fictional bakery demo app.

    python walkthrough.py            # print the walkthrough
    python walkthrough.py --save     # also write ../docs/demo-output/*.txt

It builds a throwaway git repo in a temp folder, so nothing in this repository changes.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEMO = HERE / "demo-app"
OUT = HERE.parent / "docs" / "demo-output"

BUILDER, AUDITOR = "Avery Baker", "Sam Reyes"  # fictional people
log = []  # (section, text)


def say(section, text=""):
    print(text)
    log.append((section, text))


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)


def ledger(root, section, *args):
    env = dict(os.environ, PYTHONPATH=str(HERE), LEDGER_FIXED_TIME="2026-11-21T12:00:00+00:00",
               PYTHONIOENCODING="utf-8")
    shown = " ".join(f'"{a}"' if " " in a else a for a in args)
    say(section, f"$ ledger {shown}")
    p = subprocess.run([sys.executable, "-m", "ledger", "--root", str(root), *args], env=env,
                       capture_output=True, text=True)
    for line in (p.stdout + p.stderr).rstrip().splitlines():
        say(section, line)
    say(section, f"(exit code {p.returncode})")
    say(section)
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="write the transcripts to ../docs/demo-output/")
    args = ap.parse_args()

    root = Path(tempfile.mkdtemp(prefix="ledger-demo-")) / "bakery"
    shutil.copytree(DEMO, root, ignore=shutil.ignore_patterns('0*.md', '__pycache__'))
    for cmd in (["init", "-b", "main"], ["config", "user.name", "Demo"], ["config", "user.email", "demo@example.invalid"],
                ["config", "commit.gpgsign", "false"], ["add", "-A"], ["commit", "-m", "initial"],
                ["checkout", "-b", "feature/bulk-discount"]):
        git(root, *cmd)

    say("setup", "# 1. A builder adds a bulk discount: a model change (hard to undo) and a data migration (cannot be undone).")
    model = root / "app/model/order.py"
    model.write_text(model.read_text(encoding="utf-8") + "\n    def discounted_total(self) -> float:\n"
                     "        qty = sum(self.items.values())\n"
                     "        return round(self.total() * (0.9 if qty >= 10 else 1.0), 2)\n", encoding="utf-8", newline="\n")
    (root / "db/migrations/003_add_discount.sql").write_text(
        "-- Fictional migration for the demo app.\nALTER TABLE orders ADD COLUMN discount_pct INTEGER DEFAULT 0;\n",
        encoding="utf-8", newline="\n")
    git(root, "add", "-A")
    git(root, "commit", "-m", "Add bulk discount")
    say("setup")

    say("failing", "# 2. The pull request has no Ledger record. The gate refuses it.")
    ledger(root, "failing", "check", "--base", "main")

    say("flow", "# 3. The Ledger drafts a record for the change (offline template).")
    ledger(root, "flow", "draft", "--title", "Add bulk discount", "--spec", "BAKE-17",
           "--files", "app/model/order.py", "db/migrations/003_add_discount.sql")
    rec = next((root / "records").glob("0001-*.md"))
    text = rec.read_text(encoding="utf-8")
    text = text.replace("TODO: say why the change is needed.", "Customers who buy ten or more items asked for a discount.")
    text = text.replace("TODO: state what was decided, in plain words.", "Orders of ten or more items get 10 percent off. The discount rate is stored with each order.")
    text = text.replace("TODO: list the serious alternatives, with their pros and cons.", "- A coupon code: simpler, but customers must remember it.\n- A fixed price list: no maths, but less flexible.")
    text = text.replace("TODO: what becomes easier or harder, and what could go wrong.", "Receipts can show a discount. Old orders have no discount column value, so the migration defaults it to zero.")
    rec.write_text(text, encoding="utf-8", newline="\n")
    say("flow", "# 4. The builder edits the record until it is true, then signs it.")
    ledger(root, "flow", "attest", "0001", "--by", BUILDER)

    say("failing", "# 5. Signed, but not audited yet. The gate still refuses.")
    ledger(root, "failing", "check", "--base", "main")

    say("flow", "# 6. The auditor, a different person, tries to pass it after an explain-back only.")
    say("flow", "#    The migration cannot be undone, so policy also requires an independent stress test.")
    ledger(root, "flow", "audit", "0001", "--auditor", AUDITOR, "--explain-back",
           "Builder explained the ten-item rule and why the default is zero for old rows.")

    say("flow", "# 7. The auditor adds the stress test and passes it.")
    ledger(root, "flow", "audit", "0001", "--auditor", AUDITOR, "--explain-back",
           "Builder explained the ten-item rule and why the default is zero for old rows.",
           "--stress", "Ran the migration twice and on a table with 10,000 fictional rows; ran quantities 0, 9, 10 and -1.")

    say("passing", "# 8. Signed, audited, and the hash matches. The gate passes.")
    ledger(root, "passing", "check", "--base", "main")

    say("failing", "# 9. Someone edits the model after the audit. The record and the code have drifted.")
    model.write_text(model.read_text(encoding="utf-8") + "\n# a late tweak\n", encoding="utf-8", newline="\n")
    git(root, "add", "-A")
    git(root, "commit", "-m", "Late tweak")
    ledger(root, "failing", "check", "--base", "main")

    if args.save:
        OUT.mkdir(parents=True, exist_ok=True)
        files = {"walkthrough.txt": None, "failing.txt": "failing", "passing.txt": "passing"}
        for name, section in files.items():
            lines = [t for s, t in log if section is None or s == section]
            (OUT / name).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
        print(f"saved transcripts to {OUT}")
    shutil.rmtree(root.parent, ignore_errors=True)


if __name__ == "__main__":
    main()
