# FAQ

## Isn't this just ADRs?

ADRs are the right starting point. An architecture decision record is a short document that captures one
decision, kept in the repository, never edited once accepted, and superseded instead (as Martin Fowler
describes it: [source](https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html)). This pattern
builds on that idea and adds four things an ADR does not give you by itself:

1. the record is **drafted automatically** for every change that needs one;
2. it is **bound to the code** by a change hash, so drift is detectable;
3. the builder **attests** to it, and the record shows whether they edited the draft;
4. a different person **audits** it, and a **gate** refuses changes without an audited record.

## Isn't this code review?

Code review looks at a diff. The audit here checks the *record against the work*, and it goes further than
reading: the auditor asks the builder to explain the change in their own words (comprehension), and runs
independent stress and adversarial tests (behaviour). The auditor is also a distinct role, independent of the
team that built the change. A reviewer who approves a diff has not necessarily understood it, which is the
problem this pattern is aimed at.

## Won't it slow us down?

It adds work, and I won't pretend otherwise. Three things keep it manageable: the Ledger drafts the record
for you, audit depth scales with how hard a change is to undo (under the default policy, an easy change needs
only the automatic consistency check; hard and irreversible changes also need an explain-back, and
irreversible ones an independent stress test), and you can start with one risky area instead of the whole codebase. The
argument for the cost is that building has become cheaper, and part of that saving is worth reinvesting in
assurance. That is an argument, not a measurement. I do not have cost data.

## How is this different from Osmani's intent ledger?

Addy Osmani writes: "Treat AGENTS.md as your intent ledger, not your config."
([source](https://addyosmani.com/blog/intent-debt/)). That is a practice: a file, kept by the team, that
records the reasons behind decisions, for people and tools to read. This pattern is a **layer in the
architecture**: it produces the evidence for every change by default, ties it to the code with a hash, and
hands it to independent auditors, with a gate that enforces it. The two fit together: his practice writes the
reasoning down, and this pattern gives it a home in the architecture and an independent check. The idea of writing
intent down is his and Storey's.

## Is the "Ledger" a blockchain?

No. It means a record of decisions kept with the code. A blockchain is not required, and none is used.

## Do I need AI to use this?

No. The reference implementation drafts records with a plain offline template, and no AI is involved. The
specification allows any drafting method (SPEC 3.5). The pattern works whether a change was written by hand or with tools, as long as there is a named builder,
a record, and an independent audit.

## Who audits the auditors?

Honestly, this is partly open. In a small team, the next stage of work tends to expose mistakes in the
previous one (testing exposes development problems, pilots expose testing gaps), and some checks are sampled.
In larger or high-sensitivity settings, a separate audit function reporting outside delivery, and external
auditors, add independence. The IIA's Three Lines Model describes internal audit as an independent third
line with external assurance providers alongside ([source](https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated-english.pdf)).

## Does an audit prevent failures?

No. Audits reduce risk. They cover one version of the work at one point in time, which is why the record
is pinned to a change hash. A 2026 preprint of 218 exploit incidents in blockchain security found that 105
of them (48%) involved a protocol that had at least one prior public audit, and noted that conventional
audits do not review things like key management, the deployment environment or the build pipeline
([source](https://arxiv.org/abs/2606.15465)). Treat that as one preprint, whose author is affiliated with an
audit firm.
