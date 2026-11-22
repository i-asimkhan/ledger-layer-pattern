---
# This is the real record format the `ledger` CLI reads and writes: Markdown with YAML front matter.
# Fictional placeholder values only. Keep the record to about a page.
id: "0000"
title: Short title of the decision
status: proposed            # proposed | attested | accepted (after a passing audit); later: superseded
covers:                     # the files this record is about
  - path/to/file.py
spec: STORY-0             # link or id of the spec or story
reversibility: easy         # easy | hard | cannot_undo  (the policy decides; this sets how deep the audit goes)
change_hash: sha256:...     # computed by the tool over the covered files
drafted_by: template        # how the draft was made (template or a provider name)
draft_body_hash: sha256:... # computed by the tool, so "edited by builder" cannot be self-reported
attested_by: null           # the builder's name, set by `ledger attest`
attested_at: null
edited_by_builder: null     # computed: did the builder change the drafted text? false is flagged
audit:
  auditor: null             # a different person from the builder
  date: null
  status: pending           # pending | pass | needs-changes
  checks:                   # filled by `ledger audit`
    consistency: {}         # done: true, result: pass | fail
    explain_back: {}        # done: true, note: "what the builder explained, in their own words"
    stress: {}              # done: true, note: "what was run, and the result"
---
# Short title of the decision

## Context

What forces are at play? What problem is this change solving?

## Decision

What was decided, in plain words.

## Alternatives considered

The serious alternatives, with their pros and cons.

## Consequences

What becomes easier or harder, and what could go wrong.
