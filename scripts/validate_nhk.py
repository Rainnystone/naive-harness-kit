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
    "If bootstrap is creating, structurally repairing, or making the specific semantic "
    "policy/recovery migration above",
    "Do not load an instruction template when only a companion or archive surface is "
    "missing and the canonical instruction has no superseded NHK-owned policy or "
    "recovery text.",
)

REFERENCES = (
    "AGENTS-template.md",
    "CLAUDE-template.md",
    "coding-agent-guide-template.md",
    "implementation-planning-template.md",
    "worker-policy-template.md",
    "execution-recovery-template.md",
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
    "worker-policy-template.md": 140,
    "execution-recovery-template.md": 140,
    "documentation-governance-template.md": 160,
    "archive-readme-template.md": 40,
}

FINAL_LIMITS = {"simple": 100, "medium": 125, "complex": 150}

COMPANION_FINAL_LIMITS = {
    "coding-guide": 80,
    "planning-guide": 80,
    "worker-policy": 100,
    "execution-recovery": 80,
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

WORKER_POLICY_HEADINGS = (
    "Dispatch Contract",
    "Review Gates",
    "Codex Routing",
    "Claude Routing",
)

EXECUTION_RECOVERY_HEADINGS = (
    "Triggers and Accounting",
    "Main-thread Reassessment",
    "Independent Diagnosis",
    "Recovery and Stop",
)

PLANNING_WORKFLOW_TOKENS = (
    "Superpowers",
    "Files",
    "Interfaces",
    "TDD steps",
    "commands",
    "expected results",
    "necessary code",
)

PLANNING_TASK_CONTRACT_TOKENS = (
    "None",
    "mechanical",
    "standard",
    "judgment",
)

PLANNING_WIDE_CHANGE_TOKENS = (
    "expand",
    "migrate",
    "contract",
    "integration branch",
)

PLANNING_FIELD_PATTERNS = {
    field: re.compile(
        rf"^[ \t]*(?:[-+]\s+)?\*\*{re.escape(field)}:\*\*[ \t]+\S",
        re.IGNORECASE | re.MULTILINE,
    )
    for field in ("Delivers", "Blocked by", "Worker class")
}

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
    r"worker-policy|execution-recovery|documentation-governance)\.md\b"
)

COMMON_VERBATIM_HEADINGS = {
    "Execution Rules",
    "Context and Documentation",
    "Subagents and Packets",
    "Blockers and Human Approval",
    "Testing and Verification",
    "Git and Delivery",
}

LEGACY_CODEX_PRESET_LADDER = (
    "GPT-5.6 Luna max → GPT-5.5 xhigh → GPT-5.6 Terra high → "
    "GPT-5.6 Terra xhigh → GPT-5.6 Terra max → GPT-5.6 Sol xhigh → "
    "GPT-5.6 Sol max"
)

CODEX_PRESET_BANDS = (
    ("GPT-5.6 Luna max", "GPT-6 Astra low"),
    ("GPT-5.6 Sol medium", "GPT-5.6 Sol high", "GPT-6 Astra medium"),
    ("GPT-5.6 Sol xhigh", "GPT-6 Astra xhigh"),
)
CODEX_RESERVED_DISPLAY_PRESETS = ("GPT-6 Astra max",)
CODEX_ALLOWED_FAMILY_NAMES = ("GPT-5.6 Luna", "GPT-5.6 Sol", "GPT-6 Astra")
CODEX_ALLOWED_RUNTIME_IDS = ("gpt-5.6-luna", "gpt-5.6-sol", "gpt-6-astra")
CODEX_DISPLAY_PRESET_RE = re.compile(
    r"\bGPT-\d+(?:\.\d+)?"
    r"(?:"
    r"(?:\s+[A-Z][A-Za-z0-9]+)+(?:\s+(?:low|medium|high|xhigh|max))?"
    r"|"
    r"\s+(?:low|medium|high|xhigh|max)"
    r")\b"
)
CODEX_RUNTIME_ID_RE = re.compile(r"\bgpt-\d[\w.-]*\b", re.IGNORECASE)

INSTRUCTION_COMPANION_ROUTES = (
    "Read `coding-agent-guide.md` to route a task or symptom to code and first-pass verification.",
    "Read `implementation-planning.md` before writing, approving, or materially revising an implementation plan.",
    "Read `worker-policy.md` only when orchestrating, dispatching, or reviewing workers. Load its common sections and the current platform section.",
    "Read `execution-recovery.md` after five failed rounds on one task or one acceptance gap, or earlier evidence of architectural stagnation.",
    "Treat `documentation-governance.md` as the source of truth for documentation lifecycle rules.",
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
    "python3 -B scripts/validate_nhk.py --final <worker-policy.md> --kind worker-policy",
    "python3 -B scripts/validate_nhk.py --final <execution-recovery.md> --kind execution-recovery",
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


def second_level_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    body: list[str] = []
    for _, line in active_markdown_lines(text):
        match = TOP_HEADING_RE.match(line)
        if match:
            if current is not None:
                sections[current] = "\n".join(body)
            current = match.group(1).strip()
            body = []
        elif current is not None:
            body.append(line)
    if current is not None:
        sections[current] = "\n".join(body)
    return sections


def final_shape_sections(text: str) -> tuple[tuple[str, ...], dict[str, str]]:
    lines = text.splitlines()
    try:
        start = lines.index("## Required Final Shape") + 1
        end = lines.index("## Final Check", start)
    except ValueError:
        return (), {}

    headings: list[str] = []
    sections: dict[str, str] = {}
    current: str | None = None
    body: list[str] = []
    for line in lines[start:end]:
        match = re.match(r"^###(?!#)\s+(.+?)\s*$", line)
        if match:
            if current is not None:
                sections[current] = "\n".join(body)
            current = match.group(1).strip()
            headings.append(current)
            body = []
        elif current is not None:
            body.append(line)
    if current is not None:
        sections[current] = "\n".join(body)
    return tuple(headings), sections


def require_section_text(
    sections: dict[str, str],
    heading: str,
    snippets: Iterable[str],
    label: str,
    issues: list[str],
) -> None:
    body = sections.get(heading, "")
    for snippet in snippets:
        if snippet not in body:
            issues.append(f"{label} {heading} is missing {snippet!r}")


def validate_exact_codex_bands(
    codex: str, label: str, issues: list[str]
) -> None:
    found: dict[int, list[str]] = {}
    for line in codex.splitlines():
        match = re.match(r"^\s*-\s*Band\s+(\d+):\s*(.*?)\s*$", line)
        if not match:
            continue
        band = int(match.group(1))
        raw = match.group(2).removesuffix(".")
        found.setdefault(band, []).extend(
            item.strip().removesuffix(".") for item in raw.split(";") if item.strip()
        )

    for band in sorted(set(found) - {1, 2, 3}):
        issues.append(
            f"{label} Codex Routing has unexpected Band {band}; exact unordered "
            "preset sets exist only for Bands 1-3"
        )

    for band, expected in enumerate(CODEX_PRESET_BANDS, 1):
        actual = found.get(band, [])
        if len(actual) != len(expected) or set(actual) != set(expected):
            issues.append(
                f"{label} Codex Routing Band {band} must contain the exact unordered "
                f"preset set: {'; '.join(expected)}"
            )


def validate_codex_declared_presets(
    codex: str, label: str, issues: list[str]
) -> None:
    allowed_display = {
        *(preset.lower() for band in CODEX_PRESET_BANDS for preset in band),
        *(preset.lower() for preset in CODEX_RESERVED_DISPLAY_PRESETS),
        *(name.lower() for name in CODEX_ALLOWED_FAMILY_NAMES),
    }
    allowed_runtime = {item.lower() for item in CODEX_ALLOWED_RUNTIME_IDS}
    seen: set[str] = set()

    for match in CODEX_DISPLAY_PRESET_RE.finditer(codex):
        declared = " ".join(match.group(0).split()).lower()
        if declared in allowed_display or declared in seen:
            seen.add(declared)
            continue
        seen.add(declared)
        issues.append(
            f"{label} Codex Routing declares unapproved versioned preset "
            f"{match.group(0)!r}; allowed presets are the Band 1-3 sets and "
            "reserved GPT-6 Astra max"
        )

    leftover = CODEX_DISPLAY_PRESET_RE.sub(" ", codex)
    for match in CODEX_RUNTIME_ID_RE.finditer(leftover):
        token = match.group(0).lower()
        if token in allowed_runtime or token in seen:
            continue
        seen.add(token)
        issues.append(
            f"{label} Codex Routing declares unapproved versioned preset "
            f"{match.group(0)!r}; allowed presets are the Band 1-3 sets and "
            "reserved GPT-6 Astra max"
        )


def validate_worker_policy_contract(
    text: str,
    headings: tuple[str, ...],
    sections: dict[str, str],
    label: str,
    issues: list[str],
) -> None:
    if headings != WORKER_POLICY_HEADINGS:
        issues.append(
            f"{label} headings must be exactly: " + ", ".join(WORKER_POLICY_HEADINGS)
        )

    require_section_text(
        sections,
        "Dispatch Contract",
        (
            "Authorization comes from the allowed role or preset for the packet, not the main thread's current model or effort",
            "Explicit user budgets still bind",
            "explicitly runtime-supported model and effort",
            "never inherit a top preset silently",
            "Recursive delegation needs separate human authorization for a named packet",
            "Keep subagent-driven implementers sequential",
            "The main thread owns integration",
        ),
        label,
        issues,
    )
    require_section_text(
        sections,
        "Review Gates",
        (
            "one independent read-only reviewer",
            "separate spec-compliance and task-quality verdicts",
            "Both must pass; self-review is not a substitute",
            "fixed BASE and HEAD revisions",
            "one whole-change final review",
            "at most one concentrated fix wave and one scoped re-review",
        ),
        label,
        issues,
    )
    require_section_text(
        sections,
        "Codex Routing",
        (
            "`fork_turns: none`",
            "Presets within a band are unordered task-fit choices",
            "there is no mandatory Band 1 trial",
            "Escalate one band only",
            "ordinary Band 3 ceiling",
            "GPT-5.6 Luna may perform low-risk scoped re-review, never an initial task review",
            "GPT-6 Astra max is reserved for whole-change final review of a complex Superpowers plan, not ordinary implementation, debugging, or recovery",
            "Ultra requires human approval naming the packet and current run",
            "Ultra authorization and recursion authorization never imply each other",
        ),
        label,
        issues,
    )
    require_section_text(
        sections,
        "Claude Routing",
        (
            "Use Sonnet for ordinary implementation and review",
            "Use Opus for difficult work, debugging, architecture, final review",
            "Use Fable only when the human explicitly chooses or approves it for the main thread",
            "Specify Sonnet or Opus for every worker so Fable is never inherited",
            "Do not add a Haiku band",
        ),
        label,
        issues,
    )
    validate_exact_codex_bands(sections.get("Codex Routing", ""), label, issues)
    validate_codex_declared_presets(sections.get("Codex Routing", ""), label, issues)


def validate_execution_recovery_contract(
    headings: tuple[str, ...],
    sections: dict[str, str],
    label: str,
    issues: list[str],
) -> None:
    if headings != EXECUTION_RECOVERY_HEADINGS:
        issues.append(
            f"{label} headings must be exactly: "
            + ", ".join(EXECUTION_RECOVERY_HEADINGS)
        )

    require_section_text(
        sections,
        "Triggers and Accounting",
        (
            "systematic-debugging",
            "architecture check after three failed fixes",
            "five fix-review rounds per task",
            "five rounds for the same stable acceptance gap across tasks",
            "Reaching either the task-round bound or stable-gap bound stops ordinary fixing",
            "Worker, session, model, commit, task rename, or replanning never resets a task or gap count",
            "existing authoritative execution record",
            "In SDD, this is the SDD ledger",
            "do not create an SDD-only or parallel state system",
            "Read-only diagnosis spends no fix round and grants no additional modification authority",
        ),
        label,
        issues,
    )
    require_section_text(
        sections,
        "Main-thread Reassessment",
        (
            "original intent, approved spec and public contracts, verification signal, prior attempts, and cross-task consequences",
            "Classify the failure as implementation, design or ownership, spec conflict, invalid oracle, reviewer error, or external conditions",
            "how the new explanation differs from old hypotheses",
            "concrete command or input, observed result, and expected before-and-after result",
            "original scope and authority",
            "require a human decision",
        ),
        label,
        issues,
    )
    require_section_text(
        sections,
        "Independent Diagnosis",
        (
            "competing explanations, review-versus-implementation conflict, or an unverified old premise",
            "at most one fresh-context Band 3 or Opus read-only diagnostic worker",
            "challenge one concrete hypothesis",
            "does not authorize a fix",
            "Do not start a diagnostic chain",
        ),
        label,
        issues,
    )
    require_section_text(
        sections,
        "Recovery and Stop",
        (
            "at most one recovery fix wave and one independent re-review",
            "may be the sixth modification and supersedes an old absolute “No sixth patch” rule",
            "stop automatic fixes and ask the human",
            "Changing model, plan, or task never renews recovery",
            "Final review retains one concentrated fix wave and one scoped re-review",
            "An exhausted earlier gap cannot use final review as another repair allowance",
            "never return to the ordinary loop",
        ),
        label,
        issues,
    )

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


def active_markdown_lines(text: str) -> Iterable[tuple[int, str]]:
    fence_char: str | None = None
    fence_width = 0
    in_comment = False

    for number, raw_line in enumerate(text.splitlines(), 1):
        if fence_char is not None:
            stripped = raw_line.lstrip()
            closing = re.fullmatch(
                rf"{re.escape(fence_char)}{{{fence_width},}}[ \t]*", stripped
            )
            if closing:
                fence_char = None
                fence_width = 0
            continue

        visible, in_comment = strip_html_comments(raw_line, in_comment)
        stripped = visible.lstrip()
        fence = re.match(r"(`{3,}|~{3,})", stripped)
        if fence:
            fence_char = fence.group(1)[0]
            fence_width = len(fence.group(1))
            continue

        yield number, visible


def valid_import_lines(text: str) -> list[int]:
    imports: list[int] = []

    for number, visible in active_markdown_lines(text):
        trimmed = visible.strip()
        if not trimmed or trimmed.startswith(">"):
            continue
        if trimmed in {"@AGENTS.md", "@./AGENTS.md"}:
            imports.append(number)

    return imports


def active_companion_imports(text: str) -> list[tuple[int, str]]:
    imports: list[tuple[int, str]] = []

    for number, visible in active_markdown_lines(text):
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
    if agent_only:
        issues.append(
            "AGENTS-template.md: unexpected platform-specific verbatim block(s): "
            + ", ".join(sorted(agent_only))
        )
    if claude_only:
        issues.append(
            "CLAUDE-template.md: unexpected platform-specific verbatim block(s): "
            + ", ".join(sorted(claude_only))
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
        "independent, reviewable packet",
        "fewest workers",
        "apply `worker-policy.md`",
        "brief self-contained",
        "Run writes sequentially",
        "progress and lifecycle",
        "main thread owns integration",
    )
    for token in worker_contract_tokens:
        if token not in worker_block:
            issues.append(f"templates: shared worker contract is missing {token!r}")

    for template_name, blocks in (
        ("AGENTS-template.md", agents),
        ("CLAUDE-template.md", claude),
    ):
        context_block = blocks.get("Context and Documentation", "")
        for token in INSTRUCTION_COMPANION_ROUTES:
            if token not in context_block:
                issues.append(
                    f"{template_name}: Context and Documentation conditional companion "
                    f"route is missing {token!r}"
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

    for companion in (
        "coding-agent-guide.md",
        "implementation-planning.md",
        "worker-policy.md",
        "execution-recovery.md",
        "documentation-governance.md",
    ):
        if f"`{companion}`" not in text:
            issues.append(
                f"{name}/SKILL.md: seven-surface foundation must name "
                f"`{companion}`"
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
        "ten controlled references",
        "seven required pieces",
        "Superpowers overlay",
        "configuration allowed for the task",
        "three practical Codex bands",
        "both checks must pass",
        "one recovery fix and one independent re-review",
    ):
        require_text(english, token, "README.md", issues, case_sensitive=False)
    for token in (
        "十个受控 reference",
        "七项基础内容",
        "Superpowers overlay",
        "任务允许使用的配置",
        "三个 Codex 档位，档内不排座次",
        "是否符合需求、实现质量是否过关，两项都要通过",
        "一轮恢复修正和一次复审",
    ):
        require_text(chinese, token, "README_CN.md", issues, case_sensitive=False)
    for token in ("five-round limit", "same unresolved problem across tasks"):
        require_text(english, token, "README.md", issues, case_sensitive=False)
    for token in ("每项任务最多五轮普通修复与复审", "同一个未解决的问题"):
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
        (
            "strict preset ladder",
            re.compile(re.escape(LEGACY_CODEX_PRESET_LADDER), re.IGNORECASE),
        ),
    )
    allowed_versioned_model_surfaces = {
        Path("references/worker-policy-template.md"),
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
        model_matches = list(versioned_model.finditer(text))
        if relative not in allowed_versioned_model_surfaces and model_matches:
            issues.append(
                f"{relative}: forbidden versioned model outside Codex policy surfaces: "
                f"{model_matches[0].group(0)}"
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
        for token in (
            *PLANNING_GUIDE_HEADINGS,
            *PLANNING_WORKFLOW_TOKENS,
            *PLANNING_FIELD_PATTERNS,
            *PLANNING_TASK_CONTRACT_TOKENS,
            *PLANNING_WIDE_CHANGE_TOKENS,
            "80 lines",
        ):
            require_text(
                planning_template,
                token,
                "implementation-planning-template.md",
                issues,
            )

    worker_template = read_text(
        root / "references" / "worker-policy-template.md",
        issues,
        "references/worker-policy-template.md",
    )
    if worker_template is not None:
        headings, sections = final_shape_sections(worker_template)
        validate_worker_policy_contract(
            worker_template,
            headings,
            sections,
            "worker-policy-template.md",
            issues,
        )
        for token in (
            "Final file hard limit: 100 lines",
            "Source-template hard limit: 140 lines",
            "Start with `# Worker Policy`",
            "Never use a Claude `@` import",
        ):
            require_text(worker_template, token, "worker-policy-template.md", issues)

    recovery_template = read_text(
        root / "references" / "execution-recovery-template.md",
        issues,
        "references/execution-recovery-template.md",
    )
    if recovery_template is not None:
        headings, sections = final_shape_sections(recovery_template)
        validate_execution_recovery_contract(
            headings,
            sections,
            "execution-recovery-template.md",
            issues,
        )
        for token in (
            "Final file hard limit: 80 lines",
            "Source-template hard limit: 140 lines",
            "Start with `# Execution Recovery`",
            "Never use a Claude `@` import",
        ):
            require_text(
                recovery_template,
                token,
                "execution-recovery-template.md",
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
            "`worker-policy.md`",
            "`execution-recovery.md`",
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
    for number, imported in active_companion_imports(text):
        issues.append(
            f"final file auto-imports companion {imported!r} at line {number}; "
            "use a backticked literal path and load it on demand"
        )
    if FINAL_MARKER_LEAK_RE.search(text):
        issues.append("final file contains a template marker")
    generation_leaks = (
        "generation contract",
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
    if kind == "planning-guide" and "template contract" in lower:
        issues.append("final file contains generation-only text: 'template contract'")
    if kind == "planning-guide" and re.search(
        r"<(?:one observable|task identifiers|mechanical\s*\|\s*standard\s*\|\s*judgment)",
        text,
        re.IGNORECASE,
    ):
        issues.append("final file contains a generation-only planning placeholder")

    headings = [
        match.group(1).strip()
        for _, line in active_markdown_lines(text)
        if (match := TOP_HEADING_RE.match(line))
    ]
    all_heading_titles = [
        title
        for _, line in active_markdown_lines(text)
        if (title := heading_title(line))
    ]
    forbidden_heading_names = {
        "NHK Governance",
        "NHK Govern",
        "Instruction Coverage",
        "Template Notes",
        "Agent Instructions Template",
        "Claude Code Project Instructions Template",
    }
    for _, line in active_markdown_lines(text):
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
            for _, line in active_markdown_lines(text)
            if (match := re.match(r"^#(?!#)\s+(.+?)\s*$", line))
        ]
        expected_h1 = {
            "coding-guide": "Coding Agent Guide",
            "planning-guide": "Implementation Planning",
            "worker-policy": "Worker Policy",
            "execution-recovery": "Execution Recovery",
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
            sections = second_level_sections(text)
            workflow = sections.get("Workflow Compatibility", "")
            for token in PLANNING_WORKFLOW_TOKENS:
                if token.lower() not in workflow.lower():
                    issues.append(
                        "planning-guide Workflow Compatibility is missing "
                        + repr(token)
                    )
            task_contract = sections.get("Task Contract", "")
            for field, pattern in PLANNING_FIELD_PATTERNS.items():
                if not pattern.search(task_contract):
                    issues.append(
                        f"planning-guide Task Contract is missing field syntax for {field!r}"
                    )
            for token in PLANNING_TASK_CONTRACT_TOKENS:
                if token.lower() not in task_contract.lower():
                    issues.append(
                        f"planning-guide Task Contract is missing {token!r}"
                    )
            wide_changes = sections.get("Wide Changes", "")
            for token in PLANNING_WIDE_CHANGE_TOKENS:
                if token.lower() not in wide_changes.lower():
                    issues.append(
                        f"planning-guide Wide Changes is missing {token!r}"
                    )
        elif kind == "worker-policy":
            validate_worker_policy_contract(
                text,
                tuple(headings),
                second_level_sections(text),
                "worker-policy final file",
                issues,
            )
        elif kind == "execution-recovery":
            validate_execution_recovery_contract(
                tuple(headings),
                second_level_sections(text),
                "execution-recovery final file",
                issues,
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
            roles = second_level_sections(text).get("Document Roles", "")
            for token in ("worker-policy.md", "execution-recovery.md"):
                if token not in roles:
                    issues.append(
                        f"doc-governance Document Roles is missing {token!r}"
                    )
        return issues

    imports = valid_import_lines(text)
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
    context = second_level_sections(text).get("Context and Documentation", "")
    for route in INSTRUCTION_COMPANION_ROUTES:
        if route not in context:
            companion = next(
                name
                for name in (
                    "coding-agent-guide.md",
                    "implementation-planning.md",
                    "worker-policy.md",
                    "execution-recovery.md",
                    "documentation-governance.md",
                )
                if name in route
            )
            issues.append(
                "standalone final Context and Documentation must contain the "
                f"conditional literal route for `{companion}`"
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
            "worker-policy",
            "execution-recovery",
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
