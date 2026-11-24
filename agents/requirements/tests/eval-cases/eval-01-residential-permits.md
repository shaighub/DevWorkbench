# Eval 01 — Residential parking permit note

Mechanical checks for the worked package. Run:

```bash
python3 agents/requirements/tests/eval-cases/check_handoff.py
```

`jsonschema` must be installed. The script validates `examples/output-sample/srs.json` against `shared/schemas/srs.schema.json` and `requirement.schema.json`, and checks the links, the single shall, the empty design and test columns, and the refusals below.

## Input

`agents/requirements/examples/input-brd-sample.md`

## Pass when

- The script exits 0.
- Status is `proposed`. Human approval is not recorded. G5 is `ready`, not a forged handoff.
- `FR-016` is Should. The sponsor said the monthly totals may slip. It is not upgraded to Must.
- No shall contains a household cap, a retention period, a restore time, a resident-page time budget, a wire format, a cipher, or fuzzy matching.
- Electric-vehicle-only bays, visitor permits, citations, meter payment, address override, and post-expiry renewal are out of scope with priority Won't, not requirements.
- Open questions OQ-001 through OQ-007 are still `open`, and each names a decision that must not be invented.
- Every shall cites a BRD section that exists, and the shall text in `srs.md` matches `srs.json` and `rtm.csv`.
- Use-case steps and user stories cite requirement ids. They are not the only place a rule appears.
- Nine ISO/IEC 25010:2023 characteristics are present. Safety is not applicable with a reason. Maintainability is not stated, and no index was invented.

## Fail when

- Any shall answers an open question.
- The package status is `approved` or `handed-off`.
- A design element id or a test case id is filled in.
