---
name: requirements-08-validation
description: >
  Use at gate G3, after elicitation, to judge the draft against the
  validation checklist and ISO/IEC/IEEE 29148. Use on every loop. Source
  gaps and contradictions return to intake. Wording and structure defects
  return to the skill that owns them. This skill does not invent a repair.
---

# 08 — Validation

## Purpose

Decide whether the elicited requirements are fit to baseline. Validation compares the draft to the source and to the checklist. It is not an editing pass that quietly improves sentences. A repair that adds a fact the source does not contain is a failed validation, even if the sentence reads better.

The characteristics applied here are the individual and set characteristics in ISO/IEC/IEEE 29148:2018 clause 5.2: necessary, implementation-free, unambiguous, consistent, complete, singular, feasible, traceable, and verifiable.

## Inputs

- Working products from skills 01–07.
- `source/`, opened beside any shall you challenge.
- `checklist.md` in this directory. Every row is in scope.
- `shared/schemas/requirement.schema.json`.
- The current validation cycle number, starting at 1, maximum 3 (`config.yaml`).

## Method

1. Validate every object in the functional and non-functional JSON against `requirement.schema.json`. Record schema errors as CHK-27. Do not hand-fix meaning while you fix a comma. If the fix would change a statement, it is not minor.
2. Walk every requirement with CHK-01 through CHK-14. For each shall, keep the source quotation next to the statement. If you cannot find the quotation, the result is fail, severity blocker, and the requirement returns to `draft` or is marked `rejected` with rationale "unsupported by source". Do not rewrite it into a weaker shall that you could support.
3. Walk the set: coverage of needs (CHK-15), contradictions (CHK-16), priority (CHK-17), and the verb law (CHK-18).
   Contradiction procedure: quote both sides and the source spans. If one side has no source, reject that side. If both sides have source, both requirements return to `draft`, a blocking open question is raised, and you do not propose the compromise. A compromise is a third invention.
4. Walk acceptance criteria (CHK-19–CHK-22), the nine quality rows (CHK-23–CHK-26), and scenarios, interfaces, data, glossary, and identifiers (CHK-27–CHK-32).
5. Confirm every unknown sits in an open question (CHK-33) and that blocking flags are honest (CHK-34). A question is blocking when a requested shall is still ambiguous. Marking it non-blocking so G5 can proceed is a defect.
6. Assign each fail a return path.
   - Blocker → skill 01, after the bad statements are drafted or rejected. The orchestrator will not run skill 09.
   - Major → skill 04, 05, 06, or 07, whichever owns the object. Name it.
   - Minor → correct it in the owning file without changing statements, priorities, or numbers. Re-read the statement after the edit.
7. If this cycle is the third and any blocker or major remains, CHK-35 fails the gate. Copy the open defects into `open-questions.md`. Stop. Do not produce a "best effort" SRS.
8. A pass is every row `pass` or `na`, with evidence, and zero requirements left in `draft` that you intend to baseline. Drafts that exist only because a blocking question is open are allowed to remain drafts, and G3 can pass only if those drafts are excluded from the proposed set and the question is recorded. G5 still will not be ready while a blocking question is open. Say that in the gate notes so skill 10 does not miss it.
9. Write `working/gate-G3.json` with `pass` or `fail` and the cycle number.

## Output format

Markdown `working/08-validation.md`: cycle number, then the checklist table (id, result, severity, evidence, return path), then the list of statements withdrawn or returned to draft.

JSON `working/08-validation.json`:

```json
{
  "cycle": 1,
  "items": [
    {
      "id": "CHK-01",
      "result": "pass",
      "severity": null,
      "evidence": "Each requirement citation was matched to a source heading.",
      "returnTo": null
    }
  ],
  "withdrawnRequirementIds": [],
  "draftRequirementIds": [],
  "newOpenQuestionIds": []
}
```

`result` is `pass`, `fail`, or `na`. Do not omit a checklist id.

## Quality checklist

- All 35 checklist ids appear once.
- Every fail has severity and a return path.
- No statement was rewritten to include a new fact during this skill.
- Contradictions do not have a chosen winner.
- Cycle number matches the orchestrator's count.
- Gate file agrees with the checklist. A single unresolved fail means `gate-G3.json` is `fail`.

## Gate

**Requirements G3: Requirements Validated.**

Pass authorizes skill 09. Fail loops as the orchestrator describes: blockers to G1, majors to the owning G2 skill, and a third failure stops the engagement without a baseline. This skill does not assemble the SRS.
