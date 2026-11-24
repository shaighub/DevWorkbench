# High-level need: Residential Parking Permit Portal

City of Northwind, Department of Parking and Mobility.
Sponsor: Dana Okonkwo, Parking Services Manager.
Source of this note: working session on 12 March 2026. Dana asked that this note be the whole request. Where she left a topic open, it stays open.

## 1. What this note is

This is a high-level request. It is not a specification and it is not permission to fill blanks with ordinary city practice. Policies are cited only as far as the sentences below.

## 2. Problem

Residents of eligible streets buy an annual parking permit at the counter and bring a paper proof of address. Clerks retype the form. An officer who wants to know whether a plate is permitted phones the office, and the office reads the resident's name and address back over the phone. Dana wants a resident to be able to apply and pay online, and an officer to be able to check a plate without receiving the resident's personal details.

## 3. Outcome

A resident can submit one application for one vehicle, pay the published fee, and receive a permit an officer can verify by plate. A clerk can refuse an ineligible application and can stop a permit from being treated as valid when eligibility lapses or fraud is found. Management can see monthly counts and fees by zone. Dana said she will still open the service to residents if those monthly totals slip to the next increment.

## 4. People

- Resident: applies, pays, and renews. The resident does not get a city network account.
- Parking clerk: reviews applications, and suspends or revokes permits. The clerk uses the city sign-on.
- Enforcement officer: looks a plate up from the existing handheld. The officer does not review applications.
- Finance: reconciles what CityPay collected against permits. Finance does not use the portal day to day and needs the amounts and the CityPay references.
- Dana is the sponsor. She accepts or rejects scope for this request.
- She said the city's accessibility coordinator and the privacy officer will review the result against the policies in section 7. They were not in the room and have not added requests of their own.

## 5. Scope the sponsor already drew

In this request:

- an online application for a resident
- one proof-of-address file on that application
- a clerk decision to approve or reject
- payment of the annual fee
- issuing the permit
- renewal inside the window in section 6.7
- an officer lookup by plate
- email to the resident at submission, rejection, and issuance
- monthly totals by zone, which may slip to the next increment (section 3)

Out of this request, in Dana's words:

- Visitor permits, temporary permits, and commercial permits. "Not this project."
- Writing citations or taking appeals. The handheld already does citations.
- Paying a meter.
- Electric-vehicle-only bays. "Not decided. Leave them out until I say otherwise."
- A clerk override that approves an address which is not on the list. "Do not build that until I decide."
- A household cap. "We have not written that policy. Do not pick a number for me."
- A grace period after expiry. Renewal is only the window in section 6.7. After expiry, this project does not include a renewal.

## 6. Rules the sponsor stated

### 6.1 One vehicle

One application names one license plate and that plate's jurisdiction, meaning the state or province. It also names the resident's legal name, residential street address, and email address.

### 6.2 Fees and zones

The current ordinance card:

- Zone R-A, Residential Core: 60 US dollars for a one-year permit.
- Zone R-B, Waterfront: 90 US dollars for a one-year permit.

Fees change by ordinance at least once a year and must be changeable without a software release. The same is true of the address list. The amount the resident is shown, and the amount sent to CityPay, is the current fee for the zone at the moment the resident is sent to pay.

### 6.3 Addresses

Parking Services will supply the eligible-address list, already cleaned, for each zone. Compare the street address the resident entered with that list. If the address is not on the list for the selected zone, the resident cannot submit. Do not add fuzzy matching. Example Dana gave: if the R-A list contains 100 Market Street and does not contain 9 Dock Lane, then 9 Dock Lane cannot be submitted for R-A.

She does not yet know whether the cleaned list is produced from the tax roll, from utility accounts, or from a spreadsheet, and she does not know how often she will refresh it.

### 6.4 Proof-of-address file

The file is required before submit. Exactly one file. PDF, JPEG, or PNG. No larger than 10 megabytes. The resident who uploaded it, and a parking clerk, are the only people who may retrieve it. The officer's lookup must not include it.

### 6.5 Rejection reason

A clerk who rejects must type a reason at least 15 characters long. Without that reason the application stays Submitted.

### 6.6 Approval, payment, and issuance

An application is Draft while the resident is filling it in. It becomes Submitted when it is accepted onto the clerk queue, and the submission time is recorded in UTC. A clerk may set Submitted to Approved, or to Rejected under section 6.5. Nobody approves or rejects a Draft from the queue, because a Draft is not on the queue.

The resident is sent to CityPay only after the application is Approved. CityPay is the city's existing card processor. It hosts the card page. On success it reports a payment reference and the amount paid. The portal records that reference and that amount. If CityPay does not report success, the portal records no successful payment.

A permit is issued only when the application is Approved and a successful payment is recorded. The permit is then Active. It receives a permit number the portal has not issued before. The expiry date is 365 days after the issue date. Issue and expiry dates are calendar dates.

### 6.7 Renewal

The resident may start a renewal on or after the date 45 days before the expiry date, and on or before the expiry date. The resident must authenticate with the same email address stored on that Active permit. The renewal starts as a new application prefilled with the legal name, residential street address, license plate, and jurisdiction from the current permit. It is reviewed, paid, and issued under the same rules as a first application. The previous permit is unchanged and keeps its own expiry date.

### 6.8 Suspension and revocation

A parking clerk may change an Active permit to Suspended, or to Revoked, only by recording one of these reason codes: eligibility-lapsed, non-payment, fraud, other. A Suspended permit is not an Active result on lookup. A Revoked permit is not an Active result on lookup.

### 6.9 Email

Email goes through CityNotify, the city's existing mail relay, to the email address on the application. Send one message when the application becomes Submitted, one when it becomes Rejected, and one when a permit is issued. If CityNotify does not accept the message, record the failure, try at most 3 times for that event, and do not undo the submission, the rejection, or the issuance. Clerks already phone residents when mail fails.

### 6.10 Sign-on and the handheld

A resident signs in by opening a one-time link the portal sends to the email address the resident typed. The resident does not get a city password. A resident session starts only after that link is opened.

A clerk signs in with the city single sign-on. The group claim `parking-clerk` is the clerk role. A clerk session starts only when that group is asserted. The city identity team already operates that sign-on.

Officers do not sign in to the portal. The handheld team will call a lookup the portal exposes, on the city network. Dana said not to invent the wire format. The handheld team will specify the representation in design. The business content of the lookup is section 6.11.

### 6.11 Lookup contents

The lookup is asked for a license plate and a jurisdiction. It returns the matching permit's zone, status, and expiry date. If nothing matches, the result is not-found. Not-found is not an Active permit. A lookup on a date after the expiry date is not an Active result, even if nobody has edited the permit. The lookup does not return the resident's legal name, residential street address, email address, or proof-of-address file.

The enforcement captain told Dana that up to 50 officers look a plate up at a shift change, and that a lookup slower than 2 seconds will not be used. At least 95 percent of those lookups must come back within 2 seconds.

### 6.12 Card data

The portal must not store the card number or the card security code. The resident enters those only on CityPay's page. This is the same rule as POL-SEC-04 in section 7.

### 6.13 Audit

Each approval, rejection, issuance, suspension, and revocation appends an audit record with the actor, the time in UTC, and the reason or the payment reference.

### 6.14 Monthly totals

For a calendar month, produce three figures for each zone: the number of permits whose issue date falls in that month, the number of permits whose expiry date falls in that month, and the sum of amounts on payments CityPay reported as successful in that month. A payment's zone is the zone on the application that was paid. Who is allowed to request the report was not discussed.

## 7. Policies cited

Dana cited these by name and stated the parts this request must meet. She did not attach the full policy texts.

- POL-ACC-01. City digital accessibility standard. Resident and clerk flows meet WCAG 2.2 Level AA. Resident tasks are completable at a viewport width of 360 CSS pixels with no horizontal scrolling. The tasks she named are entering the application, uploading the file, and being handed off to CityPay.
- POL-BROWSER-02. City browser standard. The current major version and the immediately previous major version of Chrome, Firefox, Safari, and Edge. This applies to the resident flows.
- POL-AVAIL-03. Citizen portal availability. The resident flows and the plate lookup are available for at least 99.5 percent of the minutes in each calendar month, excluding maintenance windows that were published at least 48 hours before they start.
- POL-SEC-04. Card data stays with the certified processor. See section 6.12.

## 8. Volume the sponsor stated

The only volume Dana stated is the lookup volume in section 6.11. She did not state a response time for resident pages and she did not state how many applications arrive in an hour.

## 9. Left open on purpose

- How many Active permits a household may hold. No number exists.
- Which upstream record produces the cleaned address list, and how often Parking Services will refresh it.
- How long proof-of-address files must be kept. Legal has not answered. Dana did not name a person in Legal.
- The response time and peak volume for resident pages.
- How quickly the portal must be restored after an unplanned outage. The 48-hour rule is only the notice for planned maintenance.
- Who may request the monthly totals.

## 10. Not a design

This note does not choose technologies, databases, screen layouts, encryption mechanisms, or the handheld's wire format. It does not authorize a default for any item in section 9.
