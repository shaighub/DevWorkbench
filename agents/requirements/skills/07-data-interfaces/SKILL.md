---
name: requirements-data-interfaces
description: >
  Use during gate G2, after functional and non-functional requirements
  exist, to describe logical data and external interfaces at business level.
  Use again when validation finds a physical design, an invented protocol,
  or an interface that no requirement uses.
---

# 07 — Data and interfaces

## Purpose

State the business information the requirements already depend on, and the business content that crosses the boundary with each external party the source named. This is the logical database and external-interface content of a 29148 SRS (sections 3.5 and 3.1). It is not a schema, an API, a table design, or a sequence diagram.

ISO/IEC/IEEE 29148 asks for interfaces in four classes: user, software, hardware, and communications. Record a class only where the source supports it. Most engagements of this kind have user behavior already covered by the FRs, plus software interfaces to named parties. Do not add a hardware interface to look complete.

## Inputs

- Functional and non-functional requirements, scope context list, glossary, constraints, open questions.
- `source/`, for what an external party sends or receives.
- The Won't list.

## Method

1. Walk the nouns in the proposed shall statements and the glossary status words. Each noun that has attributes the rules already talk about is a candidate entity (`ENT-###`): an application, a permit, a fee, a file, an audit record. If a noun has no sourced attributes, it is not an entity yet.
2. For each attribute, write the business meaning and, where the source listed them, the allowed values. Allowed values are the sponsor's lists (Submitted, Approved, Rejected), not database enums. Do not add types, lengths, nullability, keys, indexes, or table names. Do not add an attribute because a normal record would have it (created-by, version, locale) unless a requirement uses it.
3. If two requirements use the same word for different states, stop and raise a blocking question. Do not pick a canonical model and move on.
4. Retention, deletion, and "who owns the record" are requirements only when the source stated them. Silence is an open question if a shall would otherwise include a retention period, and it is silence if nobody is asking for one. Do not write "retain for 7 years" from habit.
5. Interfaces (`IF-###`), one per external party on the skill 03 context list. For each:
   - `kind`: software, user, hardware, or communications, as the source supports.
   - `direction`: inbound, outbound, or bidirectional, from the product's point of view.
   - `dataSent` and `dataReceived`: business facts, in the glossary's words. A lookup that returns zone, status, and expiry lists those words and nothing else.
   - `errorBehavior`: only the reaction the source described (record the failure, do not undo the issuance, not-found is not Active). If the source did not describe the failure, write an open question and set `errorBehavior` to point at that question rather than inventing retries, backoff, or codes.
   - `representation`: if the source mandated a format, record it. If the source deferred representation to design, write that deferral and the constraint id. Do not add HTTP, JSON, status codes, headers, or authentication schemes to be helpful. A mandated sign-on the source named ("city single sign-on", "group parking-clerk") may be named because it is a business rule, still without a token format.
6. Every interface lists `requirementIds` it serves. An interface with an empty list is a party you invented or a design step you started. Delete it.
7. Every entity lists the requirement ids that use it. An attribute no requirement and no glossary entry needs is deleted.
8. User-interface detail stays at the behavior in the FRs (what the person must be able to accomplish). Layout, navigation, and component choice are design. Do not write them as interface objects unless the source constrained them (for example a stated viewport width, which is already an NFR, not a new interface).
9. Read `mustNotBeInvented` on every open question. If an entity attribute or a dataSent entry would decide that question, remove the entry.

## Output format

Markdown `working/07-data-interfaces.md` with an entity section (attributes and meanings) and an interface section (party, direction, data, errors, representation, requirement ids).

JSON `working/07-data-interfaces.json`:

```json
{
  "dataEntities": [],
  "interfaces": []
}
```

Objects match `#/$defs/dataEntity` and `#/$defs/interface`.

## Quality checklist

- No physical types, keys, indexes, or vendor products that the source did not name.
- Every interface party appears on the G1 context list.
- Every interface and entity cites requirement ids that exist.
- Error behavior is sourced or explicitly points at an open question. It does not describe an unsourced retry policy.
- Representation is either sourced or an explicit deferral to design.
- No Won't topic and no open question is resolved by an attribute or a payload field.
- User-interface layout is absent.

## Gate

**Requirements G2: Requirements Elicited.**

After this skill, evaluate G2 using the exit criteria in `docs/sdlc-gates.md`. Write `working/gate-G2.json`. On pass, skill 08 is next. On fail, name which of skills 04–07 must rerun. Do not start validation on a package you already know is missing citations.
