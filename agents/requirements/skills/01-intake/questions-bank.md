# Question bank

Ask only what the source does not already answer. When you record "answered", cite the span. When you record "unanswered", create an open question. Do not soften a hard question into one the source happens to answer.

A usable answer names a decision, a number, a list, or a person. "We will figure it out" is unanswered.

## Problem and outcome

| Id | Ask | Why | A usable answer | If unanswered |
| --- | --- | --- | --- | --- |
| QB-01 | What is going wrong today, in the sponsor's words? | The problem statement is the root of every need. | A situation a reader can recognize, with who is harmed. | Blocking. Stop. There is nothing to specify. |
| QB-02 | What outcome would make this request successful? | Separates the lack from a guessed solution. | The change in the world, not a technology. | Blocking. |
| QB-03 | What is explicitly not a success of this request? | Stops later skills from widening scope. | A list the sponsor owns. | Non-blocking only if the in-scope list is already tight. Otherwise blocking. |

## People and decisions

| Id | Ask | Why | A usable answer | If unanswered |
| --- | --- | --- | --- | --- |
| QB-04 | Who are the people or roles that touch this, and what does each one do? | Stakeholders and actors. | Names or roles, plus the action they perform. | Blocking if no user is named. |
| QB-05 | Who can accept or reject scope? | Approval and priority disputes. | A person or a role with that right. | Blocking before G5. Non-blocking for drafting if a sponsor is at least named. |
| QB-06 | Who was mentioned but not spoken to? | Stops invented quotes. | A name or a role, and the fact they were absent. | Not applicable when the source lists only people who spoke. |

## Scope

| Id | Ask | Why | A usable answer | If unanswered |
| --- | --- | --- | --- | --- |
| QB-07 | What is in this request? | In-scope list. | Items the sponsor enumerated. | Blocking. |
| QB-08 | What did the sponsor exclude or postpone? | Won't items. | Topics with the sponsor's reason. | Non-blocking. Record nothing extra. Do not build a catalog of imaginary exclusions. |
| QB-09 | Which postponed item must stay out until the sponsor speaks? | Distinguishes Won't from an open question. | "Leave it out" versus "I have not decided". | If the words are missing, treat the topic as an open question, not as a feature. |

## Rules and data

| Id | Ask | Why | A usable answer | If unanswered |
| --- | --- | --- | --- | --- |
| QB-10 | What business rules are already decided, including limits and lists? | The only legal source of shall text. | A rule a tester could apply, with its numbers. | Non-blocking per missing rule. Do not write the shall. |
| QB-11 | What are the statuses of the main records, and which transitions exist? | Prevents a state model invented in design. | Named states and who moves them. | Blocking for any shall that names a status. |
| QB-12 | What must be true before each transition, in boundaries the sponsor accepts? | Inclusive or exclusive limits. | A boundary ("on or before", "no larger than"). | Blocking for that rule. Do not pick the boundary. |
| QB-13 | What information does each actor supply, and what do they get back? | Feeds functions and interfaces without designing them. | A list of business facts. | Blocking for the interface that would otherwise be invented. |
| QB-14 | Which of those facts are forbidden to some actor? | Confidentiality without guessing a control. | Actor, fact, allowed or denied. | Blocking before a confidentiality shall. |

## Priority and quality

| Id | Ask | Why | A usable answer | If unanswered |
| --- | --- | --- | --- | --- |
| QB-15 | Which outcomes fail the release if they are missing, and which may follow? | MoSCoW from the sponsor, not from enthusiasm. | Must versus "can slip" in the sponsor's words. | Leave priority unset and raise a question. Do not default to Must. |
| QB-16 | Which policies did the sponsor cite, and which sentences of them apply? | Keeps 25010 and accessibility tied to a source. | Policy id plus the obligation they stated. | Do not import the rest of the policy from memory. |
| QB-17 | What time, volume, availability, or restore targets did the sponsor state? | Scale, meter, and target. | A measure and a number they said. | Non-blocking question. Do not insert an industry number. |
| QB-18 | What must the product not store, not decide, or not design? | Constraints and implementation freedom. | A prohibition ("do not invent the wire format"). | Not applicable if none was stated. Do not add prohibitions they did not ask for, other than the agent's own rule against invention. |

## Acceptance

| Id | Ask | Why | A usable answer | If unanswered |
| --- | --- | --- | --- | --- |
| QB-19 | Which examples did the sponsor give that a test could replay? | Gherkin fixtures that are not made up. | Concrete values they uttered. | Use a labeled example only for a boundary the rule already fixes (14 characters against a stated minimum of 15). Do not invent a business example and treat it as theirs. |
| QB-20 | What happens on the failure paths the sponsor mentioned? | Extensions and error behavior. | The business outcome of failure, not a retry algorithm they did not state. | Question if a shall would otherwise invent the failure behavior. |

## Using the results

Later skills may quote an "answered" row. They may not convert an unanswered row into a mild shall ("the system shall support configurable retention"). That sentence is an invention with extra words.

If a bank question is not applicable, one sentence is enough. Do not force a question about safety-critical hardware onto a purely administrative request. Skill 06 still records the 25010 safety row as not applicable, with a reason, when you get there.
