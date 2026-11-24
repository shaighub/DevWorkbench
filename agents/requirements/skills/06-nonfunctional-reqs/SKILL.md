---
name: requirements-06-nonfunctional-reqs
description: >
  Use during gate G2, after functional requirements exist, to write
  non-functional shall statements under ISO/IEC 25010:2023 and to record a
  coverage decision for every characteristic. Use again when validation
  finds a missing quality row, an invented target, or a mechanism written
  where an obligation was required.
---

# 06 — Non-functional requirements

## Purpose

Specify how well the product must perform the functions, using the sponsor's measures, under ISO/IEC 25010:2023. A non-functional requirement is still a shall. It has a scale (what is measured), a meter (how it is observed), and a target (the value the source stated). If any of the three is missing, there is no requirement. There is an open question, or an honest "not stated".

Do not clone functional requirements into this skill under a quality label. Functional suitability is carried by the FR set.

## Inputs

- G1 package, functional requirements, and open questions.
- Policies recorded as constraints, limited to the sentences the sponsor stated. Do not open a remembered copy of WCAG or a security standard and copy clauses they did not cite.
- The nine characteristics below. The 2011 names are aliases for readers who still use them. Do not emit both taxonomies.

| 2023 characteristic | 2011 alias | Typical subcharacteristics you may need |
| --- | --- | --- |
| functional-suitability | functional suitability | Covered by FRs. Do not duplicate. |
| performance-efficiency | performance efficiency | time-behaviour, resource-utilization, capacity |
| compatibility | compatibility | co-existence, interoperability |
| interaction-capability | usability | operability, inclusivity, learnability, user-error-protection, self-descriptiveness |
| reliability | reliability | availability, fault-tolerance, recoverability |
| security | security | confidentiality, integrity, non-repudiation, accountability, authenticity |
| maintainability | maintainability | modularity, reusability, analysability, modifiability, testability |
| flexibility | portability | adaptability, scalability, installability, replaceability |
| safety | (none; added in 2023) | operational-constraint, risk-identification, fail-safe, hazard-warning |

## Method

1. Create nine coverage rows, one per characteristic, before writing any NFR. You will fill disposition as you go. An empty disposition at the end is a G2 failure.
2. For each sourced quality obligation, draft an `NFR-###` in the same way as a functional shall: one shall, exact numbers, no answer to an open question.
   - Scale, meter, and target all come from the source. "The lookup is fast" does not have a target. Do not write "within 2 seconds" unless the source said 2 seconds.
   - Name `qualityAttribute` and `qualitySubcharacteristic` from the table. Pick the subcharacteristic that matches the measure. Availability is not time-behaviour. A browser matrix is flexibility/adaptability (2011: portability), not a second performance requirement.
   - Write Gherkin whose Then clause a tester or an analyst can judge. For a percentage over a month, the Then states the arithmetic (up minutes divided by minutes in the month, with the sourced exclusion for published maintenance). Verification is `analysis` when the month will not be executed as a click-through, and `test` when a controlled run can observe the target.
3. Confidentiality and accountability name who may see or who is recorded. They do not name algorithms, ciphers, or products the source did not name. "Encrypt with AES-256" is a design. "Only the uploading resident and a parking clerk may retrieve the file" is a requirement, if the source said that.
4. Authenticity is often already an FR (how a session starts). Point the coverage row at those FR ids. Do not write a second shall that repeats the sign-on rule in vaguer words.
5. Interoperability is often already the interface behavior. Point at those requirement ids. Skill 07 will name the parties. This skill does not invent the protocol.
6. Choose a disposition for each characteristic:
   - `covered` when one or more requirement ids state the sourced obligations. You may also list open questions for subcharacteristics the source left blank. Say so in the rationale.
   - `not-applicable` when the product cannot affect that characteristic and you can say why in terms of this product. Safety is not applicable when the software does not control equipment or a physical process. Say that. "N/A" alone is not a rationale. Do not mark security or confidentiality not applicable merely because the sponsor was brief.
   - `open-question` when a user-visible quality the sponsor touched is unquantified (they require the service to be up, but gave no restore time). The row's `openQuestionIds` must be non-empty. Do not also write a shall with a borrowed target.
   - `not-stated` when the sponsor said nothing and the characteristic is about construction quality you might otherwise pad (a maintainability index, a reuse quota). The rationale names the pad you refused to write. Not-stated is visible. It is not permission for design to invent a product shall. Design standards, if an organization has them, are not this SRS unless the sponsor cited them.
7. Priority follows the same MoSCoW rule as skill 04. A policy the sponsor said the release must meet is Must. Do not mark every NFR Must by reflex, and do not mark them all Should to look flexible.
8. Cross-check FRs. If an NFR contradicts an FR, do not reconcile it yourself. Blocking open question, both ids back to `draft`.

## Output format

Markdown `working/06-nonfunctional-reqs.md`: the nine-row coverage table, then one block per NFR in the same shape as `fr-template.md`, plus the quality attribute and subcharacteristic.

JSON `working/06-nonfunctional-reqs.json`:

```json
{
  "requirements": [],
  "qualityModelCoverage": []
}
```

Each requirement validates against `requirement.schema.json` with `type` `non-functional` and both quality fields set. Coverage objects match `#/$defs/qualityCoverage`. There are exactly nine, and the characteristics are the nine names above, each once.

## Quality checklist

- Nine coverage rows, no duplicates, no characteristic omitted.
- Every NFR has one shall, a target taken from the source, a subcharacteristic, Gherkin, a need id, and a citation.
- No cipher, framework, or cloud control appears unless the source named it.
- No NFR repeats an FR in weaker language. Overlap is allowed only when the NFR adds a quality obligation the FR does not state.
- `covered` rows have requirement ids. `open-question` rows have question ids. `not-applicable` and `not-stated` rationales say what was decided and what was refused.
- Functional requirements were not modified except to add links this skill is not expected to add. This skill does not change FR statements.

## Gate

**Requirements G2: Requirements Elicited.**

G2 fails if any of the nine characteristics has no row, or if a target in an NFR is not in the source.
