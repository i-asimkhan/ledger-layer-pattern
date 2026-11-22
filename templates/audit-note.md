# Audit note

<!--
For audits of work that has no code diff (a requirements or design audit, a release check), or for a longer
write-up than the record's `audit:` block holds. For code changes the `audit:` block of the record is the
audit record. Fictional placeholder values only. One note per audited item.
-->

Stage: requirements | design | code | test | release
Record: [link to the decision record this note belongs to]
Auditor: [name]                       <!-- never the builder of the work -->
Date: [date]

## Scope

What was examined, and which version (hash or commit).

## Reversibility and depth

Reversibility: easy | hard | cannot be undone
Checks required by the policy for that level: [consistency | + explain-back | + stress test]

## Checks performed

- Consistency: [pass | fail, and how it was checked]
- Explain-back: [who asked, and a short note of what the builder explained, in their own words]
- Stress / adversarial testing: [what was run, and the result]

## Findings

Each finding: what, where, how severe, what follows.

## Outcome

pass | needs-changes

## Follow-up

Re-check needed? By whom? By when?
