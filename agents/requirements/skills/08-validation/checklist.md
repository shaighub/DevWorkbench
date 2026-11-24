# Validation checklist

Skill 08 applies every row. Result is `pass`, `fail`, or `na`. A fail records severity (`blocker`, `major`, `minor`), the ids involved, and the skill that must act. Evidence is a quotation, an identifier, or a schema error. "Looks fine" is not evidence.

`na` requires a reason tied to this package. Do not mark a row `na` to skip it.

## Source fidelity

| Id | Check | Fail when |
| --- | --- | --- |
| CHK-01 | Every shall traces to a quotation | Any `FR-` or `NFR-` whose citations do not locate text that supports the obligation |
| CHK-02 | No invented number, role, or list | A value in a statement or criterion is absent from the source and is not arithmetic on a sourced limit |
| CHK-03 | Open questions are not answered inside shalls | A statement decides a topic named in `mustNotBeInvented` |
| CHK-04 | Exclusions stay excluded | A shall delivers an `SC-OUT` item |
| CHK-05 | Needs are not shalls | A need statement contains shall |

## ISO/IEC/IEEE 29148 clause 5.2, each requirement

| Id | Characteristic | Fail when |
| --- | --- | --- |
| CHK-06 | Necessary | The shall has no need, or removing it would not change the sponsor's outcome and no cited rule requires it |
| CHK-07 | Implementation-free | The shall names a mechanism, layout, protocol, or product the source did not mandate |
| CHK-08 | Unambiguous | Two readers could apply different tests. Watch "support", "handle", "as appropriate", "including" used as an open list, "etc.", "and/or", "fast", "user-friendly" |
| CHK-09 | Singular | The word shall appears more than once, or two independent obligations share an id |
| CHK-10 | Verifiable | No acceptance criterion, or the Then clause is a feeling rather than an observation |
| CHK-11 | Traceable | Missing need id or citation |
| CHK-12 | Feasible | The shall contradicts a constraint in this package. Do not judge feasibility by how hard the build looks |
| CHK-13 | Complete, individual | A condition the source stated is missing, so the tester must invent the other case |
| CHK-14 | Consistent, individual | This shall disagrees with another shall, a glossary definition, or a sourced rule |

## The set

| Id | Check | Fail when |
| --- | --- | --- |
| CHK-15 | Set complete | An in-scope need has no requirement, no exclusion, and no open question |
| CHK-16 | Set consistent | Two requirements assign different outcomes to the same condition. Do not pick a winner |
| CHK-17 | Priority grounded | MoSCoW value has no `priorityRationale` citing the sponsor's commitment language |
| CHK-18 | Verb law | A statement uses should or may, or encodes a soft priority by weakening shall |

## Acceptance criteria

| Id | Check | Fail when |
| --- | --- | --- |
| CHK-19 | Gherkin shape | Missing Given, When, or Then |
| CHK-20 | Id link | Criterion id is not `AC-<parent id>-##` |
| CHK-21 | No new scope | The Then clause obliges behavior the shall and the source do not |
| CHK-22 | Thresholds | A minimum, maximum, or "only when" shall has no negative criterion |

## ISO/IEC 25010:2023

| Id | Check | Fail when |
| --- | --- | --- |
| CHK-23 | Nine rows | A characteristic is missing or duplicated |
| CHK-24 | Disposition matches evidence | `covered` without requirement ids, `open-question` without question ids, or `not-applicable` / `not-stated` with an empty rationale |
| CHK-25 | Targets are sourced | An NFR number is not in the source |
| CHK-26 | No padded controls | A security or reliability shall names a control the source did not ask for |

## Structure, data, scenarios

| Id | Check | Fail when |
| --- | --- | --- |
| CHK-27 | Schema | A requirement object fails `requirement.schema.json` |
| CHK-28 | Scenarios add nothing | A use-case step, extension, or user story has no requirement id, or its wording exceeds the cited shall |
| CHK-29 | Interfaces | A party, payload field, error behavior, or representation is not sourced and is not an explicit deferral |
| CHK-30 | Logical data | An entity carries a physical type, key, or unsourced attribute |
| CHK-31 | Glossary | A definition adds a rule that is not in a shall, or a shall uses an undefined status word |
| CHK-32 | Identifiers | Duplicate ids, reused retired ids, or a gap that was closed by renumbering |

## Gate hygiene

| Id | Check | Fail when |
| --- | --- | --- |
| CHK-33 | Questions are explicit | An unknown remains only in prose ("later", "TBD") instead of an `OQ-###` |
| CHK-34 | Blocking flags | A shall the sponsor requested is still ambiguous and its question is marked non-blocking |
| CHK-35 | Cycle count | This is the third failed cycle. Result of the gate is fail and the orchestrator stops |

Severity guide: CHK-01, CHK-02, CHK-03, CHK-04, CHK-16 are blockers and return to G1. CHK-07 and CHK-26 are blockers when the mechanism was invented, and major when it was only poorly worded. Singular, Gherkin, coverage, and scenario defects are major and return to the owning G2 skill. JSON punctuation that does not change a statement is minor.
