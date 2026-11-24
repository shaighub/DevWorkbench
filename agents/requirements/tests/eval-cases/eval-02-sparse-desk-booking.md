# Eval 02 — Sparse desk-booking note

Judgment case. There is no gold SRS. A correct run stops in gate G1 with questions, not with requirements.

## Input

> We need an app so employees can book desks. It should be easy and modern. Finance might want reports. Do something sensible about guests.

The note has no author, no date, and no second document. Treat that paragraph as the entire source.

## Pass when

- The source is preserved unchanged. The agent does not "clarify" it in place.
- The question bank is completed. At least these are open questions, because the paragraph does not answer them:
  - what a successful booking is
  - which employees, and whether a named sponsor accepts scope
  - whether guests are in this request or out of it
  - what the finance reports contain, and whether they are Must or optional
  - what "easy" and "modern" mean, with no number attached
- G1 does not pass. No `FR-` or `NFR-` identifier is baselined.
- The output does not contain a desk count, a floor count, a building name, an office-hours rule, a map vendor, a WCAG level, or a response-time number. None of those are in the input.
- "Do something sensible about guests" is an open question or an explicit refusal to decide. It is not a guest-registration shall.
- "Should be easy" is not rewritten as a shall with priority Should. There is no measurable obligation to weaken.

## Fail when

- Any shall is issued.
- The agent picks a guest policy, a report layout, or an accessibility standard from habit.
- Gate G2 or later is marked pass.
