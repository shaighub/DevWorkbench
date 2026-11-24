# Functional requirement template

Copy this block for each `FR-###`. Delete the parenthetical hints. The `statement` line is the normative shall. Do not paraphrase it again underneath.

```markdown
### FR-000 — (short name, not a second statement)

- Type: functional
- Status: draft | proposed
- Priority: Must | Should | Could | Won't
- Priority rationale: (sponsor's commitment words, with citation)
- Need ids: NEED-000
- Stakeholder ids: STK-000
- Policy ids: (omit the line if none)
- Citations: BRD §0
- Verification: test | demonstration | inspection | analysis
- Use case ids: (filled by skill 05; leave empty until then)
- Story ids: (filled by skill 05)

Statement:

> The portal shall (one observable obligation, with the sourced condition and limit).

Rationale:

> (Why this obligation exists. Which open question or exclusion was deliberately not folded in.)

Acceptance criteria:

#### AC-FR-000-01 — (title)

Given (sourced precondition or labeled fixture)
When (one action)
Then (observable outcome a tester can decide)
```

## Anatomy of the statement

| Piece | Rule | Bad | Good |
| --- | --- | --- | --- |
| Subject | The product, not the user and not an external company | The clerk shall try to be careful. | The portal shall let a user in the parking-clerk role change a Submitted application to Approved. |
| Verb | shall, once | The portal should quickly support approval and also email the user. | One shall for the decision. A different FR for the email, if the source asked for email. |
| Object | One obligation | The portal shall approve, reject, suspend, and report. | Split. Four obligations, four ids. |
| Condition | From the source, or omitted | The portal shall approve when appropriate. | The portal shall let a parking clerk change an application to Approved only when its status is Submitted. |
| Limit | Exact | The portal shall reject a file that is too large. | The portal shall accept submission only when the file is no larger than 10 megabytes. |
| Priority | Attribute, not a softer verb | The portal should send the monthly totals. | The portal shall produce the monthly totals. Priority: Should. Rationale cites the sponsor allowing a slip. |

A completeness rule can list several fields when they are one gate: "The portal shall record, on one application, a legal name, a residential street address, an email address, one license plate, and that plate's jurisdiction." Say in the rationale that the source treats the set as one completeness rule. Do not hide two user-visible services behind one and.

## Acceptance criteria

Write the criterion so a person who was not in the room can pass or fail it.

Bad:

```gherkin
Given the user is unhappy
When they use the system
Then it is intuitive
```

Good, when the source both set the fee rule and gave the card values:

```gherkin
Given the current fee for zone R-B is 90 US dollars
When the resident is sent to pay an Approved application for zone R-B
Then the amount shown immediately before the handoff is 90 US dollars
```

Good negative case, from a sourced minimum of 15 characters:

```gherkin
Given an application in status Submitted
When a parking clerk tries to reject it with a reason of 14 characters
Then the application remains Submitted
```

Do not add a Then that states a new business rule. If the Then is not already in the shall or in a sourced definition of a word in the shall, the criterion is scope creep.

## Worked miniature

Source fragment, imagined only for this template: "A member may place a hold on one title. The hold expires after 7 days. We are not building fines in this release."

```markdown
### FR-014 — Place a title hold

- Priority: Must
- Priority rationale: The sponsor stated the hold as the behavior of the release, not as a follow-up. Source §2.
- Need ids: NEED-003
- Citations: Source §2
- Verification: test

Statement:

> The library system shall place a hold on one title for a member and shall end that hold at the end of the seventh day.

```

That miniature is **wrong**, and it is here so you will reject it. It uses shall twice, so it is two obligations (place a hold, end a hold). It also says "may" was in the source; the product shall is still correct only after you split. Fines are Won't and do not appear in a neighboring shall "to leave a hook".

Split form of the same fragment:

Statement of FR-014:

> The library system shall place a hold for a member on one title.

Statement of FR-015:

> The library system shall end a hold at the end of the seventh day after it was placed.

Priority on both is an attribute. Neither statement says should.
