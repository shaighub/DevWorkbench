# Residential Parking Permit Portal — software requirements specification

Status of this file: **proposed**. Gate G5 is ready for a person to approve. The requirements agent has not approved it and has not marked it handed off. Design, build, and test do not start from a proposed package.

The shall statements below are the same strings as `srs.json`. If they differ, the package is not ready.

| Field | Value |
| --- | --- |
| Document id | SRS-RPP-001 |
| Version | 0.1.0 |
| Status | proposed |
| Standard | ISO/IEC/IEEE 29148:2018 |
| Quality model | ISO/IEC 25010:2023 |
| Priority | MoSCoW |
| Acceptance criteria | Gherkin |
| Source | agents/requirements/examples/input-brd-sample.md |
| Prepared by | requirements-agent |

## 1. Introduction

### 1.1 Purpose

This software requirements specification is the proposed baseline for design, build, and test of the Residential Parking Permit Portal. It tells the sponsor what will be held as requirements and tells later agents which decisions they must not make. It is not an approved handoff until a named person records approval.

### 1.2 Scope

The product lets a resident apply for one vehicle, prove an eligible address, pay the current ordinance fee after a clerk approves, and receive a permit an officer can check by plate without seeing personal details. Topics the sponsor excluded are out of scope. Topics the sponsor left open are open questions, not defaults. A topic in neither list is not a requirement.

### 1.3 Product overview

#### 1.3.1 Product perspective

Residents sign in with a one-time email link and do not receive a city password. Clerks sign in through the city single sign-on. The portal sends the resident to CityPay for card entry, sends three notices through CityNotify, and answers a lookup the enforcement handheld will call. Parking Services supplies the cleaned address list and the current fees as data. No other external party is in the source.

Context, from parties the source names:

- Resident → portal, by a one-time link (channel unanswered, OQ-007).
- Portal → CityPay hosted page, after approval, and CityPay → portal with a success report.
- Portal → CityNotify for submission, rejection, and issuance email.
- Enforcement handheld → portal lookup. Representation is deferred (CON-003).
- City single sign-on → portal, group `parking-clerk`.
- Parking Services → portal, as data: cleaned address list and current fees.

#### 1.3.2 Product functions

- Record one application for one vehicle and accept submission only when the address and the file pass (FR-001, FR-002, FR-003, FR-004).
- Let a parking clerk approve or reject a submitted application (FR-005, FR-006).
- Show the current fee, take payment on CityPay, and issue an Active permit (FR-007, FR-008, FR-009, FR-010).
- Email the resident at submission, rejection, and issuance (FR-011, FR-012).
- Start a renewal inside the stated window from the current permit (FR-013).
- Suspend or revoke with a reason code, and keep that permit off Active lookups (FR-014, FR-015).
- Answer a plate lookup with zone, status, and expiry only (FR-019, FR-020).
- Produce the monthly zone figures (FR-016).

#### 1.3.3 User characteristics

- Residents were not in the working session. The sponsor said they do not get a city network account (STK-001).
- Parking clerks use the city sign-on and decide applications and permit status under the stated rules (STK-002).
- Enforcement officers use the existing handheld and do not review applications (STK-003).
- Finance reconciles references and amounts and does not use the portal day to day (STK-004).
- The accessibility coordinator and the privacy officer were named as reviewers and were not interviewed. They have no quotations in the source (STK-005, STK-006).
- Dana Okonkwo was interviewed and accepts or rejects scope (STK-007). Interest and influence values elsewhere in the register are analyst judgments or are unknown.

#### 1.3.4 Limitations

- Visitor, temporary, and commercial permits, citations, appeals, meter payment, electric-vehicle-only bays, address overrides, a household cap, and post-expiry renewal are Won't (SC-OUT-01 through SC-OUT-07).
- Open questions OQ-001 through OQ-007 are unanswered. Downstream work must not invent those decisions.
- Handheld representation and clerk sign-on token format are deferred to design inside the business data already stated.
- No assumption was required. Where a fact was missing, a question was raised instead.

### 1.4 Definitions

Normative terms are in `glossary.md` and in the glossary array of `srs.json`. A definition does not add a shall.

## 2. References

| Id | Citation |
| --- | --- |
| REF-SRC | Sponsor working note, 12 March 2026, preserved at agents/requirements/examples/input-brd-sample.md. |
| REF-29148 | ISO/IEC/IEEE 29148:2018, Systems and software engineering — Life cycle processes — Requirements engineering. |
| REF-25010 | ISO/IEC 25010:2023, Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model. |
| POL-ACC-01 | Named by the sponsor. Full text is not in the source. The sentences that apply are in BRD §7. |
| POL-BROWSER-02 | Named by the sponsor. Full text is not in the source. The sentences that apply are in BRD §7. |
| POL-AVAIL-03 | Named by the sponsor. Full text is not in the source. The sentences that apply are in BRD §7. |
| POL-SEC-04 | Named by the sponsor. Full text is not in the source. The sentences that apply are in BRD §6.12 and BRD §7. |

## 3. Specific requirements

### 3.1 External interfaces

#### IF-001 — CityPay payment

- Kind: software. Direction: bidirectional. Party: CityPay.
- Purpose: Collect the current zone fee after approval and return the processor's success report.
- Data sent: Application identifier; Current fee amount in US dollars.
- Data received: Success or absence of success; Payment reference when successful; Amount paid when successful.
- Error behavior: If CityPay does not report success, the portal records no successful payment and does not issue a permit.
- Representation: The source mandates CityPay's hosted card page. Any further message format is deferred to design and may not add card storage.
- Requirements: FR-007, FR-008, FR-009, FR-010, NFR-006.
- Citations: BRD §6.2, BRD §6.6, BRD §6.12.

#### IF-002 — CityNotify resident email

- Kind: software. Direction: outbound. Party: CityNotify.
- Purpose: Send the submission, rejection, and issuance notices to the application email address.
- Data sent: Recipient email address; Event: Submitted, Rejected, or permit issued; Application or permit identifier.
- Data received: Whether CityNotify accepted the message.
- Error behavior: Record the failure, send at most 3 attempts for that event, and do not change the application or permit status because the message failed.
- Representation: Deferred to design. The source names CityNotify and the business content only. This interface does not carry the one-time sign-in link (OQ-007).
- Requirements: FR-011, FR-012.
- Citations: BRD §6.9.

#### IF-003 — Enforcement plate lookup

- Kind: software. Direction: inbound. Party: Enforcement handheld.
- Purpose: Answer a plate and jurisdiction with zone, status, and expiry, or not-found, without personal details.
- Data sent: Zone, status, and expiry date of a match, or a not-found result.
- Data received: License plate; Jurisdiction.
- Error behavior: Not-found is a normal result and is not an Active permit. A lookup date after the expiry date is not an Active result.
- Representation: Deferred to design under CON-003. The source forbade inventing the wire format. Business content is FR-015, FR-019, and FR-020.
- Requirements: FR-015, FR-019, FR-020, NFR-001.
- Citations: BRD §6.10, BRD §6.11.

#### IF-004 — City single sign-on for clerks

- Kind: software. Direction: inbound. Party: City single sign-on.
- Purpose: Start a parking-clerk session only when the group parking-clerk is asserted.
- Data sent: Parking-clerk session, or no session.
- Data received: Assertion of the group parking-clerk, or its absence.
- Error behavior: If the group is not asserted, a parking-clerk session does not start.
- Representation: The source names the city single sign-on and the group claim. Token format and protocol were not specified and are deferred to design.
- Requirements: FR-018.
- Citations: BRD §6.10.

### 3.2 Functions

Use cases and user stories in `srs.json` are an index. They do not add behavior. The shall is the requirement.

### FR-017

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.10.
- Status: proposed
- Needs: NEED-009
- Citations: BRD §6.10
- Verification: test

Statement:

The portal shall start a resident session only after the resident opens a one-time link that the portal sent to the email address the resident entered.

Rationale:

The sponsor forbade a city password for residents. The channel that carries the link is not named and is OQ-007. This statement does not assume CityNotify.

Acceptance criteria:

#### AC-FR-017-01 — The link starts a session

```gherkin
Given a resident who entered an email address
And a one-time link the portal sent to that address
When the resident opens the link
Then the portal starts a resident session for that email address
```

#### AC-FR-017-02 — No link means no session

```gherkin
Given a resident who entered an email address
When the resident has not opened a one-time link sent to that address
Then the portal does not start a resident session
```

### FR-001

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.1.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.1
- Verification: test

Statement:

The portal shall record, on one application by an authenticated resident, a legal name, a residential street address, an email address, one license plate, and that plate's jurisdiction.

Rationale:

BRD §6.1 treats these fields as the contents of one application, so they stay one completeness rule. A second plate, a household limit, and guest permits are not added: the first is contrary to this rule, and the others are SC-OUT-06, OQ-001, and SC-OUT-01.

Acceptance criteria:

#### AC-FR-001-01 — One application holds the sourced fields and one plate

```gherkin
Given an authenticated resident
When the resident records a legal name, a residential street address, an email address, one license plate, and a jurisdiction on an application
Then the application contains those values
And the application does not contain a second license plate
```

#### AC-FR-001-02 — A missing jurisdiction is not a complete application

```gherkin
Given an authenticated resident who has not recorded a jurisdiction
When the resident tries to treat the application as complete
Then the portal does not treat the application as containing the required set of fields
```

### FR-002

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.3.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.3
- Verification: test

Statement:

The portal shall refuse submission of an application whose residential street address is not on the eligible-address list Parking Services supplied for that application's zone.

Rationale:

The comparison is against the cleaned list the sponsor will supply. Fuzzy matching is forbidden by CON-001. A clerk override is SC-OUT-05. Which upstream system produces the list is OQ-002 and is not decided here.

Acceptance criteria:

#### AC-FR-002-01 — Sponsor's own example address is refused

```gherkin
Given the eligible-address list for zone R-A contains 100 Market Street
And that list does not contain 9 Dock Lane
When a resident tries to submit an application for zone R-A at 9 Dock Lane
Then the portal refuses submission
And the application does not become Submitted
```

#### AC-FR-002-02 — An address on the list is not refused by this rule

```gherkin
Given the eligible-address list for zone R-A contains 100 Market Street
When a resident submits an otherwise complete application for zone R-A at 100 Market Street
Then this address rule does not refuse the submission
```

### FR-003

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.4.
- Status: proposed
- Needs: NEED-001, NEED-007
- Citations: BRD §6.4
- Verification: test

Statement:

The portal shall accept submission only when the application has exactly one proof-of-address file whose media type is PDF, JPEG, or PNG and whose size is no greater than 10 megabytes.

Rationale:

The file rule is the sponsor's list and size cap. Who may later retrieve the file is NFR-005. How long the file is kept is OQ-003 and is not given a period here.

Acceptance criteria:

#### AC-FR-003-01 — One PNG at the stated cap satisfies the file rule

```gherkin
Given an application with no proof-of-address file yet
When the resident attaches one PNG file of 10 megabytes
Then the file rule is satisfied for that application
```

#### AC-FR-003-02 — A file over the cap is refused

```gherkin
Given an application
When the resident attaches one PNG file larger than 10 megabytes
Then the portal does not accept submission on the strength of that file
```

#### AC-FR-003-03 — A second file is refused

```gherkin
Given an application that already has one PDF proof-of-address file
When the resident attaches a second file
Then the portal does not accept submission with two proof-of-address files
```

### FR-004

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.6.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.6
- Verification: test

Statement:

The portal shall record an accepted submission as status Submitted, with the submission time in UTC, on the clerk review queue.

Rationale:

Accepted means the address rule and the file rule already passed. Draft applications are not on the queue, which is the sponsor's state model in BRD §6.6, not an extra workflow.

Acceptance criteria:

#### AC-FR-004-01 — A passing submission joins the queue

```gherkin
Given an application that has passed the address rule and the file rule
When the resident submits it
Then the status is Submitted
And the submission time is recorded in UTC
And the application is on the clerk review queue
```

### FR-018

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.10.
- Status: proposed
- Needs: NEED-010
- Citations: BRD §6.10
- Verification: test

Statement:

The portal shall start a parking-clerk session only when a city single sign-on asserts the group parking-clerk.

Rationale:

The group claim is the sponsor's rule. Token format and protocol are not specified and stay deferred to design under CON-003's sibling constraint for representation, recorded on IF-004.

Acceptance criteria:

#### AC-FR-018-01 — The group starts a clerk session

```gherkin
Given a city single sign-on that asserts the group parking-clerk
When the portal establishes the session
Then the session is a parking-clerk session
```

#### AC-FR-018-02 — A sign-on without the group does not start a clerk session

```gherkin
Given a city single sign-on that does not assert the group parking-clerk
When the portal considers a clerk session
Then the portal does not start a parking-clerk session
```

### FR-005

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.6.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.6
- Verification: test

Statement:

The portal shall let a user in the parking-clerk role change an application from status Submitted to status Approved.

Rationale:

Approval is a clerk action on a Submitted application. The sponsor did not define a clerk override for an address off the list, so this statement does not add one (SC-OUT-05).

Acceptance criteria:

#### AC-FR-005-01 — A clerk approves a submitted application

```gherkin
Given a user in the parking-clerk role
And an application in status Submitted
When the clerk approves it
Then the application status is Approved
```

#### AC-FR-005-02 — A draft is not approved from the queue

```gherkin
Given a user in the parking-clerk role
And an application in status Draft
When the clerk looks for it on the review queue
Then the application is not on the queue and is not changed to Approved
```

### FR-006

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.5.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.5
- Verification: test

Statement:

The portal shall let a user in the parking-clerk role change an application from status Submitted to status Rejected only when that user supplies a reason at least 15 characters long.

Rationale:

The 15-character floor is the sponsor's work rule. A shorter reason leaves the application Submitted, which BRD §6.5 states directly.

Acceptance criteria:

#### AC-FR-006-01 — Fifteen characters rejects

```gherkin
Given a user in the parking-clerk role
And an application in status Submitted
When the clerk rejects it with a reason of 15 characters
Then the application status is Rejected
And the reason is retained
```

#### AC-FR-006-02 — Fourteen characters does not reject

```gherkin
Given a user in the parking-clerk role
And an application in status Submitted
When the clerk tries to reject it with a reason of 14 characters
Then the application status remains Submitted
```

### FR-007

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.2.
- Status: proposed
- Needs: NEED-002
- Citations: BRD §6.2
- Verification: test

Statement:

The portal shall show the current ordinance fee for the application's zone, in US dollars, immediately before the resident is sent to pay.

Rationale:

The fee is the current card amount at the moment of handoff, not a copy frozen at submission, because BRD §6.2 says the amount shown and the amount sent are the current fee at that moment. The card values are data, not hard-coded shall text, so an ordinance change does not require a new requirement.

Acceptance criteria:

#### AC-FR-007-01 — The shown amount is the current zone fee

```gherkin
Given the current fee for zone R-A is 60 US dollars
And the current fee for zone R-B is 90 US dollars
When the resident is about to be sent to pay an Approved application for zone R-B
Then the portal shows 90 US dollars
And the resident has not yet been sent to CityPay
```

### FR-008

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.6.
- Status: proposed
- Needs: NEED-002
- Citations: BRD §6.6
- Verification: test

Statement:

The portal shall send the resident to the CityPay hosted page for an application only when that application is Approved.

Rationale:

Payment before approval is excluded by the sponsor's sequence. Card capture itself is NFR-006 and stays on CityPay's page.

Acceptance criteria:

#### AC-FR-008-01 — An approved application can be handed to CityPay

```gherkin
Given an application in status Approved
When the resident continues to payment
Then the portal sends the resident to the CityPay hosted page for that application
```

#### AC-FR-008-02 — A submitted application is not handed to CityPay

```gherkin
Given an application in status Submitted
When the resident tries to pay
Then the portal does not send the resident to the CityPay hosted page
```

### FR-009

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.6.
- Status: proposed
- Needs: NEED-002, NEED-007
- Citations: BRD §6.6, BRD §6.12
- Verification: test

Statement:

The portal shall record the CityPay payment reference and the amount CityPay reported when CityPay reports that the fee was paid successfully.

Rationale:

The portal records the reference and the amount the processor reports. It does not record the card number. Absence of a success report is not turned into a success by a timeout the sponsor did not state.

Acceptance criteria:

#### AC-FR-009-01 — A success report is stored

```gherkin
Given an Approved application whose current fee was shown as 60 US dollars
When CityPay reports success with a payment reference and an amount of 60 US dollars
Then the portal records that reference and that amount against the application
```

#### AC-FR-009-02 — No success report means no successful payment

```gherkin
Given an Approved application
When CityPay has not reported success
Then the portal has no successful payment recorded for that application
```

### FR-010

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.6.
- Status: proposed
- Needs: NEED-001, NEED-002
- Citations: BRD §6.6, BRD §6.7
- Verification: test

Statement:

The portal shall issue a new permit in status Active, with a permit number the portal has not issued before and with an expiry date 365 days after the issue date, only when the linked application is Approved and a successful CityPay payment is recorded for it.

Rationale:

Issuance is the same gate for a first application and for a renewal. BRD §6.7 says a renewal issues a new permit and leaves the previous permit unchanged. This statement does not shorten the previous permit and does not add a grace period (SC-OUT-07).

Acceptance criteria:

#### AC-FR-010-01 — Approval plus payment issues a new Active permit

```gherkin
Given an Approved application with a successful CityPay payment recorded
When the portal issues the permit
Then the new permit is Active
And its permit number has not been issued before
And its expiry date is 365 days after its issue date
```

#### AC-FR-010-02 — Approval without payment does not issue

```gherkin
Given an Approved application with no successful CityPay payment recorded
When issuance is considered
Then the portal does not create an Active permit for that application
```

### FR-011

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.9.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.9
- Verification: test

Statement:

The portal shall send one email through CityNotify to the application's email address when the application becomes Submitted, when it becomes Rejected, and when a permit is issued for it.

Rationale:

The three events are the sponsor's list. The one-time sign-in link is a different send (FR-017). The source does not say that link uses CityNotify, so this statement does not attach it. That channel is OQ-007.

Acceptance criteria:

#### AC-FR-011-01 — Submission sends one email

```gherkin
Given an application that has just become Submitted
When the portal sends the submission notice
Then one email is sent through CityNotify to the email address on the application
```

#### AC-FR-011-02 — Rejection sends one email

```gherkin
Given an application that has just become Rejected
When the portal sends the rejection notice
Then one email is sent through CityNotify to the email address on the application
```

#### AC-FR-011-03 — Issuance sends one email

```gherkin
Given a permit that has just been issued for an application
When the portal sends the issuance notice
Then one email is sent through CityNotify to the email address on the application
```

### FR-012

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.9.
- Status: proposed
- Needs: NEED-001
- Citations: BRD §6.9
- Verification: test

Statement:

The portal shall record a failed CityNotify attempt, stop after 3 attempts for that event, and leave the application or permit status unchanged when CityNotify does not accept the message.

Rationale:

BRD §6.9 binds the record, the cap of 3, and the refusal to undo the business action as one failure behavior. Clerks phoning the resident is outside the product and is not turned into a shall.

Acceptance criteria:

#### AC-FR-012-01 — A refused message does not undo issuance

```gherkin
Given a permit that has just been issued
When CityNotify does not accept the issuance message
Then the portal records the failed attempt
And the permit remains issued
```

#### AC-FR-012-02 — Attempts stop at three

```gherkin
Given an event whose CityNotify message has already failed 3 times
When the portal considers another attempt for that same event
Then the portal does not send a fourth attempt
```

### FR-013

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.7.
- Status: proposed
- Needs: NEED-004
- Citations: BRD §6.7
- Verification: test

Statement:

The portal shall let a resident authenticated with the email address on an Active permit start a renewal application on or after the date 45 days before that permit's expiry date and on or before that expiry date, prefilled with that permit's legal name, residential street address, license plate, and jurisdiction.

Rationale:

The window bounds are the sponsor's, inclusive of day 45 and of the expiry date. A different email cannot start that renewal. After expiry is SC-OUT-07, not a late-renewal shall.

Acceptance criteria:

#### AC-FR-013-01 — The window opens on day 45 and prefills the four fields

```gherkin
Given an Active permit whose expiry date is 45 days after the current date
And a resident authenticated with the email address on that permit
When the resident starts a renewal
Then the portal creates a renewal application
And that application is prefilled with that permit's legal name, residential street address, license plate, and jurisdiction
```

#### AC-FR-013-02 — A day earlier than the window does not start a renewal

```gherkin
Given an Active permit whose expiry date is 46 days after the current date
And a resident authenticated with the email address on that permit
When the resident tries to start a renewal
Then the portal does not create a renewal application
```

### FR-014

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.8.
- Status: proposed
- Needs: NEED-005
- Citations: BRD §6.8
- Verification: test

Statement:

The portal shall change a permit from Active to Suspended or from Active to Revoked only when a user in the parking-clerk role records a reason code of eligibility-lapsed, non-payment, fraud, or other.

Rationale:

The four reason codes are the sponsor's closed list. Lookup consequences are FR-015, not a second copy of this decision.

Acceptance criteria:

#### AC-FR-014-01 — A listed reason code suspends

```gherkin
Given a user in the parking-clerk role
And a permit in status Active
When the clerk suspends it with reason code eligibility-lapsed
Then the permit status is Suspended
And the reason code is retained
```

#### AC-FR-014-02 — A missing reason code does not revoke

```gherkin
Given a user in the parking-clerk role
And a permit in status Active
When the clerk tries to revoke it without a reason code
Then the permit status remains Active
```

### FR-015

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.8.
- Status: proposed
- Needs: NEED-003, NEED-005
- Citations: BRD §6.8, BRD §6.11
- Verification: test

Statement:

The portal shall report a lookup status of Active only when the matched permit is stored as Active and the lookup date is on or before that permit's expiry date.

Rationale:

Suspended, Revoked, a date after expiry, and not-found are all outside Active, by BRD §6.8 and §6.11. The statement does not invent a stored status called Expired. The report counts expiry dates separately (FR-016).

Acceptance criteria:

#### AC-FR-015-01 — A current Active permit is reported Active

```gherkin
Given a permit stored as Active whose expiry date is on or after the lookup date
When a plate lookup matches that permit
Then the reported status is Active
```

#### AC-FR-015-02 — Suspended, revoked, and past expiry are not Active

```gherkin
Given a plate lookup that matches a permit stored as Suspended
When the same kind of lookup is repeated for a permit stored as Revoked and for a permit whose expiry date is before the lookup date
Then none of those three results reports status Active
```

### FR-019

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.11.
- Status: proposed
- Needs: NEED-003
- Citations: BRD §6.11
- Verification: test

Statement:

The portal shall answer a plate-and-jurisdiction lookup with the matching permit's zone, status, and expiry date, or with a not-found result when no permit matches that plate and jurisdiction.

Rationale:

The response business content is fixed here. The wire format is deferred to design (CON-003, IF-003). Not-found is a normal result, not an error code invented by this specification.

Acceptance criteria:

#### AC-FR-019-01 — A matching plate returns zone, status, and expiry

```gherkin
Given a permit for plate ABC123 in a jurisdiction, with a zone and an expiry date
When a lookup asks for plate ABC123 and that jurisdiction
Then the result contains that zone, the permit status, and that expiry date
```

#### AC-FR-019-02 — An unknown plate is not-found

```gherkin
Given no permit for plate ZZZ999 and the requested jurisdiction
When a lookup asks for that plate and jurisdiction
Then the result is not-found
And the result is not an Active permit
```

### FR-020

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.4.
- Status: proposed
- Needs: NEED-003, NEED-007
- Citations: BRD §6.4, BRD §6.11
- Verification: test

Statement:

The portal shall omit the resident's legal name, residential street address, email address, and proof-of-address file from every plate-lookup response.

Rationale:

This is the sponsor's replacement for the office reading personal details over the phone. It does not prescribe encryption or a token scheme.

Acceptance criteria:

#### AC-FR-020-01 — A hit omits personal details and the file

```gherkin
Given a permit that matches the requested plate and jurisdiction
When the lookup response is returned
Then the response does not contain the resident's legal name, residential street address, email address, or proof-of-address file
```

### FR-016

- Priority: Should
- Priority rationale: BRD §3 says the sponsor will still open the service to residents if the monthly totals slip to the next increment.
- Status: proposed
- Needs: NEED-008
- Citations: BRD §3, BRD §6.14
- Verification: test

Statement:

The portal shall produce, for a calendar month it is given, the count of permits whose issue date falls in that month, the count of permits whose expiry date falls in that month, and the sum of successful CityPay amounts recorded in that month, each grouped by zone.

Rationale:

The three aggregations are defined by BRD §6.14. Who is allowed to request the report is OQ-006, so this statement names no role. Priority is Should because the sponsor will open the resident service even if the report slips.

Acceptance criteria:

#### AC-FR-016-01 — Fixture records roll up by the stated definitions

```gherkin
Given a calendar month in which zone R-A has one permit with an issue date in the month, one permit with an expiry date in the month, and successful CityPay payments totaling 60 US dollars
And zone R-B has none of those
When the figures for that month are produced
Then zone R-A shows 1 issued, 1 expired, and 60 US dollars
And zone R-B shows 0 issued, 0 expired, and 0 US dollars
```

### 3.3 Usability requirements

ISO/IEC 25010:2023 names this characteristic interaction capability. The 2011 name is usability.

### NFR-002

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §7.
- Status: proposed
- Needs: NEED-006
- Citations: BRD §7
- Verification: demonstration
- Quality: interaction-capability / operability

Statement:

The portal shall let a resident complete application entry, proof-of-address upload, and the handoff to CityPay at a viewport width of 360 CSS pixels without horizontal scrolling.

Rationale:

The width and the three tasks are what the sponsor stated from POL-ACC-01. No other breakpoint is added.

Acceptance criteria:

#### AC-NFR-002-01 — The three named tasks fit the stated width

```gherkin
Given a viewport 360 CSS pixels wide
When a resident completes application entry, proof-of-address upload, and the handoff to CityPay
Then none of those tasks requires horizontal scrolling
```

### NFR-003

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §7.
- Status: proposed
- Needs: NEED-006
- Citations: BRD §7
- Verification: inspection
- Quality: interaction-capability / inclusivity

Statement:

The portal shall conform the resident flows and the clerk flows to WCAG 2.2 Level AA.

Rationale:

The sponsor cited WCAG 2.2 Level AA for resident and clerk flows and did not attach the rest of POL-ACC-01. This shall is that citation, not a private selection of success criteria. The accessibility coordinator was not in the room and is not quoted.

Acceptance criteria:

#### AC-NFR-003-01 — Named flows are inspected against the cited level

```gherkin
Given the resident flows and the clerk flows
When those flows are inspected against WCAG 2.2 Level AA
Then each flow conforms to that level
```

### 3.4 Performance requirements

### NFR-001

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.11.
- Status: proposed
- Needs: NEED-003
- Citations: BRD §6.11
- Verification: test
- Quality: performance-efficiency / time-behaviour

Statement:

The portal shall return a plate-lookup response within 2 seconds for at least 95 percent of lookups when 50 authenticated lookup clients call the lookup at the same time.

Rationale:

Scale is lookup response time, the meter is the share of lookups observed at the portal under the stated concurrency, and the target is the captain's figure as Dana recorded it. No resident-page budget is copied from this number. That gap is OQ-004.

Acceptance criteria:

#### AC-NFR-001-01 — The sourced load meets the sourced time

```gherkin
Given 50 authenticated lookup clients calling the plate lookup at the same time
When the responses are measured
Then at least 95 percent of those responses are returned within 2 seconds
```

Resident-page response time and peak application volume are OQ-004. They are not specified by copying the lookup target.

### 3.5 Logical database requirements

Business entities only. No physical types, keys, or indexes.

#### ENT-001 — Application

One resident request for one vehicle, from drafting through a clerk decision.

| Attribute | Meaning |
| --- | --- |
| legal name | The resident's legal name recorded on the application. |
| residential street address | The address compared to the eligible-address list. |
| email address | The address that receives CityNotify mail for this application and that receives the one-time link at sign-in. |
| license plate | The single plate named on the application. |
| jurisdiction | The state or province of that plate. |
| zone | The ordinance zone the application is for. |
| status | Draft while the resident is filling it in, Submitted on the queue, Approved or Rejected after a clerk decision. Allowed values: Draft, Submitted, Approved, Rejected. |
| submission time | The time the application became Submitted, in UTC. |
| rejection reason | The clerk's reason, present when status is Rejected, at least 15 characters. |

Requirements: FR-001, FR-002, FR-004, FR-005, FR-006.

#### ENT-002 — ProofOfAddressFile

The single file required before submission.

| Attribute | Meaning |
| --- | --- |
| media type | The file kind the sponsor allowed. Allowed values: PDF, JPEG, PNG. |
| size | The file size. Submission requires it to be no greater than 10 megabytes. |
| owning application | The application the file belongs to. |

Requirements: FR-003, FR-020, NFR-005.

#### ENT-003 — Permit

The permission issued after approval and successful payment, including a renewal's new permit.

| Attribute | Meaning |
| --- | --- |
| permit number | A number the portal has not issued before. |
| status | Active at issuance. Suspended or Revoked only with a listed reason code. A lookup does not report Active after the expiry date even if the stored status is still Active. Allowed values: Active, Suspended, Revoked. |
| issue date | The calendar date the permit was issued. |
| expiry date | The calendar date 365 days after the issue date. |
| zone | The zone on the issued permit. |
| license plate | The plate on the permit. |
| jurisdiction | The plate jurisdiction on the permit. |
| email address | The email a resident must authenticate with to start a renewal of this permit. |
| legal name | Prefilled onto a renewal. Not returned on a plate lookup. |
| residential street address | Prefilled onto a renewal. Not returned on a plate lookup. |

Requirements: FR-010, FR-013, FR-014, FR-015.

#### ENT-004 — ZoneFee

The current ordinance amount for a zone.

| Attribute | Meaning |
| --- | --- |
| zone | R-A or R-B on the current card, or a later zone supplied as data. |
| current amount | The US dollar amount shown and sent to CityPay at the moment of handoff. |

Requirements: FR-007, NFR-008.

#### ENT-005 — EligibleAddress

One street address on the cleaned list Parking Services supplies for a zone.

| Attribute | Meaning |
| --- | --- |
| zone | The zone the list entry belongs to. |
| street address | The cleaned address text the application is compared to. |

Requirements: FR-002, NFR-008.

#### ENT-006 — Payment

The record of what CityPay reported for an application.

| Attribute | Meaning |
| --- | --- |
| application | The application the payment is for. |
| amount | The amount CityPay reported, present on success. |
| reference | The CityPay payment reference, present on success. |
| outcome | Success only when CityPay reported success. Otherwise no successful payment is recorded. |

Requirements: FR-009, FR-010, FR-016.

#### ENT-007 — Notification

One CityNotify send for a Submitted, Rejected, or issued event.

| Attribute | Meaning |
| --- | --- |
| event | Submitted, Rejected, or permit issued. |
| recipient | The email address on the application. |
| attempt count | How many times this event was sent. The cap is 3. |
| accepted | Whether CityNotify accepted the message. |

Requirements: FR-011, FR-012.

#### ENT-008 — AuditRecord

The record appended for each approval, rejection, issuance, suspension, and revocation.

| Attribute | Meaning |
| --- | --- |
| actor | Who performed the action. |
| time | When the action was recorded, in UTC. |
| action | Approval, rejection, issuance, suspension, or revocation. |
| reason or payment reference | The clerk's reason, the reason code, or the CityPay reference, as the action requires. |

Requirements: NFR-009.

### 3.6 Design constraints

- **CON-001.** Do not add fuzzy matching. Compare the entered street address to the cleaned list. (BRD §6.3)
- **CON-002.** Do not store the card number or the card security code. Collect them only on the CityPay page. (BRD §6.12)
- **CON-003.** Do not invent the handheld wire format. Representation is a design decision constrained by the lookup business content. (BRD §6.10)
- **CON-004.** A zone fee and the eligible-address list must be changeable without a software release. (BRD §6.2)
- **CON-005.** Submission time and audit time are recorded in UTC. (BRD §6.6, BRD §6.13)

Dependencies, which are duties of other parties and not product shall statements:

- **DEP-001.** CityPay hosts the card page and, on success, reports a payment reference and the amount paid. (BRD §6.6)
- **DEP-002.** CityNotify is the mail relay used for the submission, rejection, and issuance emails. (BRD §6.9)
- **DEP-003.** The city single sign-on can assert the group parking-clerk for a clerk. (BRD §6.10)
- **DEP-004.** Parking Services supplies the cleaned eligible-address list for each zone. (BRD §6.3)
- **DEP-005.** The handheld team will call the lookup. They will specify representation in design. (BRD §6.10)

### 3.7 Software system attributes

| Characteristic | Disposition | Requirements | Open questions |
| --- | --- | --- | --- |
| functional-suitability | covered | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020 | — |
| performance-efficiency | covered | NFR-001 | OQ-004 |
| compatibility | covered | FR-008, FR-009, FR-011, FR-018, FR-019 | — |
| interaction-capability | covered | NFR-002, NFR-003 | — |
| reliability | covered | NFR-007 | OQ-005 |
| security | covered | NFR-005, NFR-006, NFR-009, FR-017, FR-018, FR-020 | — |
| maintainability | not-stated | — | — |
| flexibility | covered | NFR-004, NFR-008 | — |
| safety | not-applicable | — | — |

- **functional-suitability.** Functional suitability is specified by the functional requirements. Those statements are not copied again as non-functional requirements.
- **performance-efficiency.** Lookup time-behaviour is specified. Resident-page time and capacity were not stated and stay in OQ-004. No target was invented for them.
- **compatibility.** Interoperability is the sourced behavior with CityPay, CityNotify, city single sign-on, and the handheld lookup. Co-existence with another named product on the same host was not required and is not applicable.
- **interaction-capability.** The 2011 name is usability. The sponsor's cited obligations are the 360 CSS pixel tasks and WCAG 2.2 Level AA.
- **reliability.** Availability is the cited monthly percentage. Recoverability after an unplanned outage was not stated and is OQ-005.
- **security.** Confidentiality, accountability, and authenticity are the sourced obligations. No cipher, vault, or token format was added.
- **maintainability.** The sponsor stated no analysability, modifiability, testability, or reuse target. No maintainability index was invented. This is not a design standard imported from outside the source.
- **flexibility.** The 2011 name is portability. Adaptability covers the cited browser matrix and the requirement that fees and the address list change without a software release.
- **safety.** The portal does not control vehicles, barriers, or signals. A wrong permit status is specified as functional correctness and confidentiality, not as the safety characteristic.

### NFR-004

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §7.
- Status: proposed
- Needs: NEED-006
- Citations: BRD §7
- Verification: test
- Quality: flexibility / adaptability

Statement:

The portal shall present the resident flows in the current major version and the immediately previous major version of Chrome, Firefox, Safari, and Edge.

Rationale:

POL-BROWSER-02 as the sponsor stated it. No other browser and no clerk-flow browser matrix is added, because the sponsor applied this policy to resident flows.

Acceptance criteria:

#### AC-NFR-004-01 — Each named browser at both stated generations presents the resident flows

```gherkin
Given the current major version and the immediately previous major version of Chrome, Firefox, Safari, and Edge
When a resident uses each of those versions for the resident flows
Then the resident flows are presented in each of those versions
```

### NFR-005

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.4.
- Status: proposed
- Needs: NEED-007
- Citations: BRD §6.4
- Verification: test
- Quality: security / confidentiality

Statement:

The portal shall let a proof-of-address file be retrieved only by the resident who uploaded it and by a user in the parking-clerk role.

Rationale:

The allowed people are the sponsor's list. The statement does not choose storage encryption, a document-management product, or a retention period (OQ-003).

Acceptance criteria:

#### AC-NFR-005-01 — Clerk and uploading resident can retrieve the file

```gherkin
Given a proof-of-address file uploaded by a resident
When that resident retrieves it and a user in the parking-clerk role retrieves it
Then both retrievals are allowed
```

#### AC-NFR-005-02 — Another resident cannot retrieve the file

```gherkin
Given a proof-of-address file uploaded by one resident
When a different resident tries to retrieve it
Then the portal does not return the file
```

### NFR-006

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.12.
- Status: proposed
- Needs: NEED-002, NEED-007
- Citations: BRD §6.12, BRD §7
- Verification: test
- Quality: security / confidentiality

Statement:

The portal shall keep payment card numbers and card security codes out of portal storage by collecting them only on the CityPay hosted page.

Rationale:

POL-SEC-04 as the sponsor applied it. No card-vault product and no cipher suite is named.

Acceptance criteria:

#### AC-NFR-006-01 — Card entry is on CityPay and the values are not stored

```gherkin
Given a resident paying an Approved application
When the resident enters a card number and a card security code
Then that entry happens on the CityPay hosted page
And the portal has not stored the card number or the card security code
```

### NFR-007

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §7.
- Status: proposed
- Needs: NEED-001, NEED-003
- Citations: BRD §7
- Verification: analysis
- Quality: reliability / availability

Statement:

The portal shall keep the resident flows and the plate lookup available for at least 99.5 percent of the minutes in each calendar month outside maintenance windows published at least 48 hours before they start.

Rationale:

The percentage, the month, the two surfaces, and the 48-hour notice are POL-AVAIL-03 as stated. Restore time after an unplanned outage is not in the policy sentence and is OQ-005.

Acceptance criteria:

#### AC-NFR-007-01 — Monthly minutes meet the stated percentage

```gherkin
Given a calendar month and the maintenance windows that were published at least 48 hours before they started
When available minutes of the resident flows and of the plate lookup are divided by the minutes in that month outside those windows
Then the result is at least 99.5 percent
```

### NFR-008

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.2.
- Status: proposed
- Needs: NEED-001, NEED-002
- Citations: BRD §6.2
- Verification: demonstration
- Quality: flexibility / adaptability

Statement:

The portal shall apply an update to a zone's current fee or to the eligible-address list without a software release.

Rationale:

The sponsor required ordinance changes to take effect without a release. Who types the update is not stated, so no editor role is added. Provenance of the address list remains OQ-002.

Acceptance criteria:

#### AC-NFR-008-01 — A fee change is visible without a release

```gherkin
Given zone R-A has a current fee of 60 US dollars
When that current fee is updated to 70 US dollars without a software release
Then an Approved R-A application handed to payment after the update shows 70 US dollars
```

#### AC-NFR-008-02 — An address-list change is applied without a release

```gherkin
Given 9 Dock Lane is not on the zone R-A eligible-address list
When 9 Dock Lane is added to that list without a software release
Then a later submission for zone R-A at 9 Dock Lane is not refused by the address rule
```

### NFR-009

- Priority: Must
- Priority rationale: The sponsor stated this as behavior of this request, not as an optional later increment. BRD §6.13.
- Status: proposed
- Needs: NEED-005, NEED-007
- Citations: BRD §6.13
- Verification: test
- Quality: security / accountability

Statement:

The portal shall append an audit record containing the actor, the time in UTC, and the reason or the payment reference for each approval, rejection, issuance, suspension, and revocation.

Rationale:

The five actions and the three fields are the sponsor's audit rule. No log product is named.

Acceptance criteria:

#### AC-NFR-009-01 — A revocation writes the sourced audit fields

```gherkin
Given a user in the parking-clerk role
When that user revokes an Active permit with reason code fraud
Then an audit record is appended with that actor, the time in UTC, and the reason code
```

#### AC-NFR-009-02 — Issuance records the payment reference

```gherkin
Given a successful CityPay payment reference on an Approved application
When the portal issues the permit
Then an audit record is appended with the actor, the time in UTC, and that payment reference
```

### 3.8 Supporting information

The traceability matrix is `rtm.csv`. Design Element ID and Test Case ID are empty on every row. Identifiers are frozen. Needs without coverage, orphan requirements, and requirements missing acceptance criteria are empty lists.

## 4. Verification

| Requirement | Method |
| --- | --- |
| FR-001 | test |
| FR-002 | test |
| FR-003 | test |
| FR-004 | test |
| FR-005 | test |
| FR-006 | test |
| FR-007 | test |
| FR-008 | test |
| FR-009 | test |
| FR-010 | test |
| FR-011 | test |
| FR-012 | test |
| FR-013 | test |
| FR-014 | test |
| FR-015 | test |
| FR-016 | test |
| FR-017 | test |
| FR-018 | test |
| FR-019 | test |
| FR-020 | test |
| NFR-001 | test |
| NFR-002 | demonstration |
| NFR-003 | inspection |
| NFR-004 | test |
| NFR-005 | test |
| NFR-006 | test |
| NFR-007 | analysis |
| NFR-008 | demonstration |
| NFR-009 | test |

Gherkin in section 3 is the acceptance criterion. This section does not record test results. The test phase writes case ids into the matrix after a human has approved the package.

## 5. Appendices

### Appendix A. Needs

- **NEED-001** (Must, proposed). A resident of an eligible address needs a one-year permission to park one stated vehicle without coming to the counter. Citations: BRD §2, BRD §3.
- **NEED-002** (Must, proposed). The resident needs to pay the published fee for that permission, and finance needs the CityPay reference and amount. Citations: BRD §3, BRD §6.12.
- **NEED-003** (Must, proposed). An enforcement officer needs a plate's permit zone, status, and expiry without receiving the resident's name, address, email, or proof-of-address file. Citations: BRD §2, BRD §6.11.
- **NEED-004** (Must, proposed). A resident who holds an Active permit needs to start a renewal inside the stated window without retyping the stored name, address, plate, and jurisdiction. Citations: BRD §6.7.
- **NEED-005** (Must, proposed). A parking clerk needs to stop an Active permit from being treated as valid when eligibility has lapsed or fraud has been found, and needs that decision recorded. Citations: BRD §3, BRD §6.8, BRD §6.13.
- **NEED-006** (Must, proposed). A resident needs to complete application entry, file upload, and the CityPay handoff on a phone and under the accessibility and browser policies the sponsor cited. Citations: BRD §7.
- **NEED-007** (Must, proposed). The resident's proof-of-address file and payment card data need to stay with the people and the processor the sponsor named. Citations: BRD §6.4, BRD §6.12.
- **NEED-008** (Should, proposed). The sponsor needs monthly counts of permits issued, permits expired, and fees collected, grouped by zone, and will still open the resident service if this slips. Citations: BRD §3, BRD §6.14.
- **NEED-009** (Must, proposed). A resident needs to sign in by proving control of an email address, without a city-issued password. Citations: BRD §6.10.
- **NEED-010** (Must, proposed). A clerk's authority needs to come from the city single sign-on group parking-clerk, not from an account this product invents. Citations: BRD §6.10.

### Appendix B. Open questions

The sponsor-facing copy is `open-questions.md`. None of these is answered in this package.

- **OQ-001** (not blocking). How many Active permits may one household hold?
- **OQ-002** (not blocking). Which record produces the cleaned eligible-address list, and how often will Parking Services refresh it?
- **OQ-003** (not blocking). How long must a proof-of-address file be kept?
- **OQ-004** (not blocking). What response time is required for resident page tasks, and how many applications arrive in a peak hour?
- **OQ-005** (not blocking). How quickly must the portal be restored after an unplanned outage?
- **OQ-006** (not blocking). Who is allowed to request the monthly zone totals?
- **OQ-007** (not blocking). Which channel sends the resident's one-time sign-in link?

### Appendix C. Traceability matrix

See `rtm.csv`.

### Appendix D. Approval

Gates G1 through G4 passed. G5 is ready. `approval.humanApproval.recorded` is false. Status stays `proposed`. Residual risk has not been accepted. A named person may approve only after reading the open questions and either answering them in a new source note or explicitly accepting them as residual. Answering them inside a design is not approval.
