# The Ledger layer and audit layer: specification

**Version 0.1 (draft).** This is a proposal. It is not a standard issued by any body.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be read as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## 1. Terms

- **Change:** a set of modifications to files in a repository, proposed for merge.
- **Record:** a text document that explains a change and carries its evidence (section 2).
- **Builder:** the named person responsible for a change. Builders use whatever tools they like.
- **Auditor:** a named person, other than the builder, who checks the record against the work.
- **Ledger:** the tooling that drafts records. The word means a record of decisions. It does not mean a blockchain.
- **Gate:** the automated check that decides whether a change may merge.
- **Reversibility:** how hard a change is to undo: *easy*, *hard*, or *cannot be undone*.

## 2. The record

2.1 A record MUST be a text file stored in the same repository as the code it covers.

2.2 A record MUST have a unique identifier, MUST list the files it covers, and MUST carry a **change
hash** computed over the content of those files.

2.3 A record MUST contain the context, the decision, the alternatives considered, and the consequences.

2.4 A record SHOULD link the specification or story the change belongs to, and SHOULD state the
reversibility of the change.

2.5 Once an audit has passed, the decision content of a record MUST NOT be changed. A later decision
SHOULD supersede it by a new record that links to it. Implementations MAY enforce this with repository
rules such as code owners.

## 3. The Ledger

3.1 The Ledger SHOULD draft a record for every change that needs one.

3.2 A drafted record MUST state how it was drafted (for example, the name of the template or provider).

3.3 The Ledger MUST NOT attest or audit a record. Those are human acts.

3.4 The Ledger MAY use any drafting method, including a plain offline template. This specification does
not depend on any particular tool or model.

## 4. Attestation

4.1 A named builder MUST attest every record. By attesting, the builder takes ownership of its content.

4.2 The record MUST show whether the builder edited the drafted text. Implementations SHOULD compute this
and SHOULD NOT rely on the builder to report it.

4.3 Implementations SHOULD flag a record that was attested with zero edits to a drafted text, and MAY
treat it as a failure.

## 5. Audit

5.1 The auditor MUST be a different person from the builder. **Nobody audits their own work.**

5.2 The auditor MUST perform the **consistency** check: the change hash in the record matches the code.

5.3 The auditor MUST perform the **comprehension** check (explain-back) and the **behaviour** check
(independent stress and adversarial testing) at the depth the policy requires (section 7).

5.4 The audit result MUST be recorded in the record, with the auditor's identity, the date, the result of
each check and a short note for the comprehension and behaviour checks.

5.5 An organisation MAY sample explain-backs at low reversibility levels. It SHOULD NOT sample them for
changes that cannot be undone.

## 6. The gate

6.1 The gate MUST refuse a change when any file in it needs a record and any of the following is true:

- (a) no record covers the file;
- (b) the record has not been attested;
- (c) the audit has not passed;
- (d) the auditor is the builder;
- (e) a check that the policy requires for this change is missing;
- (f) the change hash in the record no longer matches the code.

6.2 The gate MUST evaluate required checks against the **current** policy, not the level the record
claims for itself.

6.3 The gate SHOULD be configured as a required status check, so that it cannot be skipped.

## 7. Policy

7.1 A policy MUST map paths to reversibility levels, and levels to the checks they require.

7.2 The policy file SHOULD itself be treated as a *hard* (or deeper) path, because changing it changes the rules.

7.3 A sensible default is: *easy* requires consistency; *hard* adds explain-back; *cannot be undone* adds
an independent stress test. Organisations MAY change this.

## 8. Independence

8.1 The audit function MUST NOT report to the person or team whose work it audits.

8.2 Tools used for audit SHOULD be independent of the tools used to build. Independence is a design
requirement; how to achieve it is left to implementers.

8.3 Independence SHOULD scale with risk. Small teams SHOULD have at least *technical* independence (an
auditor who did not build the work). Larger organisations SHOULD add *managerial* and *financial*
independence (a separate function, with its own budget). High-sensitivity work MAY add external auditors,
with the audit scope pinned to an exact version of the code.

## 9. Conformance

An implementation conforms to v0.1 if it satisfies every MUST in sections 2 to 7. Sections 8 and 9
describe organisational practice and are not machine-checkable. The reference implementation in this
repository is a demo and does not implement everything above (for example, it does not enforce 2.5).
