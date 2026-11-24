# Agent handoff

The requirements agent is the producer. Design, build, and test agents do not exist yet. This document is the contract they will be built against, so the requirements package does not have to be reshaped later.

Agents do not hand off by chatting. They hand off by files that validate against `shared/schemas/`. Narrative Markdown is for people. JSON and CSV are for the next agent. The two carry the same identifiers, the same priorities, and the same shall strings.

## Package

An engagement is a directory:

```text
agents/requirements/output/<engagement-id>/
  source/                         # untouched high-level request
  working/                        # one Markdown and one JSON fragment per skill
  srs.md                          # ISO/IEC/IEEE 29148:2018 clause 9.6
  srs.json                        # validates against shared/schemas/srs.schema.json
  rtm.csv                         # columns from shared/templates/rtm.csv
  glossary.md
  open-questions.md
```

`srs.json` is the normative machine copy of the baseline. `srs.md` is the same baseline for review. If they disagree, the package is not ready. Skill 10 refuses to mark G5 ready until they match and `srs.json` validates.

The worked example is `agents/requirements/examples/output-sample/`. It is a proposed package for the sample request, not a second schema.

## Who may write which fields

| Artifact | Requirements agent | Design (later) | Build (later) | Test (later) |
| --- | --- | --- | --- | --- |
| Shall statement, priority, need ids, acceptance criteria | Writes until G4, then freezes | Reads | Reads | Reads |
| Requirement `status` of approved, deferred, rejected | Writes only after a human decision | Does not change | Does not change | Does not change |
| `open-questions.md` and open-question objects | Writes. Does not answer from imagination | Does not close | Does not close | Does not close |
| Interface representation (protocol, payload, codes) | Writes only when the source mandated it. Otherwise records the deferral | Specifies inside the business data already listed | Implements that specification | Verifies it |
| Logical entities | Writes business attributes | May add a physical model in its own artifact, never inside `srs.json` | Implements | Uses as the oracle for data rules |
| RTM Design Element ID | Leaves blank | Fills | Reads | Reads |
| RTM Test Case ID | Leaves blank | Leaves blank | Leaves blank | Fills |
| New shall, new priority, new acceptance criterion | Only through a new requirements cycle | Forbidden | Forbidden | Forbidden |

Blank consumer cells are empty strings. They are not `TBD`, `N/A`, or a guessed component name.

## Identifier grammar

| Prefix | Thing | Frozen at |
| --- | --- | --- |
| NEED-### | Stakeholder need | G4 |
| STK-### | Stakeholder | G4 |
| FR-### | Functional requirement | G4 |
| NFR-### | Non-functional requirement | G4 |
| AC-FR-###-## or AC-NFR-###-## | Acceptance criterion of that requirement | G4 |
| UC-### | Use case | G4 |
| US-### | User story | G4 |
| IF-### | External interface | G4 |
| ENT-### | Logical data entity | G4 |
| OQ-### | Open question | Remains open until answered by the source and reprocessed by the requirements agent |
| SC-IN-## / SC-OUT-## | Scope in / scope out | G4 |
| CON-### / DEP-### / ASM-### | Constraint, dependency, assumption | G4 |
| POL-AAA-## | Policy the source cited | G4 |

Rules:

- Three digits, except scope items, which use two, and acceptance criteria, which append a two-digit suffix.
- An identifier is never reused, including after `deferred` or `rejected`.
- Downstream artifacts cite these ids. They do not invent parallel numbering for the same obligation.
- User stories are communication. The shall is the baselined obligation. A story that is not tied to a requirement id is not a requirement.

## Status and when a consumer may start

| `meta.status` | Meaning | May design, build, or test start? |
| --- | --- | --- |
| draft | Skills still running, or validation has not passed | No |
| proposed | G1–G4 passed, G5 is ready, a human has not approved | No |
| approved | A named human approved the baseline | Design may start. Build waits for design allocation |
| handed-off | Approved package published as the input to the next phase | Yes, under the rules in this document |

The requirements agent is allowed to set `draft` and `proposed`. It is not allowed to set `approved` or `handed-off`. That is a human record in `approval.humanApproval`: who approved, and that `recorded` is true. The sample package stays `proposed` on purpose, so a reader can see the agent's stopping point.

`accepted-residual` on an open question means a human accepted shipping without an answer. It is not an answer. Consumers still must not invent the missing decision. `residualRiskAccepted` may be set true only in the same human record.

## Open questions

Each open question states:

- the question, in a form the sponsor can answer
- why it matters
- whether it is blocking
- the decision that must not be invented while it is open
- who can answer it, as far as the source says
- the citation for the silence or the conflict

Blocking means a shall the sponsor already asked for cannot be made unambiguous. G2 does not finish elicitation of that shall, and G5 is not marked ready, while a blocking question is open.

Non-blocking means the written shalls do not depend on the answer. The temptation would have been to add a shall. The question records the refusal. Consumers treat the topic as undecided, not as permission to choose.

A consumer that "resolves" an open question inside a design note, a default constant, or a test fixture has broken the handoff. The fix is a new intake, a new or revised requirement, and a new baseline.

## What design, build, and test are promised

They can rely on, once status is `approved` or `handed-off`:

- Shall text, MoSCoW, verification method, and Gherkin for every requirement in `proposed` or `approved` status.
- Need-to-requirement-to-criterion links in `rtm.csv`.
- Interface business data, direction, and sourced error behavior.
- Logical entities and the glossary meanings of status words.
- The coverage row for each ISO/IEC 25010:2023 characteristic, including characteristics marked not applicable or not stated.
- The list of decisions they are not allowed to take (`openQuestions[].mustNotBeInvented`).

They cannot rely on:

- Working papers under `working/` as a second baseline. Those are audit trail. The package files win.
- Anything in an assumption, except as a risk. If the assumption is false, the named requirement ids return to the requirements agent.
- Empty design and test columns.
- A `proposed` sample, including `agents/requirements/examples/output-sample/`, as an approved city specification. The example exists to show shape and discipline.

## Change after baseline

A change to behavior is a new requirements cycle:

1. Intake the change against the frozen ids.
2. Add a new id, or create a new version of the SRS that marks the old id `deferred` or `rejected` and issues a new id for the replacement statement.
3. Re-run validation and traceability.
4. A human approves the new baseline.

Build does not "interpret the requirement more sensibly" in code. Test does not weaken a criterion because the run failed. Both send the conflict back as a defect or as a new intake.

## Standards, and where they show up in the files

| Standard | What the handoff uses it for |
| --- | --- |
| ISO/IEC/IEEE 29148:2018 | SRS section outline (clause 9.6). Requirement characteristics (clause 5.2): necessary, implementation-free, unambiguous, consistent, complete, singular, feasible, traceable, verifiable. Modal verb shall for binding product obligations. Verification methods: inspection, demonstration, test, analysis. |
| ISO/IEC 25010:2023 | The nine product-quality characteristics on non-functional requirements and in `qualityModelCoverage`. Names from 2011 (usability, portability) are recorded in the non-functional skill as aliases, not as a second taxonomy. |
| MoSCoW | `priority` on requirements and needs. Won't is an exclusion in `scope.outOfScope`, not a shall, except when a frozen requirement is later dropped and must keep its id. |
| Gherkin | `acceptanceCriteria[].gherkin` with Given, When, and Then. The test phase turns these into cases and writes the case id on the RTM. It does not replace them. |
