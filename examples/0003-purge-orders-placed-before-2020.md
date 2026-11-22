---
id: '0003'
title: Purge orders placed before 2020
status: attested
covers:
- db/migrations/002_purge_old_orders.sql
spec: BAKE-21
reversibility: cannot_undo
change_hash: sha256:deb97cc3dd327748f68a0f43d75abaa5b49b1ed8bfc0716f8c4a9d4ab7d64a69
drafted_by: template
draft_body_hash: sha256:ee2ce9419b8e8610fcd6769e2f6a105c9d8f64a57e3465a3da710adcd03e0265
attested_by: Jordan Lee
attested_at: '2026-11-21T12:00:00+00:00'
edited_by_builder: true
audit:
  auditor: Sam Reyes
  date: '2026-11-21T12:00:00+00:00'
  status: needs-changes
  checks:
    consistency:
      done: true
      result: pass
    explain_back:
      done: true
      note: Builder could not say which reports or customer lookups still read orders
        from before 2020.
    stress:
      done: true
      note: 'Ran it on a copy: it deleted 4,812 fictional rows in one statement, and
        two fictional customer lookups then returned nothing. No dry run, no backup.
        Audit result: needs changes.'
---
# Purge orders placed before 2020

## Context

Reports are slow, and the shop does not think it needs orders from before 2020.

## Decision

A migration permanently deletes every order placed before 2020.

## Alternatives considered

- Archive the old orders to a separate table first: safer, but needs storage.
- Keep them and add an index: no data is lost, but reports stay slow.

## Consequences

The rows are gone once the migration runs. The script takes no backup and has no dry-run mode.
