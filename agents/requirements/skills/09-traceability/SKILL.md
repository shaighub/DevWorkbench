---
name: requirements-traceability
description: >
  Use at gate G4, after validation has passed, to build the requirements
  traceability matrix, prove need and requirement coverage, and freeze
  identifiers. Use again when a link is broken after a validation loop.
---

# 09 — Traceability

## Purpose

Make every obligation reachable in both directions before anyone designs or tests it. Forward: each need is a requirement, an exclusion, or an open question. Backward: each requirement cites a need that exists, and each acceptance criterion cites its requirement. Sideways: use cases, stories, interfaces, and entities cite requirement ids that exist.

This skill freezes identifiers. After a pass, no skill renumbers or reuses an id. Design and test, when they exist, add their own columns. They do not add rows for new obligations.

## Inputs

- The validated working products from skills 01–07 and the passing `working/08-validation.json`.
- `shared/templates/rtm.csv` for the column order.
- `docs/agent-handoff.md` for who may write the design and test columns.

## Method

1. Build one RTM row per requirement in `proposed` status. Column order is exactly the template: Requirement ID, Type, Statement, Priority, Status, Source Need IDs, Citations, Stakeholder IDs, Use Case IDs, User Story IDs, Acceptance Criteria IDs, Verification Method, Quality Attribute, Design Element ID, Test Case ID.
2. Join multiple ids inside a cell with a single space. Do not introduce a second delimiter. Quote the statement so commas survive CSV.
3. Leave Design Element ID and Test Case ID empty. Empty means the consumer has not run. Do not write TBD, N/A, unknown, or a guessed component. A pre-filled design column fails G4.
4. Quality Attribute is empty for functional rows and the 25010 characteristic for non-functional rows.
5. Forward coverage. For each need, the row is covered when at least one proposed requirement lists it, or an exclusion's rationale cites it, or an open question cites it as the reason a shall was not written. Record uncovered need ids. Any uncovered need fails G4 and returns to skill 04 or skill 01, whichever failed to classify it.
6. Backward coverage. Every `source.needIds` entry exists in the needs file. A requirement with none, or with a dangling id, is an orphan. Orphans fail G4. Do not delete an orphan in this skill if it was validated; send it back. If validation already rejected it, keep it out of the proposed matrix and list the retired id in the traceability notes so it will not be reused.
7. Resolve every acceptance-criterion id, use-case id, and story id. A dangling id fails G4 and returns to the skill that wrote the link (04 or 05).
8. Confirm interfaces and entities refer only to requirement ids on the matrix. A dangling reference returns to skill 07.
9. Freeze. Set `idFreeze` true. Write the id policy into the traceability notes: identifiers on this matrix are immutable; withdrawn ids are not reused; the next cycle appends the next free number. Do not renumber to make the matrix pretty.
10. Write the coverage summary that skill 10 will copy into `srs.json` `traceability`: `needsWithoutCoverage`, `orphanRequirementIds`, `requirementsMissingAcceptanceCriteria`. All three are empty arrays on a pass.

## Output format

`rtm.csv` at the engagement root, header identical to `shared/templates/rtm.csv`.

Markdown `working/09-traceability.md`: counts, uncovered needs, orphans, dangling links, retired ids, and the freeze statement.

JSON `working/09-traceability.json` matches `#/$defs/traceability`:

```json
{
  "matrix": "rtm.csv",
  "idFreeze": true,
  "needsWithoutCoverage": [],
  "orphanRequirementIds": [],
  "requirementsMissingAcceptanceCriteria": [],
  "designColumn": "Blank until the design agent writes an element id. Requirements skills leave it empty.",
  "testColumn": "Blank until the test agent writes a case id. Requirements skills leave it empty."
}
```

## Quality checklist

- Row count equals the number of proposed requirements. Rejected and deferred ids are listed in the notes, not dropped silently and not reused.
- Header matches the template, including the two consumer columns.
- Those two columns are empty on every row.
- The three coverage arrays are empty.
- Every need id, stakeholder id, criterion id, use-case id, and story id on the matrix resolves.
- Statements in the CSV match the requirement `statement` strings exactly.
- `idFreeze` is true only when the checks above passed.

## Gate

**Requirements G4: Traceability Baselined.**

Write `working/gate-G4.json`. Pass authorizes skill 10. Fail does not freeze ids and does not assemble an SRS. A broken link is not repaired by deleting the row to force a pass.
