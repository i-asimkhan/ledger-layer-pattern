---
id: '0001'
title: Show prices with two decimals
status: accepted
covers:
- app/view/order_view.py
spec: BAKE-30
reversibility: easy
change_hash: sha256:53ff29326064eeedf47035d745c7b5a3d27e4489cf717b35a4d3f2efc3409ed7
drafted_by: template
draft_body_hash: sha256:65be378afb1434f010456cd94e2db947f07888988e57a19720d33649e712fa3d
attested_by: Avery Baker
attested_at: '2026-11-22T12:00:00+00:00'
edited_by_builder: true
audit:
  auditor: Sam Reyes
  date: '2026-11-22T12:00:00+00:00'
  status: pass
  checks:
    consistency:
      done: true
      result: pass
---
# Show prices with two decimals

## Context

This change touches 1 file(s):

- `app/view/order_view.py` (11 lines)

Prices were shown with a varying number of decimals.

## Decision

Prices are always shown with two decimals.

## Alternatives considered

- Round to whole numbers: simpler, but loses cents.

## Consequences

Receipts line up. No data changes, so it is easy to undo.
