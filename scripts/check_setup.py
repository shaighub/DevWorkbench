#!/usr/bin/env python3
"""Install each tool adapter in a temp copy and check the published files.

Stdlib only. Exits 0 when setup is safe to re-run and the skills resolve.

    python3 scripts/check_setup.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ("in order", "failed gate", "intake", "Never guess", "proposed")


def load_setup():
    path = ROOT / "scripts" / "setup.py"
    spec = importlib.util.spec_from_file_location("devworkbench_setup", path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


setup = load_setup()


def run(cmd: list[str], cwd: Path, ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if ok and result.returncode != 0:
        raise AssertionError(
            f"{cmd} -> {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def copy_repo(dst: Path) -> None:
    skip_root = {".git", ".claude", ".cursor", ".opencode", ".devworkbench", "CLAUDE.md", "AGENTS.md"}

    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored = {"__pycache__", ".git"}
        if Path(directory).resolve() == ROOT.resolve():
            ignored |= skip_root
        return {name for name in names if name in ignored}

    shutil.copytree(ROOT, dst, ignore=ignore)


def skill_snapshot(root: Path, relative: str) -> list[tuple[str, str, bytes | str]]:
    path = root / relative
    rows: list[tuple[str, str, bytes | str]] = []
    if not path.exists() and not path.is_symlink():
        return rows
    files = [path] if path.is_file() or path.is_symlink() else sorted(item for item in path.rglob("*"))
    for item in files:
        rel = item.relative_to(root).as_posix()
        if item.is_symlink():
            rows.append((rel, "link", os.readlink(item)))
        elif item.is_file():
            rows.append((rel, "file", item.read_bytes()))
    return rows


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"ok {message}")


def check_sources() -> None:
    try:
        agents = setup.discover(ROOT)
    except SystemExit as exc:
        raise AssertionError(str(exc)) from exc
    by_id = {agent.id: agent for agent in agents}
    require("requirements" in by_id, "requirements agent discovered")
    requirements = by_id["requirements"]
    names = [skill.name for skill in requirements.skills]
    disk = sorted(
        path.name
        for path in (ROOT / "agents" / "requirements" / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    require(names == [f"requirements-{name}" for name in disk], "skill names follow <agent>-<directory>")
    require("requirements-01-intake" in names and len(names) >= 10, "requirements publishes the ten skills")
    intake = (ROOT / "agents/requirements/skills/01-intake/SKILL.md").read_text(encoding="utf-8")
    front = setup.parse_frontmatter(intake)
    require(
        front["name"] == "requirements-01-intake" and front["description"].startswith("Use at the start"),
        "intake frontmatter parses",
    )
    require(
        setup.mode_for(False, False, None, "win32") == "copy"
        and setup.mode_for(False, False, None, "linux") == "link"
        and setup.mode_for(False, False, "link", "win32") == "link"
        and setup.mode_for(True, False, "link", "linux") == "copy"
        and setup.mode_for(False, True, "copy", "win32") == "link",
        "mode defaults to copy on Windows and keeps a recorded mode",
    )


def check_remove_path(tmp: Path) -> None:
    src = tmp / "source-skill"
    src.mkdir(parents=True)
    (src / "SKILL.md").write_text("keep\n", encoding="utf-8", newline="\n")
    link = tmp / "linked-skill"
    try:
        link.symlink_to(src, target_is_directory=True)
    except OSError as exc:
        print(f"ok directory symlink safety skipped ({exc})")
        return
    setup.remove_path(link)
    require(not link.exists() and (src / "SKILL.md").read_text(encoding="utf-8") == "keep\n", "remove_path unlinks a directory symlink and leaves the target")


def check_wrappers() -> None:
    cmd = (ROOT / "setup.cmd").read_bytes()
    shell = (ROOT / "setup.sh").read_bytes()
    require(b"\r\n" in cmd and b"\n" not in cmd.replace(b"\r\n", b""), "setup.cmd is CRLF")
    require(b"py -3" in cmd and b"python" in cmd and b"powershell" not in cmd.lower(), "setup.cmd calls py -3 and falls back to python")
    require(b"\r" not in shell and shell.startswith(b"#!"), "setup.sh is LF")
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    require("*.cmd text eol=crlf" in attributes and "*.sh text eol=lf" in attributes, ".gitattributes pins cmd and sh line endings")
    patterns = setup.gitignore_patterns(ROOT)
    adapters = json.loads((ROOT / "shared/tool-adapters/adapters.json").read_text(encoding="utf-8"))
    for spec in adapters["targets"].values():
        if spec["instruction"]:
            require(setup.gitignore_covers(spec["instruction"], patterns), f"gitignore covers {spec['instruction']}")
        if spec["skills"]:
            require(
                setup.gitignore_covers(spec["skills"] + "/example", patterns),
                f"gitignore covers {spec['skills']}/",
            )
        if spec["commands"]:
            require(
                setup.gitignore_covers(spec["commands"] + "/example.md", patterns),
                f"gitignore covers {spec['commands']}/",
            )
    require(
        setup.gitignore_covers(".devworkbench/setup-manifest.json", patterns),
        "gitignore covers the setup manifest",
    )
    require(not (ROOT / "CLAUDE.md").exists() and not (ROOT / "AGENTS.md").exists(), "working tree has no generated instruction files")
    shell_bin = shutil.which("sh")
    if shell_bin is None:
        print("ok shell wrapper execution skipped")
        return
    result = run([shell_bin, "setup.sh"], ROOT, ok=False)
    require(result.returncode != 0 and "target" in result.stderr.lower(), "setup.sh with no target fails")
    require(not (ROOT / "CLAUDE.md").exists(), "failed setup.sh writes nothing")


def setup_py(tmp: Path, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, "scripts/setup.py", *args], tmp, ok=ok)


def published_skill(tmp: Path, tool_root: str, name: str = "requirements-01-intake") -> Path:
    return tmp / tool_root / "skills" / name / "SKILL.md"


def check_rules(text: str, label: str) -> None:
    for phrase in RULES:
        require(phrase in text, f"{label} contains {phrase!r}")


def check_claude_copy(tmp: Path) -> None:
    copy_repo(tmp)
    (tmp / "CLAUDE.md").write_text("# local notes\n", encoding="utf-8", newline="\n")
    refused = setup_py(tmp, "claude", "--copy", ok=False)
    require(refused.returncode != 0 and "CLAUDE.md" in refused.stderr, "hand-written CLAUDE.md is left in place")
    require((tmp / "CLAUDE.md").read_text(encoding="utf-8").startswith("# local notes"), "hand-written CLAUDE.md is unchanged")
    require(not (tmp / ".claude").exists(), "refused setup publishes no skills")
    (tmp / "CLAUDE.md").unlink()

    setup_py(tmp, "claude", "--copy")
    source = tmp / "agents/requirements/skills/01-intake"
    skill = published_skill(tmp, ".claude")
    require(skill.is_file() and not skill.is_symlink(), "claude --copy writes a real SKILL.md")
    require(skill.parent.name == "requirements-01-intake" and not skill.parent.is_symlink(), "published folder name is the skill id")
    require(skill.read_bytes() == (source / "SKILL.md").read_bytes(), "copied SKILL.md matches the source")
    require(
        (skill.parent / "questions-bank.md").read_bytes() == (source / "questions-bank.md").read_bytes(),
        "sibling questions-bank.md is copied with the skill",
    )
    command = (tmp / ".claude/commands/requirements.md").read_text(encoding="utf-8")
    require("agents/requirements/agent/orchestrator.md" in command and "$ARGUMENTS" in command, "claude command points at the orchestrator")
    check_rules(command, "claude command")
    instructions = (tmp / "CLAUDE.md").read_text(encoding="utf-8")
    check_rules(instructions, "CLAUDE.md")
    require("requirements-01-intake" in instructions and "Requirements Agent" in instructions, "CLAUDE.md lists the requirements skills")
    require(b"\r" not in (tmp / "CLAUDE.md").read_bytes(), "CLAUDE.md is LF")

    marker = "\n<!-- refresh-probe -->\n"
    source_skill = source / "SKILL.md"
    source_skill.write_bytes(source_skill.read_bytes() + marker.encode("utf-8"))
    require(marker not in skill.read_text(encoding="utf-8"), "a copy stays stale until setup runs again")
    (skill.parent / "extra.txt").write_text("stale\n", encoding="utf-8", newline="\n")
    outside = tmp / "outside-keep"
    outside.mkdir()
    (outside / "keep.txt").write_text("keep\n", encoding="utf-8", newline="\n")
    alias = skill.parent / "alias"
    try:
        alias.symlink_to(outside, target_is_directory=True)
    except OSError:
        alias = None
    before = skill_snapshot(tmp, ".claude/skills/requirements-01-intake")
    setup_py(tmp, "claude")
    skill = published_skill(tmp, ".claude")
    require(not skill.is_symlink() and marker in skill.read_text(encoding="utf-8"), "re-run keeps copy mode and refreshes bytes")
    require(not (skill.parent / "extra.txt").exists(), "re-run removes a stale extra file")
    if alias is not None:
        require((outside / "keep.txt").is_file() and not alias.exists(), "re-run drops a directory symlink without deleting its target")
    setup_py(tmp, "--sync")
    after = skill_snapshot(tmp, ".claude/skills/requirements-01-intake")
    require(before != after or marker in skill.read_text(encoding="utf-8"), "sync refreshed the copy")
    second = skill_snapshot(tmp, ".claude")
    setup_py(tmp, "--sync")
    require(skill_snapshot(tmp, ".claude") == second, "a second sync is stable")

    manifest = tmp / ".devworkbench/setup-manifest.json"
    manifest.unlink()
    setup_py(tmp, "--clean")
    require(not skill.exists() and (source / "SKILL.md").is_file(), "clean without a manifest removes managed copies and keeps the source")
    require(not (tmp / "CLAUDE.md").exists(), "clean removes generated CLAUDE.md")


def check_links(tmp: Path) -> None:
    copy_repo(tmp)
    result = setup_py(tmp, "cursor")
    skill = published_skill(tmp, ".cursor")
    source = tmp / "agents/requirements/skills/01-intake/SKILL.md"
    if skill.is_symlink():
        require(skill.resolve() == source.resolve(), "cursor link resolves to the source skill")
        source.write_bytes(source.read_bytes() + b"\n<!-- live -->\n")
        require("<!-- live -->" in skill.read_text(encoding="utf-8"), "a linked skill shows a source edit immediately")
    else:
        require(
            sys.platform == "win32" or "copying" in result.stderr.lower(),
            "cursor falls back to copy when symlinks are unavailable",
        )
        require(skill.read_bytes() == source.read_bytes(), "fallback copy matches the source")
    agents = (tmp / "AGENTS.md").read_text(encoding="utf-8")
    check_rules(agents, "AGENTS.md")
    require((tmp / ".cursor/commands/requirements.md").is_file(), "cursor command file exists")


def check_all_and_clean(tmp: Path) -> None:
    copy_repo(tmp)
    run(["git", "init", "-b", "main"], tmp)
    run(["git", "config", "user.email", "devworkbench-check@example.com"], tmp)
    run(["git", "config", "user.name", "DevWorkbench Check"], tmp)
    run(["git", "add", "-A"], tmp)
    run(["git", "commit", "-m", "base"], tmp)
    setup_py(tmp, "all", "--copy")
    claude = (tmp / "CLAUDE.md").read_bytes()
    agents = (tmp / "AGENTS.md").read_bytes()
    require(claude == agents, "CLAUDE.md and AGENTS.md are the same bytes")
    for tool in (".claude", ".cursor", ".opencode"):
        skill = published_skill(tmp, tool)
        require(skill.is_file() and not skill.is_symlink(), f"{tool} skill exists as a copy")
        command = tmp / tool / "commands" / "requirements.md"
        require(command.is_file(), f"{tool} requirements command exists")
    status = run(["git", "status", "--porcelain"], tmp)
    require(status.stdout.strip() == "", "setup leaves a clean git status")
    setup_py(tmp, "cursor", "--clean")
    require(not (tmp / ".cursor").exists(), "cursor --clean removes .cursor")
    require((tmp / "AGENTS.md").is_file() and (tmp / "CLAUDE.md").is_file(), "shared AGENTS.md stays while OpenCode remains")
    require((tmp / ".opencode/skills/requirements-01-intake/SKILL.md").is_file(), "opencode skills stay")
    setup_py(tmp, "opencode", "--clean")
    require(not (tmp / "AGENTS.md").exists() and (tmp / "CLAUDE.md").is_file(), "AGENTS.md goes away with the last reader")
    setup_py(tmp, "--clean")
    require(
        not (tmp / "CLAUDE.md").exists()
        and not (tmp / ".claude").exists()
        and not (tmp / ".devworkbench").exists(),
        "clean removes the remaining generated files",
    )
    require((tmp / "agents/requirements/skills/01-intake/SKILL.md").is_file(), "clean leaves the source skill")
    status = run(["git", "status", "--porcelain"], tmp)
    require(status.stdout.strip() == "", "clean leaves a clean git status")


def check_directory_symlink_replaced(tmp: Path) -> None:
    copy_repo(tmp)
    src = tmp / "agents/requirements/skills/01-intake"
    dest = tmp / ".claude/skills/requirements-01-intake"
    dest.parent.mkdir(parents=True)
    try:
        dest.symlink_to(src, target_is_directory=True)
    except OSError as exc:
        print(f"ok replacing a directory symlink skipped ({exc})")
        return
    setup_py(tmp, "claude", "--copy")
    require((src / "SKILL.md").is_file(), "replacing a directory symlink keeps the source")
    require(dest.is_dir() and not dest.is_symlink() and (dest / "SKILL.md").is_file(), "the published skill is a real directory")


def check_second_agent(tmp: Path) -> None:
    copy_repo(tmp)
    skill = tmp / "agents/demo/skills/01-start"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: demo-01-start\ndescription: Start a demo engagement.\n---\n\n# Start\n",
        encoding="utf-8",
        newline="\n",
    )
    agent = tmp / "agents/demo/agent"
    agent.mkdir(parents=True)
    (agent / "orchestrator.md").write_text("# Demo orchestrator\n", encoding="utf-8", newline="\n")
    (agent / "config.yaml").write_text(
        "agent:\n  id: demo\n  name: Demo Agent\nskills:\n  - id: \"01\"\n    directory: skills/01-start\n    name: demo-01-start\n",
        encoding="utf-8",
        newline="\n",
    )
    setup_py(tmp, "opencode", "--copy")
    require(
        (tmp / ".opencode/skills/demo-01-start/SKILL.md").is_file()
        and (tmp / ".opencode/skills/requirements-10-srs-assembly/SKILL.md").is_file(),
        "a new agent is published beside requirements",
    )
    command = (tmp / ".opencode/commands/demo.md").read_text(encoding="utf-8")
    require("/demo" in command or "demo" in command and "$ARGUMENTS" in command, "demo command is generated")
    text = (tmp / "AGENTS.md").read_text(encoding="utf-8")
    require("Demo Agent" in text and "Requirements Agent" in text, "AGENTS.md lists every discovered agent")


def check_bad_skill(tmp: Path) -> None:
    copy_repo(tmp)
    path = tmp / "agents/requirements/skills/01-intake/SKILL.md"
    path.write_text(path.read_text(encoding="utf-8").replace("name: requirements-01-intake", "name: Not Kebab", 1), encoding="utf-8", newline="\n")
    result = setup_py(tmp, "claude", "--copy", ok=False)
    require(result.returncode != 0 and "requirements-01-intake" in result.stderr, "a non-kebab skill name fails setup")
    require(not (tmp / "CLAUDE.md").exists(), "a rejected skill publishes nothing")


def check_config_mismatch(tmp: Path) -> None:
    copy_repo(tmp)
    path = tmp / "agents/requirements/agent/config.yaml"
    path.write_text(path.read_text(encoding="utf-8").replace("name: requirements-01-intake", "name: requirements-intake", 1), encoding="utf-8", newline="\n")
    result = setup_py(tmp, "all", ok=False)
    require(result.returncode != 0 and "requirements-01-intake" in result.stderr, "config skill name must match frontmatter")


def main() -> int:
    check_sources()
    check_wrappers()
    with tempfile.TemporaryDirectory(prefix="devworkbench-setup-") as raw:
        root = Path(raw)
        check_remove_path(root / "unlink")
        check_claude_copy(root / "copy")
        check_links(root / "link")
        check_all_and_clean(root / "all")
        check_directory_symlink_replaced(root / "dirlink")
        check_second_agent(root / "demo")
        check_bad_skill(root / "bad")
        check_config_mismatch(root / "mismatch")
        fresh = root / "fresh"
        copy_repo(fresh)
        sync = setup_py(fresh, "--sync", ok=False)
        require(sync.returncode != 0, "sync with no previous install fails")
        setup_py(fresh, "--clean")
        require(not (fresh / "CLAUDE.md").exists(), "clean on a fresh tree writes nothing")
    print("check_setup: all checks passed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        sys.exit(1)
