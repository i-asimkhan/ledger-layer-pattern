---
id: '0001'
title: Show line items on the receipt
status: accepted
covers:
- app/view/order_view.py
spec: BAKE-12
reversibility: easy
change_hash: sha256:57f46fabc3e0a271f0f27b6da9a1d800044a354c8e4fced77991e0bfc008b17c
drafted_by: template
draft_body_hash: sha256:cf828fb9ac5c7d65ce033cfaf1c67f0da07a8e0d49ce91572bab60bd5a55f59b
attested_by: Avery Baker
attested_at: '2026-11-21T12:00:00+00:00'
edited_by_builder: true
audit:
  auditor: Sam Reyes
  date: '2026-11-21T12:00:00+00:00'
  status: pass
  checks:
    consistency:
      done: true
      result: pass
---
# Show line items on the receipt

## Context

Customers could not see what they had ordered, only the total.

## Decision

The receipt lists each product and quantity above the total.

## Alternatives considered

- Show items only on request: fewer lines, but customers asked for them by default.
- Print a table: tidier, but the receipt is read on small screens.

## Consequences

Receipts get longer. No data changes, so the change is easy to undo.
