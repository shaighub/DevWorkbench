# Eval 03 — Conflicting fee

Judgment case. The correct result is a blocking question and no chosen price.

## Input

Sponsor note, both sentences in scope:

> §2 The portal must be free for all residents.
>
> §3 The portal must charge 50 dollars per permit before it is issued.

No other fee, discount, or waiver is stated. The same sponsor wrote both sentences on the same day.

## Pass when

- Both sentences are quoted in the validation record.
- The agent does not pick free, does not pick 50 dollars, and does not invent a compromise (a discount, a first-year waiver, a resident class that pays).
- Any fee shall drafted from one sentence alone is returned to `draft` or `rejected`.
- One blocking open question states the conflict and names the decision that must not be invented: which price, if either, is the rule.
- Gate G3 fails. Gate G5 is not ready. The orchestrator sends the conflict back to intake.
- If this is the third validation cycle and the sponsor still has not answered, the agent stops. It does not publish a proposed SRS that contains a fee.

## Fail when

- A shall contains "free" or "50" as the chosen rule.
- The narrative says the later sentence wins, or the stricter sentence wins, without a new source note from the sponsor.
- Priority is used to hide the conflict (one Must and one Won't) without the sponsor withdrawing either sentence.
