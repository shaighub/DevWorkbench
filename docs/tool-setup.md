# Set up DevWorkbench in an editor

Skill files under `agents/<agent>/skills/` are the source of truth. `scripts/setup.py` discovers every agent that has `agent/orchestrator.md` and skill directories, then publishes the files that Claude Code, Cursor, and OpenCode actually read. Generated files are listed in `.gitignore`. The sources, the templates, and the scripts are what you commit.

The setup needs Python 3.8 or newer on `PATH`. It uses the standard library only.

## Windows

Open `cmd.exe` in the repository root and run:

```bat
setup.cmd all
```

`setup.cmd` is a batch file. It runs `py -3` and, when the Python launcher is not installed, `python`. It does not use PowerShell.

The first run on Windows copies each skill file. Windows symlinks need Developer Mode or an elevated prompt, so the script does not try them unless you pass `--link`. After you edit, add, or rename a file inside a skill, refresh the copies:

```bat
setup.cmd --sync
```

A plain re-run of `setup.cmd all` refreshes them too. `--sync` with no target repeats the mode recorded in `.devworkbench/setup-manifest.json`.

Install one tool only when that is the tool you use:

```bat
setup.cmd claude
setup.cmd cursor
setup.cmd opencode
```

`--copy` and `--link` choose the mode for that run. A later re-run keeps the recorded mode until you pass the other flag.

Remove the published files with:

```bat
setup.cmd --clean
```

`setup.cmd claude --clean` removes the Claude Code files and leaves Cursor and OpenCode in place. `CLAUDE.md` and `AGENTS.md` are removed only when no remaining target still uses that file.

## macOS, Linux, and Git Bash

```sh
./setup.sh all
```

If the executable bit did not survive checkout, `sh setup.sh all` does the same thing. The first run symlinks each skill file and falls back to copying if the filesystem refuses the link. Refresh copies with `./setup.sh --sync`. Linked files already show source edits; re-run setup after you add or rename a file inside a skill directory.

## Open the repository and run an agent

Open the repository in VS Code with the tool you installed. In that tool's chat, run:

```text
/requirements
```

and give it the high-level need (a paragraph, a business request, a ticket, or a transcript). The requirements command reads `agents/requirements/agent/orchestrator.md` and runs the ten skills in order.

The same command exists for every later agent under `agents/<name>/`. The command name is the agent directory name.

## What each target publishes

| Target | Always-on instructions | Skills | Command |
| --- | --- | --- | --- |
| `claude` | `CLAUDE.md` | `.claude/skills/<skill>/SKILL.md` | `.claude/commands/<agent>.md`, invoked as `/<agent>` |
| `cursor` | `AGENTS.md` | `.cursor/skills/<skill>/SKILL.md` | `.cursor/commands/<agent>.md`, invoked as `/<agent>` |
| `opencode` | `AGENTS.md` | `.opencode/skills/<skill>/SKILL.md` | `.opencode/commands/<agent>.md`, invoked as `/<agent>` |

`CLAUDE.md` and `AGENTS.md` are generated from `shared/tool-adapters/instructions.md.tmpl`, so the procedure text is the same file twice. It tells the tool to run skills in order, stop at a failed gate, loop validation gaps to intake, never guess facts, and set status only as far as `proposed`.

The published skill directory is a real folder whose name is the skill id (`requirements-01-intake`). Cursor requires that folder name to match the frontmatter `name`. Inside it, each file is a symlink or a copy of the file in `agents/<agent>/skills/<directory>/`, including sibling notes such as `questions-bank.md`. The source folder keeps its short name (`01-intake`).

GitHub Copilot and other AGENTS.md readers use the `AGENTS.md` produced by `cursor`, `opencode`, or `all`. Copilot Chat in VS Code, the Copilot cloud agent, and Copilot CLI all read that file. Ask Copilot to follow `AGENTS.md` and run the requirements orchestrator on the need. This setup does not add a Copilot slash command; the custom-instructions docs confirm `AGENTS.md`, and they do not document a project command directory for this repository to fill.

Running `all` publishes every column. Cursor also discovers `.claude/skills/` for compatibility, so a checkout that installed both can list the same skill twice in Cursor. OpenCode loads `.opencode/skills/` ahead of `.claude/skills/` for the same id, so it keeps a single skill. Install the one target you use when you want a single copy.

## Skill names

Each `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: requirements-01-intake
description: >
  When to use the skill.
---
```

`name` is `<agent-directory>-<skill-directory>`, lowercase kebab-case, unique across the repository, and at most 64 characters. `requirements-01-intake` is the skill in `agents/requirements/skills/01-intake/`. `description` is required. Claude Code, Cursor, and OpenCode all use those two fields. The same name is stored on the skill entry in `agent/config.yaml`.

## Add an agent

Create `agents/<id>/agent/orchestrator.md`, optional `agents/<id>/agent/config.yaml`, and `agents/<id>/skills/<nn-name>/SKILL.md`. The directory `<id>` is the slash command. Re-run setup. The publisher does not have a list of agents in code.

When `config.yaml` exists, its `agent.id` matches the directory, and its `skills` list matches the skill directories. The `name` on each skill matches the frontmatter.

## Add a tool adapter

Adapters live in `shared/tool-adapters/adapters.json`. A target names the three paths that tool reads. Use `null` when the tool has no equivalent.

```json
"my-tool": {
  "instruction": "AGENTS.md",
  "skills": ".my-tool/skills",
  "commands": ".my-tool/commands"
}
```

Then:

1. Add anchored `.gitignore` rules for every new path. Directory rules need a trailing slash (`/.my-tool/`). File rules name the file (`/AGENTS.md` already covers a shared instruction file).
2. Leave `instructions` and `command` unset to reuse `instructions.md.tmpl` and `command.md.tmpl`. Set either key to another file under `shared/tool-adapters/` when that tool needs different text. Two adapters that write the same path must produce the same bytes.
3. Run `python3 scripts/check_setup.py`. The `all` target picks the new adapter up by reading the JSON.

Paths are relative to the repository root. The script refuses `..`.

## Check

```bat
py -3 scripts\check_setup.py
py -3 agents\requirements\tests\eval-cases\check_handoff.py
```

```sh
python3 scripts/check_setup.py
python3 agents/requirements/tests/eval-cases/check_handoff.py
```

`check_setup.py` copies the repository to a temp directory, runs setup for each target, and checks that the published files exist, that skill bytes resolve to the source, that a second run is stable, that `--clean` removes only what setup wrote, and that a second sample agent is discovered without a code change. `check_handoff.py` validates the sample requirements package and needs the `jsonschema` package.

## Conventions checked, and what was not run

The paths above were taken from the tool docs while this publisher was written:

- Claude Code skills and commands: [Extend Claude with skills](https://code.claude.com/docs/en/skills) and [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory). Project skills are `.claude/skills/<name>/SKILL.md`. A file `.claude/commands/<name>.md` is `/<name>`. `$ARGUMENTS` is the command argument. When `CLAUDE.md` and `AGENTS.md` both exist, Claude Code reads `CLAUDE.md` by default ([memory](https://code.claude.com/docs/en/memory)).
- Cursor skills: [Agent Skills](https://cursor.com/docs/skills). Project skills are `.cursor/skills/<name>/SKILL.md` (`.agents/skills/` is the other project root). `name` and `description` are required, and `name` must match the parent folder. `AGENTS.md` is the plain project instruction file ([Rules](https://cursor.com/docs/rules)).
- Cursor commands: the [Cursor 1.6 changelog](https://cursor.com/changelog/1-6) stores project commands at `.cursor/commands/<name>.md` and invokes them with `/` in Agent chat. [Customize Cursor](https://cursor.com/docs/customize-cursor) describes commands as markdown invoked with `/` and documents the home directory `~/.cursor/commands/`. The current skills page still treats workspace slash commands as real files (`/migrate-to-skills` converts them). A current docs table that repeats the project path `.cursor/commands/` was not found, and `$ARGUMENTS` is not documented for Cursor commands. The command text tells the agent to use the rest of the user message when the token is not expanded.
- OpenCode: [Instructions](https://opencode.ai/docs/instructions/), [Skills](https://opencode.ai/docs/skills/), and [Commands](https://opencode.ai/docs/commands/). `AGENTS.md` wins over `CLAUDE.md` in the same directory. Skills are `.opencode/skills/<id>/SKILL.md`. The id is the directory name; frontmatter `name` is a display label, and the portability guidance says to keep them aligned. Commands are `.opencode/commands/<name>.md` and expand `$ARGUMENTS`.
- GitHub Copilot: [repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) and the [support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support). `AGENTS.md` is the agent-instruction file for Copilot Chat in VS Code, the cloud agent, and Copilot CLI. Copilot CLI also reads `CLAUDE.md`, so a machine that generated both can see the same procedure twice on that surface. `.github/copilot-instructions.md` is a third channel and is not generated.

Claude Code, Cursor, and OpenCode were not launched in this environment, so file discovery is checked on disk and not by those products loading a session.
