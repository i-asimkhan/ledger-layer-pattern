# Example records

Three fictional records for the demo bakery app. Fictional people and data only. Their change hashes
are real: they cover files of the demo app as shipped in `reference-implementation/demo-app/`.

| Record | Reversibility | What it shows |
|---|---|---|
| [0001](0001-show-line-items-on-the-receipt.md) | easy | The lightest case: consistency check only |
| [0002](0002-reject-unknown-products-at-the-controller.md) | hard | A change to the model, so an explain-back is required |
| [0003](0003-create-the-orders-table.md) | cannot be undone | A migration: explain-back and an independent stress test are both required. **This record was attested with zero edits to the drafted text**, so the template placeholders are still in it, and a gate configured with `zero_edit: warn` would flag it. It is here to show what a flagged record looks like. |

To regenerate records like these, see `reference-implementation/walkthrough.py`.
