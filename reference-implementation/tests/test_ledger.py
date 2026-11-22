from pathlib import Path

import pytest

from ledger import audit as audit_mod
from ledger import check as check_mod
from ledger import draft as draft_mod
from ledger.policy import Policy, glob_to_regex
from ledger.records import Record, change_hash, find

from conftest import commit_change, git

VIEW = "app/view/order_view.py"            # level: easy
MODEL = "app/model/order.py"               # level: hard
MIGRATION = "db/migrations/003_add_notes.sql"  # level: cannot_undo


def result(root):
    return {f.path: f for f in check_mod.check(root, "main")}


def full_flow(root, files, title="A change", auditor="Sam Auditor", explain="Builder explained it.",
              stress="", edit=True):
    """draft -> (edit) -> attest -> audit, returning the record."""
    policy = Policy.load(root)
    rec = draft_mod.draft(root, policy, files, title)
    if edit:
        rec.body = rec.body.replace("TODO: state what was decided, in plain words.", "We decided X, because Y.")
        rec.save()
    audit_mod.attest(root, rec, "Avery Builder")
    return audit_mod.audit(root, policy, Record.load(rec.path), auditor, explain, stress)


# ---- policy -------------------------------------------------------------
def test_glob_and_levels():
    assert glob_to_regex("db/migrations/**").match("db/migrations/001.sql")
    assert glob_to_regex("**/*.md").match("docs/a/b.md") and glob_to_regex("**/*.md").match("a.md")
    assert not glob_to_regex("app/*.py").match("app/model/order.py")
    policy = Policy.load(Path(__file__).resolve().parent.parent / "demo-app")
    assert policy.level_for("db/migrations/001.sql") == "cannot_undo"
    assert policy.level_for(MODEL) == "hard"
    assert policy.level_for(VIEW) == "easy"
    assert policy.level_for_paths([VIEW, MODEL]) == "hard"  # the deepest level wins


def test_change_hash_ignores_line_endings(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"one\ntwo\n")
    h1 = change_hash(tmp_path, ["a.txt"])
    (tmp_path / "a.txt").write_bytes(b"one\r\ntwo\r\n")
    assert change_hash(tmp_path, ["a.txt"]) == h1
    (tmp_path / "a.txt").write_bytes(b"one\ntwo!\n")
    assert change_hash(tmp_path, ["a.txt"]) != h1


# ---- the gate -----------------------------------------------------------
def test_gate_fails_without_a_record(repo):
    commit_change(repo, VIEW, "# changed\n")
    f = result(repo)[VIEW]
    assert not f.ok and "no Ledger record" in f.problems[0]


def test_ignored_files_need_no_record(repo):
    commit_change(repo, "NOTES.md", "notes\n")
    assert check_mod.check(repo, "main") == []


def test_unattested_and_unaudited_records_fail(repo):
    commit_change(repo, VIEW, "# changed\n")
    draft_mod.draft(repo, Policy.load(repo), [VIEW], "A change")
    problems = result(repo)[VIEW].problems
    assert any("not attested" in p for p in problems) and any("not audited" in p for p in problems)


def test_full_flow_passes(repo):
    commit_change(repo, VIEW, "# changed\n")
    full_flow(repo, [VIEW])
    f = result(repo)[VIEW]
    assert f.ok and f.warnings == []


def test_gate_detects_drift_after_audit(repo):
    commit_change(repo, VIEW, "# changed\n")
    full_flow(repo, [VIEW])
    commit_change(repo, VIEW, "# changed again, after the audit\n")
    assert any("drifted" in p for p in result(repo)[VIEW].problems)


def test_nobody_audits_their_own_work(repo):
    commit_change(repo, VIEW, "# changed\n")
    policy = Policy.load(repo)
    rec = draft_mod.draft(repo, policy, [VIEW], "A change")
    audit_mod.attest(repo, rec, "Avery Builder")
    with pytest.raises(SystemExit, match="nobody audits their own work"):
        audit_mod.audit(repo, policy, Record.load(rec.path), "avery builder")
    # even a forged record is caught by the gate
    rec = Record.load(rec.path)
    rec.meta["audit"] = {"auditor": "Avery Builder", "date": "x", "status": "pass",
                         "checks": {"consistency": {"done": True, "result": "pass"}}}
    rec.save()
    assert any("nobody audits their own work" in p for p in result(repo)[VIEW].problems)


def test_depth_follows_reversibility(repo):
    commit_change(repo, MODEL, "# model changed\n")
    commit_change(repo, MIGRATION, "ALTER TABLE orders ADD notes TEXT;\n")
    policy = Policy.load(repo)
    # 'hard' needs explain-back
    rec = draft_mod.draft(repo, policy, [MODEL], "Model change")
    audit_mod.attest(repo, rec, "Avery Builder")
    with pytest.raises(SystemExit, match="explain_back"):
        audit_mod.audit(repo, policy, Record.load(rec.path), "Sam Auditor")
    # 'cannot_undo' needs explain-back and a stress test
    rec2 = draft_mod.draft(repo, policy, [MIGRATION], "Add notes column")
    audit_mod.attest(repo, rec2, "Avery Builder")
    with pytest.raises(SystemExit, match="stress"):
        audit_mod.audit(repo, policy, Record.load(rec2.path), "Sam Auditor", explain_back="explained")
    audit_mod.audit(repo, policy, Record.load(rec2.path), "Sam Auditor", "explained", "ran 200 adversarial inputs")
    assert result(repo)[MIGRATION].ok
    assert not result(repo)[MODEL].ok  # still unaudited


def test_gate_enforces_current_policy_not_the_record(repo):
    """A record audited at a shallow depth cannot launder a deep change."""
    commit_change(repo, MIGRATION, "ALTER TABLE orders ADD notes TEXT;\n")
    policy = Policy.load(repo)
    rec = draft_mod.draft(repo, policy, [MIGRATION], "Add notes column")
    audit_mod.attest(repo, rec, "Avery Builder")
    rec = Record.load(rec.path)
    rec.meta["audit"] = {"auditor": "Sam Auditor", "date": "x", "status": "pass",
                         "checks": {"consistency": {"done": True, "result": "pass"}}}
    rec.save()
    problems = result(repo)[MIGRATION].problems
    assert any("explain_back" in p for p in problems) and any("stress" in p for p in problems)


def test_zero_edit_is_flagged(repo):
    commit_change(repo, VIEW, "# changed\n")
    full_flow(repo, [VIEW], edit=False)
    f = result(repo)[VIEW]
    assert f.ok and any("zero edits" in w for w in f.warnings)
    # it can be made a hard failure, but the rule must change on the base branch (main), not in the pull request
    git(repo, "checkout", "main")
    policy_file = repo / "ledger.yml"
    policy_file.write_text(policy_file.read_text().replace("zero_edit: warn", "zero_edit: fail"), encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "make zero-edit signatures fail")
    git(repo, "checkout", "feature")
    git(repo, "merge", "main", "--no-edit")
    assert not result(repo)[VIEW].ok and any("zero edits" in p for p in result(repo)[VIEW].problems)


def test_a_pull_request_cannot_loosen_its_own_gate(repo):
    """The policy is read from the base branch. Editing ledger.yml in the branch must not switch the gate off."""
    policy_file = repo / "ledger.yml"
    policy_file.write_text(policy_file.read_text().replace("ignore:\n", 'ignore:\n  - "**"\n'), encoding="utf-8")
    commit_change(repo, VIEW, "# changed in the same pull request\n")
    findings = result(repo)
    assert not findings[VIEW].ok and "no Ledger record" in findings[VIEW].problems[0]
    assert not findings["ledger.yml"].ok  # changing the policy needs an audited record too
    _, source = Policy.load_from_base(repo, "main")
    assert source.startswith("read from main")


def test_first_adoption_falls_back_with_a_warning(tmp_path):
    import shutil
    from conftest import DEMO, SKIP, git

    root = tmp_path / "shop"
    shutil.copytree(DEMO, root, ignore=shutil.ignore_patterns(*SKIP))
    (root / "ledger.yml").rename(tmp_path / "ledger.yml.hold")  # main has no policy yet
    for args in (("init", "-b", "main"), ("config", "user.name", "T"), ("config", "user.email", "t@example.invalid"),
                 ("config", "commit.gpgsign", "false"), ("add", "-A"), ("commit", "-m", "initial"),
                 ("checkout", "-b", "feature")):
        git(root, *args)
    (tmp_path / "ledger.yml.hold").rename(root / "ledger.yml")
    commit_change(root, VIEW, "# changed\n")
    _, source = Policy.load_from_base(root, "main")
    assert source.startswith("WARNING")
    assert not check_mod.check(root, "main")[0].ok  # the branch's policy still applies, so the gate still works


# ---- drafting ------------------------------------------------------------
def test_attest_computes_edited_flag(repo):
    commit_change(repo, VIEW, "# changed\n")
    policy = Policy.load(repo)
    rec = draft_mod.draft(repo, policy, [VIEW], "A change")
    assert audit_mod.attest(repo, find(repo / policy.records_dir, rec.id), "Avery").meta["edited_by_builder"] is False
