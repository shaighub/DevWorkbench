# Software requirements specification — <project>

> Author guidance: delete every blockquote before a document is marked proposed. Section numbers follow the software requirements specification outline in ISO/IEC/IEEE 29148:2018 clause 9.6. Write requirements once, in section 3, as shall statements that also appear unchanged in `srs.json`. Do not copy a shall into the introduction in different words.

| Field | Value |
| --- | --- |
| Document id | SRS-… |
| Version | 0.1.0 |
| Status | draft |
| Standard | ISO/IEC/IEEE 29148:2018 |
| Quality model | ISO/IEC 25010:2023 |
| Priority | MoSCoW (attribute, not a modal verb) |
| Acceptance criteria | Gherkin |
| Source | (path of the untouched high-level request) |
| Prepared by | requirements-agent |

## 1. Introduction

### 1.1 Purpose

> Who will read this SRS (design, build, test, the sponsor) and what decision it authorizes. This section does not contain shall statements.

### 1.2 Scope

> The product name, what it will and will not cover, and the benefit the sponsor asked for. Point at section 1.3.4 and at `open-questions.md` for anything undecided. State the boundary rule: a topic absent from the source is not a requirement.

### 1.3 Product overview

#### 1.3.1 Product perspective

> How the product sits among the users and external systems the source actually named. A short context list (actor → product → external party) is enough. Do not add unnamed systems. Representation of interfaces is not specified here unless the source required it.

#### 1.3.2 Product functions

> A short list of functions, each traceable to a need. No detail that section 3 does not already specify.

#### 1.3.3 User characteristics

> What the source says about each user class (skills, environment, whether they were interviewed). Analyst judgments about interest and influence are labeled as judgments.

#### 1.3.4 Limitations

> Out-of-scope items (MoSCoW Won't), constraints, dependencies, and assumptions. Every assumption says which identifiers must be rewritten if it is false. Open questions are listed by id, not answered here.

### 1.4 Definitions

> Normative terms. The same entries as `glossary.md`. A definition is not a second requirement.

## 2. References

> Source document, cited policies, and the standards (29148, 25010). A policy the sponsor named but did not attach is cited as "named by the sponsor; full text not in the source," and any obligation taken from it is only what the sponsor stated.

| Id | Citation |
| --- | --- |
| REF-01 | |

## 3. Specific requirements

> Each requirement is one shall, with identifier, MoSCoW, source need, citation, rationale, verification method, and Gherkin acceptance criteria. Wording here and in `srs.json` is identical. Withdrawn identifiers stay in a table at the end of this section with status deferred or rejected and are not reused.

### 3.1 External interfaces

> One subsection per interface (IF-###): party, direction, business data sent, business data received, sourced error behavior, and the requirement ids it serves. If the source left the wire format to design, say so. Do not invent protocols, status codes, or field types.

### 3.2 Functions

> Functional requirements, grouped by user goal. Use cases and user stories may follow each group as explanation. A story or a scenario step that is not already a shall is a defect, not new scope.

### 3.3 Usability requirements

> ISO/IEC 25010:2023 calls this characteristic interaction capability (ISO/IEC 25010:2011 called it usability). Put those NFRs here.

### 3.4 Performance requirements

> Performance efficiency NFRs. Each one has a scale, a meter, and a target taken from the source. Missing numbers stay in `open-questions.md`.

### 3.5 Logical database requirements

> Business entities and attributes the functions already use (ENT-###). No tables, types, indexes, or retention periods the source did not state.

### 3.6 Design constraints

> Constraints the source imposed (mandated parties, banned storage, "do not invent the wire format"). These bind design. They are not an excuse to add unspecified controls.

### 3.7 Software system attributes

> Remaining quality requirements: reliability, security, flexibility, compatibility, maintainability, safety. Record every 25010 characteristic as covered, not applicable, open question, or not stated.

### 3.8 Supporting information

> Traceability summary, identifier freeze, and the columns design and test will fill. Point at `rtm.csv`.

## 4. Verification

> For each requirement, the primary method: inspection, demonstration, test, or analysis. The Gherkin in section 3 is the acceptance criterion the test phase turns into a case. This section does not record results.

## 5. Appendices

### Appendix A. Needs

> NEED-### in stakeholder language, each cited. No shall.

### Appendix B. Open questions

> The same register as `open-questions.md`. Unanswered items are not decisions.

### Appendix C. Traceability matrix

> `rtm.csv`. Design Element ID and Test Case ID are blank at handoff.

### Appendix D. Approval

> The agent sets status to proposed and gate G5 to ready. A named human records approval before status becomes approved or handed-off. The agent does not sign for the sponsor.
