# Diagrams

Editable draw.io sources (`*.drawio`) with exports in [`exports/`](exports/): SVG, and a 2x PNG for each.
Diagrams 01, 02 and 04 also have a LinkedIn-sized PNG (1200 x 627).

Every title states the point. Colours: purple is tooling, teal is records, amber is a human decision,
red is audit, slate is the gate or controls.

| # | Diagram | Source | PNG | SVG | LinkedIn size |
|---|---|---|---|---|---|
| 01 | The Ledger layer creates the evidence. Audit gives it meaning. | [drawio](01-ledger-layer-architecture.drawio) | [png](exports/01-ledger-layer-architecture.png) | [svg](exports/01-ledger-layer-architecture.svg) | [png](exports/01-ledger-layer-architecture-linkedin-1200x627.png) |
| 02 | One change: drafted, signed by its builder, then audited | [drawio](02-change-lifecycle.drawio) | [png](exports/02-change-lifecycle.png) | [svg](exports/02-change-lifecycle.svg) | [png](exports/02-change-lifecycle-linkedin-1200x627.png) |
| 03 | Independent audit sits outside the teams that build | [drawio](03-three-lines-for-software.drawio) | [png](exports/03-three-lines-for-software.png) | [svg](exports/03-three-lines-for-software.svg) | |
| 04 | Every build role has an audit role beside it | [drawio](04-roles-rotation.drawio) | [png](exports/04-roles-rotation.png) | [svg](exports/04-roles-rotation.svg) | [png](exports/04-roles-rotation-linkedin-1200x627.png) |
| 05 | One record: what was decided, who signed it, who checked it | [drawio](05-adr-anatomy.drawio) | [png](exports/05-adr-anatomy.png) | [svg](exports/05-adr-anatomy.svg) | |
| 06 | Independence grows with risk: one pattern, three sizes | [drawio](06-three-sizes.drawio) | [png](exports/06-three-sizes.png) | [svg](exports/06-three-sizes.svg) | |
| 07 | Transition now, transformation later | [drawio](07-transition-roadmap.drawio) | [png](exports/07-transition-roadmap.png) | [svg](exports/07-transition-roadmap.svg) | |

Diagram 03 is a software mapping of the IIA Three Lines Model (2020). Diagram 06 uses the IV&V terms
technical, managerial and financial independence.

The exports were rendered from the same layout as the `.drawio` files, so they match. If you open a
`.drawio` file in draw.io and re-export, small text spacing differences are normal.
