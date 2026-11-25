# DevWorkbench

DevWorkbench is a workbench of AI agents for the software lifecycle. Each agent owns one phase, runs a fixed sequence of skills, and hands a validated package to the next phase. Agents do not invent facts the source did not state. What they cannot close becomes an open question, not a guess.

This repository currently contains one agent: **requirements**. Design, build, test, release, and operate are named in the roadmap so the requirements package has a defined consumer. Those agents are not built yet.

The architecture of the workbench, including what is still a target, is in [docs/architecture.md](docs/architecture.md).

The requirements agent is independent of any particular bot product or agent framework. The procedure is Markdown. Any assistant that can read the skill files and write the output folder can run it.

## Set up a coding tool

`agents/<agent>/skills/` stays the source of truth. One setup command publishes those skills to Claude Code, Cursor, or OpenCode. Windows uses a batch file and does not need PowerShell.

On Windows, from `cmd.exe` in this repository:

```bat
setup.cmd all
```

`setup.cmd` runs `py -3` and falls back to `python`. The first Windows run copies the skill files. After you edit a skill, refresh the copies with `setup.cmd --sync`.

On macOS, Linux, or Git Bash:

```sh
./setup.sh all
```

That run symlinks the skill files so an edit shows up immediately, and it copies them if a symlink cannot be created. Targets are `claude`, `cursor`, `opencode`, and `all`.

Open the repository in VS Code and run `/requirements` followed by the high-level need. GitHub Copilot and other AGENTS.md readers pick up `AGENTS.md` from a `cursor`, `opencode`, or `all` setup. The file list, the refresh and clean commands, and the steps for adding another tool are in [docs/tool-setup.md](docs/tool-setup.md).

## Roadmap

| Phase | Agent | What it will take | What it will produce | State |
| --- | --- | --- | --- | --- |
| Requirements | `agents/requirements/` | A high-level need | A proposed SRS, traceability matrix, glossary, and open questions | This repository |
| Design | not started | An approved SRS | Allocation of each requirement to elements, interface representation inside the SRS business data, design column of the matrix | Planned |
| Build | not started | Approved design allocation | An implementation that traces to requirement ids and does not add behavior | Planned |
| Test | not started | SRS acceptance criteria and a build | A result for each Gherkin criterion, test column of the matrix | Planned |
| Release | not started | Test evidence for the Must set | A release note that still lists unanswered questions | Planned |
| Operate | not started | A released system | Feedback that re-enters requirements intake | Planned |

The architecture is in [docs/architecture.md](docs/architecture.md). Gates, entry and exit criteria, and the skill mapping are in [docs/sdlc-gates.md](docs/sdlc-gates.md). The file contract between agents is in [docs/agent-handoff.md](docs/agent-handoff.md).

## Standards the requirements agent applies

- **ISO/IEC/IEEE 29148:2018.** SRS outline (clause 9.6) and the characteristics of a good requirement (clause 5.2). Binding product statements use **shall**. One obligation per statement.
- **ISO/IEC 25010:2023.** The nine product-quality characteristics for non-functional requirements. Usability in the 2011 edition is interaction capability here. Portability in the 2011 edition is flexibility here. Safety is its own characteristic.
- **MoSCoW.** Must, Should, Could, Won't, stored as a priority attribute. Won't is an exclusion. The statement does not switch to should or may to express priority.
- **Gherkin.** Given / When / Then acceptance criteria, one or more per requirement, for the test phase to pick up.

## How to run the requirements agent

Set the editor up with [docs/tool-setup.md](docs/tool-setup.md), then run `/requirements` and the high-level need. The steps below are the procedure that command follows.

1. Put the high-level request somewhere durable. Do not let the agent "improve" it in place. The sample request is [agents/requirements/examples/input-brd-sample.md](agents/requirements/examples/input-brd-sample.md).
2. Give the assistant [agents/requirements/agent/orchestrator.md](agents/requirements/agent/orchestrator.md) and [agents/requirements/agent/config.yaml](agents/requirements/agent/config.yaml) as its procedure.
3. Tell it the engagement id and the output directory, normally `agents/requirements/output/<engagement-id>/`.
4. Let it run the ten skills in order. It must stop at a failed gate. It must write unknowns to `open-questions.md` instead of choosing a plausible answer.
5. Review the proposed package: `srs.md`, `srs.json`, `rtm.csv`, `glossary.md`, `open-questions.md`.
6. A person records approval. The agent sets status only as far as `proposed`. Design does not start from a proposed package. See [docs/agent-handoff.md](docs/agent-handoff.md).

Skill files are the steps. Each has YAML front matter (`name`, `description`) and the same sections: Purpose, Inputs, Method, Output format, Quality checklist, Gate. The `name` is `<agent>-<skill-directory>` in kebab-case, for example `requirements-01-intake`. Shared shapes are [shared/schemas/requirement.schema.json](shared/schemas/requirement.schema.json) and [shared/schemas/srs.schema.json](shared/schemas/srs.schema.json). The empty narrative skeleton is [shared/templates/srs-ieee29148.md](shared/templates/srs-ieee29148.md).

## What the agent will not do

- It will not write a shall that has no citation in the source.
- It will not pick a side in a contradiction. Both statements come out, and a blocking question goes in.
- It will not turn a user story or a use-case step into new behavior.
- It will not fill performance, security, or retention numbers from habit.
- It will not invent an API, a schema, or a control the source did not require. Business data and the deferral to design are recorded instead.
- It will not mark the SRS handed off. That is a human signature.
- It will not answer `open-questions.md` while doing design, build, or test. Those questions come back to this agent.

## Layout

```text
DevWorkbench/
  README.md
  setup.cmd
  setup.sh
  docs/architecture.md
  docs/sdlc-gates.md
  docs/agent-handoff.md
  docs/tool-setup.md
  scripts/setup.py
  scripts/check_setup.py
  shared/schemas/requirement.schema.json
  shared/schemas/srs.schema.json
  shared/templates/srs-ieee29148.md
  shared/templates/rtm.csv
  shared/templates/glossary.md
  shared/tool-adapters/
  agents/requirements/
    agent/orchestrator.md
    agent/config.yaml
    skills/01-intake/ … 10-srs-assembly/
    examples/input-brd-sample.md
    examples/output-sample/
    output/.gitkeep
    tests/eval-cases/
```

`output/` stays empty in git. Generated engagements are local working files. The sample under `examples/output-sample/` is the reference package for the parking-permit request: a proposed SRS a later phase can read, with the questions the source left open still open.

## Example

The sample source is a working note from a city parking sponsor. It states rules, limits, exclusions, and the topics the sponsor refused to decide: a household cap, address-list provenance, file retention, resident-page performance, restore time, and who may request the monthly report. The sample also leaves the sign-in link's mail channel open, because the note never names it. Shall statements do not answer those questions. Status is `proposed`.

Check the sample package:

```bash
python3 scripts/check_setup.py
python3 agents/requirements/tests/eval-cases/check_handoff.py
```

The script validates `srs.json` against the shared schemas and checks identifier consistency, a single shall per statement, source citations, empty design and test columns, and the refusal to invent the closed topics. `jsonschema` is required (`pip install jsonschema`). Two further eval cases are judgment tests for a sparse request and a contradiction. They have no gold SRS, because the correct result is questions rather than requirements.

## GitHub tracking

Requirements work is tracked as five milestones (G1–G5) and one issue per skill. Milestone titles and bodies are in [docs/sdlc-gates.md](docs/sdlc-gates.md). Whether this repository already has those objects depends on the credentials that created it. If they are missing, the milestone section of that document is the text to create.
