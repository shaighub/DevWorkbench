# Open questions — rpp-2026-03

These questions are unanswered. An unanswered question is not a decision, including a question that looks easy to close with a usual city practice.

Design, build, and test must not invent the decision named on each question. Bring an answer back as a new source note and re-enter requirements intake.

None of these is blocking for the shall statements already written, because those statements were scoped to avoid them. Each one is blocking for any future shall that would depend on the answer. Gate G5 is ready for human review with that limit. Status of the SRS is proposed, not handed off.

## OQ-001

- Question: How many Active permits may one household hold?
- Why it matters: A cap would be a new eligibility rule. The sponsor said no number exists.
- Blocking: no
- Must not be invented: Any number of permits per household, and any shall that limits or grants a household cap.
- Raised by: 01-intake
- Answerable by: Dana Okonkwo, the sponsor. She said the policy is not written.
- Status: open
- Citations: BRD §5, BRD §9

## OQ-002

- Question: Which record produces the cleaned eligible-address list, and how often will Parking Services refresh it?
- Why it matters: An upstream interface or a freshness shall would depend on this answer.
- Blocking: no
- Must not be invented: Any integration to a tax roll, utility account, or other system of record, and any refresh interval.
- Raised by: 03-scope-context
- Answerable by: Dana Okonkwo. She said she does not yet know.
- Status: open
- Citations: BRD §6.3, BRD §9

## OQ-003

- Question: How long must a proof-of-address file be kept?
- Why it matters: A retention or deletion shall cannot be tested without a period.
- Blocking: no
- Must not be invented: Any retention period, deletion date, or archive rule for the file.
- Raised by: 07-data-interfaces
- Answerable by: The sponsor said Legal has not answered and named no person. Dana Okonkwo is the person who can bring that answer into the request.
- Status: open
- Citations: BRD §9

## OQ-004

- Question: What response time is required for resident page tasks, and how many applications arrive in a peak hour?
- Why it matters: The only quantified performance target in the source is the plate lookup.
- Blocking: no
- Must not be invented: Any page-response budget or application-volume figure.
- Raised by: 06-nonfunctional-reqs
- Answerable by: Dana Okonkwo. She stated that she did not have these figures.
- Status: open
- Citations: BRD §8, BRD §9

## OQ-005

- Question: How quickly must the portal be restored after an unplanned outage?
- Why it matters: POL-AVAIL-03 as cited sets monthly availability and planned-maintenance notice, not a restore time.
- Blocking: no
- Must not be invented: Any restore-time target or unplanned-outage procedure.
- Raised by: 06-nonfunctional-reqs
- Answerable by: Dana Okonkwo.
- Status: open
- Citations: BRD §9

## OQ-006

- Question: Who is allowed to request the monthly zone totals?
- Why it matters: FR-016 states the figures and names no actor, because the source names none.
- Blocking: no
- Must not be invented: Any role, including clerk or sponsor, as the only party allowed to request the report.
- Raised by: 04-functional-reqs
- Answerable by: Dana Okonkwo. BRD §6.14 records that this was not discussed.
- Status: open
- Citations: BRD §6.14, BRD §9

## OQ-007

- Question: Which channel sends the resident's one-time sign-in link?
- Why it matters: CityNotify is mandated for three other emails. The sign-in link is a separate send, and the source does not name its channel.
- Blocking: no
- Must not be invented: A decision that the link uses CityNotify, or a second mail product.
- Raised by: 07-data-interfaces
- Answerable by: Dana Okonkwo.
- Status: open
- Citations: BRD §6.9, BRD §6.10
