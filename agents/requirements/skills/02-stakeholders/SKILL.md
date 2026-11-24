---
name: requirements-02-stakeholders
description: >
  Use during gate G1, after intake has a cited problem and needs, to build
  the stakeholder register from people and roles the source names. Use again
  when a new source note names a new person or changes who decides.
---

# 02 — Stakeholders

## Purpose

Name every person and role the source gives you, what they do, what they care about that was actually said, and who may decide. Later skills may use only these ids as actors. A stakeholder added because a project "usually has one" is a defect.

## Inputs

- `working/01-intake.md` and `.json`, especially the people pile and the needs.
- `source/`, when you need the quotation rather than the intake paraphrase.
- Open questions already raised. Do not answer them here.

## Method

1. List candidates from the source only: people present, roles described, and roles named as future reviewers. Mark `interviewed` false for anyone the source says was absent.
2. Assign `STK-###` in the order they appear. Do not reserve numbers for roles you might add later.
3. For each stakeholder, record only sourced material in `concerns` and `decisionRights`.
   - A concern is something the source says that person or role is trying to protect or achieve. Cite it in the sentence.
   - Decision rights are powers the source grants ("accepts or rejects scope", "may reject an application"). If none is stated, write "None recorded." Do not promote a user into an approver.
4. Set `interest` and `influence` to `unknown` unless the source itself ranks them. You may set a value as an analyst judgment only when the source gives evidence (the sponsor "accepts or rejects scope" supports influence `high`). Set `interestIsJudgment` true whenever the value is yours. A judgment is not a requirement and must not be cited as one.
5. Absent reviewers keep `interest` and `influence` as `unknown`. Do not infer that a privacy officer has high influence because privacy officers often do.
6. Attach stakeholder ids to each need from intake. A need with no stakeholder returns to skill 01. Do not invent a stakeholder to hold the need.
7. If two sourced concerns conflict, write a blocking open question that quotes both. Do not average them into a compromise role.
8. Update the intake JSON so each need's `stakeholderIds` match this register. Do not change need statements in this skill.

## Output format

Markdown `working/02-stakeholders.md` with one section per stakeholder: id, name, role, interviewed, concerns, decision rights, interest, influence, and whether those ratings are judgments.

JSON `working/02-stakeholders.json`:

```json
{
  "stakeholders": [],
  "needLinks": [
    {"needId": "NEED-001", "stakeholderIds": ["STK-001"]}
  ]
}
```

Each stakeholder object matches `#/$defs/stakeholder` in `shared/schemas/srs.schema.json`.

## Quality checklist

- Every stakeholder has `namedInSource` true. If you cannot say where they are named, delete the row.
- Absent people have no fabricated quotations.
- Decision rights are quoted powers or "None recorded."
- Every need id from intake appears in `needLinks`.
- No `FR-` or `NFR-` ids were created.
- Interest and influence are `unknown` or labeled with `interestIsJudgment` true.
- Open questions are appended, not answered.

## Gate

**Requirements G1: Intake and Scope.**

This skill's exit: a register that later skills can use as the closed set of actors, with needs linked to stakeholders. G1 still fails if skill 03 has not finished scope.
