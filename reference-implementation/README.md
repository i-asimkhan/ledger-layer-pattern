# Reference implementation

A small, runnable demo of the pattern on a fictional bakery ordering app. It shows the idea. It is not
a product: an **illustration** of the idea. It does not implement everything in [SPEC.md](../SPEC.md).

## The 60-second walkthrough

```bash
cd reference-implementation
pip install -e ".[test]"
python walkthrough.py
```

The walkthrough builds a throwaway git repository and plays one change through the whole cycle:

1. A builder adds a bulk discount (a model change and a data migration). **The gate refuses**: no record covers the files.
2. `ledger draft` drafts a record with an offline template. The builder edits it until it is true, then `ledger attest` signs it. **The gate still refuses**: not audited.
3. A different person runs `ledger audit`. The migration cannot be undone, so the policy also requires an independent stress test. The first attempt is **rejected**; the second, with the stress test, passes.
4. **The gate passes.**
5. Someone edits the model after the audit. **The gate refuses again**: the record and the code have drifted.

Captured output is in [`../docs/demo-output/`](../docs/demo-output/): [failing](../docs/demo-output/failing.txt),
[passing](../docs/demo-output/passing.txt), [full](../docs/demo-output/walkthrough.txt). (Screenshots of a failing
and a passing pull request can be added once the repository is on GitHub.)

## The CLI

```text
ledger draft  --title "..." [--files a b ...] [--spec ID] [--provider template|pkg.mod:func]
ledger attest ID --by "Builder Name"
ledger audit  ID --auditor "Another Person" [--explain-back "..."] [--stress "..."] [--status pass|needs-changes]
ledger check  [--base main]        # the gate; exit code 1 on failure
```

Use `--root <folder>` to point at a project that has a `ledger.yml`.

## Records

Markdown with YAML front matter, readable by people and checkable by the gate. See
[`../examples/`](../examples/) and [`../templates/`](../templates/). "Edited by builder" is computed
from the text, not self-reported.

## The policy file: `ledger.yml`

Maps paths to reversibility (easy / hard / cannot be undone) and reversibility to required checks. This
turns "irreversibility sets audit depth" into configuration. See [`demo-app/ledger.yml`](demo-app/ledger.yml).
The gate always uses the **current** policy, so a record cannot claim a shallower level than the policy
requires.

## AI drafting is optional and pluggable

By default the Ledger drafts with an offline template, so the demo runs anywhere with no key and no network.
A provider is any function that takes `{path: line_count}` and returns the four section texts (context,
decision, alternatives, consequences):

```bash
ledger draft --title "..." --provider my_package.my_module:my_function
```

There are no product names in this repository. If you build an "explain-back helper" that suggests questions
to the auditor, it SHOULD use a different model from the one that wrote the code, and a person still signs.
No such helper is included.

## Use the gate in CI

The gate ships as a reusable GitHub Action: [`../action.yml`](../action.yml). The README at the repository
root shows the workflow (about three lines). The action has not been run on GitHub yet.

## Tests

```bash
pytest        # 15 tests
```

They cover the policy, the hash, and the gate: missing record, unattested, unaudited, passing flow, drift,
auditing your own work, depth by reversibility, the policy being re-read at check time, a pull request that
tries to loosen its own gate, first adoption (no policy on the base branch yet), the zero-edit flag, pluggable
providers and the computed "edited" flag.

## Limits (honest)

- Names are text. The demo does not use cryptographic signatures. Use pull request identities and branch
  protection to establish who did what.
- The change hash covers whole files, not a diff.
- Records are not locked after audit. SPEC 2.5 says they should be. A pull request could also edit an
  existing record, because the gate reads records from the branch under test. Use code owners or repository
  rules to protect `records/`.
- The gate reads the **policy** from the base branch, so a pull request cannot loosen its own gate. Only when
  the base branch has no `ledger.yml` yet (first adoption) does it use the branch's policy, and it prints a warning.
- The Ledger does not propose diagram updates (SPEC 3.2b). It drafts the record, links the spec and hashes the change.
- It checks files in the repository. It cannot see operations, keys or infrastructure.
- The package is about 400 lines including the CLI and comments, so it is small enough to read in one sitting.
