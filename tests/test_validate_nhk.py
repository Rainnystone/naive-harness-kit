from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_instruction_examples import assemble_companion, assemble_standalone


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_nhk.py"

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

REFERENCES = (
    "AGENTS-template.md",
    "CLAUDE-template.md",
    "coding-agent-guide-template.md",
    "implementation-planning-template.md",
    "worker-policy-template.md",
    "execution-recovery-template.md",
    "documentation-governance-template.md",
    "archive-readme-template.md",
    "claude-agents-template.md",
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

TASK_ROUTING_COLUMNS = (
    "Task or Symptom",
    "Read First",
    "Likely Change Surface",
    "Targeted Verification",
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

LEGACY_CODEX_PRESET_LADDER = (
    "GPT-5.6 Luna max → GPT-5.5 xhigh → GPT-5.6 Terra high → "
    "GPT-5.6 Terra xhigh → GPT-5.6 Terra max → GPT-5.6 Sol xhigh → "
    "GPT-5.6 Sol max"
)

CODEX_PRESET_BAND_LINES = (
    "Band 1: GPT-6 Luna max.",
    "Band 2: GPT-6 Astra medium.",
    "Band 3: GPT-6 Astra xhigh.",
)

COMPANION_ROUTES = (
    "`coding-agent-guide.md`",
    "`implementation-planning.md`",
    "`worker-policy.md`",
    "`execution-recovery.md`",
    "`documentation-governance.md`",
)

def run_cli(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *(str(arg) for arg in args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def standalone_text(extra_lines: int = 0) -> str:
    lines: list[str] = []
    for heading in FINAL_HEADINGS:
        lines.extend((f"## {heading}", "", f"- Project rule for {heading}.", ""))
        if heading == "Project Map":
            lines.extend(
                (
                    "- Use `coding-agent-guide.md` for task routing.",
                    "- Use `documentation-governance.md` for document lifecycle rules.",
                    "- Read `implementation-planning.md` only before plan work.",
                    "- Read `worker-policy.md` only when dispatching or reviewing workers.",
                    "- Read `execution-recovery.md` only after its recovery trigger fires.",
                    "",
                )
            )
    lines.extend(f"- extra {index}" for index in range(extra_lines))
    return "\n".join(lines).rstrip() + "\n"


def coding_guide_text(extra_lines: int = 0) -> str:
    lines = [
        "# Coding Agent Guide",
        "",
        "Use this guide to route coding tasks without loading a full repository map.",
        "",
        "## Task Routing",
        "",
        "| Task or Symptom | Read First | Likely Change Surface | Targeted Verification |",
        "| --- | --- | --- | --- |",
        "| UI behavior | `src/ui/` | `src/ui/` | `npm test -- ui` |",
    ]
    lines.extend(f"- extra {index}" for index in range(extra_lines))
    return "\n".join(lines).rstrip() + "\n"


def doc_governance_text(extra_lines: int = 0) -> str:
    sections = {
        "Document Roles": (
            "Instructions govern behavior; the routing guide routes coding work; "
            "`implementation-planning.md` owns stable task sizing; "
            "`worker-policy.md` owns dispatch; `execution-recovery.md` owns recovery."
        ),
        "Active Documentation Surfaces": "Active plans and tracking contain active work only.",
        "Workspace and Document Map": "Use `AGENTS.md`, the routing guide, active docs, and `archive/README.md`.",
        "Lifecycle Rules": (
            "Keep `implementation-planning.md` active; archive completed "
            "implementation plans with their workstreams."
        ),
        "Naming and Loading": "Use distinct names and load only task-relevant documents.",
        "Archive Transition Invariants": (
            "Explicit human approval is required before archiving. Copy materials and update "
            "the archive index before verification. If verification fails, preserve every "
            "active original. Reset tracking only when no other live workstream depends on it."
        ),
    }
    lines = ["# Documentation Governance", ""]
    for heading, body in sections.items():
        lines.extend((f"## {heading}", "", body, ""))
    lines.extend(f"- extra {index}" for index in range(extra_lines))
    return "\n".join(lines).rstrip() + "\n"


def planning_guide_text(extra_lines: int = 0) -> str:
    text = assemble_companion(
        ROOT / "references" / "implementation-planning-template.md", "Implementation Planning"
    )
    for placeholder in (
        "one observable, independently acceptable result",
        "task identifiers, or None",
        "mechanical | standard | judgment",
    ):
        text = text.replace(f"<{placeholder}>", placeholder)
    return text + "extra\n" * extra_lines


def human_routing_exception(**overrides: str) -> str:
    record = {
        "target": "billing-module",
        "scope": "src/billing/",
        "role": "module-implementation",
        "preset": "GPT-6 Astra xhigh",
        "approval": "decisions/billing.md#low-route",
    }
    record.update(overrides)
    return "- Human routing exception: " + json.dumps(record)


def literal_routing_record_cases():
    records = (
        human_routing_exception(approval="decisions/gpt-6-astra-low.md#billing"),
        human_routing_exception(approval="https://example.test/gpt-6-astra-xhigh.md#billing"),
        human_routing_exception(target="gpt-6-astra-low-module"),
        human_routing_exception(scope="src/gpt-6-astra-low/"),
        human_routing_exception(scope="docs/GPT-6 Astra xhigh review.md"),
    )
    for record in records:
        yield record, "", None, 0
    record = records[0]
    yield record, "Whole modules may use GPT-6 Astra low.", None, 1
    yield record, "Use GPT-6 Astra xhigh for ordinary implementation.", None, 1
    yield record, "", ("GPT-6 Luna max", "GPT-6 Luna high"), 1
    yield human_routing_exception(approval="decisions/gpt-6-astra-low.md"), "", None, 1
    yield human_routing_exception(preset="GPT-6 Astra max"), "", None, 1


def worker_policy_text() -> str:
    return assemble_companion(
        ROOT / "references" / "worker-policy-template.md", "Worker Policy"
    )


def execution_recovery_text() -> str:
    return assemble_companion(
        ROOT / "references" / "execution-recovery-template.md", "Execution Recovery"
    )


class ValidatorTestCase(unittest.TestCase):
    def make_source_fixture(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for skill in SKILLS:
            shutil.copytree(ROOT / skill, root / skill)
        shutil.copytree(ROOT / "references", root / "references")
        shutil.copy2(ROOT / "AGENTS.md", root / "AGENTS.md")
        shutil.copy2(ROOT / "CLAUDE.md", root / "CLAUDE.md")
        shutil.copy2(ROOT / "README.md", root / "README.md")
        shutil.copy2(ROOT / "README_CN.md", root / "README_CN.md")
        return root

    def make_install_fixture(self, nested: bool = False) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        target = root / "nhk" if nested else root
        target.mkdir(exist_ok=True)
        for skill in SKILLS:
            shutil.copytree(ROOT / skill, target / skill)
        shutil.copytree(ROOT / "references", target / "references")
        return root

    def write_final(self, content: str) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "instruction.md"
        path.write_text(content, encoding="utf-8")
        return path


class SourceValidationTests(ValidatorTestCase):
    def test_compliant_source_fixture_passes(self) -> None:
        result = run_cli("--root", self.make_source_fixture())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_reference_fails(self) -> None:
        root = self.make_source_fixture()
        (root / "references" / "dependency-setup.md").unlink()
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("dependency-setup.md", result.stdout)

    def test_missing_new_companion_templates_fail(self) -> None:
        for name in ("worker-policy-template.md", "execution-recovery-template.md"):
            with self.subTest(name=name):
                root = self.make_source_fixture()
                (root / "references" / name).unlink()
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(name, result.stdout)

    def test_missing_planning_reference_fails(self) -> None:
        root = self.make_source_fixture()
        (root / "references" / "implementation-planning-template.md").unlink(
            missing_ok=True
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("implementation-planning-template.md", result.stdout)

    def test_bad_skill_frontmatter_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "nhk-upkeep" / "SKILL.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "name: nhk-upkeep", "name: wrong-name", 1
            ),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("frontmatter", result.stdout.lower())

    def test_skill_description_leading_words_fail(self) -> None:
        for skill, leading_word in SKILL_DESCRIPTION_LEADS.items():
            with self.subTest(skill=skill):
                root = self.make_source_fixture()
                path = root / skill / "SKILL.md"
                lines = path.read_text(encoding="utf-8").splitlines()
                description = next(
                    index
                    for index, line in enumerate(lines)
                    if line.startswith("description:")
                )
                lines[description] = "description: Use when NHK work needs attention."
                path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(leading_word, result.stdout)

    def test_router_handoff_contract_fails(self) -> None:
        cases = (
            ("**Dependencies**", "**Tools**"),
            ("only in conversation", "available temporarily"),
            ("current workspace", "selected workspace"),
            (
                "dependency state, instruction topology, foundation state, "
                "lifecycle intent, or workspace changes",
                "workspace changes",
            ),
            ("human choice remains unresolved", "a choice is pending"),
        )
        for required, replacement in cases:
            with self.subTest(required=required):
                root = self.make_source_fixture()
                path = root / "welcome-to-nhk" / "SKILL.md"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(required, replacement, 1),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("handoff", result.stdout.lower())

    def test_leaf_router_handoff_contract_fails(self) -> None:
        cases = (
            ("## Router Handoff", "## Entry Check"),
            ("absent, unresolved, or stale", "unavailable"),
            ("If it selects another route", "If routing differs"),
        )
        for skill in ("nhk-bootstrap", "nhk-upkeep", "nhk-archive"):
            for required, replacement in cases:
                with self.subTest(skill=skill, required=required):
                    root = self.make_source_fixture()
                    path = root / skill / "SKILL.md"
                    path.write_text(
                        path.read_text(encoding="utf-8").replace(
                            required, replacement, 1
                        ),
                        encoding="utf-8",
                    )
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("handoff", result.stdout.lower())

    def test_upkeep_requires_installed_contract_reconciliation(self) -> None:
        cases = (
            ("welcome-to-nhk", "after an NHK update needs workspace reconciliation"),
            ("nhk-upkeep", "even when workspace documents look complete and project facts have not changed"),
            ("nhk-upkeep", "Preserve correct project facts and human-authorized exceptions"),
            ("nhk-upkeep", "every compared surface matches the current installed contract or has a recorded human-authorized exception or unresolved conflict"),
        )
        for skill, required in cases:
            with self.subTest(skill=skill, required=required):
                root = self.make_source_fixture()
                path = root / skill / "SKILL.md"
                content = path.read_text()
                self.assertIn(required, content)
                path.write_text(content.replace(required, "only repair visible structural damage", 1))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("update reconciliation", result.stdout)

    def test_source_rejects_additive_model_routes(self) -> None:
        cases = (
            ("worker-policy-template.md", "Codex Routing", "GPT-6 Astra xhigh is approved for ordinary implementation."),
            ("execution-recovery-template.md", "Independent Diagnosis", "Dispatch GPT-6 Astra max for diagnosis."),
        )
        for file, heading, extra in cases:
            with self.subTest(file=file):
                root = self.make_source_fixture()
                path = root / "references" / file
                path.write_text(path.read_text().replace(f"### {heading}", f"### {heading}\n\n- {extra}", 1))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("routing", result.stdout)

    def test_bootstrap_handoff_and_instruction_loading_contract_fails(self) -> None:
        cases = (
            (
                "After bootstrap changes the foundation, rerun `welcome-to-nhk`",
                "After bootstrap changes the foundation, continue",
            ),
            (
                "If bootstrap is creating, structurally repairing, or making the specific "
                "semantic policy/recovery migration above",
                "For the instruction surface",
            ),
            (
                "Do not load an instruction template when only a companion or "
                "archive surface is missing and the canonical instruction has no "
                "superseded NHK-owned policy or recovery text.",
                "Use the matching template.",
            ),
        )
        for required, replacement in cases:
            with self.subTest(required=required):
                root = self.make_source_fixture()
                path = root / "nhk-bootstrap" / "SKILL.md"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(required, replacement, 1),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("bootstrap", result.stdout.lower())

    def test_flat_local_reference_inventory_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "welcome-to-nhk" / "SKILL.md"
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n## Local References\n\n- `../references/validation-scenarios.md`\n",
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("conditional context pointer", result.stdout.lower())

    def test_nested_marker_and_outside_text_fail(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "AGENTS-template.md"
        text = path.read_text(encoding="utf-8")
        text = "outside\n" + text.replace(
            "[[FINAL_VERBATIM:BEGIN]]",
            "[[FINAL_VERBATIM:BEGIN]]\n[[FINAL_ADAPT:BEGIN]]",
            1,
        )
        path.write_text(text, encoding="utf-8")
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("marker", result.stdout.lower())

    def test_shared_verbatim_drift_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "CLAUDE-template.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "Prefer the smallest direct change",
                "Prefer a broad speculative change",
                1,
            ),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("shared verbatim", result.stdout.lower())

    def test_instruction_templates_require_all_conditional_companion_routes(self) -> None:
        cases = (
            (
                "`worker-policy.md` only when orchestrating, dispatching, or reviewing workers",
                "`worker-policy.md` when useful",
            ),
            (
                "`execution-recovery.md` after five failed rounds on one task or one acceptance gap, or earlier evidence of architectural stagnation",
                "`execution-recovery.md` after problems",
            ),
        )
        for template_name in ("AGENTS-template.md", "CLAUDE-template.md"):
            for required, replacement in cases:
                with self.subTest(template=template_name, required=required):
                    root = self.make_source_fixture()
                    path = root / "references" / template_name
                    path.write_text(
                        path.read_text(encoding="utf-8").replace(
                            required, replacement, 1
                        ),
                        encoding="utf-8",
                    )
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("conditional companion route", result.stdout.lower())

    def test_instruction_route_wording_elsewhere_does_not_satisfy_context_section(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "AGENTS-template.md"
        required = (
            "- Read `worker-policy.md` only when orchestrating, dispatching, or reviewing "
            "workers. Load its common sections and the current platform section."
        )
        path.write_text(
            path.read_text(encoding="utf-8").replace(required, "", 1)
            + f"\n{required}\n",
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Context and Documentation", result.stdout)

    def test_template_source_line_limit_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "AGENTS-template.md"
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n".join(f"extra {index}" for index in range(80)),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("190", result.stdout)

    def test_companion_source_line_limits_fail(self) -> None:
        cases = (
            ("coding-agent-guide-template.md", 140),
            ("implementation-planning-template.md", 120),
            ("worker-policy-template.md", 140),
            ("execution-recovery-template.md", 140),
            ("documentation-governance-template.md", 160),
            ("archive-readme-template.md", 40),
        )
        for name, limit in cases:
            with self.subTest(name=name):
                root = self.make_source_fixture()
                path = root / "references" / name
                path.write_text(
                    path.read_text(encoding="utf-8") + "\n".join(
                        f"extra {index}" for index in range(200)
                    ),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(str(limit), result.stdout)

    def test_planning_template_requires_final_contract(self) -> None:
        for token in (*PLANNING_GUIDE_HEADINGS, "80 lines"):
            with self.subTest(token=token):
                mutated = self.make_source_fixture()
                mutated_path = (
                    mutated / "references" / "implementation-planning-template.md"
                )
                mutated_path.write_text(
                    planning_guide_text().replace(token, "missing contract", 1),
                    encoding="utf-8",
                )
                result = run_cli("--root", mutated)
                self.assertEqual(result.returncode, 1)
                self.assertIn(token, result.stdout)

    def test_governance_template_requires_new_companion_paths(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "documentation-governance-template.md"
        text = path.read_text(encoding="utf-8")
        start = text.index("### Document Roles")
        end = text.index("### Active Documentation Surfaces")
        chunk = (
            text[start:end]
            .replace("`worker-policy.md`", "`other-companion.md`")
            .replace("`execution-recovery.md`", "`other-companion.md`")
        )
        path.write_text(text[:start] + chunk + text[end:], encoding="utf-8")
        self.assertIn("`worker-policy.md`", path.read_text(encoding="utf-8"))
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Document Roles", result.stdout)
        self.assertIn("worker-policy.md", result.stdout)

    def test_review_source_alias_and_class_conflicts(self) -> None:
        cases = (
            ("worker-policy-template.md", "### Dispatch Contract", "Use Extra High for ordinary implementation."),
            ("worker-policy-template.md", "### Codex Routing", "Use Light for module implementation."),
            ("implementation-planning-template.md", "### Task Contract", "Whole modules may use mechanical workers."),
            ("implementation-planning-template.md", "## Required Final Shape", "Assign mechanical as the worker class for complete modules."),
            ("implementation-planning-template.md", "### Task Contract", "Worker class: mechanical for whole modules."),
        )
        for filename, anchor, clause in cases:
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(filename=filename, clause=clause, wrapper=wrapper):
                    root = self.make_source_fixture()
                    path = root / "references" / filename
                    path.write_text(path.read_text().replace(anchor, anchor + "\n\n" + wrapper.format(clause), 1))
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_source_helper_cadence(self) -> None:
        for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
            root = self.make_source_fixture()
            for filename in ("AGENTS-template.md", "CLAUDE-template.md"):
                path = root / "references" / filename
                clause = wrapper.format("Check each helper's progress every\n5 minutes.")
                path.write_text(path.read_text().replace("## Git and Delivery", "## Git and Delivery\n" + clause, 1))
            result = run_cli("--root", root)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_source_fields_must_remain_active(self) -> None:
        for wrapper in ("<!-- {} -->", "```md\n{}\n```"):
            root = self.make_source_fixture()
            path = root / "references" / "implementation-planning-template.md"
            text = path.read_text()
            start = text.index("**Delivers:**")
            end = text.index("\n", text.index("**Worker class:**", start))
            path.write_text(text[:start] + wrapper.format(text[start:end]) + text[end:])
            result = run_cli("--root", root)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("field syntax", result.stdout)

    def test_review_source_helper_function_timeout_remains_valid(self) -> None:
        root = self.make_source_fixture()
        for filename in ("AGENTS-template.md", "CLAUDE-template.md"):
            path = root / "references" / filename
            path.write_text(path.read_text().replace("## Git and Delivery", "## Git and Delivery\nThe HTTP helper function has a timeout of 15 seconds.", 1))
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_review_source_human_routing_exception_records(self) -> None:
        for heading, record, expected in (
            ("### Codex Routing", human_routing_exception(), 0),
            ("### Dispatch Contract", human_routing_exception(), 1),
            ("## Template Contract", human_routing_exception(), 1),
            ("## Final Check", human_routing_exception(), 1),
            ("### Codex Routing", human_routing_exception(target="all-modules"), 1),
            ("### Codex Routing", human_routing_exception(approval="approved"), 1),
        ):
            root = self.make_source_fixture()
            path = root / "references" / "worker-policy-template.md"
            path.write_text(path.read_text().replace(heading, heading + "\n" + record, 1))
            result = run_cli("--root", root)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_source_literal_record_data_is_not_policy(self) -> None:
        for record, adjacent, drift, expected in literal_routing_record_cases():
            with self.subTest(record=record, adjacent=adjacent, drift=drift):
                root = self.make_source_fixture()
                path = root / "references" / "worker-policy-template.md"
                text = path.read_text().replace("### Codex Routing", "### Codex Routing\n" + record + "\n" + adjacent, 1)
                if drift:
                    text = text.replace(*drift)
                path.write_text(text)
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_source_exception_marker_cannot_move_to_another_file(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "implementation-planning-template.md"
        path.write_text(path.read_text() + "\n- Human routing exception\n")
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("routing exception", result.stdout)

    def test_worker_source_rejects_preamble_and_wrong_section_band_routes(self) -> None:
        for anchor, clause in (
            ("# Worker Policy Template", "Whole modules may use GPT-6 Astra low."),
            ("## Required Final Shape", "Whole modules may use GPT-6 Astra low."),
            ("### Dispatch Contract", "- Band 1: Whole modules may use GPT-6 Astra low."),
        ):
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(anchor=anchor, wrapper=wrapper):
                    root = self.make_source_fixture()
                    path = root / "references" / "worker-policy-template.md"
                    path.write_text(path.read_text().replace(anchor, anchor + "\n\n" + wrapper.format(clause), 1))
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_module_source_contract_rejects_additive_and_inactive_rules(self) -> None:
        for filename, anchor, clause in (
            ("worker-policy-template.md", "### Codex Routing", "Whole modules may use GPT-6 Astra low."),
            ("worker-policy-template.md", "### Review Gates", "Consolidation resets the repair count."),
            ("AGENTS-template.md", "## Subagents and Packets", "A wait return triggers a status check."),
        ):
            with self.subTest(filename=filename, clause=clause):
                root = self.make_source_fixture()
                path = root / "references" / filename
                path.write_text(path.read_text().replace(anchor, anchor + "\n- " + clause))
                if filename == "AGENTS-template.md":
                    paired = root / "references" / "CLAUDE-template.md"
                    paired.write_text(paired.read_text().replace(anchor, anchor + "\n- " + clause))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
        for filename, clause in (
            ("worker-policy-template.md", "Default module implementation, internal debugging, tests, and integration to Band 2."),
            ("implementation-planning-template.md", "Group implementation, tests, configuration, migration, and documentation for the same capability and working context."),
        ):
            for inactive in ("<!-- " + clause + " -->", "```md\n" + clause + "\n```"):
                root = self.make_source_fixture()
                path = root / "references" / filename
                self.assertIn(clause, path.read_text())
                path.write_text(path.read_text().replace(clause, inactive))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_worker_policy_source_contract_fails(self) -> None:
        mutations = (
            (
                CODEX_PRESET_BAND_LINES[0],
                "Band 1: GPT-5.6 Luna max.",
            ),
            ("Presets within a band are unordered task-fit choices", "Use the listed order"),
            ("there is no mandatory Band 1 trial", "always start in Band 1"),
            ("roles determine permission", "Escalate whenever useful"),
            (
                "Ultra authorization and recursion authorization never imply each other",
                "Ultra also authorizes recursion",
            ),
        )
        for required, replacement in mutations:
            with self.subTest(required=required):
                root = self.make_source_fixture()
                path = root / "references" / "worker-policy-template.md"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        required, replacement, 1
                    ),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("worker-policy", result.stdout.lower())

    def test_worker_policy_source_rejects_models_outside_exact_bands(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "worker-policy-template.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                CODEX_PRESET_BAND_LINES[1],
                CODEX_PRESET_BAND_LINES[1].replace("GPT-6 Astra medium", "GPT-6 Astra max"),
                1,
            ),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("exact unordered preset", result.stdout.lower())

    def test_policy_surfaces_reject_legacy_strict_ladder(self) -> None:
        root = self.make_source_fixture()
        for name in ("README.md", "README_CN.md"):
            path = root / name
            path.write_text(
                path.read_text(encoding="utf-8")
                + f"\n{LEGACY_CODEX_PRESET_LADDER}\n",
                encoding="utf-8",
            )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("strict preset ladder", result.stdout.lower())

    def test_all_skills_require_every_companion_in_the_foundation(self) -> None:
        for skill in SKILLS:
            for companion in COMPANION_ROUTES:
                with self.subTest(skill=skill, companion=companion):
                    root = self.make_source_fixture()
                    path = root / skill / "SKILL.md"
                    path.write_text(
                        path.read_text(encoding="utf-8").replace(
                            companion, "`missing-companion.md`"
                        ),
                        encoding="utf-8",
                    )
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("seven-surface foundation", result.stdout.lower())

    def test_sdd_check_interval_and_exceptions_are_required(self) -> None:
        for old, new in (
            ("at least 1800 seconds", "at least 30 seconds"),
            ("Respond immediately: completion, questions, failures, user messages", "All communication must wait"),
            ("Wait returns or silence alone never justify", "every wait-tool return warrants a progress check"),
        ):
            with self.subTest(old=old):
                root = self.make_source_fixture()
                for template in ("AGENTS-template.md", "CLAUDE-template.md"):
                    path = root / "references" / template
                    content = path.read_text()
                    self.assertIn(old, content)
                    path.write_text(content.replace(old, new, 1))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("shared worker contract", result.stdout)

    def test_check_interval_does_not_allow_fixed_worker_timeouts(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "AGENTS-template.md"
        path.write_text(path.read_text() + "\nReplace a worker after 300 seconds.\n")
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("fixed timeout", result.stdout)

    def test_forbidden_legacy_rule_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "welcome-to-nhk" / "SKILL.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\nUse gpt-5.5 for workers.\n",
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("gpt-5.5", result.stdout)

    def test_forbidden_legacy_variants_fail(self) -> None:
        variants = (
            "Use gpt-5.6-codex for every worker.",
            "Model price: $10 per 1M tokens.",
            "| Model | Input |\n| --- | --- |\n| current | $10 / 1M tokens |",
            "Supported effort: low, medium, high, xhigh.",
            "Wait 120 seconds, then 180s, then 300 seconds.",
            "Spec text budget: max 40000 tokens per session.",
            "Spec text budget: max 40k tokens per session.",
            "Use a default coverage threshold of 80%.",
        )
        for legacy_rule in variants:
            with self.subTest(legacy_rule=legacy_rule):
                root = self.make_source_fixture()
                path = root / "welcome-to-nhk" / "SKILL.md"
                path.write_text(
                    path.read_text(encoding="utf-8") + f"\n{legacy_rule}\n",
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_readme_fact_drift_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "README.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "five recurring jobs", "several recurring jobs"
            ),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("five recurring jobs", result.stdout.lower())

    def test_readme_recovery_guidance_drift_fails(self) -> None:
        root = self.make_source_fixture()
        for name in ("README.md", "README_CN.md"):
            path = root / name
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "five-round limit", "unbounded task loop"
                ),
                encoding="utf-8",
            )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("five-round", result.stdout.lower())

    def test_readme_main_thread_guidance_removal_fails(self) -> None:
        cases = (("README.md",), ("README_CN.md",), ("README.md", "README_CN.md"))
        for names in cases:
            with self.subTest(names=names):
                root = self.make_source_fixture()
                for name in names:
                    path = root / name
                    paragraphs = path.read_text(encoding="utf-8").split("\n\n")
                    guidance = [p for p in paragraphs if "GPT-6 Sol" in p]
                    self.assertEqual(len(guidance), 1)
                    paragraphs.remove(guidance[0])
                    path.write_text("\n\n".join(paragraphs), encoding="utf-8")
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                for name in names:
                    self.assertIn(f"{name}: missing required fact", result.stdout)

    def test_readme_main_thread_guidance_drift_fails(self) -> None:
        cases = (
            ("README.md", "we suggest GPT-6 Sol", "we suggest another available model"),
            ("README.md", "human-facing suggestion only", "mandatory main-thread policy"),
            ("README.md", "you choose the main-thread model and effort", "NHK chooses the main-thread model and effort"),
            ("README.md", "NHK worker permissions do not depend on that choice", "NHK worker permissions depend on that choice"),
            ("README_CN.md", "建议考虑 GPT-6 Sol", "建议考虑其他可用型号"),
            ("README_CN.md", "这只是给使用者的建议", "这是强制的主线程规则"),
            ("README_CN.md", "主线程型号和 effort 由你选择", "主线程型号和 effort 由 NHK 选择"),
            ("README_CN.md", "NHK 的 worker 权限不依赖该选择", "NHK 的 worker 权限依赖该选择"),
        )
        for name, required, replacement in cases:
            with self.subTest(name=name, required=required):
                root = self.make_source_fixture()
                path = root / name
                content = path.read_text(encoding="utf-8")
                self.assertIn(required, content)
                path.write_text(content.replace(required, replacement, 1), encoding="utf-8")
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f"{name}: missing required fact", result.stdout)

    def test_readme_routing_and_claude_loading_drift_fails(self) -> None:
        root = self.make_source_fixture()
        replacements = (
            ("README.md", "routing table is the shallow code map"),
            ("README_CN.md", "路由表就是新手需要的浅层 code map"),
        )
        for name, fact in replacements:
            path = root / name
            path.write_text(
                path.read_text(encoding="utf-8").replace(fact, "routing details"),
                encoding="utf-8",
            )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("shallow code map", result.stdout.lower())

    def test_readme_planning_and_worker_policy_drift_fails(self) -> None:
        cases = (
            ("README.md", "eleven controlled references", "several references"),
            ("README.md", "Every Claude helper runs Opus", "Claude helpers use a model"),
            ("README.md", "Claude Code main thread, we suggest Opus", "Claude Code main thread, pick anything"),
            ("README.md", "seven required pieces", "the foundation"),
            ("README.md", "Superpowers overlay", "planning helper"),
            (
                "README.md",
                "three practical Codex bands",
                "several worker options",
            ),
            ("README_CN.md", "十一个受控 reference", "几份 reference"),
            ("README_CN.md", "Claude 的帮手全部使用 Opus", "Claude 的帮手随便选"),
            ("README_CN.md", "Claude Code 主线程，建议使用 Opus", "Claude Code 主线程随意"),
            ("README_CN.md", "七项基础内容", "基础文档"),
            ("README_CN.md", "Superpowers overlay", "规划辅助"),
        )
        for name, required, replacement in cases:
            with self.subTest(name=name, required=required):
                root = self.make_source_fixture()
                path = root / name
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        required, replacement, 1
                    ),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(required, result.stdout)

    def test_claude_agents_template_contract(self) -> None:
        mutations = (
            ("model: opus\neffort: medium", "model: inherit\neffort: medium", "model: opus"),
            ("effort: low", "effort: max", "effort"),
            ("effort: high", "effort: low", "effort"),
            ("disallowedTools: Write, Edit, NotebookEdit\n", "", "disallowedTools"),
            (
                "description: NHK standard band worker.",
                "description: NHK standard band worker. Use proactively.",
                "proactive",
            ),
            ("name: nhk-deep", "name: nhk-heavy", "nhk-deep"),
            ("## Shared Body", "## Shared Body\n\nPrefer Sonnet when it is cheaper.", "Sonnet"),
        )
        for required, replacement, message in mutations:
            with self.subTest(required=required, replacement=replacement):
                root = self.make_source_fixture()
                path = root / "references" / "claude-agents-template.md"
                text = path.read_text(encoding="utf-8")
                self.assertIn(required, text)
                path.write_text(text.replace(required, replacement, 1), encoding="utf-8")
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("claude-agents-template.md", result.stdout)
                self.assertIn(message.lower(), result.stdout.lower())

    def test_missing_claude_agents_template_fails(self) -> None:
        root = self.make_source_fixture()
        (root / "references" / "claude-agents-template.md").unlink()
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("claude-agents-template.md", result.stdout)

    def test_skills_route_claude_agent_definitions(self) -> None:
        for skill in ("nhk-bootstrap", "nhk-upkeep"):
            with self.subTest(skill=skill):
                root = self.make_source_fixture()
                path = root / skill / "SKILL.md"
                text = path.read_text(encoding="utf-8")
                self.assertIn("../references/claude-agents-template.md", text)
                path.write_text(
                    text.replace("../references/claude-agents-template.md", "the agent notes"),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("claude-agents-template.md", result.stdout)


class InstallValidationTests(ValidatorTestCase):
    def test_correct_sibling_layout_allows_unrelated_skills(self) -> None:
        root = self.make_install_fixture()
        (root / "unrelated-skill").mkdir()
        result = run_cli("--install-root", root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_references_fails(self) -> None:
        root = self.make_install_fixture()
        shutil.rmtree(root / "references")
        result = run_cli("--install-root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("references", result.stdout.lower())

    def test_missing_new_companion_templates_fail(self) -> None:
        for name in ("worker-policy-template.md", "execution-recovery-template.md"):
            with self.subTest(name=name):
                root = self.make_install_fixture()
                (root / "references" / name).unlink()
                result = run_cli("--install-root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(name, result.stdout)

    def test_missing_planning_reference_fails(self) -> None:
        root = self.make_install_fixture()
        (root / "references" / "implementation-planning-template.md").unlink(
            missing_ok=True
        )
        result = run_cli("--install-root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("implementation-planning-template.md", result.stdout)

    def test_extra_nhk_nesting_fails(self) -> None:
        root = self.make_install_fixture(nested=True)
        result = run_cli("--install-root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("one level", result.stdout.lower())

    def test_mixed_version_fails(self) -> None:
        root = self.make_install_fixture()
        path = root / "nhk-archive" / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
        result = run_cli("--install-root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("differs", result.stdout.lower())


class FinalValidationTests(ValidatorTestCase):
    def test_simple_medium_and_complex_standalone_pass(self) -> None:
        for template_name, kind in (
            ("AGENTS-template.md", "agents"),
            ("CLAUDE-template.md", "claude"),
        ):
            for complexity in ("simple", "medium", "complex"):
                with self.subTest(template=template_name, complexity=complexity):
                    path = self.write_final(
                        assemble_standalone(
                            ROOT / "references" / template_name, complexity
                        )
                    )
                    result = run_cli(
                        "--final",
                        path,
                        "--kind",
                        kind,
                        "--mode",
                        "standalone",
                        "--complexity",
                        complexity,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_simple_line_limit_fails(self) -> None:
        path = self.write_final(standalone_text(extra_lines=80))
        result = run_cli(
            "--final",
            path,
            "--kind",
            "agents",
            "--mode",
            "standalone",
            "--complexity",
            "simple",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("100", result.stdout)

    def test_standalone_requires_literal_companion_routes(self) -> None:
        for route in COMPANION_ROUTES:
            with self.subTest(route=route):
                content = assemble_standalone(
                    ROOT / "references" / "CLAUDE-template.md", "simple"
                ).replace(route, "the relevant companion")
                path = self.write_final(content)
                result = run_cli(
                    "--final", path, "--kind", "claude", "--mode", "standalone"
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(route.strip("`"), result.stdout)

    def test_missing_heading_and_marker_leak_fail(self) -> None:
        content = standalone_text().replace("## Project Map", "## Project Overview", 1)
        path = self.write_final("[[FINAL_ADAPT:BEGIN]]\n" + content)
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "standalone"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("marker", result.stdout.lower())
        self.assertIn("top-level", result.stdout.lower())

    def test_valid_thin_claude_passes(self) -> None:
        path = self.write_final(
            "@AGENTS.md\n\n# Claude Code Notes\n\n- Keep Claude-specific notes here.\n"
        )
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_thin_claude_rejects_standalone_mix(self) -> None:
        path = self.write_final("@./AGENTS.md\n\n" + standalone_text())
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("standalone", result.stdout.lower())

    def test_import_in_code_fence_does_not_make_thin(self) -> None:
        path = self.write_final("```md\n@AGENTS.md\n```\n")
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("valid import", result.stdout.lower())

    def test_fence_content_that_starts_with_ticks_is_not_a_close(self) -> None:
        path = self.write_final(
            "```md\n```not-a-closing-fence\n@AGENTS.md\n```\n"
        )
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("valid import", result.stdout.lower())

    def test_thin_rejects_standalone_heading_at_any_level(self) -> None:
        for prefix in ("#", "###"):
            with self.subTest(prefix=prefix):
                path = self.write_final(f"@AGENTS.md\n\n{prefix} Project Map\n")
                result = run_cli(
                    "--final", path, "--kind", "claude", "--mode", "thin"
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("standalone", result.stdout.lower())

    def test_legal_wikilink_is_not_a_template_marker(self) -> None:
        path = self.write_final(
            "@AGENTS.md\n\n# Claude Code Notes\n\n- Read [[Project Guide]] first.\n"
        )
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_valid_companion_files_pass(self) -> None:
        cases = (
            ("coding-guide", coding_guide_text()),
            ("planning-guide", planning_guide_text()),
            ("worker-policy", worker_policy_text()),
            ("execution-recovery", execution_recovery_text()),
            ("doc-governance", doc_governance_text()),
        )
        for kind, content in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_standalone_allows_project_template_contract_language(self) -> None:
        content = assemble_standalone(
            ROOT / "references" / "AGENTS-template.md", "simple"
        ).replace(
            "- Atlas Notes is a Python CLI that turns reviewed Markdown notes into a local search index.",
            "- The email template contract is owned by `src/mail`.",
            1,
        )
        path = self.write_final(content)
        result = run_cli(
            "--final",
            path,
            "--kind",
            "agents",
            "--mode",
            "standalone",
            "--complexity",
            "simple",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_companion_line_limits_fail(self) -> None:
        cases = (
            ("coding-guide", coding_guide_text(extra_lines=80), 80),
            ("planning-guide", planning_guide_text(extra_lines=80), 80),
            ("worker-policy", worker_policy_text() + ("extra\n" * 100), 100),
            (
                "execution-recovery",
                execution_recovery_text() + ("extra\n" * 80),
                80,
            ),
            ("doc-governance", doc_governance_text(extra_lines=100), 100),
        )
        for kind, content, limit in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 1)
                self.assertIn(str(limit), result.stdout)

    def test_review_final_alias_and_class_conflicts(self) -> None:
        cases = (
            ("worker-policy", worker_policy_text(), "Use max for ordinary implementation."),
            ("worker-policy", worker_policy_text(), "Use xhigh for ordinary implementation."),
            ("worker-policy", worker_policy_text(), "Use Extra High for ordinary implementation."),
            ("worker-policy", worker_policy_text(), "Use Light for module implementation."),
            ("worker-policy", worker_policy_text(), "Use Light."),
            ("worker-policy", worker_policy_text(), "Use Extra High."),
            ("worker-policy", worker_policy_text(), "Extra High is allowed for debugging."),
            ("planning-guide", planning_guide_text(), "Whole modules may use mechanical workers."),
            ("planning-guide", planning_guide_text(), "Assign mechanical as the worker class for complete modules."),
            ("planning-guide", planning_guide_text(), "Module implementation uses the mechanical worker class."),
            ("planning-guide", planning_guide_text(), "Worker class: mechanical for whole modules."),
            ("planning-guide", planning_guide_text(), "The module worker class is mechanical."),
        )
        for kind, text, clause in cases:
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(kind=kind, clause=clause, wrapper=wrapper):
                    content = text + "\n" + wrapper.format(clause)
                    result = run_cli("--final", self.write_final(content), "--kind", kind)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_helper_function_timeouts_and_immediate_events_remain_valid(self) -> None:
        for platform in ("AGENTS", "CLAUDE"):
            text = assemble_standalone(ROOT / "references" / (platform + "-template.md"), "simple")
            for fact in (
                "The HTTP helper function has a timeout of 15 seconds.",
                "The HTTP helper function checks status every 5 seconds.",
                "The HTTP helper reports request progress every 5 seconds.",
                "The request helper retries after 10 seconds.",
                "Respond immediately to a helper question or a concrete failure.",
            ):
                with self.subTest(platform=platform, fact=fact):
                    result = run_cli("--final", self.write_final(text + "\n" + fact), "--kind", platform.lower(), "--mode", "standalone", "--complexity", "simple")
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_review_final_helper_cadence(self) -> None:
        for platform in ("AGENTS", "CLAUDE"):
            text = assemble_standalone(ROOT / "references" / (platform + "-template.md"), "simple")
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(platform=platform, wrapper=wrapper):
                    content = text + "\n" + wrapper.format("Check each helper's progress every\n5 minutes.")
                    result = run_cli("--final", self.write_final(content), "--kind", platform.lower(), "--mode", "standalone", "--complexity", "simple")
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_planning_template_assembles_without_hidden_repairs(self) -> None:
        text = assemble_companion(ROOT / "references" / "implementation-planning-template.md", "Implementation Planning")
        for value in ("one observable, independently acceptable result", "task identifiers, or None", "mechanical | standard | judgment"):
            text = text.replace("<" + value + ">", value)
        result = run_cli("--final", self.write_final(text), "--kind", "planning-guide")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_review_final_fields_must_remain_active(self) -> None:
        text = planning_guide_text()
        start = text.index("**Delivers:**")
        end = text.index("\n", text.index("**Worker class:**", start))
        for wrapper in ("<!-- {} -->", "```md\n{}\n```"):
            content = text[:start] + wrapper.format(text[start:end]) + text[end:]
            result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("field syntax", result.stdout)

    def test_review_human_routing_exception_is_narrow(self) -> None:
        text = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + human_routing_exception(), 1)
        result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for extra in ("Whole modules may use GPT-6 Astra low.", "Use Extra High for ordinary implementation."):
            result = run_cli("--final", self.write_final(text + "\n" + extra), "--kind", "worker-policy")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_review_human_routing_exception_rejects_malformed_or_special_permissions(self) -> None:
        records = (
            "- Human routing exception",
            "- Human routing exception: []",
            human_routing_exception(extra="all work is authorized"),
            human_routing_exception(approval=""),
            human_routing_exception(approval="https://[invalid/decision#billing"),
            human_routing_exception(approval="https://@/decision#billing"),
            human_routing_exception(approval="https://example.test:invalid/decision#billing"),
            human_routing_exception().replace('"approval":', '"target": "billing-module", "approval":'),
            human_routing_exception(target="all-modules"),
            human_routing_exception(scope="."),
            human_routing_exception(scope="src/../"),
            human_routing_exception(scope="src/*"),
            human_routing_exception(approval="approved"),
            human_routing_exception(role="all"),
            human_routing_exception(preset="GPT-6 Astra max"),
            human_routing_exception(preset="Ultra"),
            human_routing_exception(role="recursive-delegation"),
            human_routing_exception(role="initial-module-review", preset="GPT-6 Luna max"),
            human_routing_exception() + " Whole modules may use GPT-6 Astra low.",
        )
        for record in records:
            with self.subTest(record=record):
                content = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + record, 1)
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("routing exception", result.stdout.lower())
        for heading in ("# Worker Policy", "## Dispatch Contract", "## Review Gates", "## Claude Routing"):
            content = worker_policy_text().replace(heading, heading + "\n" + human_routing_exception(), 1)
            result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_review_exception_evidence_and_scope_remain_literal(self) -> None:
        for record in (
            human_routing_exception(approval="https://example.test/decisions/42#billing-low"),
            human_routing_exception(target="计费模块", scope="src/计费/", approval="decisions/计费.md#批准"),
            human_routing_exception(target="billing-project"),
            human_routing_exception(role="initial-module-review"),
            human_routing_exception(role="scoped-re-review", preset="GPT-6 Luna max"),
        ):
            text = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + record, 1)
            result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = human_routing_exception()
        text = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + record + "\n" + record, 1)
        result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("duplicates", result.stdout)
        result = run_cli("--final", self.write_final(planning_guide_text() + "\n" + record), "--kind", "planning-guide")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("belongs only", result.stdout)

    def test_review_final_literal_record_data_is_not_policy(self) -> None:
        for record, adjacent, drift, expected in literal_routing_record_cases():
            with self.subTest(record=record, adjacent=adjacent, drift=drift):
                text = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + record + "\n" + adjacent, 1)
                if drift:
                    text = text.replace(*drift)
                result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_review_inactive_exception_and_project_facts_remain_harmless(self) -> None:
        for wrapper in ("<!-- {} -->", "```md\n{}\n```"):
            text = worker_policy_text() + "\n" + wrapper.format(human_routing_exception(target="all"))
            result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = planning_guide_text() + "\nThe billing module parses mechanical sensor data."
        result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_worker_final_rejects_preamble_and_wrong_section_band_routes(self) -> None:
        for anchor, clause in (
            ("# Worker Policy", "Whole modules may use GPT-6 Astra low."),
            ("## Dispatch Contract", "- Band 1: Whole modules may use GPT-6 Astra low."),
        ):
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(anchor=anchor, wrapper=wrapper):
                    text = worker_policy_text().replace(anchor, anchor + "\n\n" + wrapper.format(clause), 1)
                    result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_shared_contracts_scan_active_preambles(self) -> None:
        for kind, text, clause, extra_args in (
            ("planning-guide", planning_guide_text(), "Use the smallest-reviewable task.", ()),
            ("agents", assemble_standalone(ROOT / "references" / "AGENTS-template.md", "simple"),
             "Replace workers after 1800 seconds.", ("--mode", "standalone", "--complexity", "simple")),
        ):
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(kind=kind, wrapper=wrapper):
                    content = wrapper.format(clause) + "\n\n" + text
                    result = run_cli("--final", self.write_final(content), "--kind", kind, *extra_args)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_module_contract_requires_active_correct_sections(self) -> None:
        cases = (
            ("worker-policy", worker_policy_text(), "Codex Routing", "Claude Routing",
             "Default module implementation, internal debugging, tests, and integration to Band 2."),
            ("planning-guide", planning_guide_text(), "Plan Layers", "Plan Review",
             "A Module is related work with a defined responsibility, prerequisites, interfaces, and complete acceptance; it need not match a file or directory. Default one Superpowers Task is one Module; independently dispatched mechanical work is the explicit exception."),
        )
        for kind, text, section, wrong_section, clause in cases:
            for replacement in ("<!-- " + clause + " -->", "```md\n" + clause + "\n```", ""):
                with self.subTest(kind=kind, replacement=replacement):
                    self.assertIn(clause, text)
                    mutated = text.replace(clause, replacement, 1)
                    if not replacement:
                        mutated = mutated.replace("## " + wrong_section, "## " + wrong_section + "\n" + clause, 1)
                    result = run_cli("--final", self.write_final(mutated), "--kind", kind)
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertIn(section, result.stdout)

    def test_module_contract_accepts_reuse_and_inactive_conflicts(self) -> None:
        text = worker_policy_text()
        self.assertIn("Prefer the original implementer", text)
        self.assertIn("original independent reviewer", text)
        self.assertIn("cause, intended behavior, approach, impact, and verification are clear", text)
        self.assertIn("Standalone mechanical work must be independent", text)
        for extra in ("<!-- Whole modules may use Band 1. -->", "```md\nWhole modules may use Band 1.\n```"):
            result = run_cli("--final", self.write_final(text + "\n" + extra), "--kind", "worker-policy")
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_standalone_wait_contract_preserves_project_timing_facts(self) -> None:
        text = assemble_standalone(ROOT / "references" / "AGENTS-template.md", "simple")
        text = text.replace("## Project Map", "## Project Map\n- Client timeout is 15 seconds; wait for index writes before reading.")
        result = run_cli("--final", self.write_final(text), "--kind", "agents", "--mode", "standalone", "--complexity", "simple")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_standalone_wait_contract_rejects_old_and_additive_rules(self) -> None:
        for template in ("AGENTS-template.md", "CLAUDE-template.md"):
            text = assemble_standalone(ROOT / "references" / template, "simple")
            for mutated in (
                text.replace("at least 1800 seconds", "at least 300 seconds"),
                text + "\nReplace workers after 1800 seconds.\n",
                text + "\nReplace workers after\n1800 seconds.\n",
                text + "\nA wait return triggers a status check.\n",
                text.replace("In SDD, wait at least 1800 seconds after dispatch or resumption and between unsolicited progress checks.", "<!-- In SDD, wait at least 1800 seconds after dispatch or resumption and between unsolicited progress checks. -->"),
            ):
                with self.subTest(template=template, mutated=mutated[-90:]):
                    result = run_cli("--final", self.write_final(mutated), "--kind", "agents" if template.startswith("AGENTS") else "claude", "--mode", "standalone", "--complexity", "simple")
                    self.assertEqual(result.returncode, 1, result.stdout)

    def test_module_routing_rejects_additive_authorizations(self) -> None:
        for clause in (
            "Whole modules may use GPT-6 Astra low.",
            "Module implementation may use GPT-6 Luna max.",
            "Mechanical fixes may include design judgment and use Band 1.",
            "Initial module reviews may use Band 1.",
        ):
            with self.subTest(clause=clause):
                text = worker_policy_text().replace("## Claude Routing", clause + "\n\n## Claude Routing")
                result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_module_review_rejects_additive_consolidation(self) -> None:
        for clause in (
            "A passed module review satisfies final review for a multi-module plan.",
            "Reuse the module review after HEAD changes without re-evaluation.",
            "Consolidation resets the repair count.",
        ):
            with self.subTest(clause=clause):
                text = worker_policy_text().replace("## Codex Routing", clause + "\n\n## Codex Routing")
                result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_worker_policy_requires_exact_headings(self) -> None:
        for heading in (
            "Dispatch Contract",
            "Review Gates",
            "Codex Routing",
            "Claude Routing",
        ):
            with self.subTest(heading=heading):
                path = self.write_final(
                    worker_policy_text().replace(f"## {heading}", f"## {heading} Notes", 1)
                )
                result = run_cli("--final", path, "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1)
                self.assertIn("headings", result.stdout.lower())

    def test_gpt6_routing_defaults_to_medium_with_bounded_xhigh(self) -> None:
        content = worker_policy_text()
        for clause in (
            "Band 1: GPT-6 Luna max.",
            "Band 2: GPT-6 Astra medium.",
            "Band 3: GPT-6 Astra xhigh.",
            "Default module implementation, internal debugging, tests, and integration to Band 2.",
            "Select Band 3 only for a concrete reasoning difficulty remaining after sizing and context checks, or demonstrated Band 2 capability limits.",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, content)
                mutated = content.replace(clause, "", 1)
                result = run_cli("--final", self.write_final(mutated), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_planning_requires_sizing_before_capability_and_no_fragmentation(self) -> None:
        content = planning_guide_text()
        for clause in (
            "Before increasing capability, separate unrelated decisions and resolve missing interfaces or context; preserve tightly coupled logic and its verification.",
            "When many tasks need higher capability, recheck boundaries and shared constraints; use no fixed quota and keep irreducible difficult modules intact.",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, content)
                result = run_cli("--final", self.write_final(content.replace(clause, "", 1)), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_worker_policy_accepts_reordered_exact_band_rows(self) -> None:
        content = worker_policy_text()
        original = "\n- ".join(CODEX_PRESET_BAND_LINES)
        self.assertIn(original, content)
        content = content.replace(original, "\n- ".join(reversed(CODEX_PRESET_BAND_LINES)), 1)
        result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_worker_policy_rejects_wrong_missing_extra_or_duplicate_presets(self) -> None:
        valid = CODEX_PRESET_BAND_LINES[1]
        invalid = (
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra max"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra high"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra xhigh"),
            valid.replace("GPT-6 Astra medium", "GPT-5.6 Terra xhigh"),
            valid.replace("GPT-6 Astra medium", "GPT-5.5 xhigh"),
            valid.replace("GPT-6 Astra medium", ""),
            valid.replace("GPT-6 Astra medium", "GPT-5.6 Sol medium"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra medium; GPT-6 Luna max"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra medium; GPT-6 Astra medium"),
            valid + "\n- Band 3: GPT-6 Astra xhigh.",
        )
        for replacement in invalid:
            with self.subTest(replacement=replacement):
                self.assertNotEqual(replacement, valid)
                path = self.write_final(worker_policy_text().replace(valid, replacement, 1))
                result = run_cli("--final", path, "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1)
                self.assertIn("exact unordered preset", result.stdout.lower())

    def test_worker_policy_rejects_drift_in_review_and_special_roles(self) -> None:
        mutations = (
            (
                "Both must pass; self-review is not a substitute.",
                "Either verdict may pass; self-review is enough.",
                "Review Gates",
            ),
            (
                "GPT-6 Luna may perform low-risk scoped re-review, never an initial task review.",
                "GPT-6 Luna may perform any initial task review.",
                "Codex Routing",
            ),
            (
                "Independent diagnosis and complex whole-change final review use Band 3, or GPT-6 Astra max when deeper reasoning is needed. Max is limited to these read-only roles; after a failed Band 3 implementation it may be selected directly for the one independent diagnosis.",
                "GPT-6 Astra max may perform ordinary implementation and recovery.",
                "Codex Routing",
            ),
            (
                "Use Fable only when the human explicitly chooses or approves it for the main thread.",
                "Use Fable for workers when it is available.",
                "Claude Routing",
            ),
            (
                "Ultra authorization and recursion authorization never imply each other.",
                "Ultra authorization also authorizes recursion.",
                "Codex Routing",
            ),
        )
        for required, replacement, section in mutations:
            with self.subTest(required=required):
                path = self.write_final(
                    worker_policy_text().replace(required, replacement, 1)
                )
                result = run_cli("--final", path, "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1)
                self.assertIn(section, result.stdout)

    def test_three_band_routing_rejects_default_ceiling_and_fallback_drift(self) -> None:
        mutations = (
            ("ordinary Band 3 ceiling", "ordinary Band 2 ceiling"),
            ("Initial independent reviews default to Band 2", "Initial independent reviews default to Band 3"),
            ("it does not authorize a different band, an older model, or a special-role preset as fallback",
             "it authorizes Astra max when Band 2 is unavailable"),
            ("Default module implementation, internal debugging, tests, and integration to Band 2.",
             "Default module implementation, internal debugging, tests, and integration to Band 3."),
        )
        for required, replacement in mutations:
            with self.subTest(required=required):
                content = worker_policy_text()
                self.assertIn(required, content)
                result = run_cli("--final", self.write_final(content.replace(required, replacement, 1)), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Codex Routing", result.stdout)

    def test_recovery_diagnosis_uses_worker_policy_role(self) -> None:
        route = "using the independent diagnosis role in `worker-policy.md`"
        for replacement in ("using Band 2", "using Band 3", "using GPT-6 Astra max"):
            with self.subTest(replacement=replacement):
                content = execution_recovery_text()
                self.assertIn(route, content)
                result = run_cli("--final", self.write_final(content.replace(route, replacement, 1)), "--kind", "execution-recovery")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Independent Diagnosis", result.stdout)

    def test_additive_reserved_routes_fail(self) -> None:
        for preset in ("GPT-6 Astra max", "gpt-6-astra max"):
            for role in ("ordinary implementation", "debugging", "scoped re-review"):
                with self.subTest(preset=preset, role=role):
                    content = worker_policy_text().replace(
                        "## Claude Routing",
                        f"- {preset} is approved for {role}.\n\n## Claude Routing",
                    )
                    result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertIn("reserved routing", result.stdout)

    def test_additive_diagnostic_routes_fail(self) -> None:
        for route in ("Band 3", "GPT-6 Astra xhigh", "GPT-6 Astra max", "gpt-6-astra max", "Sonnet", "max", "xhigh", "Extra High"):
            with self.subTest(route=route):
                content = execution_recovery_text().replace(
                    "## Recovery and Stop",
                    f"- Dispatch {route} for diagnosis.\n\n## Recovery and Stop",
                )
                result = run_cli("--final", self.write_final(content), "--kind", "execution-recovery")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("diagnostic routing", result.stdout)

    def test_inactive_alternate_routes_do_not_change_contract(self) -> None:
        for kind, content, heading in (
            ("worker-policy", worker_policy_text(), "Codex Routing"),
            ("execution-recovery", execution_recovery_text(), "Independent Diagnosis"),
        ):
            content = content.replace(f"## {heading}", f"## {heading}\n\n```text\nDispatch GPT-6 Astra xhigh for diagnosis.\n```\n<!-- Dispatch Band 3 for diagnosis. -->")
            result = run_cli("--final", self.write_final(content), "--kind", kind)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_worker_policy_requires_explicit_budget_clause(self) -> None:
        content = worker_policy_text().replace(
            "Explicit user budgets still bind.",
            "The main thread's model and effort are the worker cost ceiling.",
            1,
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Dispatch Contract", result.stdout)

    def test_worker_policy_allows_explicit_prohibitions(self) -> None:
        content = worker_policy_text().replace(
            "## Codex Routing",
            """## Codex Routing

- Do not use GPT-6 Astra max for ordinary implementation.
- GPT-6 Luna max must not perform initial task reviews.
- Ultra approval never authorizes recursive delegation.""",
            1,
        ).replace(
            "## Claude Routing",
            """## Claude Routing

- Workers may not inherit Fable for ordinary coding.""",
            1,
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_worker_policy_rejects_presets_declared_outside_band_lines(self) -> None:
        extras = (
            "GPT-9 Nova max is also approved for ordinary implementation.",
            "GPT-5.6 Luna max is also approved for ordinary implementation.",
            "GPT-6 Astra low is also approved for ordinary implementation.",
            "GPT-6 Sol xhigh is also approved for ordinary implementation.",
            "GPT-5.6 Sol high is also approved for ordinary implementation.",
            "gpt-5.6-sol is also approved for ordinary implementation.",
            "GPT-6 Nova max is also approved for ordinary implementation.",
            "GPT-5.5 xhigh is also approved for ordinary implementation.",
            "GPT-6 Astra ultra is also approved for ordinary implementation.",
            "GPT-6 Astra turbo is also approved for ordinary implementation.",
        )
        for extra in extras:
            with self.subTest(extra=extra):
                path = self.write_final(
                    worker_policy_text().replace(
                        "## Codex Routing",
                        f"## Codex Routing\n\n- {extra}",
                        1,
                    )
                )
                result = run_cli("--final", path, "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1)
                self.assertIn("unapproved versioned preset", result.stdout.lower())

    def test_worker_policy_section_false_positive_fails(self) -> None:
        required = "Both must pass; self-review is not a substitute."
        content = worker_policy_text().replace(required, "", 1)
        content = content.replace(
            "## Claude Routing", f"## Claude Routing\n\n- {required}", 1
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Review Gates", result.stdout)

    def test_execution_recovery_requires_exact_headings(self) -> None:
        for heading in (
            "Triggers and Accounting",
            "Main-thread Reassessment",
            "Independent Diagnosis",
            "Recovery and Stop",
        ):
            with self.subTest(heading=heading):
                path = self.write_final(
                    execution_recovery_text().replace(
                        f"## {heading}", f"## {heading} Notes", 1
                    )
                )
                result = run_cli(
                    "--final", path, "--kind", "execution-recovery"
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("headings", result.stdout.lower())

    def test_execution_recovery_rejects_drift_in_gap_and_limit_clauses(self) -> None:
        mutations = (
            (
                "Worker, session, model, commit, task rename, or replanning never "
                "resets a task or gap count.",
                "Changing the model resets the stable acceptance-gap count.",
                "Triggers and Accounting",
            ),
            (
                "at most one recovery fix wave and one independent re-review",
                "An additional recovery fix wave is allowed after exhaustion.",
                "Recovery and Stop",
            ),
            (
                "An exhausted earlier gap cannot use final review as another repair allowance",
                "Final review may repair an exhausted earlier gap afresh.",
                "Recovery and Stop",
            ),
        )
        for required, replacement, section in mutations:
            with self.subTest(required=required):
                content = execution_recovery_text().replace(
                    required, replacement, 1
                )
                path = self.write_final(content)
                result = run_cli(
                    "--final", path, "--kind", "execution-recovery"
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(section, result.stdout)

    def test_execution_recovery_allows_explicit_prohibitions(self) -> None:
        content = execution_recovery_text().replace(
            "## Triggers and Accounting",
            """## Triggers and Accounting

- Changing the model must not reset the stable acceptance-gap count.""",
            1,
        ).replace(
            "## Recovery and Stop",
            """## Recovery and Stop

- No additional recovery fix wave is allowed after exhaustion.
- Final review never grants another repair allowance for an exhausted gap.""",
            1,
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "execution-recovery")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_execution_recovery_scopes_gap_accounting_to_trigger_section(self) -> None:
        required = (
            "Worker, session, model, commit, task rename, or replanning never resets "
            "a task or gap count."
        )
        content = execution_recovery_text().replace(required, "", 1)
        content = content.replace(
            "## Independent Diagnosis", f"## Independent Diagnosis\n\n- {required}", 1
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "execution-recovery")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Triggers and Accounting", result.stdout)

    def test_companion_inactive_markdown_cannot_satisfy_contract(self) -> None:
        cases = (
            ("worker-policy", worker_policy_text()),
            ("execution-recovery", execution_recovery_text()),
        )
        wrappers = (
            lambda body: f"```md\n{body.rstrip()}\n```\n",
            lambda body: f"<!--\n{body.rstrip()}\n-->\n",
        )
        for kind, content in cases:
            for wrap in wrappers:
                wrapped = wrap(content)
                with self.subTest(kind=kind, wrapper=wrapped[:4]):
                    path = self.write_final(wrapped)
                    result = run_cli("--final", path, "--kind", kind)
                    self.assertEqual(result.returncode, 1)
                    self.assertRegex(
                        result.stdout.lower(),
                        r"heading|# worker policy|# execution recovery",
                    )

    def test_companion_fenced_heading_does_not_satisfy_or_pollute_contract(self) -> None:
        missing = worker_policy_text().replace("## Claude Routing\n", "", 1)
        missing += "\n```md\n## Claude Routing\n```\n"
        path = self.write_final(missing)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 1)
        self.assertIn("headings", result.stdout.lower())

        extra_example = worker_policy_text().replace(
            "## Claude Routing",
            "## Claude Routing\n\n```md\n## Extra Catalog\n```",
            1,
        )
        path = self.write_final(extra_example)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_overindented_fence_does_not_hide_following_heading(self) -> None:
        extra = "\n    ```md\n## Extra Section\n"
        cases = (
            ("worker-policy", worker_policy_text() + extra, "headings"),
            ("doc-governance", doc_governance_text() + extra, "Extra Section"),
        )
        for kind, content, needle in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 1)
                self.assertIn(needle, result.stdout)

        still_fenced = worker_policy_text() + "\n   ```md\n## Extra Section\n   ```\n"
        path = self.write_final(still_fenced)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_companion_final_rejects_active_companion_imports(self) -> None:
        cases = (
            (
                "worker-policy",
                worker_policy_text() + "\nRead @execution-recovery.md after exhaustion.\n",
            ),
            (
                "execution-recovery",
                execution_recovery_text() + "\nRead @worker-policy.md before dispatch.\n",
            ),
        )
        for kind, content in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 1)
                self.assertIn("auto-imports companion", result.stdout.lower())

    def test_ordinary_project_model_text_is_allowed(self) -> None:
        content = assemble_standalone(
            ROOT / "references" / "AGENTS-template.md", "simple"
        ).replace(
            "Atlas Notes is a Python CLI",
            "Atlas Notes is a Python CLI that catalogs GPT-4 and GPT-6 API usage",
            1,
        )
        path = self.write_final(content)
        result = run_cli(
            "--final", path, "--kind", "agents", "--mode", "standalone"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_planning_guide_requires_exact_sections_and_task_contract(self) -> None:
        for heading in PLANNING_GUIDE_HEADINGS:
            with self.subTest(heading=heading):
                content = planning_guide_text().replace(f"## {heading}\n", "", 1)
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1)
                self.assertIn(heading, result.stdout)

        for token in ("Delivers", "Blocked by", "Worker class"):
            with self.subTest(token=token):
                content = planning_guide_text().replace(token, "Missing field")
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1)
                self.assertIn(token, result.stdout)

    def test_planning_guide_requires_field_syntax_in_task_contract(self) -> None:
        content = planning_guide_text().replace(
            "**Delivers:** one observable, independently acceptable result\n"
            "**Blocked by:** task identifiers, or None\n"
            "**Worker class:** mechanical | standard | judgment",
            "Do not use Delivers, Blocked by, or Worker class. "
            "The forbidden worker classes are mechanical, standard, and judgment.",
            1,
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "planning-guide")
        self.assertEqual(result.returncode, 1)
        self.assertIn("field syntax", result.stdout.lower())

    def test_planning_guide_scopes_superpowers_details_to_workflow_section(self) -> None:
        content = planning_guide_text().replace(
            "Preserve its `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code.",
            "Keep the active Superpowers plan format.",
            1,
        ).replace(
            "## Plan Review",
            "## Plan Review\nFiles, Interfaces, TDD steps, commands, expected results, and necessary code.",
            1,
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "planning-guide")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Workflow Compatibility", result.stdout)

    def test_planning_guide_rejects_generation_prompts_and_placeholders(self) -> None:
        cases = (
            "Template Contract",
            "Replace explanatory examples with workspace facts.",
            "**Delivers:** <one observable result>",
        )
        for leaked in cases:
            with self.subTest(leaked=leaked):
                path = self.write_final(planning_guide_text() + f"\n{leaked}\n")
                result = run_cli("--final", path, "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1)
                self.assertIn("generation", result.stdout.lower())

    def test_coding_guide_requires_routing_columns(self) -> None:
        content = coding_guide_text().replace("Likely Change Surface", "Change Here")
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "coding-guide")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Likely Change Surface", result.stdout)

    def test_coding_guide_rejects_legacy_sections(self) -> None:
        for heading in (
            "Current Execution State",
            "High-Frequency Packet Routing",
            "Implementation Packet Checklist",
            "Code Entry Map",
            "Default Verification",
            "Anti-Detour Advice",
        ):
            with self.subTest(heading=heading):
                path = self.write_final(coding_guide_text() + f"\n## {heading}\n")
                result = run_cli("--final", path, "--kind", "coding-guide")
                self.assertEqual(result.returncode, 1)
                self.assertIn(heading, result.stdout)

    def test_coding_guide_rejects_unexpected_sections(self) -> None:
        path = self.write_final(coding_guide_text() + "\n## Architecture Overview\n")
        result = run_cli("--final", path, "--kind", "coding-guide")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Architecture Overview", result.stdout)

    def test_doc_governance_requires_headings_and_archive_invariants(self) -> None:
        for heading in DOC_GOVERNANCE_HEADINGS:
            with self.subTest(heading=heading):
                content = doc_governance_text().replace(f"## {heading}\n", "", 1)
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", "doc-governance")
                self.assertEqual(result.returncode, 1)
                self.assertIn(heading, result.stdout)

        content = doc_governance_text().replace(
            "Explicit human approval is required before archiving. ", ""
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "doc-governance")
        self.assertEqual(result.returncode, 1)
        self.assertIn("human approval", result.stdout.lower())

        content = doc_governance_text().replace(
            "`implementation-planning.md`", "the planning guide"
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "doc-governance")
        self.assertEqual(result.returncode, 1)
        self.assertIn("implementation-planning.md", result.stdout)

    def test_doc_governance_requires_worker_and_recovery_paths(self) -> None:
        for token in ("`worker-policy.md`", "`execution-recovery.md`"):
            with self.subTest(token=token):
                path = self.write_final(
                    doc_governance_text().replace(token, "`other-companion.md`", 1)
                )
                result = run_cli("--final", path, "--kind", "doc-governance")
                self.assertEqual(result.returncode, 1)
                self.assertIn(token.strip("`"), result.stdout)

        aliased = (
            doc_governance_text()
            .replace("`worker-policy.md`", "`legacy-worker-policy.md`", 1)
            .replace("`execution-recovery.md`", "`legacy-execution-recovery.md`", 1)
        )
        path = self.write_final(aliased)
        result = run_cli("--final", path, "--kind", "doc-governance")
        self.assertEqual(result.returncode, 1)
        self.assertIn("worker-policy.md", result.stdout)
        self.assertIn("execution-recovery.md", result.stdout)

    def test_claude_rejects_companion_auto_imports(self) -> None:
        cases = (
            ("thin", "@AGENTS.md\n\nRead @coding-agent-guide.md before editing.\n"),
            (
                "thin",
                "@AGENTS.md\n\nRead @implementation-planning.md before planning.\n",
            ),
            (
                "standalone",
                standalone_text()
                + "\nRead @./documentation-governance.md before editing.\n",
            ),
            (
                "thin",
                "@AGENTS.md\n\nRead @worker-policy.md before dispatching.\n",
            ),
            (
                "standalone",
                standalone_text()
                + "\nRead @./execution-recovery.md after failure.\n",
            ),
        )
        for mode, content in cases:
            with self.subTest(mode=mode):
                path = self.write_final(content)
                result = run_cli(
                    "--final", path, "--kind", "claude", "--mode", mode
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("companion", result.stdout.lower())

    def test_claude_allows_non_active_companion_import_examples(self) -> None:
        examples = (
            "`@coding-agent-guide.md`",
            "`@implementation-planning.md`",
            "`@worker-policy.md`",
            "`@execution-recovery.md`",
            "> @coding-agent-guide.md",
            "> @implementation-planning.md",
            "> @worker-policy.md",
            "> @execution-recovery.md",
            "<!-- @coding-agent-guide.md -->",
            "<!-- @implementation-planning.md -->",
            "<!-- @worker-policy.md -->",
            "<!-- @execution-recovery.md -->",
            "```md\n@coding-agent-guide.md\n```",
            "```md\n@implementation-planning.md\n```",
            "```md\n@worker-policy.md\n```",
            "```md\n@execution-recovery.md\n```",
        )
        for example in examples:
            with self.subTest(example=example):
                path = self.write_final(
                    "@AGENTS.md\n\n# Claude Code Notes\n\n" + example + "\n"
                )
                result = run_cli(
                    "--final", path, "--kind", "claude", "--mode", "thin"
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_comment_fence_text_cannot_hide_active_imports(self) -> None:
        hidden_companion = self.write_final(
            """@AGENTS.md

<!--
```md
-->
Read @worker-policy.md before dispatching.
"""
        )
        result = run_cli(
            "--final", hidden_companion, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("worker-policy.md", result.stdout)

        hidden_agents = self.write_final(
            """<!--
```md
-->
@AGENTS.md
"""
        )
        result = run_cli(
            "--final", hidden_agents, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_comment_markers_inside_real_fence_do_not_change_comment_state(self) -> None:
        path = self.write_final(
            """```md
<!--
-->
```
@AGENTS.md
Read @worker-policy.md before dispatching.
"""
        )
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("worker-policy.md", result.stdout)
        self.assertNotIn("valid import line", result.stdout)

    def test_claude_routing_is_opus_only_by_band(self) -> None:
        mutations = (
            ("Every Claude worker runs Opus.", "Every Claude worker runs Sonnet."),
            ("Initial reviews start at `nhk-standard`.", "It may also perform initial reviews."),
            (
                "Built-in agents also receive `model: opus` explicitly, so Fable is never inherited.",
                "Built-in agents inherit the main thread model.",
            ),
            (
                "continue that worker with the open items, at most twice.",
                "continue that worker until it finishes.",
            ),
        )
        for required, replacement in mutations:
            with self.subTest(required=required):
                text = worker_policy_text()
                self.assertIn(required, text)
                result = run_cli(
                    "--final", self.write_final(text.replace(required, replacement, 1)),
                    "--kind", "worker-policy",
                )
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Claude Routing", result.stdout)

    def test_claude_routing_rejects_additional_routes(self) -> None:
        for extra in (
            "Use Sonnet for ordinary implementation and review.",
            "Use `nhk-deep` for every module implementation.",
            "Dispatch `nhk-diagnosis` for ordinary fixes.",
        ):
            with self.subTest(extra=extra):
                content = worker_policy_text().rstrip() + f"\n- {extra}\n"
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout)


class CliContractTests(ValidatorTestCase):
    def test_mutually_exclusive_modes_return_two(self) -> None:
        root = self.make_install_fixture()
        result = run_cli("--root", root, "--install-root", root)
        self.assertEqual(result.returncode, 2)

    def test_agents_thin_is_cli_error(self) -> None:
        path = self.write_final("@AGENTS.md\n")
        result = run_cli(
            "--final", path, "--kind", "agents", "--mode", "thin"
        )
        self.assertEqual(result.returncode, 2)

    def test_final_requires_kind_and_mode(self) -> None:
        path = self.write_final(standalone_text())
        result = run_cli("--final", path)
        self.assertEqual(result.returncode, 2)

    def test_instruction_kind_still_requires_mode(self) -> None:
        path = self.write_final(standalone_text())
        result = run_cli("--final", path, "--kind", "agents")
        self.assertEqual(result.returncode, 2)

    def test_companion_kind_rejects_mode_and_complexity(self) -> None:
        kinds = (
            ("coding-guide", coding_guide_text()),
            ("planning-guide", planning_guide_text()),
            ("worker-policy", worker_policy_text()),
            ("execution-recovery", execution_recovery_text()),
            ("doc-governance", doc_governance_text()),
        )
        flags = (("--mode", "standalone"), ("--complexity", "simple"))
        for kind, content in kinds:
            for flag, value in flags:
                with self.subTest(kind=kind, flag=flag):
                    path = self.write_final(content)
                    result = run_cli(
                        "--final", path, "--kind", kind, flag, value
                    )
                    self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
