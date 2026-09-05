from __future__ import annotations

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
    "Band 1: GPT-5.6 Luna max; GPT-6 Astra low.",
    "Band 2: GPT-5.6 Sol medium; GPT-5.6 Sol high; GPT-6 Astra medium.",
    "Band 3: GPT-5.6 Sol xhigh; GPT-6 Astra xhigh.",
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
    sections = {
        "Workflow Compatibility": (
            "Keep the active Superpowers plan format, including Files, Interfaces, "
            "TDD steps, commands, expected results, and necessary code."
        ),
        "Plan Layers": "Separate the plan outcome and approach from executable tasks.",
        "Task Contract": (
            "Each task declares these fields:\n\n"
            "**Delivers:** one observable, independently acceptable result\n"
            "**Blocked by:** task identifiers or None\n"
            "**Worker class:** mechanical | standard | judgment"
        ),
        "Dependencies and Execution": (
            "Blocked by records real dependencies; SDD implementation remains sequential."
        ),
        "Wide Changes": (
            "Use expand, migrate batches, then contract. Use an integration branch and "
            "an integrate-and-verify task when a batch cannot stay green alone."
        ),
        "Plan Review": (
            "Reject a task that cannot deliver one worthwhile, independently acceptable "
            "result with a complete implementation-and-verification loop. Each task must "
            "fit one fresh implementer context, one coherent acceptance result, one reviewer "
            "gate, and one independent return. A task may contain multiple necessary TDD "
            "cycles. Split genuinely independent results, judgments, or ownership boundaries; "
            "keep one transaction, permission decision, or recovery path together, and keep "
            "setup, tests, configuration, and documentation with the result they enable."
        ),
    }
    lines = ["# Implementation Planning", ""]
    for heading, body in sections.items():
        lines.extend((f"## {heading}", "", body, ""))
    lines.extend(f"- extra {index}" for index in range(extra_lines))
    return "\n".join(lines).rstrip() + "\n"


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

    def test_worker_policy_source_contract_fails(self) -> None:
        mutations = (
            (
                CODEX_PRESET_BAND_LINES[0],
                "Band 1: GPT-5.6 Luna max.",
            ),
            ("Presets within a band are unordered task-fit choices", "Use the listed order"),
            ("there is no mandatory Band 1 trial", "always start in Band 1"),
            ("Escalate one band only", "Escalate whenever useful"),
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
            ("README.md", "ten controlled references", "several references"),
            ("README.md", "seven required pieces", "the foundation"),
            ("README.md", "Superpowers overlay", "planning helper"),
            (
                "README.md",
                "three practical Codex bands",
                "several worker options",
            ),
            ("README_CN.md", "十个受控 reference", "几份 reference"),
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

    def test_worker_policy_accepts_reordered_exact_band_membership(self) -> None:
        content = worker_policy_text().replace(
            "Band 2: GPT-5.6 Sol medium; GPT-5.6 Sol high; GPT-6 Astra medium.",
            "Band 2: GPT-6 Astra medium; GPT-5.6 Sol high; GPT-5.6 Sol medium.",
            1,
        )
        path = self.write_final(content)
        result = run_cli("--final", path, "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_worker_policy_rejects_wrong_missing_extra_or_duplicate_presets(self) -> None:
        valid = CODEX_PRESET_BAND_LINES[1]
        invalid = (
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra max"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra high"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra xhigh"),
            valid.replace("GPT-6 Astra medium", "GPT-5.6 Terra xhigh"),
            valid.replace("GPT-6 Astra medium", "GPT-5.5 xhigh"),
            valid.replace("GPT-5.6 Sol medium; ", ""),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra medium; GPT-5.6 Luna max"),
            valid.replace("GPT-6 Astra medium", "GPT-6 Astra medium; GPT-6 Astra medium"),
            valid + "\n- Band 4: GPT-6 Astra xhigh.",
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
                "GPT-5.6 Luna may perform low-risk scoped re-review, never an initial task review.",
                "GPT-5.6 Luna may perform any initial task review.",
                "Codex Routing",
            ),
            (
                "GPT-6 Astra max is reserved for whole-change final review of a complex Superpowers plan, not ordinary implementation, debugging, or recovery.",
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
- GPT-5.6 Luna max must not perform initial task reviews.
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
            "Each task declares these fields:\n\n"
            "**Delivers:** one observable, independently acceptable result\n"
            "**Blocked by:** task identifiers or None\n"
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
            "Keep the active Superpowers plan format, including Files, Interfaces, "
            "TDD steps, commands, expected results, and necessary code.",
            "Keep the active Superpowers plan format.",
            1,
        ).replace(
            "Reject a task that cannot produce one observable result",
            "Mention Files, Interfaces, TDD steps, commands, expected results, and "
            "necessary code here. Reject a task that cannot produce one observable result",
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
