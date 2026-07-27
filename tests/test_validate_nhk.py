from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


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

CODEX_PRESET_LADDER = (
    "GPT-5.6 Luna max → GPT-5.5 xhigh → GPT-5.6 Terra high → "
    "GPT-5.6 Terra xhigh → GPT-5.6 Terra max → GPT-5.6 Sol xhigh → "
    "GPT-5.6 Sol max"
)

IMPLEMENTATION_PLANNING_POINTER = (
    "Before writing, approving, or materially revising an implementation plan, "
    "read `implementation-planning.md`; do not dispatch a task that fails its "
    "packet contract."
)

CONVERGENCE_BACKSTOP = (
    "Five failed fix–verify or fix–review rounds on the same acceptance gap "
    "trigger a mandatory stop. Invoke or restart `systematic-debugging`, count "
    "those rounds as failed fixes, and forbid a sixth fix until root-cause and "
    "architecture reassessment is complete."
)

INSTALL_COMMAND = (
    "cp -R welcome-to-nhk nhk-bootstrap nhk-upkeep nhk-archive references "
    "<skills-root>/"
)

COMPANION_VALIDATOR_COMMANDS = """python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance"""


def run_cli(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *(str(arg) for arg in args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def english_readme() -> str:
    names = "\n".join(f"- `{name}`" for name in (*SKILLS, *REFERENCES))
    return f"""# NHK

[中文](README_CN.md)

NHK handles five recurring jobs with four prompt-first skills.

{names}

Install the five sibling directories directly under one skills root:

```bash
{INSTALL_COMMAND}
```

`scripts/` and `tests/` are maintainer-only and are not runtime installation content.
The Python validator is optional and has no third-party dependencies:
`python3 -B scripts/validate_nhk.py --install-root <skills-root>`.
After validation, refresh the session and confirm that all four skills are discoverable.
Maintainers can validate generated companion docs:
{COMPANION_VALIDATOR_COMMANDS}

NHK keeps eight controlled references and five mandatory foundation surfaces.
Its implementation-planning companion is a Superpowers overlay loaded only for plan work.
The practical Codex preset ladder is: {CODEX_PRESET_LADDER}.
The user's main-thread model and effort set each worker's cost ceiling.
If the same gap remains after round five, invoke systematic-debugging. No sixth patch
is allowed before root-cause and architecture reassessment.
For beginner-sized projects, the routing table is the shallow code map.
Thin CLAUDE imports only AGENTS; companion docs use backticked literal paths and load on demand.
"""


def chinese_readme() -> str:
    names = "\n".join(f"- `{name}`" for name in (*SKILLS, *REFERENCES))
    return f"""# NHK 中文说明

[English](README.md)

NHK 用四个 prompt-first skill 处理 5 类反复出现的工作。

{names}

把下面五个同级目录直接复制到同一个 skills root：

```bash
{INSTALL_COMMAND}
```

`scripts/` 和 `tests/` 只供维护者使用，不属于运行时安装内容。
Python validator 是可选、零第三方依赖的检查工具：
`python3 -B scripts/validate_nhk.py --install-root <skills-root>`。
验证后仍要刷新会话，并确认四个 skill 都可发现。
维护者可以验证生成后的 companion docs：
{COMPANION_VALIDATOR_COMMANDS}

NHK 带有八个受控 reference 和五个强制 foundation surface。
implementation-planning companion 是只在规划工作中加载的 Superpowers overlay。
Codex 实践型 preset 阶梯是：{CODEX_PRESET_LADDER}。
用户选择的主线程 model 和 effort 是每个 worker 的成本上限。
同一个 gap 到第五轮仍未解决时，调用 systematic-debugging；根因和架构重审前不准贴第六块补丁。
对新手项目来说，路由表就是新手需要的浅层 code map。
thin CLAUDE 只 import AGENTS；companion docs 使用反引号普通路径并按需读取。
"""


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
            "`implementation-planning.md` owns stable task sizing."
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
            "Reject a task that cannot produce one observable result in one fresh context "
            "with one test cycle and reviewer gate."
        ),
    }
    lines = ["# Implementation Planning", ""]
    for heading, body in sections.items():
        lines.extend((f"## {heading}", "", body, ""))
    lines.extend(f"- extra {index}" for index in range(extra_lines))
    return "\n".join(lines).rstrip() + "\n"


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
        (root / "README.md").write_text(english_readme(), encoding="utf-8")
        (root / "README_CN.md").write_text(chinese_readme(), encoding="utf-8")
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
                "If bootstrap is creating or structurally repairing the "
                "instruction surface",
                "For the instruction surface",
            ),
            (
                "Do not load an instruction template when only a companion or "
                "archive surface is missing.",
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

    def test_missing_convergence_backstop_fails(self) -> None:
        root = self.make_source_fixture()
        for name in ("AGENTS-template.md", "CLAUDE-template.md"):
            path = root / "references" / name
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    f"- {CONVERGENCE_BACKSTOP}\n", ""
                ),
                encoding="utf-8",
            )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("convergence backstop", result.stdout.lower())

    def test_missing_on_demand_planning_pointer_fails(self) -> None:
        root = self.make_source_fixture()
        for name in ("AGENTS-template.md", "CLAUDE-template.md"):
            path = root / "references" / name
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    IMPLEMENTATION_PLANNING_POINTER,
                    "Read the planning guide when useful.",
                    1,
                ),
                encoding="utf-8",
            )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("implementation-planning pointer", result.stdout.lower())

    def test_claude_template_rejects_openai_model_names(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "CLAUDE-template.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "Choose the lowest-cost configuration",
                "Choose GPT-5.6 Luna max as the lowest-cost configuration",
                1,
            ),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("CLAUDE-template.md", result.stdout)
        self.assertIn("model", result.stdout.lower())

    def test_template_source_line_limit_fails(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "AGENTS-template.md"
        path.write_text(
            path.read_text(encoding="utf-8") + ("\n" * 50), encoding="utf-8"
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("190", result.stdout)

    def test_companion_source_line_limits_fail(self) -> None:
        cases = (
            ("coding-agent-guide-template.md", 140),
            ("implementation-planning-template.md", 120),
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

    def test_codex_worker_routing_contract_fails(self) -> None:
        mutations = (
            (CODEX_PRESET_LADDER, "GPT-5.6 Luna max → GPT-5.6 Sol max"),
            ("explicitly specify both model and effort", "use a suitable worker"),
            ("split the packet before escalating", "escalate when useful"),
            ("above the main thread's model or effort", "uses more capacity"),
            ("specific packet and current run", "current project"),
        )
        for required, replacement in mutations:
            with self.subTest(required=required):
                root = self.make_source_fixture()
                path = root / "references" / "AGENTS-template.md"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        required, replacement, 1
                    ),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("worker routing", result.stdout.lower())

    def test_policy_surfaces_reject_models_outside_ladder(self) -> None:
        for model in ("GPT-9 max", "GPT-5.6 Orion max"):
            with self.subTest(model=model):
                root = self.make_source_fixture()
                path = root / "README.md"
                path.write_text(
                    path.read_text(encoding="utf-8")
                    + f"\nUse {model} for every worker.\n",
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("unapproved versioned model", result.stdout.lower())

    def test_all_skills_require_the_planning_foundation(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill):
                root = self.make_source_fixture()
                path = root / skill / "SKILL.md"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        "`implementation-planning.md`",
                        "`missing-planning.md`",
                    ),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn("planning foundation", result.stdout.lower())

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

    def test_readme_convergence_guidance_drift_fails(self) -> None:
        root = self.make_source_fixture()
        for name in ("README.md", "README_CN.md"):
            path = root / name
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "systematic-debugging", "ordinary debugging"
                ),
                encoding="utf-8",
            )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("systematic-debugging", result.stdout.lower())

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
            ("README.md", "eight controlled references", "several references"),
            ("README.md", "five mandatory foundation surfaces", "the foundation"),
            ("README.md", "Superpowers overlay", "planning helper"),
            ("README.md", CODEX_PRESET_LADDER, "choose a suitable worker"),
            ("README_CN.md", "八个受控 reference", "几份 reference"),
            ("README_CN.md", "五个强制 foundation surface", "基础文档"),
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
        for complexity in ("simple", "medium", "complex"):
            with self.subTest(complexity=complexity):
                path = self.write_final(standalone_text())
                result = run_cli(
                    "--final",
                    path,
                    "--kind",
                    "agents",
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
        content = standalone_text()
        content = content.replace("`coding-agent-guide.md`", "coding guide")
        content = content.replace(
            "`implementation-planning.md`", "implementation planning"
        )
        content = content.replace(
            "`documentation-governance.md`", "documentation governance"
        )
        path = self.write_final(content)
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "standalone"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("coding-agent-guide.md", result.stdout)
        self.assertIn("implementation-planning.md", result.stdout)
        self.assertIn("documentation-governance.md", result.stdout)

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
            ("doc-governance", doc_governance_text()),
        )
        for kind, content in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_standalone_allows_project_template_contract_language(self) -> None:
        content = standalone_text().replace(
            "- Project rule for Project Map.",
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
            ("doc-governance", doc_governance_text(extra_lines=100), 100),
        )
        for kind, content, limit in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 1)
                self.assertIn(str(limit), result.stdout)

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
            "> @coding-agent-guide.md",
            "> @implementation-planning.md",
            "<!-- @coding-agent-guide.md -->",
            "<!-- @implementation-planning.md -->",
            "```md\n@coding-agent-guide.md\n```",
            "```md\n@implementation-planning.md\n```",
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
