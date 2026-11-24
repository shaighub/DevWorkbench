---
name: requirements-srs-assembly
description: >
  Use at gate G5, after traceability is frozen and no blocking question is
  open, to assemble the IEEE 29148 SRS in Markdown and JSON. Sets status to
  proposed and stops for a human. Does not mark the specification approved
  or handed off.
---

# 10 — SRS assembly

## Purpose

Publish one package that a person can read and a later agent can validate. The Markdown follows ISO/IEC/IEEE 29148:2018 clause 9.6. The JSON validates against `shared/schemas/srs.schema.json`. The shall strings in the two files are identical. Design, build, and test are named as consumers and are given the limits from `docs/agent-handoff.md`.

You assemble. You do not elicit, repair, or approve. If a required input is missing, stop and name the earlier skill. Do not reconstruct it from memory.

## Inputs

- Passing `working/gate-G3.json` and `working/gate-G4.json`, with `idFreeze` true.
- Working products 01–07 and `rtm.csv`.
- `open-questions.md` as accumulated so far.
- `shared/templates/srs-ieee29148.md`, `shared/templates/glossary.md`, and both schemas.
- Confirmation that every open question with `blocking` true has status `answered` or is no longer open. If any blocking question is still `open`, do not mark G5 ready.

## Method

1. Refuse the gate when G3 or G4 did not pass, when identifiers are not frozen, or when a blocking question is open. Write a short gap note instead of an SRS and stop.
2. Map working products into the template outline. Do not add sections that change the clause 9.6 order.
   - 1.1 Purpose: who uses the SRS (sponsor, design, build, test) and the decision it supports (approve a baseline). No shalls.
   - 1.2 Scope: the in-scope summary and the boundary rule from skill 03.
   - 1.3.1 Product perspective: the context list. No new parties.
   - 1.3.2 Product functions: one line per user goal, each pointing at requirement ids.
   - 1.3.3 User characteristics: the register, with judgments labeled.
   - 1.3.4 Limitations: exclusions, constraints, dependencies, assumptions, and the open-question ids.
   - 1.4 and `glossary.md`: the same entries as the glossary seeds, no new definitions.
   - 2 References: the source path, the standards, and the policies the sponsor cited.
   - 3.1 Interfaces from skill 07, including representation deferrals.
   - 3.2 Functions: functional shalls, grouped by use case. Under each shall, its Gherkin. The statement line is copied, not edited.
   - 3.3 Interaction-capability NFRs (2011 alias: usability).
   - 3.4 Performance-efficiency NFRs.
   - 3.5 Logical entities from skill 07.
   - 3.6 Constraints.
   - 3.7 The other quality rows and their NFRs: reliability, security, compatibility, flexibility, maintainability, safety. Include the coverage table so a not-stated or not-applicable characteristic is visible.
   - 3.8 and section 4: verification method per requirement, and the pointer to `rtm.csv`. Section 4 does not contain test results.
   - Section 5: needs, open questions, the matrix pointer, and the approval block.
3. Build `srs.json` from the same objects. Do not retype statements. Load them from the working JSON. `meta.status` is `proposed`. `meta.preparedBy` is `requirements-agent`. `meta.idPolicy` states that G4 froze identifiers and that withdrawn ids are not reused. `approval.status` is `proposed`. `approval.humanApproval.recorded` is false. `approval.residualRiskAccepted` is false unless a human record in the inputs already set it, which this agent does not fabricate. `approval.consumers` is `design`, `build`, and `test`.
4. Copy gate results into `approval.gates`. G1–G4 are `pass`. G5 is `ready` only when this method's checks pass. `ready` means "a human may approve". It does not mean approved.
5. Write `open-questions.md` from the JSON open questions so a sponsor can answer without reading the SRS. Each entry includes the question, why it matters, blocking, the decision that must not be invented, who can answer, status, and citations. State in the header that an unanswered question is not a decision, including questions the team is tempted to treat as obvious.
6. Diff checks before you call the package ready:
   - Every requirement `statement`, `priority`, and `id` in `srs.json` appears the same way in `srs.md`.
   - `srs.json` validates against `srs.schema.json`, which pulls in `requirement.schema.json`.
   - Criterion ids match their parent requirement.
   - RTM statements match JSON statements, and design and test cells are empty.
   - Glossary Markdown and JSON terms are the same set.
   - Open-question ids in Markdown and JSON are the same set.
   - No requirement in the proposed set has status `draft`.
7. On any failed diff, fix only mechanical assembly errors (a section skipped, a copy missed). If the fix needs a wording change, return to the owning skill. Do not "clean up" a shall at assembly time.
8. Stop. Do not set `approved` or `handed-off`. Do not write a design note, a schema, or example code. The human step, which you describe in section 5 and do not perform, is: a named person sets `approval.humanApproval.recorded` to true, names themselves, and only then may set status to `approved` or `handed-off`.

## Output format

At the engagement root:

- `srs.md` following the template, with blockquote guidance removed.
- `srs.json` validating against `shared/schemas/srs.schema.json`.
- `glossary.md` following `shared/templates/glossary.md`, guidance removed.
- `open-questions.md` as the sponsor-facing register.
- `rtm.csv` already produced by skill 09, unchanged except if a mechanical quote fix was required. Statements do not change.

`working/10-srs-assembly.md` records the diff checks and the G5 result. It is not a second SRS.

## Quality checklist

- Outline matches the template's clause 9.6 headings.
- JSON validates. Markdown shall text matches JSON.
- Status is `proposed`. Human approval is unrecorded. Residual risk is not marked accepted by the agent.
- G5 is `ready` or the package was not presented as ready.
- Blocking open questions are empty when G5 is `ready`.
- Consumers are named and the "must not invent" lines from the open questions are in the package.
- No design, build, or test artifact was added.

## Gate

**Requirements G5: SRS Approved and Handed Off.**

The agent's exit is a proposed package and a `ready` gate, or a gap note and a stop. Human approval is outside the agent. Downstream phases start only after that approval, as `docs/agent-handoff.md` requires.
