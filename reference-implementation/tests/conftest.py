import shutil
import subprocess
from pathlib import Path

import pytest

DEMO = Path(__file__).resolve().parent.parent / "demo-app"


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    """A throwaway git repo with the demo app on 'main', and a 'feature' branch checked out."""
    root = tmp_path / "shop"
    shutil.copytree(DEMO, root)
    git(root, "init", "-b", "main")
    git(root, "config", "user.name", "Test Builder")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", "-A")
    git(root, "commit", "-m", "initial")
    git(root, "checkout", "-b", "feature")
    return root


def commit_change(root, rel, text, message="change"):
    f = Path(root) / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8", newline="\n")
    git(root, "add", "-A")
    git(root, "commit", "-m", message)
