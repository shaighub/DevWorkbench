#!/usr/bin/env python3
"""Validate the sample requirements handoff and the local statement rules.

Usage:
    python3 agents/requirements/tests/eval-cases/check_handoff.py

Requires the jsonschema package (Draft 2020-12). The script checks the
worked example at agents/requirements/examples/output-sample/. It does not
call a model. Judgment cases in the sibling Markdown files are for an agent
run, not for this script.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[4]
SAMPLE = ROOT / "agents/requirements/examples/output-sample"
SCHEMA_DIR = ROOT / "shared/schemas"
BRD_PATH = ROOT / "agents/requirements/examples/input-brd-sample.md"
TEMPLATE_RTM = ROOT / "shared/templates/rtm.csv"

CHARACTERISTICS = {
    "functional-suitability",
    "performance-efficiency",
    "compatibility",
    "interaction-capability",
    "reliability",
    "security",
    "maintainability",
    "flexibility",
    "safety",
}

BANNED_IN_STATEMENT = re.compile(
    r"\b(TBD|etc\.|and/or|user-friendly|AES|OAuth|varchar|PostgreSQL|fuzzy|encrypt|household|grace)\b",
    re.IGNORECASE,
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator_for(schema: dict, registry: Registry) -> Draft202012Validator:
    return Draft202012Validator(schema, registry=registry)


def build_registry() -> tuple[dict, dict, Registry]:
    requirement = load_json(SCHEMA_DIR / "requirement.schema.json")
    srs = load_json(SCHEMA_DIR / "srs.schema.json")
    registry = Registry().with_resources(
        [
            (requirement["$id"], Resource.from_contents(requirement)),
            (srs["$id"], Resource.from_contents(srs)),
        ]
    )
    return requirement, srs, registry


def shall_count(text: str) -> int:
    return len(re.findall(r"\bshall\b", text))


def citation_targets(brd: str, citation: str, problems: list[str], where: str) -> None:
    match = re.search(r"BRD §([0-9]+(?:\.[0-9]+)?)", citation)
    if not match:
        return
    token = match.group(1)
    if "." in token:
        if token not in brd:
            problems.append(f"{where}: citation {citation} has no heading or span {token} in the BRD")
        return
    if not re.search(rf"^#{{1,6}} {re.escape(token)}\. ", brd, re.MULTILINE):
        problems.append(f"{where}: citation {citation} has no section heading {token} in the BRD")


def check_package(problems: list[str]) -> None:
    requirement_schema, srs_schema, registry = build_registry()
    srs_validator = validator_for(srs_schema, registry)
    requirement_validator = validator_for(requirement_schema, registry)
    srs = load_json(SAMPLE / "srs.json")
    markdown = (SAMPLE / "srs.md").read_text(encoding="utf-8")
    questions_md = (SAMPLE / "open-questions.md").read_text(encoding="utf-8")
    glossary_md = (SAMPLE / "glossary.md").read_text(encoding="utf-8")
    brd = BRD_PATH.read_text(encoding="utf-8")

    for error in sorted(srs_validator.iter_errors(srs), key=str):
        problems.append(f"srs.json: {error.json_path}: {error.message}")
        if len(problems) > 30:
            return

    if problems:
        return

    requirements = srs["requirements"]
    by_id = {item["id"]: item for item in requirements}
    for item in requirements:
        for error in requirement_validator.iter_errors(item):
            problems.append(f"{item['id']}: {error.json_path}: {error.message}")
        if shall_count(item["statement"]) != 1:
            problems.append(f"{item['id']}: statement must contain shall exactly once")
        if re.search(r"\b(should|may)\b", item["statement"], re.IGNORECASE):
            problems.append(f"{item['id']}: statement uses should or may")
        if BANNED_IN_STATEMENT.search(item["statement"]):
            problems.append(f"{item['id']}: statement contains a banned or unsourced token")
        if item["statement"] not in markdown:
            problems.append(f"{item['id']}: statement is missing from srs.md")
        for criterion in item["acceptanceCriteria"]:
            prefix = f"AC-{item['id']}-"
            if not criterion["id"].startswith(prefix):
                problems.append(f"{criterion['id']}: does not belong to {item['id']}")
        for citation in item["source"]["citations"]:
            citation_targets(brd, citation, problems, item["id"])

    need_ids = {need["id"] for need in srs["needs"]}
    for need in srs["needs"]:
        if re.search(r"\bshall\b", need["statement"]):
            problems.append(f"{need['id']}: a need must not be a shall statement")
        for citation in need["citations"]:
            citation_targets(brd, citation, problems, need["id"])
    covered = {need_id for item in requirements for need_id in item["source"]["needIds"]}
    missing = sorted(need_ids - covered)
    if missing:
        problems.append(f"needs without requirements: {missing}")
    orphans = sorted(
        need_id
        for item in requirements
        for need_id in item["source"]["needIds"]
        if need_id not in need_ids
    )
    if orphans:
        problems.append(f"orphan need ids: {orphans}")

    stakeholder_ids = {row["id"] for row in srs["stakeholders"]}
    for row in srs["stakeholders"]:
        if not row["namedInSource"]:
            problems.append(f"{row['id']}: stakeholder was not named in the source")
        if row["interviewed"] and row["id"] != "STK-007":
            problems.append(f"{row['id']}: only the sponsor was interviewed")

    use_case_ids = set()
    for use_case in srs["useCases"]:
        use_case_ids.add(use_case["id"])
        if use_case["primaryActorId"] not in stakeholder_ids:
            problems.append(f"{use_case['id']}: unknown actor")
        linked = set(use_case["requirementIds"])
        for step in use_case["mainSuccessScenario"]:
            linked.update(step["requirementIds"])
        for extension in use_case["extensions"]:
            linked.update(extension["requirementIds"])
        unknown = sorted(linked - set(by_id))
        if unknown:
            problems.append(f"{use_case['id']}: unknown requirements {unknown}")

    for story in srs["userStories"]:
        unknown = [rid for rid in story["requirementIds"] if rid not in by_id]
        if unknown:
            problems.append(f"{story['id']}: unknown requirements {unknown}")

    for item in requirements:
        for use_case_id in item.get("useCaseIds", []):
            if use_case_id not in use_case_ids:
                problems.append(f"{item['id']}: dangling {use_case_id}")

    seen = set()
    for row in srs["qualityModelCoverage"]:
        seen.add(row["characteristic"])
        for rid in row["requirementIds"]:
            if rid not in by_id:
                problems.append(f"coverage {row['characteristic']}: unknown {rid}")
        for qid in row["openQuestionIds"]:
            if qid not in {q['id'] for q in srs["openQuestions"]}:
                problems.append(f"coverage {row['characteristic']}: unknown {qid}")
    if seen != CHARACTERISTICS:
        problems.append(f"quality coverage is {sorted(seen)}")

    question_ids = []
    for question in srs["openQuestions"]:
        question_ids.append(question["id"])
        if question["id"] not in questions_md:
            problems.append(f"{question['id']}: missing from open-questions.md")
        if question["status"] != "open":
            problems.append(f"{question['id']}: sample questions stay open")
        for citation in question["citations"]:
            citation_targets(brd, citation, problems, question["id"])
    if any(q["blocking"] for q in srs["openQuestions"]):
        problems.append("sample still has a blocking question, so G5 must not be ready")
    if srs["approval"]["blockingOpenQuestionIds"]:
        problems.append("blockingOpenQuestionIds is not empty")

    for entry in srs["glossary"]:
        if entry["term"] not in glossary_md:
            problems.append(f"glossary term missing from markdown: {entry['term']}")

    if srs["meta"]["status"] != "proposed" or srs["approval"]["status"] != "proposed":
        problems.append("sample status must stay proposed")
    if srs["approval"]["humanApproval"]["recorded"] or srs["approval"]["residualRiskAccepted"]:
        problems.append("the agent recorded a human approval or accepted residual risk")
    gate_results = {gate["id"]: gate["result"] for gate in srs["approval"]["gates"]}
    if gate_results != {"G1": "pass", "G2": "pass", "G3": "pass", "G4": "pass", "G5": "ready"}:
        problems.append(f"unexpected gate results: {gate_results}")
    if not srs["traceability"]["idFreeze"]:
        problems.append("identifiers are not frozen")
    if srs["scope"]["assumptions"]:
        problems.append("the sample should not need assumptions")

    text = json.dumps(srs)
    if re.search(r"\b(AES|OAuth|PostgreSQL|varchar)\b", text):
        problems.append("package names a mechanism the source did not")
    if "electric-vehicle" not in json.dumps(srs["scope"]["outOfScope"]).lower() and "Electric-vehicle" not in json.dumps(srs["scope"]["outOfScope"]):
        problems.append("EV bays are not recorded as out of scope")

    header = next(csv.reader(TEMPLATE_RTM.open(encoding="utf-8")))
    with (SAMPLE / "rtm.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if rows[0] != header:
        problems.append("rtm.csv header does not match the template")
    body = rows[1:]
    if len(body) != len(requirements):
        problems.append(f"rtm row count {len(body)} != requirements {len(requirements)}")
    for row, item in zip(body, requirements):
        padded = row + [""] * (len(header) - len(row))
        record = dict(zip(header, padded))
        if record["Requirement ID"] != item["id"] or record["Statement"] != item["statement"]:
            problems.append(f"rtm row does not match {item['id']}")
        if record["Design Element ID"] or record["Test Case ID"]:
            problems.append(f"{item['id']}: consumer column was pre-filled")
        if record["Priority"] != item["priority"]:
            problems.append(f"{item['id']}: RTM priority drift")

    # Sample-specific refusals.
    if reqs_priority(by_id, "FR-016") != "Should":
        problems.append("FR-016 must stay Should; the sponsor allowed it to slip")
    joined_questions = questions_md.lower()
    for token in ("household", "retention", "restor", "address list", "resident", "monthly", "one-time"):
        if token not in joined_questions:
            problems.append(f"open-questions.md does not mention {token}")
    if any("household" in item["statement"].lower() for item in requirements):
        problems.append("a shall invented a household rule")


def reqs_priority(by_id: dict, rid: str) -> str:
    return by_id[rid]["priority"]


def self_test(problems: list[str]) -> None:
    if shall_count("The portal shall record one fact.") != 1:
        problems.append("self-test: shall counter missed a single shall")
    if shall_count("The portal shall do this and shall do that.") != 2:
        problems.append("self-test: shall counter missed a double shall")
    if not BANNED_IN_STATEMENT.search("The portal shall encrypt files with AES."):
        problems.append("self-test: banned-token scan missed AES")


def main() -> int:
    problems: list[str] = []
    self_test(problems)
    check_package(problems)
    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("sample handoff passed schema and consistency checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
