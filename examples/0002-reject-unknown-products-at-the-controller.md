---
id: '0002'
title: Reject unknown products at the controller
status: accepted
covers:
- app/controller/order_controller.py
- app/model/order.py
spec: BAKE-15
reversibility: hard
change_hash: sha256:6c0f043bba90481101e6c3c2393450473494930f992598adac7247a7c8d7a74e
drafted_by: template
draft_body_hash: sha256:b15d9efd27000986a1b1e2259422d9fbc9fca4ccc021513168581d2541fbb188
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
    explain_back:
      done: true
      note: Builder explained why the check lives in the controller and what a caller
        sees on a bad name.
---
# Reject unknown products at the controller

## Context

An order with a misspelt product reached the model and raised a confusing error.

## Decision

The controller checks every product against the price list and reports unknown names clearly.

## Alternatives considered

- Check inside the model: one place for the rule, but the model would need to know about requests.
- Silently drop unknown products: friendlier, but orders would be wrong without anyone noticing.

## Consequences

Callers must handle a ValueError. The price list becomes the single source of truth for valid products.
