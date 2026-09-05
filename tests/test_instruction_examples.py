from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
FIXTURE = ROOT / "tests" / "fixtures" / "instruction-examples" / "baseline-metrics.json"

MARKER_RE = re.compile(r"^\[\[([A-Z_]+):(BEGIN|END)\]\]$")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
FINAL_HEADINGS = (
    "Project Map",
    "Execution Rules",
    "Context and Documentation",
    "Subagents and Packets",
    "Blockers and Human Approval",
    "Testing and Verification",
    "Git and Delivery",
)
FINAL_LIMITS = {"simple": 100, "medium": 125, "complex": 150}
COMPANION_PATHS = (
    "coding-agent-guide.md",
    "implementation-planning.md",
    "worker-policy.md",
    "execution-recovery.md",
    "documentation-governance.md",
)

PROJECT_ADAPTATIONS = {
    "simple": {
        "Project Map": """## Project Map

- Atlas Notes is a Python CLI that turns reviewed Markdown notes into a local search index.
- Read `coding-agent-guide.md` to route a task or symptom to code and first-pass verification.
- Treat `fixtures/source-notes/` as immutable input.""",
        "Project-specific Approval Boundaries": "",
        "Project Verification Commands": """### Project Verification Commands

- Run `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` as the final delivery gate.""",
        "Project Git and Delivery Policy": """### Project Git and Delivery Policy

- Work on the current feature branch and commit only files owned by the task.""",
    },
    "medium": {
        "Project Map": """## Project Map

- Atlas Notes is a Python CLI and SQLite indexer for a shared research workspace.
- Read `coding-agent-guide.md` to route a task or symptom to code and first-pass verification.
- Treat `fixtures/source-notes/` as immutable input.
- Preserve the public JSON export schema unless the human approves a contract change.""",
        "Additional Project Boundaries": """### Additional Project Boundaries

- Route database migrations and export-schema changes through the compatibility checks in `coding-agent-guide.md`.""",
        "Project-specific Approval Boundaries": """### Project-specific Approval Boundaries

- Ask before changing the export schema or rewriting an existing index; diagnose against a disposable copy first.""",
        "Project Verification Commands": """### Project Verification Commands

- Run the focused module test while iterating.
- Run `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` and `python3 -m atlas smoke fixtures/source-notes` before delivery.""",
        "Project Git and Delivery Policy": """### Project Git and Delivery Policy

- Work on the current feature branch, preserve unrelated edits, and commit only files owned by the task.""",
    },
    "complex": {
        "Project Map": """## Project Map

- Atlas Notes is a Python CLI, SQLite indexer, and JSON export service for a shared research workspace.
- Read `coding-agent-guide.md` to route a task or symptom to code and first-pass verification.
- Treat `fixtures/source-notes/` as immutable input.
- Preserve the public JSON export schema and transactional index replacement unless the human approves a contract change.""",
        "Additional Project Boundaries": """### Additional Project Boundaries

- Route database migrations, concurrent indexing, and export-schema changes through the compatibility checks in `coding-agent-guide.md`.
- Run destructive migration experiments only against the disposable workspace fixture.""",
        "Project-specific Approval Boundaries": """### Project-specific Approval Boundaries

- Ask before changing the export schema, transaction boundary, or index replacement semantics.
- Reproduce data-loss symptoms against a disposable copy before proposing a repair.""",
        "Project Verification Commands": """### Project Verification Commands

- Run the focused module test while iterating.
- Run the full unit suite, schema compatibility suite, and concurrent-indexing smoke test before delivery.
- Use `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` as the final delivery gate.""",
        "Project Git and Delivery Policy": """### Project Git and Delivery Policy

- Work on the current feature branch, preserve unrelated edits, and commit only files owned by the task.
- Record the schema and migration checks in the handoff for any release-bound change.""",
    },
}


def first_heading(content: str) -> str | None:
    for line in content.splitlines():
        match = HEADING_RE.match(line)
        if match:
            return match.group(1)
    return None


def parse_blocks(text: str) -> list[tuple[str, str, str | None]]:
    blocks: list[tuple[str, str, str | None]] = []
    active_kind: str | None = None
    active_lines: list[str] = []
    for line in text.splitlines():
        marker = MARKER_RE.match(line.strip())
        if marker:
            kind, action = marker.groups()
            if action == "BEGIN":
                if active_kind is not None:
                    raise AssertionError(f"nested marker {kind} inside {active_kind}")
                active_kind = kind
                active_lines = []
            else:
                if active_kind != kind:
                    raise AssertionError(f"unmatched marker end {kind}")
                content = "\n".join(active_lines).strip()
                blocks.append((kind, content, first_heading(content)))
                active_kind = None
                active_lines = []
            continue
        if active_kind is not None:
            active_lines.append(line)
    if active_kind is not None:
        raise AssertionError(f"unclosed marker {active_kind}")
    return blocks


def assemble_standalone(template: Path, complexity: str) -> str:
    adaptation = PROJECT_ADAPTATIONS[complexity]
    output: list[str] = []
    for kind, content, heading in parse_blocks(template.read_text(encoding="utf-8")):
        if kind == "FINAL_VERBATIM":
            output.append(content)
        elif kind == "FINAL_ADAPT":
            output.append(adaptation.get(heading or "", ""))
        elif kind == "OPTIONAL_BY_COMPLEXITY" and complexity != "simple":
            output.append(adaptation.get(heading or "", ""))
    return "\n\n".join(part for part in output if part).strip() + "\n"


def assemble_thin_claude() -> str:
    return """@AGENTS.md

# Claude Code Notes

- Treat the imported `AGENTS.md` as canonical and follow its literal companion routes on demand.
"""


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def adaptation_sha256() -> str:
    payload = json.dumps(PROJECT_ADAPTATIONS, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class InstructionExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_generated_examples_reduce_always_loaded_words(self) -> None:
        self.assertEqual(self.baseline["base_commit"], "fb107f66c92fcc3d1d2672209c3984c7f3842972")
        self.assertEqual(self.baseline["adaptation_sha256"], adaptation_sha256())
        self.assertEqual(
            self.baseline["source_template_sha256"],
            {
                "AGENTS-template.md": "541b93699ec1e49864c5901cb353aa5f6d461bbe60ecec782abc7b2c283eb139",
                "CLAUDE-template.md": "294ecc4fc89817294cb1db1157bcce18fe36ee17494cc8f0433294306ca6945e",
            },
        )
        for template_name in ("AGENTS-template.md", "CLAUDE-template.md"):
            for complexity in FINAL_LIMITS:
                with self.subTest(template=template_name, complexity=complexity):
                    key = f"{template_name}:{complexity}"
                    current = word_count(
                        assemble_standalone(REFERENCES / template_name, complexity)
                    )
                    baseline = self.baseline["word_counts"][key]
                    self.assertLessEqual(
                        current * 100,
                        baseline * 80,
                        f"{key}: {current} words is not at least 20% below {baseline}",
                    )

    def test_generated_standalone_examples_are_clean_and_readable(self) -> None:
        for template_name in ("AGENTS-template.md", "CLAUDE-template.md"):
            for complexity, limit in FINAL_LIMITS.items():
                with self.subTest(template=template_name, complexity=complexity):
                    example = assemble_standalone(REFERENCES / template_name, complexity)
                    lines = example.splitlines()
                    headings = tuple(
                        line.removeprefix("## ")
                        for line in lines
                        if line.startswith("## ") and not line.startswith("### ")
                    )
                    self.assertEqual(headings, FINAL_HEADINGS)
                    self.assertLessEqual(len(lines), limit)
                    self.assertNotRegex(example, r"\[\[[A-Z_]+:(?:BEGIN|END)\]\]")
                    self.assertNotIn("Replace this guidance", example)
                    self.assertNotIn("Write two to four bullets", example)
                    self.assertLessEqual(max(word_count(line) for line in lines), 32)
                    for path in COMPANION_PATHS:
                        self.assertIn(f"`{path}`", example)

    def test_thin_claude_example_is_small_clean_and_literal(self) -> None:
        example = assemble_thin_claude()
        lines = example.splitlines()
        self.assertLessEqual(len(lines), 35)
        self.assertEqual(lines.count("@AGENTS.md"), 1)
        self.assertNotRegex(example, r"@(?:\./)?(?:coding-agent-guide|implementation-planning|worker-policy|execution-recovery|documentation-governance)\.md")
        self.assertNotIn("[[", example)
        self.assertLessEqual(max(word_count(line) for line in lines), 24)

    def test_companion_templates_cover_final_contracts(self) -> None:
        cases = {
            "worker-policy-template.md": (
                140,
                "Worker Policy",
                ("Dispatch Contract", "Review Gates", "Codex Routing", "Claude Routing"),
            ),
            "execution-recovery-template.md": (
                140,
                "Execution Recovery",
                ("Triggers and Accounting", "Main-thread Reassessment", "Independent Diagnosis", "Recovery and Stop"),
            ),
        }
        for name, (limit, h1, h2s) in cases.items():
            with self.subTest(template=name):
                text = (REFERENCES / name).read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), limit)
                self.assertIn(f"# {h1}", text)
                for heading in h2s:
                    self.assertIn(f"### {heading}", text)


if __name__ == "__main__":
    unittest.main()
