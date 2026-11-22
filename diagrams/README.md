# Diagrams

Editable draw.io sources (`*.drawio`) with exports in [`exports/`](exports/): an SVG and a 2x PNG for every
diagram. Diagrams made for LinkedIn also have two 1200 x 627 PNGs: a light one, and a **dark** one in the
newsletter style (`-linkedin-dark-1200x627.png`).

Every title states the point. Colours mean the same thing everywhere: purple is tooling (the Ledger), teal is
records, amber is a human decision, red is audit, slate is the gate or controls, grey is the existing application.
Arrows follow one rule: a clear direction, a visible arrowhead, a short verb label where the meaning is not
obvious, and no crossing lines.

| # | Diagram | Source | PNG | SVG | LinkedIn (light / dark) |
|---|---|---|---|---|---|
| 01 | The Ledger layer creates the evidence. Audit gives it meaning. | [drawio](01-ledger-layer-architecture.drawio) | [png](exports/01-ledger-layer-architecture.png) | [svg](exports/01-ledger-layer-architecture.svg) | [light](exports/01-ledger-layer-architecture-linkedin-1200x627.png) / [dark](exports/01-ledger-layer-architecture-linkedin-dark-1200x627.png) |
| 02 | One change: drafted, signed by its builder, then audited | [drawio](02-change-lifecycle.drawio) | [png](exports/02-change-lifecycle.png) | [svg](exports/02-change-lifecycle.svg) | [light](exports/02-change-lifecycle-linkedin-1200x627.png) / [dark](exports/02-change-lifecycle-linkedin-dark-1200x627.png) |
| 03 | Independent audit sits outside the teams that build | [drawio](03-three-lines-for-software.drawio) | [png](exports/03-three-lines-for-software.png) | [svg](exports/03-three-lines-for-software.svg) | |
| 04 | Every build role has an audit role beside it | [drawio](04-roles-rotation.drawio) | [png](exports/04-roles-rotation.png) | [svg](exports/04-roles-rotation.svg) | [light](exports/04-roles-rotation-linkedin-1200x627.png) / [dark](exports/04-roles-rotation-linkedin-dark-1200x627.png) |
| 05 | One record: what was decided, who signed it, who checked it | [drawio](05-adr-anatomy.drawio) | [png](exports/05-adr-anatomy.png) | [svg](exports/05-adr-anatomy.svg) | |
| 06 | Independence grows with risk: one pattern, three sizes | [drawio](06-three-sizes.drawio) | [png](exports/06-three-sizes.png) | [svg](exports/06-three-sizes.svg) | |
| 07 | Transition now, transformation later | [drawio](07-transition-roadmap.drawio) | [png](exports/07-transition-roadmap.png) | [svg](exports/07-transition-roadmap.svg) | [light](exports/07-transition-roadmap-linkedin-1200x627.png) / [dark](exports/07-transition-roadmap-linkedin-dark-1200x627.png) |
| 08a | Classic MVC: three layers, none of them remembers why (before) | [drawio](08a-mvc-classic.drawio) | [png](exports/08a-mvc-classic.png) | [svg](exports/08a-mvc-classic.svg) | [light](exports/08a-mvc-classic-linkedin-1200x627.png) / [dark](exports/08a-mvc-classic-linkedin-dark-1200x627.png) |
| 08b | MVC + the Ledger layer: the same app, now with evidence (after) | [drawio](08b-mvc-with-ledger-layer.drawio) | [png](exports/08b-mvc-with-ledger-layer.png) | [svg](exports/08b-mvc-with-ledger-layer.svg) | [light](exports/08b-mvc-with-ledger-layer-linkedin-1200x627.png) / [dark](exports/08b-mvc-with-ledger-layer-linkedin-dark-1200x627.png) |
| 09a | Classic MVVM: data binding, and still no memory of why (before) | [drawio](09a-mvvm-classic.drawio) | [png](exports/09a-mvvm-classic.png) | [svg](exports/09a-mvvm-classic.svg) | |
| 09b | MVVM + the Ledger layer: the layer does not care which pattern (after) | [drawio](09b-mvvm-with-ledger-layer.drawio) | [png](exports/09b-mvvm-with-ledger-layer.png) | [svg](exports/09b-mvvm-with-ledger-layer.svg) | |
| 10 | End to end: from a user's request to a trusted change | [drawio](10-end-to-end.drawio) | [png](exports/10-end-to-end.png) | [svg](exports/10-end-to-end.svg) | [light](exports/10-end-to-end-linkedin-1200x627.png) / [dark](exports/10-end-to-end-linkedin-dark-1200x627.png) |
| 11 | What this means for jobs (the author's view) | [drawio](11-jobs.drawio) | [png](exports/11-jobs.png) | [svg](exports/11-jobs.svg) | [light](exports/11-jobs-linkedin-1200x627.png) / [dark](exports/11-jobs-linkedin-dark-1200x627.png) |
| 12 | One change, in sequence: who calls whom, and when the gate decides | [drawio](12-change-sequence.drawio) | [png](exports/12-change-sequence.png) | [svg](exports/12-change-sequence.svg) | |

Notes:

- **Before and after.** 08a and 08b use the same positions and arrows for User, View, Controller and Model; 08b only
  adds the Ledger layer (purple), the record and the levels above. 09a and 09b do the same for MVVM, to show the layer
  does not depend on the pattern.
- **03** is a software mapping of the IIA Three Lines Model (2020): delegation flows down to management, and internal
  and external audit report up to the governing body. **06** uses the IV&V terms technical, managerial and financial
  independence.
- **12** is a UML-style sequence diagram for engineers; SPEC.md Appendix A has the same diagram in Mermaid.
- **11** is the author's view of the next 10-20 years, not a forecast from data. Its bar lengths are an illustration.
- The `.drawio` files are the light versions. The exports were rendered from the same layout, so they match. If you
  open a `.drawio` file in draw.io and re-export, small text spacing differences are normal.
