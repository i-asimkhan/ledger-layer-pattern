# Example records

Three fictional records for the demo bakery app. Fictional people and data only. Their change hashes
are real: they cover files of the demo app as shipped in `reference-implementation/demo-app/`.

| Record | Reversibility | What it shows |
|---|---|---|
| [0001](0001-show-line-items-on-the-receipt.md) | easy | The lightest case: the consistency check is enough, and the audit passes |
| [0002](0002-reject-unknown-products-at-the-controller.md) | hard | A change to the model, so an explain-back is also required. The audit passes |
| [0003](0003-purge-orders-placed-before-2020.md) | cannot be undone | A migration that permanently deletes data. The explain-back and the stress test are both required, and **the audit fails**: the builder could not say what still reads the old orders, and the stress test showed data loss with no backup. The gate would refuse this change until it is fixed and re-audited |

To see the gate refuse and then pass a change end to end, run `reference-implementation/walkthrough.py`.
