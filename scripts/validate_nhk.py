#!/usr/bin/env python3
"""Read-only deterministic validation for the NHK source, install, and final files."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKILLS = (
    "welcome-to-nhk",
    "nhk-bootstrap",
    "nhk-upkeep",
    "nhk-archive",
)

SKILL_DESCRIPTION_LEADS = {
    "welcome-to-nhk": "Route",
    "nhk-bootstrap": "Bootstrap",
    "nhk-upkeep": "Repair",
    "nhk-archive": "Archive",
}

ROUTER_HANDOFF_TOKENS = (
    "## Router Handoff",
    "**Dependencies**",
    "**Instruction**",
    "**Foundation**",
    "**Route**",
    "only in conversation",
    "current workspace",
    "current NHK run",
    "dependency state, instruction topology, foundation state, lifecycle intent, "
    "or workspace changes",
    "human choice remains unresolved",
)

LEAF_HANDOFF_TOKENS = (
    "## Router Handoff",
    "`welcome-to-nhk`",
    "current workspace",
    "current NHK run",
    "selects this skill",
    "absent, unresolved, or stale",
    "If it selects another route",
    "do not continue",
)

BOOTSTRAP_HANDOFF_TOKENS = (
    "After bootstrap changes the foundation, rerun `welcome-to-nhk`",
    "If bootstrap is creating or structurally repairing the instruction surface",
    "Do not load an instruction template when only a companion or archive surface "
    "is missing.",
)

REFERENCES = (
    "AGENTS-template.md",
    "CLAUDE-template.md",
    "coding-agent-guide-template.md",
    "implementation-planning-template.md",
    "documentation-governance-template.md",
    "archive-readme-template.md",
    "dependency-setup.md",
    "validation-scenarios.md",
)

FINAL_HEADINGS = (
    "Project Map",
    "Execution Rules",
    "Context and Documentation",
    "Subagents and Packets",
    "Blockers and Human Approval",
    "Testing and Verification",
    "Git and Delivery",
)

MARKER_TYPES = {
    "TEMPLATE_ONLY",
    "FINAL_VERBATIM",
    "FINAL_ADAPT",
    "OPTIONAL_BY_COMPLEXITY",
}

FINAL_MARKER_TYPES = MARKER_TYPES - {"TEMPLATE_ONLY"}
MARKER_RE = re.compile(r"\[\[([A-Z_]+):(BEGIN|END)\]\]")
FINAL_MARKER_LEAK_RE = re.compile(
    r"\[\[(?:TEMPLATE_ONLY|FINAL_VERBATIM|FINAL_ADAPT|OPTIONAL_BY_COMPLEXITY)"
    r"(?::(?:BEGIN|END))?\]\]"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
TOP_HEADING_RE = re.compile(r"^##(?!#)\s+(.+?)\s*$")
REFERENCE_RE = re.compile(r"\.\./references/([A-Za-z0-9._-]+)")

SOURCE_TEMPLATE_LIMITS = {
    "AGENTS-template.md": 190,
    "CLAUDE-template.md": 200,
}

PLAIN_REFERENCE_SOURCE_LIMITS = {
    "coding-agent-guide-template.md": 140,
    "implementation-planning-template.md": 120,
    "documentation-governance-template.md": 160,
    "archive-readme-template.md": 40,
}

FINAL_LIMITS = {"simple": 100, "medium": 125, "complex": 150}

COMPANION_FINAL_LIMITS = {
    "coding-guide": 80,
    "planning-guide": 80,
    "doc-governance": 100,
}

TASK_ROUTING_COLUMNS = (
    "Task or Symptom",
    "Read First",
    "Likely Change Surface",
    "Targeted Verification",
)

CODING_GUIDE_HEADINGS = (
    "Task Routing",
    "Shared Entry Points",
    "Search and Boundary Hints",
)

DOC_GOVERNANCE_HEADINGS = (
    "Document Roles",
    "Active Documentation Surfaces",
    "Workspace and Document Map",
    "Lifecycle Rules",
    "Naming and Loading",
    "Archive Transition Invariants",
)

PLANNING_GUIDE_HEADINGS = (
    "Workflow Compatibility",
    "Plan Layers",
    "Task Contract",
    "Dependencies and Execution",
    "Wide Changes",
    "Plan Review",
)

PLANNING_GUIDE_TOKENS = (
    "Delivers",
    "Blocked by",
    "Worker class",
    "mechanical",
    "standard",
    "judgment",
    "expand",
    "migrate",
    "contract",
    "integration branch",
)

LEGACY_CODING_GUIDE_HEADINGS = {
    "Current Execution State",
    "High-Frequency Packet Routing",
    "Implementation Packet Checklist",
    "Code Entry Map",
    "Default Verification",
    "Anti-Detour Advice",
}

COMPANION_IMPORT_RE = re.compile(
    r"@(?:\./)?(?:coding-agent-guide|implementation-planning|"
    r"documentation-governance)\.md\b"
)

COMMON_VERBATIM_HEADINGS = {
    "Execution Rules",
    "Context and Documentation",
    "Subagents and Packets",
    "Blockers and Human Approval",
    "Testing and Verification",
    "Git and Delivery",
}

CONVERGENCE_BACKSTOP = (
    "Five failed fix–verify or fix–review rounds on the same acceptance gap "
    "trigger a mandatory stop. Invoke or restart `systematic-debugging`, count "
    "those rounds as failed fixes, and forbid a sixth fix until root-cause and "
    "architecture reassessment is complete."
)

CODEX_PRESET_LADDER = (
    "GPT-5.6 Luna max → GPT-5.5 xhigh → GPT-5.6 Terra high → "
    "GPT-5.6 Terra xhigh → GPT-5.6 Terra max → GPT-5.6 Sol xhigh → "
    "GPT-5.6 Sol max"
)

CODEX_WORKER_ROUTING_TOKENS = (
    CODEX_PRESET_LADDER,
    "explicitly specify both model and effort",
    "split the packet before escalating",
    "above the main thread's model or effort",
    "specific packet and current run",
)

IMPLEMENTATION_PLANNING_POINTERS = (
    "Before writing, approving, or materially revising an implementation plan, "
    "read `implementation-planning.md`; do not dispatch a task that fails its "
    "packet contract.",
    "Do not load `implementation-planning.md` for ordinary coding, review, or "
    "debugging.",
)

INSTALL_COMMAND = (
    "cp -R welcome-to-nhk nhk-bootstrap nhk-upkeep nhk-archive references "
    "<skills-root>/"
)

VALIDATOR_INSTALL_COMMAND = (
    "python3 -B scripts/validate_nhk.py --install-root <skills-root>"
)

VALIDATOR_COMPANION_COMMANDS = (
    "python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide",
    "python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide",
    "python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance",
)


@dataclass(frozen=True)
class MarkerBlock:
    kind: str
    content: str
    first_heading: str | None
    start_line: int


def read_text(path: Path, issues: list[str], label: str | None = None) -> str | None:
    display = label or str(path)
    if not path.is_file():
        issues.append(f"{display}: missing file")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        issues.append(f"{display}: cannot read UTF-8 text ({error})")
        return None


def line_count(text: str) -> int:
    return len(text.splitlines())


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def heading_title(line: str) -> str | None:
    match = HEADING_RE.match(line)
    return match.group(2).strip() if match else None


def strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    remaining = line
    visible: list[str] = []
    while remaining:
        if in_comment:
            end = remaining.find("-->")
            if end < 0:
                return "".join(visible), True
            remaining = remaining[end + 3 :]
            in_comment = False
            continue
        start = remaining.find("<!--")
        if start < 0:
            visible.append(remaining)
            break
        visible.append(remaining[:start])
        remaining = remaining[start + 4 :]
        in_comment = True
    return "".join(visible), in_comment


def valid_import_lines(text: str) -> list[int]:
    imports: list[int] = []
    fence_char: str | None = None
    fence_width = 0
    in_comment = False

    for number, raw_line in enumerate(text.splitlines(), 1):
        stripped = raw_line.lstrip()
        fence = re.match(r"(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            closing = re.fullmatch(
                rf"{re.escape(fence_char)}{{{fence_width},}}[ \t]*", stripped
            )
            if closing:
                fence_char = None
                fence_width = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_width = len(fence.group(1))
            continue

        visible, in_comment = strip_html_comments(raw_line, in_comment)
        trimmed = visible.strip()
        if not trimmed or trimmed.startswith(">"):
            continue
        if trimmed in {"@AGENTS.md", "@./AGENTS.md"}:
            imports.append(number)

    return imports


def active_companion_imports(text: str) -> list[tuple[int, str]]:
    imports: list[tuple[int, str]] = []
    fence_char: str | None = None
    fence_width = 0
    in_comment = False

    for number, raw_line in enumerate(text.splitlines(), 1):
        stripped = raw_line.lstrip()
        fence = re.match(r"(`{3,}|~{3,})", stripped)
        if fence_char is not None:
            closing = re.fullmatch(
                rf"{re.escape(fence_char)}{{{fence_width},}}[ \t]*", stripped
            )
            if closing:
                fence_char = None
                fence_width = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_width = len(fence.group(1))
            continue

        visible, in_comment = strip_html_comments(raw_line, in_comment)
        if not visible.strip() or visible.lstrip().startswith(">"):
            continue
        visible = re.sub(r"`+[^`\n]*`+", "", visible)
        imports.extend(
            (number, match.group(0))
            for match in COMPANION_IMPORT_RE.finditer(visible)
        )

    return imports


def parse_template(
    path: Path, text: str, limit: int, issues: list[str]
) -> list[MarkerBlock]:
    label = path.name
    count = line_count(text)
    if count > limit:
        issues.append(f"{label}: {count} lines exceeds source-template limit {limit}")

    active_kind: str | None = None
    active_line = 0
    active_content: list[str] = []
    blocks: list[MarkerBlock] = []
    seen_types: set[str] = set()

    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        marker = MARKER_RE.fullmatch(stripped)
        if marker:
            kind, action = marker.groups()
            seen_types.add(kind)
            if kind not in MARKER_TYPES:
                issues.append(f"{label}:{number}: unknown marker type {kind}")
            if action == "BEGIN":
                if active_kind is not None:
                    issues.append(
                        f"{label}:{number}: nested marker {kind} inside {active_kind}"
                    )
                    continue
                active_kind = kind
                active_line = number
                active_content = []
                continue

            if active_kind is None:
                issues.append(f"{label}:{number}: marker END without matching BEGIN")
                continue
            if kind != active_kind:
                issues.append(
                    f"{label}:{number}: marker END {kind} does not match {active_kind}"
                )
                continue

            content = "\n".join(active_content)
            first = next(
                (heading_title(item) for item in active_content if heading_title(item)),
                None,
            )
            blocks.append(MarkerBlock(active_kind, content, first, active_line))
            active_kind = None
            active_line = 0
            active_content = []
            continue

        if "[[" in stripped or "]]" in stripped:
            issues.append(f"{label}:{number}: malformed marker syntax")
        if stripped and active_kind is None:
            issues.append(f"{label}:{number}: semantic text outside a marker block")
        if active_kind is not None:
            active_content.append(line)

    if active_kind is not None:
        issues.append(f"{label}:{active_line}: unclosed marker {active_kind}")

    missing_types = MARKER_TYPES - seen_types
    for kind in sorted(missing_types):
        issues.append(f"{label}: required marker type {kind} is absent")

    first_headings: dict[str, int] = {}
    final_headings: list[str] = []
    for block in blocks:
        if block.kind not in FINAL_MARKER_TYPES:
            continue
        if block.first_heading is None:
            issues.append(
                f"{label}:{block.start_line}: final marker block has no Markdown heading"
            )
        elif block.first_heading in first_headings:
            issues.append(
                f"{label}:{block.start_line}: duplicate first heading "
                f"{block.first_heading!r} across final blocks"
            )
        else:
            first_headings[block.first_heading] = block.start_line
        for item in block.content.splitlines():
            match = TOP_HEADING_RE.match(item)
            if match:
                final_headings.append(match.group(1).strip())

    if tuple(final_headings) != FINAL_HEADINGS:
        issues.append(
            f"{label}: final top-level headings must be exactly the seven required "
            "headings in order"
        )

    required_budget_text = (
        "simple: 100 lines",
        "medium: 125 lines",
        "complex: 150 lines",
        "There is no minimum line count",
    )
    for snippet in required_budget_text:
        if snippet not in text:
            issues.append(f"{label}: missing budget contract text {snippet!r}")
    if label == "CLAUDE-template.md" and "35 lines" not in text:
        issues.append(f"{label}: missing thin 35-line limit")

    return blocks


def verbatim_by_heading(blocks: Iterable[MarkerBlock]) -> dict[str, str]:
    return {
        block.first_heading: block.content.strip()
        for block in blocks
        if block.kind == "FINAL_VERBATIM" and block.first_heading is not None
    }


def validate_shared_templates(
    agent_blocks: list[MarkerBlock],
    claude_blocks: list[MarkerBlock],
    claude_text: str,
    issues: list[str],
) -> None:
    agents = verbatim_by_heading(agent_blocks)
    claude = verbatim_by_heading(claude_blocks)

    for heading in sorted(COMMON_VERBATIM_HEADINGS):
        if heading not in agents or heading not in claude:
            issues.append(f"templates: shared verbatim block {heading!r} is missing")
        elif agents[heading] != claude[heading]:
            issues.append(f"templates: shared verbatim block {heading!r} differs")

    agent_only = set(agents) - COMMON_VERBATIM_HEADINGS
    claude_only = set(claude) - COMMON_VERBATIM_HEADINGS
    if agent_only != {"Codex Worker Boundary"}:
        issues.append(
            "AGENTS-template.md: platform-specific verbatim blocks must contain only "
            "'Codex Worker Boundary'"
        )
    if claude_only:
        issues.append(
            "CLAUDE-template.md: unexpected platform-specific verbatim block(s): "
            + ", ".join(sorted(claude_only))
        )

    codex_boundary = agents.get("Codex Worker Boundary", "")
    for token in CODEX_WORKER_ROUTING_TOKENS:
        if token not in codex_boundary:
            issues.append(
                "AGENTS-template.md: Codex worker routing is missing " + repr(token)
            )
    if "Ultra" not in codex_boundary or "recursive delegation" not in codex_boundary:
        issues.append(
            "AGENTS-template.md: Codex worker routing must keep Ultra behind "
            "packet-specific approval and recursive-delegation authorization"
        )
    for block in agent_blocks:
        if block.first_heading != "Codex Worker Boundary" and "Ultra" in block.content:
            issues.append(
                "AGENTS-template.md: Ultra may appear only in Codex Worker Boundary"
            )

    forbidden_claude_models = re.search(
        r"\b(?:Ultra|Luna|Terra|Sol|Sonnet|Opus|Haiku)\b|\bgpt-\d",
        claude_text,
        re.IGNORECASE,
    )
    if forbidden_claude_models:
        issues.append(
            "CLAUDE-template.md: static model/effort catalog token is forbidden: "
            + forbidden_claude_models.group(0)
        )

    worker_block = agents.get("Subagents and Packets", "")
    worker_contract_tokens = (
        "fewest workers",
        "lowest-cost configuration",
        "cost ceiling for each worker",
        "split it before increasing",
        "human approval",
        "recursive delegation",
        "serially",
        "read/write authority",
        "A timeout is not proof of a blocker",
        "close idle workers",
    )
    for token in worker_contract_tokens:
        if token not in worker_block:
            issues.append(f"templates: shared worker contract is missing {token!r}")

    execution_block = agents.get("Execution Rules", "")
    if f"- {CONVERGENCE_BACKSTOP}" not in execution_block:
        issues.append("templates: shared Execution Rules are missing the convergence backstop")

    context_block = agents.get("Context and Documentation", "")
    for token in IMPLEMENTATION_PLANNING_POINTERS:
        if token not in context_block:
            issues.append(
                "templates: shared implementation-planning pointer is missing "
                + repr(token)
            )


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return None
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def validate_skill(root: Path, name: str, issues: list[str]) -> None:
    path = root / name / "SKILL.md"
    text = read_text(path, issues, f"{name}/SKILL.md")
    if text is None:
        return
    frontmatter = parse_frontmatter(text)
    if frontmatter is None:
        issues.append(f"{name}/SKILL.md: invalid frontmatter fences")
    else:
        if frontmatter.get("name") != name:
            issues.append(
                f"{name}/SKILL.md: frontmatter name must be {name!r}, got "
                f"{frontmatter.get('name')!r}"
            )
        description = frontmatter.get("description")
        if not description:
            issues.append(f"{name}/SKILL.md: frontmatter description is required")
        else:
            leading_word = SKILL_DESCRIPTION_LEADS[name]
            if not description.startswith(f"{leading_word} "):
                issues.append(
                    f"{name}/SKILL.md: description must front-load leading word "
                    f"{leading_word!r}"
                )

    if "## Local References" in text:
        issues.append(
            f"{name}/SKILL.md: replace the flat Local References inventory with "
            "a conditional context pointer beside the branch that needs it"
        )

    handoff_tokens = (
        ROUTER_HANDOFF_TOKENS if name == "welcome-to-nhk" else LEAF_HANDOFF_TOKENS
    )
    if name == "nhk-bootstrap":
        handoff_tokens += BOOTSTRAP_HANDOFF_TOKENS
    for token in handoff_tokens:
        if token not in text:
            issues.append(f"{name}/SKILL.md: router handoff is missing {token!r}")

    if "`implementation-planning.md`" not in text:
        issues.append(
            f"{name}/SKILL.md: planning foundation must name "
            "`implementation-planning.md`"
        )

    reference_root = (root / "references").resolve()
    for match in REFERENCE_RE.finditer(text):
        relative = match.group(0)
        target = (path.parent / relative).resolve()
        try:
            target.relative_to(reference_root)
        except ValueError:
            issues.append(f"{name}/SKILL.md: reference escapes references/: {relative}")
            continue
        if not target.is_file():
            issues.append(f"{name}/SKILL.md: unresolved local reference {relative}")


def require_text(
    text: str,
    snippet: str,
    label: str,
    issues: list[str],
    *,
    case_sensitive: bool = True,
) -> None:
    haystack = text if case_sensitive else text.lower()
    needle = snippet if case_sensitive else snippet.lower()
    if needle not in haystack:
        issues.append(f"{label}: missing required fact {snippet!r}")


def validate_readmes(root: Path, issues: list[str]) -> None:
    english = read_text(root / "README.md", issues, "README.md")
    chinese = read_text(root / "README_CN.md", issues, "README_CN.md")
    if english is None or chinese is None:
        return

    if not re.search(r"\[中文\]\((?:\./)?README_CN\.md\)", english):
        issues.append("README.md: missing Chinese cross-link")
    if not re.search(r"\[English\]\((?:\./)?README\.md\)", chinese):
        issues.append("README_CN.md: missing English cross-link")

    require_text(english, "five recurring jobs", "README.md", issues, case_sensitive=False)
    if not re.search(r"5\s*类", chinese):
        issues.append("README_CN.md: must describe the same 5 类 recurring jobs")

    for name in (*SKILLS, *REFERENCES):
        require_text(english, name, "README.md", issues)
        require_text(chinese, name, "README_CN.md", issues)

    normalized_install = normalize_space(INSTALL_COMMAND)
    if normalized_install not in normalize_space(english):
        issues.append("README.md: sibling install command is missing or inconsistent")
    if normalized_install not in normalize_space(chinese):
        issues.append("README_CN.md: sibling install command is missing or inconsistent")

    normalized_validator = normalize_space(VALIDATOR_INSTALL_COMMAND)
    if normalized_validator not in normalize_space(english):
        issues.append("README.md: optional install-validator command is missing")
    if normalized_validator not in normalize_space(chinese):
        issues.append("README_CN.md: optional install-validator command is missing")
    for command in VALIDATOR_COMPANION_COMMANDS:
        normalized = normalize_space(command)
        if normalized not in normalize_space(english):
            issues.append(f"README.md: companion-validator command is missing: {command}")
        if normalized not in normalize_space(chinese):
            issues.append(
                f"README_CN.md: companion-validator command is missing: {command}"
            )

    for token in ("scripts/", "tests/", "not runtime", "optional", "refresh", "discover"):
        require_text(english, token, "README.md", issues, case_sensitive=False)
    for token in ("scripts/", "tests/", "不属于运行时", "可选", "刷新", "可发现"):
        require_text(chinese, token, "README_CN.md", issues, case_sensitive=False)
    for token in (
        "eight controlled references",
        "five mandatory foundation surfaces",
        "Superpowers overlay",
        "cost ceiling",
        CODEX_PRESET_LADDER,
    ):
        require_text(english, token, "README.md", issues, case_sensitive=False)
    for token in (
        "八个受控 reference",
        "五个强制 foundation surface",
        "Superpowers overlay",
        "成本上限",
        CODEX_PRESET_LADDER,
    ):
        require_text(chinese, token, "README_CN.md", issues, case_sensitive=False)
    for token in ("round five", "systematic-debugging", "No sixth patch"):
        require_text(english, token, "README.md", issues, case_sensitive=False)
    for token in ("第五轮", "systematic-debugging", "第六块补丁"):
        require_text(chinese, token, "README_CN.md", issues, case_sensitive=False)
    for token in (
        "routing table is the shallow code map",
        "Thin CLAUDE imports only AGENTS",
        "backticked literal paths",
        "load on demand",
    ):
        require_text(english, token, "README.md", issues, case_sensitive=False)
    for token in (
        "路由表就是新手需要的浅层 code map",
        "thin CLAUDE 只 import AGENTS",
        "反引号普通路径",
        "按需读取",
    ):
        require_text(chinese, token, "README_CN.md", issues, case_sensitive=False)

    old_layout_patterns = (
        r"<skills-root>/nhk(?:/|\b)",
        r"\.agents/skills/nhk(?:/|\b)",
        r"\.claude/skills/nhk(?:/|\b)",
    )
    for label, text in (("README.md", english), ("README_CN.md", chinese)):
        for pattern in old_layout_patterns:
            if re.search(pattern, text):
                issues.append(f"{label}: old extra nhk/ install layer is forbidden")


def validate_repo_split(root: Path, issues: list[str]) -> None:
    agents = read_text(root / "AGENTS.md", issues, "AGENTS.md")
    claude = read_text(root / "CLAUDE.md", issues, "CLAUDE.md")
    if agents is not None and "NHK Repository Agent Instructions" not in agents:
        issues.append("AGENTS.md: root agent-maintenance role is not declared")
    if claude is not None:
        imports = valid_import_lines(claude)
        if len(imports) != 1:
            issues.append("CLAUDE.md: repo entrypoint must contain one valid AGENTS import")
        if line_count(claude) > 35:
            issues.append("CLAUDE.md: repo thin adapter exceeds 35 lines")
        headings = [match.group(1).strip() for line in claude.splitlines() if (match := TOP_HEADING_RE.match(line))]
        if any(heading in FINAL_HEADINGS for heading in headings):
            issues.append("CLAUDE.md: repo thin adapter mixes in standalone headings")


def validate_forbidden_legacy(root: Path, issues: list[str]) -> None:
    paths = [root / "README.md", root / "README_CN.md"]
    paths.extend(root / skill / "SKILL.md" for skill in SKILLS)
    paths.extend(root / "references" / name for name in REFERENCES)
    patterns = (
        ("Opus 4.7", re.compile(r"\bOpus\s+4\.7\b", re.IGNORECASE)),
        (
            "model price table",
            re.compile(
                r"(?:\b(?:model\s+)?(?:price|pricing|cost)\b[^\n]{0,80}"
                r"(?:US\$|\$|USD|CNY|RMB|¥|￥)\s*\d|"
                r"(?:US\$|\$|USD|CNY|RMB|¥|￥)\s*\d[^\n]{0,80}"
                r"\b(?:tokens?|million|1m)\b)",
                re.IGNORECASE,
            ),
        ),
        (
            "static effort enumeration",
            re.compile(
                r"\beffort(?:\s+levels?)?\s*(?::|are)\s*"
                r"[^\n]*(?:,|/|\|)[^\n]*(?:,|/|\|)",
                re.IGNORECASE,
            ),
        ),
        (
            "fixed timeout",
            re.compile(
                r"\b(?:120000|180000|300000)\b|"
                r"\b(?:120|180|300)\s*(?:s|secs?|seconds?|秒)\b",
                re.IGNORECASE,
            ),
        ),
        (
            "40k token cap",
            re.compile(r"\b(?:40,?000|40k)\s+tokens?\b", re.IGNORECASE),
        ),
        (
            "80% default coverage",
            re.compile(
                r"(?:\bcoverage\b[^\n]{0,60}\b80%|\b80%[^\n]{0,60}\bcoverage\b)",
                re.IGNORECASE,
            ),
        ),
        ("old adopt wording", re.compile(r"\bonly imitated\b", re.IGNORECASE)),
        (
            "static deployment table",
            re.compile(
                r"Valid deployment options include|Supported effort levels are|Recommended deployment guidance",
                re.IGNORECASE,
            ),
        ),
    )
    model_policy_surfaces = {
        Path("README.md"),
        Path("README_CN.md"),
        Path("references/AGENTS-template.md"),
        Path("references/validation-scenarios.md"),
    }
    versioned_model = re.compile(r"\bgpt-\d[\w.-]*\b", re.IGNORECASE)
    for path in paths:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        relative = path.relative_to(root)
        model_match = versioned_model.search(text)
        if model_match and relative not in model_policy_surfaces:
            issues.append(
                f"{relative}: forbidden versioned model outside Codex policy surfaces: "
                f"{model_match.group(0)}"
            )
        for label, pattern in patterns:
            match = pattern.search(text)
            if match:
                issues.append(f"{relative}: forbidden {label}: {match.group(0)}")


def validate_source(root: Path) -> list[str]:
    issues: list[str] = []
    if not root.is_dir():
        return [f"source root does not exist or is not a directory: {root}"]

    for name in REFERENCES:
        if not (root / "references" / name).is_file():
            issues.append(f"references/{name}: missing required controlled reference")
    for skill in SKILLS:
        validate_skill(root, skill, issues)

    parsed: dict[str, list[MarkerBlock]] = {}
    texts: dict[str, str] = {}
    for name, limit in SOURCE_TEMPLATE_LIMITS.items():
        path = root / "references" / name
        text = read_text(path, issues, f"references/{name}")
        if text is None:
            continue
        texts[name] = text
        parsed[name] = parse_template(path, text, limit, issues)

    if all(name in parsed for name in SOURCE_TEMPLATE_LIMITS):
        validate_shared_templates(
            parsed["AGENTS-template.md"],
            parsed["CLAUDE-template.md"],
            texts["CLAUDE-template.md"],
            issues,
        )

    for name, limit in PLAIN_REFERENCE_SOURCE_LIMITS.items():
        path = root / "references" / name
        text = read_text(path, issues, f"references/{name}")
        if text is None:
            continue
        count = line_count(text)
        if count > limit:
            issues.append(
                f"{name}: {count} lines exceeds source-template limit {limit}"
            )

    coding_template = read_text(
        root / "references" / "coding-agent-guide-template.md",
        issues,
        "references/coding-agent-guide-template.md",
    )
    if coding_template is not None:
        for token in (*TASK_ROUTING_COLUMNS, "80 lines"):
            require_text(
                coding_template,
                token,
                "coding-agent-guide-template.md",
                issues,
            )

    planning_template = read_text(
        root / "references" / "implementation-planning-template.md",
        issues,
        "references/implementation-planning-template.md",
    )
    if planning_template is not None:
        for token in (*PLANNING_GUIDE_HEADINGS, *PLANNING_GUIDE_TOKENS, "80 lines"):
            require_text(
                planning_template,
                token,
                "implementation-planning-template.md",
                issues,
            )

    governance_template = read_text(
        root / "references" / "documentation-governance-template.md",
        issues,
        "references/documentation-governance-template.md",
    )
    if governance_template is not None:
        for token in (
            *DOC_GOVERNANCE_HEADINGS,
            "100 lines",
            "`implementation-planning.md`",
            "archive completed implementation plans",
        ):
            require_text(
                governance_template,
                token,
                "documentation-governance-template.md",
                issues,
            )

    validate_readmes(root, issues)
    validate_repo_split(root, issues)
    validate_forbidden_legacy(root, issues)
    return issues


def validate_install(install_root: Path, source_root: Path) -> list[str]:
    issues: list[str] = []
    if not install_root.is_dir():
        return [f"install root does not exist or is not a directory: {install_root}"]

    nested_root = install_root / "nhk"
    if all((nested_root / name).exists() for name in (*SKILLS, "references")) and not all(
        (install_root / name).exists() for name in (*SKILLS, "references")
    ):
        issues.append(
            "NHK install is one level too deep under nhk/; the four skill directories "
            "and references/ must be siblings directly under the selected install root"
        )

    required_paths = [Path(skill) / "SKILL.md" for skill in SKILLS]
    required_paths.extend(Path("references") / name for name in REFERENCES)
    for relative in required_paths:
        installed = install_root / relative
        source = source_root / relative
        if not installed.is_file():
            issues.append(f"{relative}: missing from install root")
            continue
        if not source.is_file():
            issues.append(f"{relative}: missing from validator source package")
            continue
        try:
            if installed.read_bytes() != source.read_bytes():
                issues.append(f"{relative}: differs from source package (mixed or stale install)")
        except OSError as error:
            issues.append(f"{relative}: cannot compare install file ({error})")

    for skill in SKILLS:
        validate_skill(install_root, skill, issues)
    return issues


def validate_final(
    path: Path, kind: str, mode: str | None, complexity: str | None
) -> list[str]:
    issues: list[str] = []
    text = read_text(path, issues, str(path))
    if text is None:
        return issues

    lower = text.lower()
    if FINAL_MARKER_LEAK_RE.search(text):
        issues.append("final file contains a template marker")
    generation_leaks = (
        "generation contract",
        "template contract",
        "replace this guidance",
        "replace explanatory examples",
        "source-template hard limit",
        "hard line limits for",
        "choose exactly one mode",
        "marker protocol",
        "template usage",
    )
    for leak in generation_leaks:
        if leak in lower:
            issues.append(f"final file contains generation-only text: {leak!r}")
    if kind == "planning-guide" and re.search(
        r"<(?:one observable|task identifiers|mechanical\s*\|\s*standard\s*\|\s*judgment)",
        text,
        re.IGNORECASE,
    ):
        issues.append("final file contains a generation-only planning placeholder")

    headings = [
        match.group(1).strip()
        for line in text.splitlines()
        if (match := TOP_HEADING_RE.match(line))
    ]
    all_heading_titles = [
        title for line in text.splitlines() if (title := heading_title(line))
    ]
    forbidden_heading_names = {
        "NHK Governance",
        "NHK Govern",
        "Instruction Coverage",
        "Template Notes",
        "Agent Instructions Template",
        "Claude Code Project Instructions Template",
    }
    for line in text.splitlines():
        title = heading_title(line)
        if title in forbidden_heading_names:
            issues.append(f"final file contains invented governance heading {title!r}")

    if kind in COMPANION_FINAL_LIMITS:
        count = line_count(text)
        limit = COMPANION_FINAL_LIMITS[kind]
        if count > limit:
            issues.append(f"{kind} final file has {count} lines; limit is {limit}")

        h1_headings = [
            match.group(1).strip()
            for line in text.splitlines()
            if (match := re.match(r"^#(?!#)\s+(.+?)\s*$", line))
        ]
        expected_h1 = {
            "coding-guide": "Coding Agent Guide",
            "planning-guide": "Implementation Planning",
            "doc-governance": "Documentation Governance",
        }[kind]
        if h1_headings != [expected_h1]:
            issues.append(
                f"{kind} final file must have exactly one '# {expected_h1}' heading"
            )

        if kind == "coding-guide":
            if "Task Routing" not in headings:
                issues.append("coding-guide final file is missing 'Task Routing'")
            header_rows = [
                tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
                for line in text.splitlines()
                if line.strip().startswith("|")
            ]
            if TASK_ROUTING_COLUMNS not in header_rows:
                issues.append(
                    "coding-guide Task Routing table must use columns: "
                    + ", ".join(TASK_ROUTING_COLUMNS)
                )
            expected_headings = tuple(
                heading for heading in CODING_GUIDE_HEADINGS if heading in headings
            )
            if tuple(headings) != expected_headings:
                unexpected = next(
                    (
                        heading
                        for heading in headings
                        if heading not in CODING_GUIDE_HEADINGS
                    ),
                    None,
                )
                if unexpected is not None:
                    issues.append(
                        f"coding-guide final file contains unexpected section {unexpected!r}"
                    )
                else:
                    issues.append(
                        "coding-guide final sections must follow Task Routing, "
                        "Shared Entry Points, Search and Boundary Hints order"
                    )
            for heading in headings:
                if heading in LEGACY_CODING_GUIDE_HEADINGS:
                    issues.append(
                        f"coding-guide final file contains legacy section {heading!r}"
                    )
        elif kind == "planning-guide":
            if tuple(headings) != PLANNING_GUIDE_HEADINGS:
                issues.append(
                    "planning-guide final headings must be exactly: "
                    + ", ".join(PLANNING_GUIDE_HEADINGS)
                )
            for token in PLANNING_GUIDE_TOKENS:
                if token.lower() not in lower:
                    issues.append(
                        f"planning-guide task contract is missing {token!r}"
                    )
        else:
            if tuple(headings[: len(DOC_GOVERNANCE_HEADINGS)]) != DOC_GOVERNANCE_HEADINGS:
                issues.append(
                    "doc-governance final headings must begin with: "
                    + ", ".join(DOC_GOVERNANCE_HEADINGS)
                )
            allowed_headings = set(DOC_GOVERNANCE_HEADINGS) | {
                "Project-Specific Exceptions"
            }
            for heading in headings:
                if heading not in allowed_headings:
                    issues.append(
                        f"doc-governance final file contains unexpected section {heading!r}"
                    )
            invariant_tokens = (
                "human approval",
                "copy",
                "archive index",
                "verification fails",
                "preserve every active original",
                "no other live workstream",
                "reset",
            )
            for token in invariant_tokens:
                if token not in lower:
                    issues.append(
                        f"doc-governance archive invariants are missing {token!r}"
                    )
            for token in (
                "implementation-planning.md",
                "completed implementation plans",
            ):
                if token not in lower:
                    issues.append(
                        f"doc-governance planning lifecycle is missing {token!r}"
                    )
        return issues

    imports = valid_import_lines(text)
    companion_imports = active_companion_imports(text) if kind == "claude" else []
    for number, imported in companion_imports:
        issues.append(
            f"Claude final file auto-imports companion {imported!r} at line {number}; "
            "use a backticked literal path and load it on demand"
        )
    count = line_count(text)
    if mode == "thin":
        if count > 35:
            issues.append(f"thin CLAUDE file has {count} lines; limit is 35")
        if len(imports) != 1:
            issues.append("thin CLAUDE file must contain exactly one valid import line")
        if any(heading in FINAL_HEADINGS for heading in all_heading_titles):
            issues.append("thin CLAUDE file mixes in standalone headings")
        return issues

    selected_complexity = complexity or "complex"
    limit = FINAL_LIMITS[selected_complexity]
    if count > limit:
        issues.append(
            f"{selected_complexity} standalone file has {count} lines; limit is {limit}"
        )
    if tuple(headings) != FINAL_HEADINGS:
        issues.append(
            "standalone final top-level headings must be exactly the seven required "
            "headings in order"
        )
    if imports:
        issues.append("standalone final file mixes in a thin AGENTS import")
    for companion in (
        "coding-agent-guide.md",
        "implementation-planning.md",
        "documentation-governance.md",
    ):
        if f"`{companion}`" not in text:
            issues.append(
                f"standalone final file must route to `{companion}` by literal path"
            )
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only deterministic validation for NHK source, installs, and final files."
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--root", type=Path, help="validate an NHK source repository")
    modes.add_argument("--install-root", type=Path, help="validate an installed skills root")
    modes.add_argument("--final", type=Path, help="validate one generated instruction file")
    parser.add_argument(
        "--kind",
        choices=(
            "agents",
            "claude",
            "coding-guide",
            "planning-guide",
            "doc-governance",
        ),
    )
    parser.add_argument("--mode", choices=("standalone", "thin"))
    parser.add_argument("--complexity", choices=tuple(FINAL_LIMITS))
    return parser


def report(label: str, issues: list[str]) -> int:
    if issues:
        print(f"FAIL {label}: {len(issues)} issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"PASS {label}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    source_root = Path(__file__).resolve().parents[1]

    if args.final is not None:
        if args.kind is None:
            parser.error("--final requires --kind")
        if args.kind in COMPANION_FINAL_LIMITS:
            if args.mode is not None or args.complexity is not None:
                parser.error(
                    "companion --kind does not accept --mode or --complexity"
                )
            issues = validate_final(args.final.resolve(), args.kind, None, None)
            return report(f"final {args.final}", issues)
        if args.mode is None:
            parser.error("instruction --kind requires --mode")
        if args.mode == "thin" and args.kind != "claude":
            parser.error("thin mode is valid only for --kind claude")
        if args.mode == "thin" and args.complexity is not None:
            parser.error("--complexity applies only to standalone mode")
        issues = validate_final(args.final.resolve(), args.kind, args.mode, args.complexity)
        return report(f"final {args.final}", issues)

    if args.kind is not None or args.mode is not None or args.complexity is not None:
        parser.error("--kind, --mode, and --complexity may be used only with --final")

    if args.install_root is not None:
        install_root = args.install_root.resolve()
        return report(
            f"install {install_root}", validate_install(install_root, source_root)
        )

    root = (args.root or source_root).resolve()
    return report(f"source {root}", validate_source(root))


if __name__ == "__main__":
    sys.exit(main())
