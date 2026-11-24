---
name: requirements-03-scope-context
description: >
  Use during gate G1, after stakeholders exist, to fix in-scope and
  out-of-scope items, the context of named external parties, constraints,
  dependencies, assumptions, and glossary seeds. Use again when intake
  changes scope or a term a shall would depend on.
---

# 03 — Scope and context

## Purpose

Draw the line the rest of the specification is not allowed to cross. In-scope items are the only topics skills 04–07 may specify. Out-of-scope items are MoSCoW Won't. Silence is not scope: a topic nobody mentioned is not written as a requirement and is not written as a feature "to be safe".

This skill also fixes the words later shall statements will use, and it separates constraints and dependencies from product obligations.

## Inputs

- Intake and stakeholder working products.
- `source/`.
- `shared/templates/glossary.md` for the shape of a glossary entry.
- The open-question register.

## Method

1. Write in-scope items (`SC-IN-##`) only from the sponsor's inclusions. One item is one topic a later skill might otherwise split or merge unfairly ("renewal inside the stated window" is one item; do not add "account management" beside it). Cite each item.
2. Write out-of-scope items (`SC-OUT-##`) only from explicit exclusions and postponements. `priority` is `Won't`. The rationale quotes the sponsor. "Not decided, leave it out until I say" is Won't for this baseline, not a placeholder requirement.
3. Apply the boundary rule in one sentence at the top of the scope section: anything not in the in-scope list and not in the out-of-scope list is unspecified, and unspecified means "no requirement", not "design may choose". If a later skill is tempted by a specific unspoken topic, add an open question then. Do not pre-list every product you can imagine.
4. Context. List actors (stakeholder ids) and external parties the source names. For each external party, one line: what the source says moves between them and the product. This is a context list, not an interface specification. Do not add a maps provider, an address-cleansing API, or an identity product that was not named. Skill 07 will specify interfaces only for parties that survive this list.
5. Constraints (`CON-###`) are conditions the source imposes on any solution: a mandated party, a prohibition ("do not store the card number", "do not invent the wire format"), a standard the sponsor said applies. Cite them. A constraint is not a shall about a screen. It is input to skills 04, 06, and 07.
6. Dependencies (`DEP-###`) are duties of an external party the product relies on ("CityPay reports a reference and an amount"). Cite them. Do not turn a dependency into a requirement that the external party will change. If the product must react to the dependency, that reaction is a later shall only when the source described the reaction.
7. Assumptions (`ASM-###`) are rare. Prefer an open question. Use an assumption only when the source contains two defensible readings, the sponsor cannot be asked in this cycle, and a draft must show which reading it uses. The assumption states the reading, the ids it affects, and `ifFalse`: those ids return to intake and are rewritten. Do not use an assumption to supply a missing number.
8. Glossary seeds. For every term a shall would need (status names, "current fee", "proof-of-address file", zone identifiers), write a definition built only from the source. If the source uses a term and does not pin it down, do not define it from the dictionary. Raise an open question and do not use the term in a shall.
9. G1 check. Confirm intake's exit, the stakeholder register, this scope file, and the glossary seeds. Confirm that no `FR-` or `NFR-` identifier exists anywhere in the engagement. Write `working/gate-G1.json`. On failure, name the missing piece and stop.

## Output format

Markdown `working/03-scope-context.md` with sections: Boundary rule, Context, In scope, Out of scope, Constraints, Dependencies, Assumptions, Glossary seeds.

JSON `working/03-scope-context.json` matches `#/$defs/scope` plus:

```json
{
  "scope": {},
  "context": [
    {"actorOrParty": "CityPay", "sourceSays": "Hosts the card page and reports a reference and an amount.", "citation": "BRD §6.6"}
  ],
  "glossary": []
}
```

Glossary entries match `#/$defs/glossaryEntry`. Scope objects match the schema, including `Won't` on every exclusion.

## Quality checklist

- Every in-scope and out-of-scope row has a citation.
- No exclusion was added merely because the source was silent.
- Every external party on the context list is named in the source.
- Constraints and dependencies are not written as shall statements.
- Assumptions, if any, have `ifFalse` and affected ids. Zero assumptions is a valid result.
- Glossary definitions do not introduce new rules. If a sentence obliges the product, it does not belong in the glossary.
- G1 is fail while any requirement identifier exists.
- Open questions from the source's "left open" list are present and unanswered.

## Gate

**Requirements G1: Intake and Scope.**

Passing G1 authorizes elicitation. It does not authorize design. Skill 04 is the next skill, and only after `gate-G1.json` says `pass`.
