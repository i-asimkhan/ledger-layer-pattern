# How this differs from what you already do

This is a general comparison, not a survey. Practices vary by organisation, so read the left-hand
columns as typical descriptions.

| Practice | What it typically covers | What it typically does not | What this pattern adds |
|---|---|---|---|
| **ADRs** (Nygard; Fowler) | A short record of one decision, kept in the repository, superseded not edited | Who checks the record, whether it matches the code, whether the author understood it | Automatic drafting, a change hash, attestation, independent audit, a gate |
| **Code review** | Peer review of a code change before merge | A check of the *reasoning* against the work; a test of whether the reviewer or author understood; independence from the team | An independent audit role; the explain-back; stress testing; records |
| **Change-management controls** | Approvals and separation of duties on changes | The content of the reasoning behind a change | A record of the decision tied to the code, checked by an auditor |
| **IV&V** (NASA; IEEE independence) | Independent verification and validation throughout the software lifecycle; technical, managerial and financial independence | Cheap adoption for ordinary teams; a lightweight, repository-level evidence trail | A software-team adaptation: mirror audit roles, a gate in the pipeline, tiers from small team to external audit |
| **The intent ledger** (Osmani) | The team writes down the reasons for decisions, so people and tools can read them | Independent checking of what was written | A layer that creates the evidence by default, plus independent audit on top |
| **This pattern** | A drafted, attested, hash-pinned record; independent audit of three kinds; a gate; audit depth set by irreversibility | Everything outside the repository (operations, keys, infrastructure); a guarantee that audited work is correct | |

See [SOURCES.md](SOURCES.md) for the references behind the ADR, IV&V and intent-ledger rows. The
code-review and change-management rows are general descriptions, not claims from a specific source.
