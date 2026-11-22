---
id: '0003'
title: Create the orders table
status: accepted
covers:
- db/migrations/001_create_orders.sql
spec: BAKE-3
reversibility: cannot_undo
change_hash: sha256:461ea6061d3b2ee23ea637398274f422a0250f1f1b45320543510d6bc86a8c0a
drafted_by: template
draft_body_hash: sha256:3386aa701871ae88b96bd102df606fb71c2e3886358c8154adc99d0a1b86e393
attested_by: Jordan Lee
attested_at: '2026-11-21T12:00:00+00:00'
edited_by_builder: false
audit:
  auditor: Sam Reyes
  date: '2026-11-21T12:00:00+00:00'
  status: pass
  checks:
    consistency:
      done: true
      result: pass
    explain_back:
      done: true
      note: Builder explained the three columns and why the time is stored as text.
    stress:
      done: true
      note: Ran the migration twice and against a copy with 10,000 fictional rows;
        both runs behaved as described.
---
# Create the orders table

## Context

This change touches 1 file(s):

- `db/migrations/001_create_orders.sql` (6 lines)

TODO: say why the change is needed.

## Decision

TODO: state what was decided, in plain words.

## Alternatives considered

TODO: list the serious alternatives, with their pros and cons.

## Consequences

TODO: what becomes easier or harder, and what could go wrong.
