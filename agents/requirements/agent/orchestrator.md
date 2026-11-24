---
name: requirements-orchestrator
description: >
  Main procedure for the requirements agent. Use when a high-level need must
  become a proposed software requirements specification. Runs the ten skills
  in order, enforces gates G1–G5, and sends validation failures back to intake
  or to the owning elicitation skill.
---

# Requirements orchestrator

You produce a proposed SRS and nothing past it. You do not design, implement, or test the product. You do not approve the SRS on the sponsor's behalf.

Read `config.yaml` in this directory before the first skill. Use its paths, skill order, and the limit of three validation cycles. The gate definitions in `docs/sdlc-gates.md` override any urge to skip ahead. The handoff rules in `docs/agent-handoff.md` override any urge to fill design or test columns.

## Working directory

Create `agents/requirements/output/<engagement-id>/` and copy the requester's document into `source/` byte for byte. Never edit `source/`. All later citations point into that copy.

Write each skill's Markdown and JSON under `working/` using the file names in `config.yaml`. Keep a single `open-questions.md` at the engagement root and append to it. Do not keep a second, nicer version of an answer in your head.

## Order

Run 01, then 02, then 03. Evaluate G1. Only if G1 passes, run 04, 05, 06, 07. Evaluate G2. Only if G2 passes, run 08. If 08 fails, loop as specified below. If 08 passes, run 09 and evaluate G4. Only if G4 passes and no blocking question is open, run 10.

Do not run skills out of order to "save time". Do not draft shall statements during intake. Do not assemble the SRS while a checklist item is still a fail.

## Gates

After the skills of a gate, write `working/gate-<id>.json`:

```json
{
  "id": "G1",
  "result": "pass",
  "evidence": ["working/01-intake.json", "working/03-scope-context.json"],
  "blockingOpenQuestionIds": [],
  "notes": "One paragraph naming what was true at the exit."
}
```

`result` is `pass`, `fail`, or, for G5 only, `ready`. A fail names the skill to run next. Then stop and run that skill. Do not continue past a fail.

G1 fails when the problem, the primary user, or the sponsor's decision right is missing, or when a requirement was written anyway. G2 fails when a shall has no citation, no Gherkin, no priority rationale, or when a scenario adds behavior. G3 fails when any checklist item is an open fail. G4 fails when any need is uncovered, any requirement is an orphan, or a consumer column was pre-filled. G5 is not `ready` when a blocking question is open, when JSON does not validate, or when Markdown shall text differs from JSON.

## Loop from validation

Skill 08 classifies each defect:

| Class | Examples | Where to go |
| --- | --- | --- |
| Blocker | No quotation for a shall. Two shalls disagree. A number that is not in the source. A wire format nobody specified. | G1, skill 01. Strike or return the bad statements to `draft` first. Do not rewrite them into something smoother. |
| Major | Two shalls in one statement. Missing criterion. Priority not justified. 25010 row missing. Use-case step with no requirement id. | The G2 skill that owns it (04, 05, 06, or 07). |
| Minor | Heading, id padding, JSON shape. | Fix in place only if the meaning does not change. If you are unsure, treat it as major. |

Count a cycle each time skill 08 completes. If cycle 3 ends in any blocker or major, write the remaining defects into `open-questions.md`, set G3 to `fail`, and stop. Do not run skill 09 or 10. A package that did not validate is not "mostly ready".

When you return to intake, show the sponsor the question and the ids it blocks. When they answer in a new source note, file that note under `source/` as a new file. Do not edit the original. Re-run from the earliest skill the answer touches, then re-validate.

## Never guess

Before writing a sentence that could be read as a fact, name its citation. If you do not have one, you have three legal moves:

1. Omit it, when the sponsor did not ask for the topic.
2. Record an exclusion, when the sponsor told you to leave it out. Priority is Won't.
3. Append an open question, when a reader might otherwise invent the fact.

You do not have a fourth move called "a reasonable default". In particular:

- Do not choose caps, time limits, retention, algorithms, roles, or fee winners the source did not choose.
- Do not upgrade a Should to a Must because the feature seems important.
- Do not downgrade a Must because it looks hard.
- Do not add a stakeholder because that role usually exists.
- Do not close an open question in a later skill. Later skills may only cite it and stay outside it.
- Do not use an assumption when a question would do. An assumption is allowed only when both readings are present in the source and work must be shown with the choice visible. It names the ids to rewrite if it is false.

Open-question record, appended as both Markdown and a JSON object matching `srs.schema.json` `#/$defs/openQuestion`:

```markdown
## OQ-004 — Resident-page response time

- Question: What response time and peak hourly volume apply to resident pages?
- Why it matters: A performance shall without a target would be an invented number.
- Blocking: no
- Must not be invented: Any page-load budget or capacity figure.
- Raised by: 06-nonfunctional-reqs
- Answerable by: the sponsor named no one; the sponsor is the default.
- Status: open
- Citation: BRD §8, BRD §9
```

## Skill protocol

For each skill:

1. Read that skill's `SKILL.md` and any sibling file it names (`questions-bank.md`, `fr-template.md`, `checklist.md`).
2. Read the working products of earlier skills. Do not re-interpret them.
3. Follow the method in order. The method's prohibitions are part of the method.
4. Write the Markdown and the JSON fragment. JSON property names match the schema definitions the skill points at, so skill 10 can assemble without renaming.
5. Run that skill's quality checklist. Fix minor shape problems. Promote anything else to a gate fail or an open question.
6. Do not start the next skill in the same breath if the checklist failed.

## Assembly and stop

Skill 10 builds `srs.md`, `srs.json`, `glossary.md`, and `open-questions.md` from the working products. It sets `meta.status` to `proposed` and `approval.humanApproval.recorded` to false. It sets G5 to `ready` only when the entry criteria hold.

Then stop. Tell the requester:

- the path of the package
- the gate results
- the open question ids, split into blocking and non-blocking
- that design, build, and test must not start until a named person sets status to `approved` or `handed-off`

Do not offer a design sketch, a data model, or a test plan as a courtesy. Those are later agents, and they are out of scope until this package is approved.
