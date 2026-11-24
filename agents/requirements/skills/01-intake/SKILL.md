---
name: requirements-01-intake
description: >
  Use at the start of an engagement, when the requester has supplied a
  high-level need, BRD, ticket, or transcript. Use again when validation
  finds a missing fact, a contradiction, or a suspected invention and the
  work has looped back to gate G1.
---

# 01 — Intake

## Purpose

Turn an untouched source into a cited problem, a set of stakeholder needs, and a list of questions. Intake does not write requirements. A shall that appears here is a defect, even if it is obvious.

The output is the only vocabulary later skills may treat as sourced. If it is not in `source/` or in a later answer filed beside it, it is not a fact.

## Inputs

- The engagement directory and the preserved file under `source/`.
- `questions-bank.md` in this directory. Ask from the bank. Do not invent a parallel questionnaire.
- On a loop from skill 08: the defect list, the ids under challenge, and any new source note the sponsor supplied. Do not edit the original source file.

## Method

1. Give the engagement a stable id (`engagementId`) from the project name and the source date. Do not change it on later cycles.
2. Read the source once and mark spans you will cite. A citation is a section or paragraph the sponsor can find, such as `BRD §6.3`. A citation of "the BRD" with no location is not a citation.
3. Split the source into six piles. Every pile entry is a quotation or a close paraphrase followed by the citation. Drop anything you cannot place.
   - Problem and outcome.
   - People and who decides.
   - Rules, limits, lists, and numbers.
   - Policies the sponsor cited, limited to the sentences they actually stated.
   - Explicit exclusions.
   - Explicit unknowns, including "do not pick this for me".
4. Write the problem in one short paragraph the sponsor would recognize. Each sentence ends with its citation. Do not add causes, users, or a solution the paragraph did not contain.
5. Write needs (`NEED-###`) in stakeholder language. Use "needs" or "wants". Do not use shall. One need is one lack or desired outcome, not a screen. Give each need a MoSCoW value only when the source's commitment language supports it. "I will still open the service if this slips" is Should. A rule the sponsor stated as the way the service works is Must. If the commitment is unclear, set the need's status to `open` and raise a question instead of guessing Must.
6. Walk `questions-bank.md`. For each question, record one of three results:
   - Answered, with the citation and a one-line restatement.
   - Not applicable, with the reason tied to this source (not "usually N/A").
   - Unanswered. Append an open question. Do not draft the answer you expect.
7. Classify each open question.
   - Blocking when a behavior the sponsor already requested cannot be stated unambiguously without the answer.
   - Non-blocking when the safe action is to write no shall and to warn later skills away from the topic.
   Set `mustNotBeInvented` to the specific decision that is forbidden, not to the words "do not guess".
8. Set `answerableBy` from the source. If the sponsor said Legal has not answered and named no person, write that. Do not create a fictional counsel.
9. Stop rule. If pile "problem" is empty, or no user is named, G1 cannot pass. Write the questions and hand them back. Do not continue to skill 02 except to record the stakeholder as unknown if a name is missing. Do not sketch requirements "so the review has something to look at".

## Output format

Markdown `working/01-intake.md`:

```markdown
# Intake — <engagement id>

## Source
Path, date, and sponsor as stated.

## Problem
Cited sentences.

## Needs
### NEED-001
- Statement:
- Stakeholders: (names only; ids arrive in skill 02 and are written back here)
- Priority:
- Citations:
- Status: proposed | open

## Question bank results
| Id | Result | Citation or question id |

## Open questions raised here
(id, blocking, must not be invented)
```

JSON `working/01-intake.json` uses the `need` and `openQuestion` shapes from `shared/schemas/srs.schema.json`. Stakeholder ids may be omitted on the first pass and filled when skill 02 assigns `STK-###`. The fragment is an object:

```json
{
  "engagementId": "rpp-2026-03",
  "problem": "Cited paragraph.",
  "needs": [],
  "questionBank": [
    {"id": "QB-01", "result": "answered", "citation": "BRD §2", "note": "One line."}
  ],
  "openQuestions": []
}
```

Needs do not contain the word shall. Open questions that are still unknown have status `open`.

## Quality checklist

- The source file is unchanged.
- Every need has a citation and no shall.
- Every bank question has a result. Unanswered items have an `OQ-###`.
- No requirement id (`FR-` or `NFR-`) exists in the intake files.
- No number appears that is not in the source.
- Blocking flags are set, and each question names the decision that must not be invented.
- People who were not in the room are not given quotations.

## Gate

**Requirements G1: Intake and Scope**, together with skills 02 and 03.

Intake's own exit: a cited problem, cited needs, a completed question-bank table, and open questions for every unanswered bank item that matters to this source. Skill 03 cannot pass G1 if this exit is missing.
