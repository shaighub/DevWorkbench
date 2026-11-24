---
name: requirements-use-cases-stories
description: >
  Use during gate G2, after functional requirements exist, to group them
  into use cases and user stories for readers. Use again when validation
  finds a scenario step or a story that adds behavior the shall statements
  do not already state.
---

# 05 — Use cases and stories

## Purpose

Give design and test a narrative index over the functional requirements. A use case shows the order and the actors. A user story gives a single actor's reason. Neither one is a requirement. The shall statements from skill 04 remain the baseline. If a story is easier to say than the shall, the shall still wins.

This skill is forbidden to discover scope. If a step feels missing, the missing piece is either already an FR, or it goes back to skill 04 with a source citation, or it is an open question. It is never a new sentence that only the scenario contains.

## Inputs

- `working/04-functional-reqs.json` and the G1 scope and stakeholder register.
- Open questions and exclusions.
- The glossary, so scenario language uses the same status words.

## Method

1. Group proposed functional requirements into user-goal use cases (`UC-###`). One primary actor, taken from the stakeholder register. A goal is something that actor would stop after, such as "submit an application" or "look up a plate". Do not create a use case per field.
2. Write the main success scenario as ordered steps. Every step carries one or more requirement ids that already state that step. If you cannot name an id, delete the step. You may not write the step and leave the id for later.
3. Preconditions and triggers are sourced conditions (authenticated with the one-time link, application is Submitted). If the source did not state an order, do not invent a stricter order in the scenario than the shalls allow.
4. Extensions are the negative acceptance criteria: refusal, threshold missed, external party does not report success. Each extension cites requirement ids. An extension is not a new failure mode the sponsor did not describe. "Network partition" is not an extension unless a shall already states the product's reaction.
5. Level is `user-goal` for these cases. Use `summary` only to point at several user-goal cases without adding steps. Use `subfunction` only to share a sourced step that several goals invoke (for example the same issuance rule). A subfunction still cites FRs and adds no behavior.
6. Write user stories (`US-###`) where they help a reader. Form: As a `<role from the register>`, I want `<a restatement of one or more FRs>`, so that `<the need, not a new obligation>`. The "so that" may carry motivation from the need statement. It may not introduce a limit, a date, or a role the FRs lack.
7. Apply INVEST as a smell, not as a license to rewrite scope. Independent and small are about the story's size. Negotiable does not mean the shall is negotiable in this skill. Testable means the story points at Gherkin that already exists. If a story fails INVEST because the underlying rule is large, split the story, not the rule, unless skill 04's own singular rule was already violated. In that case return to skill 04.
8. Write the use-case and story ids back onto the functional requirements' `useCaseIds` and `userStoryIds`. Do not change `statement`.
9. Search the scenarios for topics in the open-question register and the Won't list. A hit is a defect.

## Output format

Markdown `working/05-use-cases-stories.md`: each use case with actor, preconditions, trigger, numbered steps, extensions, and requirement ids; then the stories.

JSON `working/05-use-cases-stories.json`:

```json
{
  "useCases": [],
  "userStories": []
}
```

Objects match `#/$defs/useCase` and `#/$defs/userStory` in `shared/schemas/srs.schema.json`. Every `requirementIds` entry exists in skill 04's output. Story text is not copied into `srs.json` requirements. The assembler links ids only.

## Quality checklist

- Every step and every extension has a requirement id that exists.
- No step's wording obliges something the cited shall does not.
- Primary actors are stakeholder ids.
- Stories use "I want" for behavior that an FR already states.
- No story is the only place a rule appears.
- Functional `statement` strings are unchanged.
- Won't topics and open questions do not appear as steps.

## Gate

**Requirements G2: Requirements Elicited.**

Scenarios are part of the G2 package. They are not a substitute for skill 04, and G2 fails if this skill added scope.
