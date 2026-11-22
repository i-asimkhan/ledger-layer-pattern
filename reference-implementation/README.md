# Reference implementation

> **An illustration of the pattern, not production software.** It is a small demo on a fictional bakery
> ordering app, and it does not implement everything in [SPEC.md](../SPEC.md). It is not published as a
> package (no PyPI): install it from a clone, as below.

## The 60-second walkthrough

```bash
cd reference-implementation
pip install -e ".[test]"
python walkthrough.py
```

The walkthrough builds a throwaway git repository and plays one change through the whole cycle:

1. A builder adds a bulk discount (a model change and a data migration). **The gate refuses**: no record covers the files.
2. `ledger draft` drafts a record with a plain offline template. The builder edits it until it is true, then `ledger attest` signs it. **The gate still refuses**: not audited.
3. A different person runs `ledger audit`. The migration cannot be undone, so the policy also requires an independent stress test. The first attempt is **rejected**; the second, with the stress test, passes.
4. **The gate passes.**
5. Someone edits the model after the audit. **The gate refuses again**: the record and the code have drifted.

Captured output is in [`../docs/demo-output/`](../docs/demo-output/): [failing](../docs/demo-output/failing.txt),
[passing](../docs/demo-output/passing.txt), [full](../docs/demo-output/walkthrough.txt). The gate also runs
on pull requests to this repository through [`gate-demo.yml`](../.github/workflows/gate-demo.yml).

## The CLI

```text
ledger draft  --title "..." [--files a b ...] [--spec ID]
ledger attest ID --by "Builder Name"
ledger audit  ID --auditor "Another Person" [--explain-back "..."] [--stress "..."] [--status pass|needs-changes]
ledger check  [--base main]        # the gate; exit code 1 on failure
```

Use `--root <folder>` to point at a project that has a `ledger.yml`.

## Records

Markdown with YAML front matter, readable by people and checkable by the gate. See
[`../examples/`](../examples/) and [`../templates/`](../templates/). "Edited by builder" is computed
from the text, not self-reported. The change hash is a hash of the covered files' contents.

## The policy file: `ledger.yml`

Maps paths to reversibility (easy / hard / cannot be undone) and reversibility to required checks. This
turns "irreversibility sets audit depth" into configuration. See [`demo-app/ledger.yml`](demo-app/ledger.yml).
The gate reads the policy from the **base branch**, so a record cannot claim a shallower level than the policy
requires, and a pull request cannot loosen its own gate.

## Drafting is a plain template

The Ledger drafts with an offline template, so the demo runs anywhere with no key and no network, and no AI is
involved. The template cannot know why a change was made, so it leaves TODOs that the builder must fill in. (The
spec allows any drafting method: SPEC 3.5.) If you add an "explain-back helper" that suggests questions to the
auditor, it SHOULD use a different model from the one that wrote the code, and a person still signs. No such
helper is included.

## Use the gate in CI

The gate ships as a reusable GitHub Action: [`../action.yml`](../action.yml). The README at the repository root
shows the workflow. Notes:

- The action fetches the base branch and the history it needs itself, so a plain `actions/checkout` works.
  `fetch-depth: 0` on checkout makes it a little faster.
- The tag `v0.1` does not exist until the first release is made. Until then, use a commit SHA or `@main`.
- Run it on `pull_request` events, or set the `base` input.

## Tests

```bash
pytest        # 14 tests
```

They cover the policy, the hash, and the gate: missing record, unattested, unaudited, passing flow, drift,
auditing your own work, depth by reversibility, the policy being read from the base branch, a pull request that
tries to loosen its own gate, first adoption (no policy on the base branch yet), the zero-edit flag and the
computed "edited" flag.

## Limits (honest)

- **A "signature" is a typed name.** The demo does not verify who anyone is. A real setup ties attest and audit
  to verified accounts: pull request approvals by named people, branch protection, signed commits.
- The change hash covers whole files, not a diff.
- Records are not locked after audit. SPEC 2.5 says the decision text should be frozen once accepted. A pull
  request could also edit an existing record, because the gate reads records from the branch under test. Use code
  owners or repository rules to protect `records/`.
- **The demo does not draft diagrams.** The Ledger drafts the record, links the spec and hashes the change. It does
  not propose diagram updates (SPEC 3.2b).
- It checks files in the repository. It cannot see operations, credentials or infrastructure.
- The package is about 400 lines including the CLI and comments, so it is small enough to read in one sitting.
