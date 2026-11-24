---
name: requirements-functional
description: >
  Use during gate G2, after G1 has passed, to write functional shall
  statements, MoSCoW priorities, and Gherkin acceptance criteria from
  sourced rules. Use again when validation returns a functional statement
  for wording, splitting, or a missing criterion.
---

# 04 — Functional requirements

## Purpose

Write the functional baseline: one testable shall per behavior the source already decided, traced to a need, prioritized with MoSCoW, and paired with Gherkin a later test phase can run. Functional requirements are what the product does. Quality measures belong to skill 06. Screens, schemas, and component names belong to nobody in this phase.

Use `fr-template.md` as the pattern for every requirement. A statement that does not fit the pattern is rewritten or deleted, not "close enough".

## Inputs

- Passed G1 package: intake, stakeholders, scope, glossary, open questions.
- `source/` for quotations. The intake paraphrase is not a substitute when you are about to write a shall.
- `fr-template.md`.
- `shared/schemas/requirement.schema.json`.

## Method

1. Build a coverage table from in-scope items and needs. For each row, decide one of: write one or more `FR-###`, point at an exclusion, or point at an open question. A row with none of the three is unfinished. Do not leave it for design.
2. Draft each shall in the form `The <product> shall <one observable obligation>`, plus the condition and the limit the source stated. Then edit:
   - Count the word shall. If it appears twice, split the requirement. Two refusals are two requirements. A list of attributes of one record (name, address, one plate) may stay in one shall when the source treats them as one completeness rule. Say that in the rationale.
   - Keep the subject as the product under specification. An external party's duty is a dependency from skill 03, not a shall, unless the shall is the product's reaction and the source described that reaction.
   - Copy numbers, lists, and boundaries exactly. "No larger than 10 megabytes" stays that. Do not write "about 10" and do not write "10 MiB" unless the source said so.
   - Do not use should, may, can, TBD, etc., and/or, including (as an open list), as appropriate, user-friendly, support, or fast. MoSCoW does not change the verb.
   - If a sentence would answer an open question or deliver a Won't item, delete the sentence.
3. Assign priority from the source's commitment language, and write `priorityRationale` with the citation. Must means the sponsor described the release as failing or the rule as the way the service works. Should means the sponsor allowed it to follow later. Could means they called it desirable and droppable. If you cannot point at that language, do not assign Must by default. Raise a question and leave the requirement unwritten or in `draft`.
4. Set `source.needIds` to at least one need. Set `citations` to the rule locations. Set `stakeholderIds` to the actors who touch the behavior. Set `policyIds` only for policies skill 03 recorded.
5. Write `rationale` as why this shall exists and which nearby decision you refused to include. The refusal points at an `OQ-###` or an `SC-OUT-##`.
6. Choose one verification method. Test when a run with fixtures can show the outcome. Demonstration when a person must walk the flow. Inspection when the evidence is a document or a static view. Analysis when the evidence is a calculation over a period the test will not literally sit through (skill 06 uses this more often). Do not write "test" for everything by habit.
7. Write at least one acceptance criterion. Gherkin has Given, When, and Then. Use the sponsor's examples when they exist. You may use a boundary fixture that is arithmetic on a sourced limit (14 characters against a minimum of 15, a file larger than 10 megabytes). Label business names that the sponsor did not utter as example fixtures inside Given, and do not let them become new rules. Add the refusal or the negative case when the shall is a refusal, a minimum, a maximum, or an "only when".
8. Set status to `proposed` only if steps 2–7 are done and the shall does not depend on an open question. Otherwise `draft`, and do not pretend G2 passed for that id.
9. Identifier rule: the next free `FR-###`. Never renumber to close a gap. If validation deletes a statement, that id is retired with status `rejected` and a rationale, not reused.
10. Read the open-question register and the Won't list once more against every shall. A match is a defect.

## Output format

Markdown `working/04-functional-reqs.md`: the coverage table, then one block per requirement using the headings in `fr-template.md`.

JSON `working/04-functional-reqs.json`:

```json
{
  "requirements": []
}
```

Each element validates against `shared/schemas/requirement.schema.json` with `type` `functional`. Do not set `qualityAttribute`. Acceptance-criterion ids are `AC-FR-###-##` for that requirement.

The shall string in Markdown is the same string as `statement` in JSON, character for character.

## Quality checklist

- Coverage table has no empty row.
- Each statement contains shall exactly once.
- Each statement has a need id, a citation, a priority rationale, a verification method, and at least one Gherkin criterion.
- No statement contains a value, role, or topic that is only in an open question or an exclusion.
- No statement names a storage engine, protocol, or screen layout.
- Criterion ids match the parent requirement id.
- Negative cases exist for refusals and thresholds.
- Status `proposed` is not used on a draft that still depends on an open question.

## Gate

**Requirements G2: Requirements Elicited**, with skills 05, 06, and 07.

This skill does not pass G2 alone. It does fail G2 if its own checklist fails.
