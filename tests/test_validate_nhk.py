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

NHK does not freeze a model catalog. The user's main-thread model and effort set each
worker's cost ceiling. Exact pinning is a project-level, human-approved exception.
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

NHK 不冻结型号目录；用户选择的主线程 model 和 effort 是每个 worker 的成本上限。
精确 pin 只应作为项目级、经人工确认的例外。
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
        "Document Roles": "Instructions govern behavior; the routing guide routes coding work.",
        "Active Documentation Surfaces": "Active plans and tracking contain active work only.",
        "Workspace and Document Map": "Use `AGENTS.md`, the routing guide, active docs, and `archive/README.md`.",
        "Lifecycle Rules": "Archive is historical reference, not the default execution source.",
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
            "`documentation-governance.md`", "documentation governance"
        )
        path = self.write_final(content)
        result = run_cli(
            "--final", path, "--kind", "claude", "--mode", "standalone"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("coding-agent-guide.md", result.stdout)
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
            ("doc-governance", doc_governance_text()),
        )
        for kind, content in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_companion_line_limits_fail(self) -> None:
        cases = (
            ("coding-guide", coding_guide_text(extra_lines=80), 80),
            ("doc-governance", doc_governance_text(extra_lines=100), 100),
        )
        for kind, content, limit in cases:
            with self.subTest(kind=kind):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", kind)
                self.assertEqual(result.returncode, 1)
                self.assertIn(str(limit), result.stdout)

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

    def test_claude_rejects_companion_auto_imports(self) -> None:
        cases = (
            ("thin", "@AGENTS.md\n\nRead @coding-agent-guide.md before editing.\n"),
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
            "> @coding-agent-guide.md",
            "<!-- @coding-agent-guide.md -->",
            "```md\n@coding-agent-guide.md\n```",
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
        path = self.write_final(coding_guide_text())
        cases = (
            ("--mode", "standalone"),
            ("--complexity", "simple"),
        )
        for flag, value in cases:
            with self.subTest(flag=flag):
                result = run_cli(
                    "--final", path, "--kind", "coding-guide", flag, value
                )
                self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
