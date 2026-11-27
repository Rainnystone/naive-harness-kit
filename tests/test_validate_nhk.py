from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_instruction_examples import (
    assemble_companion,
    assemble_planning_guide,
    assemble_standalone,
)


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

CODEX_TIER_LINES = (
    "`light`: GPT-6.1 Terra xhigh.",
    "`standard`: GPT-6.2 Sol xhigh.",
    "`deep`: GPT-6.2 Sol xhigh.",
    "`audit`: GPT-6.2 Sol xhigh.",
)

STANDARD_TIER_CLAUSE = (
    "`standard`: the default for ordinary implementation, local design, integration, "
    "debugging, independent investigation, and initial task reviews."
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


def planning_guide_text(extra_lines: int = 0, *, workflow: str = "Superpowers") -> str:
    return assemble_planning_guide(workflow) + "extra\n" * extra_lines


def human_routing_exception(**overrides: str) -> str:
    record = {
        "target": "billing-module",
        "scope": "src/billing/",
        "role": 'task-implementation',
        "preset": "GPT-6.2 Sol xhigh",
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
    yield record, "", ("GPT-6.1 Terra xhigh", "GPT-6.1 Terra high"), 1
    yield human_routing_exception(approval="decisions/gpt-6-astra-low.md"), "", None, 1
    yield human_routing_exception(preset="GPT-6 Astra max"), "", None, 1
    yield human_routing_exception(preset="GPT-6 Astra medium"), "", None, 1


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


class RecoveryConsultationTests(ValidatorTestCase):
    def check_recovery(self, content: str, source: bool) -> subprocess.CompletedProcess[str]:
        if source:
            root = self.make_source_fixture()
            (root / "references" / "execution-recovery-template.md").write_text(content, encoding="utf-8")
            return run_cli("--root", root)
        return run_cli("--final", self.write_final(content), "--kind", "execution-recovery")

    def recovery_input(self, source: bool) -> str:
        if source:
            return (ROOT / "references" / "execution-recovery-template.md").read_text(encoding="utf-8")
        return execution_recovery_text()

    def test_consultation_requires_handoff_evidence_and_main_thread_decision(self) -> None:
        # Missing instructions must fail in both the package and generated documents.
        required = (
            "unmet acceptance, fixed revisions and relevant diff, prior attempts and observed results",
            "explicitly state when no credible hypothesis exists",
            "investigate one concrete causal question",
            "forms its own explanation before comparing the main thread's provisional explanation",
            "at most one targeted clarification with the same diagnostic worker",
            "Record counts, diagnostic use, clarification use, and recovery use for both the task and stable acceptance gap",
            "never resets diagnostic or clarification use",
            "For ordinary uncertainty, the main thread examines available evidence",
            "reasonable experiments leave that question unresolved",
            "If either the task or stable acceptance gap has used diagnosis, the allowance is exhausted.",
            "The bounded Codex dispatch is already authorized within the current task",
            "record why advice was accepted or rejected and the verification results",
            "Agreement between agents is not causal evidence",
        )
        for source in (False, True):
            content = self.recovery_input(source)
            for clause in required:
                with self.subTest(source=source, clause=clause):
                    self.assertIn(clause, content)
                    result = self.check_recovery(content.replace(clause, "omitted", 1), source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("missing", result.stdout)

    def test_consultation_rejects_additional_permissions(self) -> None:
        grants = (
            "Dispatch a second diagnostic worker for another opinion.",
            "Allow another consultation after the first report.",
            "A second consultation is permitted after the first report.",
            "The main thread may request two targeted clarifications.",
            "Clarification may investigate a new causal question.",
            "The diagnostic worker may modify files to test its advice.",
            "After a new session, diagnostic use resets.",
            "Diagnostic use is reset after a new session.",
            "Clarification use is renewed after a new session.",
            "Dispatch another recovery consultation after the first report.",
            "Dispatch another diagnostic worker on resumption.",
            "Dispatch another diagnostic worker immediately.",
            "Dispatch another diagnostic worker.",
            "Dispatch another recovery consultation on resumption.",
            "Request another targeted clarification immediately.",
            "Use another diagnostic worker for a second opinion.",
            "Use two clarifications after the report.",
            "Dispatch another **diagnostic worker** after the first report.",
            "Dispatch another _diagnostic worker_ after the first report.",
            "Consultation resets the repair count.",
            "Agreement between agents authorizes recovery without verification.",
            "Reset the diagnosis allowance after a new session.",
            "Renew the clarification allowance on resumption.",
            "The diagnosis allowance resets after a new session.",
            "Diagnostic workers may dispatch another helper.",
            "Clarifications can be repeated after resumption.",
            "Ordinary uncertainty requires a consultation.",
            "The main thread must obtain human approval before consultation.",
            "Routine ambiguity triggers independent consultation.",
            "Consultations are required for routine bugs.",
            "A consultation requires separate human approval.",
            "Always consult another agent before continuing.",
        )
        for source in (False, True):
            for grant in grants:
                with self.subTest(source=source, grant=grant):
                    content = self.recovery_input(source)
                    # Preamble and appended grants must not escape the owning section.
                    marker = "### Triggers and Accounting" if source else "## Triggers and Accounting"
                    result = self.check_recovery(content.replace(marker, f"- {grant}\n\n{marker}", 1), source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("consultation", result.stdout)

    def test_consultation_accepts_inactive_examples_and_unrelated_facts(self) -> None:
        additions = (
            "```md\nAllow another consultation.\n```",
            "<!-- The diagnostic worker may modify files. -->",
            "The diagnosis API requires authentication. Follow-up appointments use UTC.",
            "Use `src/diagnosis.py` to reproduce the failure.",
            "Use `diagnosis.md` to reproduce the failure.",
            "Use diagnosis logs from `artifacts/diagnosis/` to reproduce the failure.",
            "The product uses diagnosis codes to group incidents.",
            "Use clarification API responses to reproduce the failure.",
            "Use diagnostic worker logs to reproduce the failure.",
            "Use two diagnosis codes to reproduce the failure.",
            "Do not dispatch a second diagnostic worker.",
            "do not dispatch a second diagnostic worker.",
            "Do not request another diagnostic worker.",
            "Diagnostic workers must authenticate to read production logs.",
            "Consultants must sign the data-access agreement before reading dashboards.",
            "Diagnostic workers can read production logs through the read-only replica.",
            "Request human confirmation before making an out-of-scope permission change.",
        )
        for source in (False, True):
            for addition in additions:
                with self.subTest(source=source, addition=addition):
                    content = self.recovery_input(source)
                    marker = "### Independent Diagnosis" if source else "## Independent Diagnosis"
                    result = self.check_recovery(content.replace(marker, f"{marker}\n\n{addition}", 1), source)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_consultation_prohibition_cannot_hide_a_following_grant(self) -> None:
        for source in (False, True):
            for addition in (
                "Do not dispatch a second diagnostic worker. Allow another clarification.",
                "do not request another **diagnostic worker**; allow another recovery consultation.",
            ):
                with self.subTest(source=source, addition=addition):
                    content = self.recovery_input(source)
                    marker = "### Independent Diagnosis" if source else "## Independent Diagnosis"
                    content = content.replace(marker, f"{marker}\n\n- {addition}", 1)
                    result = self.check_recovery(content, source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("consultation", result.stdout)

    def test_recovery_rejects_routing_routine_decisions_to_the_human(self) -> None:
        for source in (False, True):
            content = self.recovery_input(source)
            heading = "### Main-thread Reassessment" if source else "## Main-thread Reassessment"
            for rule in (
                "The main thread must hand every decision to the human when consultation is unavailable.",
                "The main thread is required to request human confirmation for all routine engineering choices.",
            ):
                with self.subTest(source=source, rule=rule):
                    invalid = content.replace(heading, f"{heading}\n\n- {rule}", 1)
                    result = self.check_recovery(invalid, source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("human decision", result.stdout)

    def test_consultation_required_clauses_must_be_active_and_in_owning_section(self) -> None:
        clause = "at most one targeted clarification with the same diagnostic worker"
        for source in (False, True):
            original = self.recovery_input(source)
            self.assertIn(clause, original)
            line = next(line for line in original.splitlines() if clause in line)
            for hidden in (f"```md\n{line}\n```", f"<!-- {line} -->", ""):
                with self.subTest(source=source, hidden=hidden):
                    content = original.replace(line, hidden, 1)
                    if not hidden:
                        marker = "### Recovery and Stop" if source else "## Recovery and Stop"
                        content = content.replace(marker, f"{marker}\n\n{line}", 1)
                    result = self.check_recovery(content, source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("Independent Diagnosis", result.stdout)


class SourceValidationTests(ValidatorTestCase):
    def check_worker_policy(self, content: str, source: bool) -> subprocess.CompletedProcess[str]:
        if source:
            root = self.make_source_fixture()
            (root / "references" / "worker-policy-template.md").write_text(content, encoding="utf-8")
            return run_cli("--root", root)
        return run_cli("--final", self.write_final(content), "--kind", "worker-policy")

    def worker_policy_input(self, source: bool) -> str:
        if source:
            return (ROOT / "references" / "worker-policy-template.md").read_text(encoding="utf-8")
        return worker_policy_text()

    def test_worker_policy_rejects_parallel_sdd_and_globally_serial_implementation(self) -> None:
        for source in (False, True):
            content = self.worker_policy_input(source)
            heading = "### Dispatch Contract" if source else "## Dispatch Contract"
            for rule in (
                "In SDD, implementers may run in parallel.",
                "Parallel implementation is allowed in SDD.",
                "Run SDD implementers in parallel.",
                "Allow parallel implementation in SDD.",
                "SDD implementers can be dispatched in parallel.",
                "SDD allows parallel implementation.",
                "In SDD, implementers are permitted to run in parallel.",
                "SDD implementation may be parallel.",
                "Never run SDD implementers in parallel. In SDD, implementers may run concurrently.",
                "All implementation is sequential.",
            ):
                with self.subTest(source=source, rule=rule):
                    invalid = content.replace(heading, f"{heading}\n\n- {rule}", 1)
                    result = self.check_worker_policy(invalid, source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("additional routing", result.stdout)

    def test_worker_policy_accepts_prohibitions_on_parallel_sdd(self) -> None:
        for source in (False, True):
            content = self.worker_policy_input(source)
            heading = "### Dispatch Contract" if source else "## Dispatch Contract"
            for rule in (
                "Never run SDD implementers in parallel.",
                "In SDD, implementers must not run concurrently.",
                "Parallel implementation is not permitted in SDD.",
                "No SDD implementers may run in parallel.",
                "Never allow parallel implementation in SDD.",
            ):
                with self.subTest(source=source, rule=rule):
                    policy = content.replace(heading, f"{heading}\n\n- {rule}", 1)
                    result = self.check_worker_policy(policy, source)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_worker_policy_limits_luna_to_an_explicit_current_run_batch(self) -> None:
        permission = (
            "A qualifying mechanical batch may use runtime-supported Luna only if the human "
            "explicitly names Luna for that batch in the current run. Never use Luna for automatic "
            "dispatch, review, recovery, or fallback. Keep that permission out of persistent routing records."
        )
        for source in (False, True):
            content = self.worker_policy_input(source)
            heading = "### Codex Routing" if source else "## Codex Routing"
            for replacement in ("", f"<!-- {permission} -->\n"):
                with self.subTest(source=source, inactive=bool(replacement)):
                    invalid = content.replace(f"- {permission}\n", replacement, 1)
                    result = self.check_worker_policy(invalid, source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("Codex Routing is missing", result.stdout)
            for grant in (
                "Automatically dispatch Luna for mechanical batches.",
                "Use Luna when Sol is unavailable.",
                "Use Luna for final review.",
                "Use Luna for recovery.",
            ):
                with self.subTest(source=source, grant=grant):
                    invalid = content.replace(heading, f"{heading}\n\n- {grant}", 1)
                    result = self.check_worker_policy(invalid, source)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("additional routing", result.stdout)

    def test_active_source_and_final_reject_extra_astra_permissions(self) -> None:
        for grant in (
            "Use GPT-6.2 Astra xhigh for implementation.",
            "Use `gpt-6.2-astra` for final review.",
            "The independent consultant may write files after reporting.",
            "For ordinary uncertainty, always consult another agent.",
            "Use the independent consultation as fallback when Sol is unavailable.",
        ):
            for source in (False, True):
                with self.subTest(source=source, grant=grant):
                    if source:
                        root = self.make_source_fixture()
                        path = root / "references" / "worker-policy-template.md"
                        content = path.read_text(encoding="utf-8")
                        heading = "### Codex Routing"
                    else:
                        content = worker_policy_text()
                        heading = "## Codex Routing"
                    content = content.replace(heading, f"{heading}\n\n- {grant}", 1)
                    if source:
                        path.write_text(content, encoding="utf-8")
                        result = run_cli("--root", root)
                    else:
                        result = run_cli(
                            "--final", self.write_final(content), "--kind", "worker-policy"
                        )
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("additional routing", result.stdout)

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
            ("**Workflow**", "**Default**"),
            ("**Dependencies**", "**Tools**"),
            ("only in conversation", "available temporarily"),
            ("current workspace", "selected workspace"),
            (
                "workflow selection, capability state, instruction topology, "
                "foundation state, lifecycle intent, or workspace changes",
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

    def test_source_requires_workflow_specific_lifecycle_contracts(self) -> None:
        cases = (
            ("welcome-to-nhk/SKILL.md", "A glossary by itself does not identify the workflow."),
            ("welcome-to-nhk/SKILL.md", "Check only capabilities required by the selected route and workstream."),
            ("nhk-bootstrap/SKILL.md", "Create the archive foundation only when the workspace default is Superpowers."),
            ("nhk-upkeep/SKILL.md", "A changed workspace default applies to the next workstream."),
            ("nhk-archive/SKILL.md", "Verify local references and report any remote access that remains unverified."),
            ("references/archive-readme-template.md", "Use confirmed tracker URLs as remote references."),
        )
        for file, required in cases:
            with self.subTest(file=file, required=required):
                root = self.make_source_fixture()
                path = root / file
                path.write_text(
                    path.read_text().replace(required, "", 1), encoding="utf-8"
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("workflow lifecycle", result.stdout.lower())

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
                "Choose the simplest maintainable solution",
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
                "`execution-recovery.md` for independent consultation, after five failed rounds on one task or acceptance gap, or earlier evidence of architectural stagnation",
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
                text = mutated_path.read_text(encoding="utf-8")
                original = f"### {token}" if token in PLANNING_GUIDE_HEADINGS else token
                mutated_path.write_text(
                    text.replace(original, "missing contract"),
                    encoding="utf-8",
                )
                result = run_cli("--root", mutated)
                self.assertEqual(result.returncode, 1)
                self.assertIn(token, result.stdout)

    def test_planning_template_requires_both_workflow_contracts(self) -> None:
        for token, workflow in (
            ("\nWorkflow: Superpowers\n", "Superpowers"),
            ("\nWorkflow: Matt\n", "Matt"),
            ("isolated worktrees", "Matt"),
            ("configured ready-state mapping", "Matt"),
            ("including untracked files", "Matt"),
            ("has a different owner", "Superpowers"),
        ):
            with self.subTest(token=token):
                root = self.make_source_fixture()
                path = root / "references" / "implementation-planning-template.md"
                text = path.read_text(encoding="utf-8")
                self.assertIn(token, text)
                path.write_text(text.replace(token, "", 1), encoding="utf-8")
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(f"implementation-planning-template.md ({workflow})", result.stdout)

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
            ("### Dispatch Contract", "- `light`: Whole modules may use GPT-6 Astra low."),
        ):
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(anchor=anchor, wrapper=wrapper):
                    root = self.make_source_fixture()
                    path = root / "references" / "worker-policy-template.md"
                    path.write_text(path.read_text().replace(anchor, anchor + "\n\n" + wrapper.format(clause), 1))
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_atomic_source_contract_rejects_additive_and_inactive_rules(self) -> None:
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
            ("worker-policy-template.md", STANDARD_TIER_CLAUSE),
            ("implementation-planning-template.md", 'Group implementation, tests, configuration, '
                                                    'migration, and documentation required for that '
                                                    "task's acceptance."),
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
                CODEX_TIER_LINES[0],
                "`light`: GPT-5.6 Luna max.",
            ),
            ("there is no mandatory `light` trial", "always start in `light`"),
            ("Tiers determine permission", "Escalate whenever useful"),
            (
                "Its trigger and existing authorization cover one fresh-context dispatch, shared with recovery diagnosis.",
                "Another fresh dispatch is allowed every time recovery starts.",
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

    def test_worker_policy_source_rejects_models_outside_exact_tiers(self) -> None:
        root = self.make_source_fixture()
        path = root / "references" / "worker-policy-template.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                CODEX_TIER_LINES[2],
                CODEX_TIER_LINES[2].replace("GPT-6.2 Sol xhigh", "GPT-6 Astra max"),
                1,
            ),
            encoding="utf-8",
        )
        result = run_cli("--root", root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("exact tier preset", result.stdout.lower())

    def test_worker_policy_rejects_superseded_codex_defaults_source_and_final(self) -> None:
        mutations = (
            (CODEX_TIER_LINES[0], "`light`: GPT-6 Luna max."),
            (CODEX_TIER_LINES[0], "`light`: GPT-6.1 Terra high."),
            (CODEX_TIER_LINES[0], "`light`: GPT-6.1 Terra max."),
            ("`gpt-6.1-terra`", "`gpt-6-luna`"),
            (CODEX_TIER_LINES[1], "`standard`: GPT-6.1 Sol xhigh."),
            (CODEX_TIER_LINES[2], "`deep`: GPT-6 Astra xhigh."),
            (CODEX_TIER_LINES[3], "`audit`: GPT-6.2 Astra xhigh."),
            ("`gpt-6.2-sol`", "`gpt-6.1-sol`"),
            ("`gpt-6.2-astra`", "`gpt-6-astra`"),
        )
        for current, superseded in mutations:
            with self.subTest(superseded=superseded):
                root = self.make_source_fixture()
                path = root / "references" / "worker-policy-template.md"
                source = path.read_text(encoding="utf-8")
                self.assertIn(current, source)
                path.write_text(source.replace(current, superseded, 1), encoding="utf-8")
                source_result = run_cli("--root", root)
                self.assertEqual(source_result.returncode, 1, source_result.stdout)
                self.assertIn("worker-policy", source_result.stdout.lower())

                final = worker_policy_text()
                self.assertIn(current, final)
                final_result = run_cli(
                    "--final", self.write_final(final.replace(current, superseded, 1)),
                    "--kind", "worker-policy",
                )
                self.assertEqual(final_result.returncode, 1, final_result.stdout)
                self.assertIn("worker-policy", final_result.stdout.lower())

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
                    self.assertIn("five-companion foundation", result.stdout.lower())

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
                    guidance = [p for p in paragraphs if "GPT-6.2 Astra" in p]
                    self.assertEqual(len(guidance), 1)
                    paragraphs.remove(guidance[0])
                    path.write_text("\n\n".join(paragraphs), encoding="utf-8")
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                for name in names:
                    self.assertIn(f"{name}: missing required fact", result.stdout)

    def test_readme_main_thread_guidance_drift_fails(self) -> None:
        cases = (
            ("README.md", "we suggest GPT-6.2 Astra xhigh", "we suggest another available model"),
            ("README.md", "human-facing suggestion only", "mandatory main-thread policy"),
            ("README.md", "You choose the main-thread model and effort", "NHK chooses the main-thread model and effort"),
            ("README.md", "NHK worker permissions do not depend on that choice", "NHK worker permissions depend on that choice"),
            ("README_CN.md", "建议使用 GPT-6.2 Astra xhigh", "建议考虑其他可用型号"),
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
            ("README.md", "Claude's light helper runs Haiku", "Claude helpers use a model"),
            ("README.md", "every other Claude helper runs Opus", "every other Claude helper runs Sonnet"),
            ("README.md", "Claude Code main thread, we suggest Opus high", "Claude Code main thread, pick anything"),
            ("README.md", "five stable guides", "several guides"),
            ("README.md", "Superpowers overlay", "planning helper"),
            ("README.md", "sorts helper work into four capability tiers", "picks helpers"),
            ("README_CN.md", "十一个受控 reference", "几份 reference"),
            ("README_CN.md", "Claude 的 light 帮手使用 Haiku", "Claude 的帮手随便选"),
            ("README_CN.md", "其余帮手全部使用 Opus", "其余帮手全部使用 Sonnet"),
            ("README_CN.md", "Claude Code 主线程，建议使用 Opus high", "Claude Code 主线程随意"),
            ("README_CN.md", "把帮手的工作分成四个能力档位", "随便挑帮手"),
            ("README_CN.md", "五份配套说明", "若干配套说明"),
            ("README_CN.md", "Superpowers overlay", "规划辅助"),
        )
        for name, required, replacement in cases:
            with self.subTest(name=name, required=required):
                root = self.make_source_fixture()
                path = root / name
                self.assertIn(required, path.read_text(encoding="utf-8"))
                path.write_text(
                    path.read_text(encoding="utf-8").replace(
                        required, replacement
                    ),
                    encoding="utf-8",
                )
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(required, result.stdout)

    def test_claude_agents_template_contract(self) -> None:
        mutations = (
            ("model: opus\neffort: medium", "model: inherit\neffort: medium", "model: opus"),
            ("effort: xhigh", "effort: max", "effort"),
            ("model: haiku\neffort: max", "model: opus\neffort: max", "model: haiku"),
            ("model: haiku\neffort: max", "model: haiku\neffort: ultra", "effort"),
            ("model: opus\neffort: medium", "model: haiku\neffort: medium", "model: opus"),
            ("name: nhk-light\n", "name: nhk-small\n", "nhk-light"),
            ("`nhk-audit` succeeds `nhk-diagnosis`", "`nhk-audit` replaces nothing", "retired definitions"),
            (
                "An older `nhk-light` is a current definition and is reconciled like the others.",
                "An older `nhk-light` is retired; report it for the human to delete.",
                "retired definitions",
            ),
            ("effort: high", "effort: low", "effort"),
            ("disallowedTools: Write, Edit, NotebookEdit\n", "", "disallowedTools"),
            (
                "description: NHK deep tier worker.",
                "description: NHK deep tier worker. Use proactively.",
                "proactive",
            ),
            (
                "## Shared Body",
                "### nhk-light\n\n```yaml\n---\nname: nhk-light\n"
                "description: NHK light worker. Dispatch only as routed by worker-policy.md.\n"
                "model: opus\neffort: low\n---\n```\n\n## Shared Body",
                "nhk-light",
            ),
            ("never deletes or renames one itself", "deletes them", "retired definitions"),
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


class AtomicRoutingRegressionTests(ValidatorTestCase):
    def test_planning_preserves_workspace_module_facts(self) -> None:
        for fact in (
            "Each task records the module it changes.",
            "One task may change more than one module.",
            "Every task checks the affected module boundary.",
        ):
            with self.subTest(fact=fact):
                content = planning_guide_text() + "\n" + fact + "\n"
                result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 0, result.stdout)
                root = self.make_source_fixture()
                path = root / "references" / "implementation-planning-template.md"
                path.write_text(path.read_text().replace("### Plan Layers", "### Plan Layers\n\n- " + fact, 1))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 0, result.stdout)

    def test_source_rejects_unconditional_task_routes(self) -> None:
        for route in (
            "Standard tasks use nhk-light.",
            "Use nhk-deep for every task implementation.",
            "Judgment tasks use nhk-light.",
            "Judgment tasks use nhk-audit.",
            "Band 2 handles ordinary implementation.",
        ):
            with self.subTest(route=route):
                root = self.make_source_fixture()
                path = root / "references" / "worker-policy-template.md"
                path.write_text(path.read_text().replace("### Claude Routing", "### Claude Routing\n\n- " + route, 1))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("additional routing", result.stdout)

    def test_worker_template_requires_bounded_legacy_migration(self) -> None:
        for phrase in (
            "same single task, scope, and confirmed approval",
            "never copy its authorization across the new tasks",
            "Legacy tier migration",
            "the superseded GPT-6.1 Sol and GPT-6 Astra presets",
            "its role remains permitted for that tier",
        ):
            with self.subTest(phrase=phrase):
                root = self.make_source_fixture()
                path = root / "references" / "worker-policy-template.md"
                content = path.read_text()
                self.assertIn(phrase, content)
                path.write_text(content.replace(phrase, "REMOVED", 1))
                result = run_cli("--root", root)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("worker-policy-template", result.stdout)

    def test_bootstrap_and_upkeep_require_atomic_migration(self) -> None:
        for skill in ("nhk-bootstrap", "nhk-upkeep"):
            for required in (
                "Reconcile atomic task sizing, planning detail",
                "Preserve completed and in-flight task identities and progress",
                "without resetting acceptance-gap counts",
                "Follow the worker-policy template migration contract for legacy module-role records",
            ):
                with self.subTest(skill=skill, required=required):
                    root = self.make_source_fixture()
                    path = root / skill / "SKILL.md"
                    content = path.read_text()
                    self.assertIn(required, content)
                    path.write_text(content.replace(required, "REMOVED", 1))
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertIn("atomic migration", result.stdout)

    def test_readmes_require_atomic_and_small_feature_guidance(self) -> None:
        for filename, phrases in (
            ("README.md", ("smallest independently testable deliveries", "The plan need not contain complete implementation code")),
            ("README_CN.md", ("能够独立测试、值得独立审查的最小交付", "计划不必给出完整实现代码")),
        ):
            for phrase in phrases:
                with self.subTest(filename=filename, phrase=phrase):
                    root = self.make_source_fixture()
                    path = root / filename
                    content = path.read_text()
                    self.assertIn(phrase, content)
                    path.write_text(content.replace(phrase, "REMOVED", 1))
                    result = run_cli("--root", root)
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertIn(filename, result.stdout)

    def test_planning_rejects_whole_module_and_step_dispatch_defaults(self) -> None:
        for clause in (
            "Default one Superpowers Task is one Module.",
            "Each task is a complete module.",
            "Every task must own a whole module.",
            "A complete module per task is required.",
            "Every Task must deliver a whole Module.",
            "Each internal TDD step becomes a task.",
        ):
            with self.subTest(clause=clause):
                content = planning_guide_text() + "\n" + clause
                result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("atomic", result.stdout.lower())

    def test_task_routing_roles_are_accepted(self) -> None:
        for role in ("task-implementation", "initial-task-review"):
            with self.subTest(role=role):
                record = human_routing_exception(role=role)
                content = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + record, 1)
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unrecognized_codex_tier_rows_fail(self) -> None:
        for row in ("- `fast`: local.", "- `fast`: GPT-6.1 Terra xhigh.", "- `audit-plus`: GPT-6 Astra xhigh."):
            with self.subTest(row=row):
                content = worker_policy_text().replace("## Claude Routing", row + "\n\n## Claude Routing", 1)
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("unexpected tier", result.stdout)

    def test_tier_words_in_project_facts_are_not_routes(self) -> None:
        for fact in (
            "The security audit log is stored in logs/audit.json.",
            "Deep links open in the light theme.",
            "The free tier limits API calls.",
        ):
            with self.subTest(fact=fact):
                content = worker_policy_text().rstrip() + "\n\n" + fact + "\n"
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                content = execution_recovery_text().rstrip() + "\n\n" + fact.replace("The", "Inspect the", 1) + "\n"
                result = run_cli("--final", self.write_final(content), "--kind", "execution-recovery")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_terra_project_facts_are_not_routes(self) -> None:
        for fact in (
            "The project name is Terra.",
            "Terra stores customer records.",
            "The Terra endpoint returns JSON.",
        ):
            for kind, content in (
                ("worker-policy", worker_policy_text()),
                ("execution-recovery", execution_recovery_text()),
            ):
                with self.subTest(fact=fact, kind=kind):
                    result = run_cli(
                        "--final", self.write_final(content.rstrip() + "\n\n" + fact + "\n"),
                        "--kind", kind,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_terra_model_selections_remain_routes(self) -> None:
        for selection in ("Use Terra.", "Dispatch Terra.", "Model: Terra.", "Terra xhigh."):
            for kind, content in (
                ("worker-policy", worker_policy_text()),
                ("execution-recovery", execution_recovery_text()),
            ):
                with self.subTest(selection=selection, kind=kind):
                    result = run_cli(
                        "--final", self.write_final(content.rstrip() + "\n\n" + selection + "\n"),
                        "--kind", kind,
                    )
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("routing", result.stdout)

    def test_legacy_band_routes_require_tier_migration(self) -> None:
        for extra in (
            "- Band 2: GPT-6 Astra medium.",
            "- Band 3: GPT-6 Astra xhigh.",
            "- Default ordinary implementation, local design, integration, debugging, and independent investigation to Band 2.",
            "- `nhk-light`: small mechanical or standard tasks meeting the low-risk implementation condition.",
            "- `nhk-diagnosis`: read-only independent diagnosis and complex whole-change final review.",
        ):
            with self.subTest(extra=extra):
                content = worker_policy_text().rstrip() + "\n" + extra + "\n"
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_legacy_module_routing_roles_require_migration(self) -> None:
        for role in ("module-implementation", "initial-module-review"):
            with self.subTest(role=role):
                record = human_routing_exception(role=role)
                content = worker_policy_text().replace("## Codex Routing", "## Codex Routing\n" + record, 1)
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("routing exception", result.stdout.lower())


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

    def test_matt_navigation_is_optional_unique_and_canonical(self) -> None:
        nav = (
            "\n## Agent skills\n\n### Issue tracker\nSee `docs/agents/issue-tracker.md`.\n"
            "\n### Domain docs\nSee [domain rules](docs/agents/domain.md).\n"
        )
        base = assemble_standalone(ROOT / "references/AGENTS-template.md", "simple")
        for kind in ("agents", "claude"):
            for section, valid in (
                (nav, True), (nav + "\n### Triage labels\nSee `docs/agents/triage-labels.md`.\n", True),
                (nav.split("### Domain docs")[0], True), ("\n## Agent skills\n### Domain docs\nSee `docs/agents/domain.md`.\n", True),
                ("\n## Agent skills\nNo routes.\n", False), (nav.replace("### Domain docs", ""), False), (nav + nav, False), (nav + "\n### Triage labels\nSee project labels.\n", False),
                (nav.replace("docs/agents/domain.md", "docs/agents/domain.md.old"), False),
                (nav.replace("See `docs/agents/issue-tracker.md`.", "<!-- `docs/agents/issue-tracker.md` -->"), False),
            ):
                with self.subTest(kind=kind, section=section):
                    result = run_cli("--final", self.write_final(base + section), "--kind", kind,
                                     "--mode", "standalone", "--complexity", "simple")
                    self.assertEqual(result.returncode, 0 if valid else 1, result.stdout)
        result = run_cli("--final", self.write_final("@AGENTS.md\n" + nav), "--kind", "claude", "--mode", "thin")
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_authorized_implementation_cannot_end_on_routine_uncertainty(self) -> None:
        base = assemble_standalone(ROOT / "references/AGENTS-template.md", "simple")
        damaged = base.replace("resolve engineering uncertainty and take the next in-scope action",
                               "ask the user about each engineering decision before proceeding")
        self.assertNotEqual(base, damaged)
        result = run_cli("--final", self.write_final(damaged), "--kind", "agents", "--mode", "standalone")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Blockers and Human Approval", result.stdout)

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
        for workflow in ("Matt", "Superpowers"):
            with self.subTest(workflow=workflow):
                text = planning_guide_text(workflow=workflow)
                result = run_cli("--final", self.write_final(text), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_matt_planning_guide_uses_native_artifacts_and_allows_other_skill_references(self) -> None:
        text = planning_guide_text(workflow="Matt")
        for token in ("`to-spec`", "`to-tickets`", "`implement-spec`", "`code-review`", "isolated worktrees"):
            self.assertIn(token, text)
        for token in ("Superpowers", "Task N", "**Files:**", "concrete TDD steps", "**Worker class:**"):
            self.assertNotIn(token, text)
        content = text + "\n- For an unrelated bug, use Superpowers `systematic-debugging` when available.\n"
        result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_matt_tickets_cannot_be_assigned_a_second_execution_workflow(self) -> None:
        guide = planning_guide_text(workflow="Matt")
        result = run_cli("--final", self.write_final(guide + "\nRun Superpowers SDD for every Matt ticket."),
                         "--kind", "planning-guide")
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_matt_planning_guide_requires_active_workflow_and_native_contract(self) -> None:
        text = planning_guide_text(workflow="Matt")
        for original, replacement, diagnostic in (
            ("Workflow: Matt", "<!-- Workflow: Matt -->", "Workflow Compatibility"),
            ("Workflow: Matt", "```md\nWorkflow: Matt\n```", "Workflow Compatibility"),
            ("Workflow: Matt", "Workflow: Superpowers", "Workflow Compatibility"),
            ("vertical slice", "component", "Plan Layers"),
            ("observable acceptance criteria", "completion", "Task Contract"),
            ("isolated worktrees", "one shared checkout", "Dependencies and Execution"),
            ("configured ready-state mapping", "call setup", "Workflow Compatibility"),
            ("including untracked files", "only committed files", "Dependencies and Execution"),
            ("has a different owner", "also uses a plugin", "Workflow Compatibility"),
            ("Keep ticket state in the configured tracker", "Duplicate ticket state in a separate ledger", "Dependencies and Execution"),
            ("verifiable batches", "one step", "Wide Changes"),
            ("Standards and Spec", "Standards alone", "Plan Review"),
        ):
            with self.subTest(original=original, replacement=replacement):
                self.assertIn(original, text)
                content = text.replace(original, replacement, 1)
                result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(diagnostic, result.stdout)

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
            human_routing_exception(preset="GPT-6 Astra medium"),
            human_routing_exception(preset="GPT-6 Astra xhigh"),
            human_routing_exception(preset="GPT-6.1 Sol xhigh"),
            human_routing_exception(preset="GPT-6.2 Astra xhigh"),
            human_routing_exception(role="independent-consultation"),
            human_routing_exception(preset="Ultra"),
            human_routing_exception(preset="GPT-6 Luna max"),
            human_routing_exception(role="recursive-delegation"),
            human_routing_exception(role='initial-task-review', preset="GPT-6.1 Terra xhigh"),
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
            human_routing_exception(role='initial-task-review'),
            human_routing_exception(role="scoped-re-review", preset="GPT-6.1 Terra xhigh"),
            human_routing_exception(role="local-fix", preset="GPT-6.2 Sol xhigh"),
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
            ("## Dispatch Contract", "- `light`: Whole modules may use GPT-6 Astra low."),
        ):
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(anchor=anchor, wrapper=wrapper):
                    text = worker_policy_text().replace(anchor, anchor + "\n\n" + wrapper.format(clause), 1)
                    result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_shared_contracts_scan_active_preambles(self) -> None:
        for kind, text, clause, extra_args in (
            ("planning-guide", planning_guide_text(), "Every Task must deliver a whole Module.", ()),
            ("agents", assemble_standalone(ROOT / "references" / "AGENTS-template.md", "simple"),
             "Replace workers after 1800 seconds.", ("--mode", "standalone", "--complexity", "simple")),
        ):
            for wrapper, expected in (("{}", 1), ("<!-- {} -->", 0), ("```md\n{}\n```", 0)):
                with self.subTest(kind=kind, wrapper=wrapper):
                    content = wrapper.format(clause) + "\n\n" + text
                    result = run_cli("--final", self.write_final(content), "--kind", kind, *extra_args)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_atomic_contract_requires_active_correct_sections(self) -> None:
        cases = (
            ("worker-policy", worker_policy_text(), "Capability Tiers", "Claude Routing",
             STANDARD_TIER_CLAUSE),
            ("planning-guide", planning_guide_text(), "Plan Layers", "Plan Review",
             'An atomic task is the smallest independently testable delivery with a complete '
             'verification loop worth its own review. Split where a reviewer could accept one result '
             'and reject its neighbor, including within the same feature.'),
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

    def test_atomic_contract_accepts_reuse_and_inactive_conflicts(self) -> None:
        text = worker_policy_text()
        self.assertIn("Prefer the original implementer", text)
        self.assertIn("original independent reviewer", text)
        self.assertIn("cause, intended behavior, approach, impact, and verification are clear", text)
        self.assertIn("`light`: small mechanical or standard tasks meeting the low-risk implementation condition", text)
        for extra in ("<!-- Whole modules may use `light`. -->", "```md\nWhole modules may use `light`.\n```"):
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

    def test_atomic_routing_rejects_additive_authorizations(self) -> None:
        for clause in (
            "Whole modules may use GPT-6 Astra low.",
            "Module implementation may use GPT-6.1 Terra xhigh.",
            "Mechanical fixes may include design judgment and use Band 1.",
            "Initial module reviews may use Band 1.",
            "Mechanical fixes may include design judgment and use `light`.",
            "Initial task reviews may use `light`.",
            "Use Terra.",
        ):
            with self.subTest(clause=clause):
                text = worker_policy_text().replace("## Claude Routing", clause + "\n\n## Claude Routing")
                result = run_cli("--final", self.write_final(text), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_atomic_review_rejects_additive_consolidation(self) -> None:
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
            "Capability Tiers",
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

    def test_tier_catalog_and_permissions_are_required(self) -> None:
        content = worker_policy_text()
        for clause in (
            *CODEX_TIER_LINES,
            STANDARD_TIER_CLAUSE,
            "`deep`: a concrete reasoning difficulty remaining after those checks, or demonstrated `standard` capability limits.",
            "`audit` is read-only and covers complex whole-change final review and independent diagnosis when the platform routes diagnosis to that tier.",
            "Other whole-change final reviews use `deep`.",
            "Map tiers to definitions: `light` uses `nhk-light`, `standard` uses `nhk-standard`, `deep` uses `nhk-deep`, and `audit` uses the read-only `nhk-audit`.",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, content)
                mutated = content.replace(clause, "", 1)
                result = run_cli("--final", self.write_final(mutated), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_planning_requires_sizing_before_capability_and_no_fragmentation(self) -> None:
        content = planning_guide_text()
        for clause in (
            'Before increasing capability, separate independent deliveries and decisions and resolve '
            'missing interfaces or context; preserve tightly coupled logic and its verification.',
            'When many tasks need higher capability, recheck boundaries and shared constraints; use '
            'no fixed quota and preserve irreducible difficult tasks.',
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, content)
                result = run_cli("--final", self.write_final(content.replace(clause, "", 1)), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1, result.stdout)

    def test_worker_policy_accepts_reordered_exact_tier_rows(self) -> None:
        content = worker_policy_text()
        original = "\n- ".join(CODEX_TIER_LINES)
        self.assertIn(original, content)
        content = content.replace(original, "\n- ".join(reversed(CODEX_TIER_LINES)), 1)
        result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_worker_policy_rejects_wrong_missing_extra_or_duplicate_presets(self) -> None:
        valid = CODEX_TIER_LINES[1]
        invalid = (
            valid.replace("GPT-6.2 Sol xhigh", "GPT-6.2 Sol max"),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-6.2 Sol high"),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-6.2 Astra xhigh"),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-5.6 Terra xhigh"),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-5.5 xhigh"),
            valid.replace("GPT-6.2 Sol xhigh", ""),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-5.6 Sol medium"),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-6.2 Sol xhigh; GPT-6.1 Terra xhigh"),
            valid.replace("GPT-6.2 Sol xhigh", "GPT-6.2 Sol xhigh; GPT-6.2 Sol xhigh"),
            valid + "\n- " + CODEX_TIER_LINES[3],
        )
        for replacement in invalid:
            with self.subTest(replacement=replacement):
                self.assertNotEqual(replacement, valid)
                path = self.write_final(worker_policy_text().replace(valid, replacement, 1))
                result = run_cli("--final", path, "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1)
                self.assertIn("exact tier preset", result.stdout.lower())

    def test_worker_policy_rejects_drift_in_review_and_special_roles(self) -> None:
        mutations = (
            (
                "Keep Superpowers SDD implementers sequential.",
                "Keep subagent-driven implementers sequential.",
                "Dispatch Contract",
            ),
            (
                "independent ready tickets may run concurrently",
                "all tickets may run concurrently",
                "Dispatch Contract",
            ),
            (
                "independent read-only Standards and Spec reviewers in parallel",
                "an independent read-only reviewer issuing one combined verdict",
                "Review Gates",
            ),
            (
                "All other Superpowers plans",
                "All other plans",
                "Review Gates",
            ),
            (
                "Both must pass; self-review is not a substitute.",
                "Either verdict may pass; self-review is enough.",
                "Review Gates",
            ),
            (
                "`light` never performs an initial task review.",
                "`light` may perform any initial task review.",
                "Capability Tiers",
            ),
            (
                "`audit` is read-only and covers complex whole-change final review and independent diagnosis when the platform routes diagnosis to that tier.",
                "`audit` may perform ordinary implementation and recovery.",
                "Capability Tiers",
            ),
            (
                "Initial reviews still exclude the `light` preset.",
                "Initial reviews may use any preset.",
                "Codex Routing",
            ),
            (
                "Use Fable only when the human explicitly chooses or approves it for the main thread.",
                "Use Fable for workers when it is available.",
                "Claude Routing",
            ),
            (
                "only for the read-only independent consultation defined in `execution-recovery.md`.",
                "for any authorized fix or final review.",
                "Codex Routing",
            ),
            (
                "Never continue a diagnostic worker for open items.",
                "Continue a diagnostic worker for open items as needed.",
                "Claude Routing",
            ),
            (
                "never the one-shot Explore or Plan agents",
                "or the Explore agent",
                "Claude Routing",
            ),
            (
                "the clarification lapses and no fresh worker replaces it",
                "dispatch a fresh worker for the clarification",
                "Claude Routing",
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

    def test_tier_routing_rejects_default_ceiling_review_and_fallback_drift(self) -> None:
        mutations = (
            ("`deep` is the ordinary ceiling", "`audit` is the ordinary ceiling"),
            ("independent investigation, and initial task reviews.", "independent investigation."),
            ("it never authorizes another tier, an older model, or the `audit` configuration as fallback",
             "it authorizes the `audit` configuration when `deep` is unavailable"),
            ("Other whole-change final reviews use `deep`.", "Other whole-change final reviews use `audit`."),
            (STANDARD_TIER_CLAUSE, "`standard`: module implementation, internal debugging, tests, and integration use `deep`."),
        )
        for required, replacement in mutations:
            with self.subTest(required=required):
                content = worker_policy_text()
                self.assertIn(required, content)
                result = run_cli("--final", self.write_final(content.replace(required, replacement, 1)), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Capability Tiers", result.stdout)

    def test_recovery_diagnosis_uses_worker_policy_role(self) -> None:
        route = "using the independent diagnosis role in `worker-policy.md`"
        for replacement in ("using Band 2", "using the `audit` tier", "using `nhk-audit`", "using GPT-6 Astra max"):
            with self.subTest(replacement=replacement):
                content = execution_recovery_text()
                self.assertIn(route, content)
                result = run_cli("--final", self.write_final(content.replace(route, replacement, 1)), "--kind", "execution-recovery")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Independent Diagnosis", result.stdout)

    def test_additive_audit_and_max_routes_fail(self) -> None:
        for route in ("GPT-6 Astra xhigh", "gpt-6-astra xhigh", "The `audit` tier", "`nhk-audit`",
                      "GPT-6 Astra max", "gpt-6-astra max"):
            for role in ("ordinary implementation", "debugging", "scoped re-review"):
                for heading in ("## Capability Tiers", "## Claude Routing"):
                    with self.subTest(route=route, role=role, heading=heading):
                        content = worker_policy_text().replace(
                            heading, f"- {route} is approved for {role}.\n\n{heading}",
                        )
                        result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                        self.assertEqual(result.returncode, 1, result.stdout)

    def test_additive_diagnostic_routes_fail(self) -> None:
        for route in ("Band 3", "the `audit` tier", "deep", "`nhk-audit`", "GPT-6 Astra xhigh", "GPT-6 Astra max", "gpt-6-astra max", "Sonnet", "Terra", "max", "xhigh", "Extra High"):
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

- Do not use the `audit` tier for ordinary implementation.
- GPT-6.1 Terra xhigh must not perform initial task reviews.""",
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

    def test_worker_policy_rejects_legacy_ultra_permissions(self) -> None:
        # Ultra is no longer a worker route; stale approvals must be migrated, not kept.
        for legacy in (
            "Ultra requires human approval naming the packet and current run. It never becomes a reusable project or session default.",
            "Ultra authorization and recursion authorization never imply each other.",
            "Ultra approval never authorizes recursive delegation.",
        ):
            with self.subTest(legacy=legacy):
                content = worker_policy_text().replace("## Codex Routing", f"## Codex Routing\n\n- {legacy}", 1)
                result = run_cli("--final", self.write_final(content), "--kind", "worker-policy")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("additional routing", result.stdout)

    def test_worker_policy_rejects_presets_declared_outside_tier_lines(self) -> None:
        extras = (
            "GPT-9 Nova max is also approved for ordinary implementation.",
            "GPT-5.6 Luna max is also approved for ordinary implementation.",
            "GPT-6 Astra low is also approved for ordinary implementation.",
            "GPT-6.1 Sol max is also approved for ordinary implementation.",
            "GPT-6 Astra max is also approved for ordinary implementation.",
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
            'Preserve its `Files`, `Interfaces`, concrete TDD steps, commands, expected results, and '
            'necessary code examples. Specify behavior, boundaries, and verification; workers own '
            'local implementation without a mandatory complete code listing in the plan.',
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

    def test_planning_guide_rejects_invalid_workflow_declarations(self) -> None:
        text = planning_guide_text().replace("Workflow: Superpowers\n", "", 1)
        for declaration, heading in (
            ("Workflow: Unknown", "Workflow Compatibility"),
            ("Workflow: Matt\nWorkflow: Superpowers", "Workflow Compatibility"),
            ("Workflow: Superpowers\nWorkflow: Superpowers", "Workflow Compatibility"),
            ("Workflow: Superpowers", "Plan Review"),
        ):
            with self.subTest(declaration=declaration, heading=heading):
                content = text.replace(f"## {heading}\n", f"## {heading}\n\n{declaration}\n", 1)
                result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Workflow Compatibility", result.stdout)

    def test_planning_guide_preserves_legacy_superpowers_contract(self) -> None:
        text = "\n".join(
            line for line in planning_guide_text().splitlines()
            if not line.startswith(("Workflow: ", "- Choose one primary workflow"))
        )
        result = run_cli("--final", self.write_final(text), "--kind", "planning-guide")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        content = text.replace("**Delivers:**", "Delivery:", 1)
        result = run_cli("--final", self.write_final(content), "--kind", "planning-guide")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("field syntax", result.stdout)

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

    def test_archive_approval_prohibitions_and_waivers(self) -> None:
        cases = (
            ("Never archive without explicit human approval.", True),
            ("Do not archive a workstream without human approval.", True),
            ("Do not bypass explicit human approval.", True),
            ("Never archive draft release notes and tickets without explicit human approval.", True),
            ("Never archive draft tickets but proceed without human approval.", False),
            ("No workstream may be archived without human approval.", True),
            ("Archive without explicit human approval.", False),
            ("Human approval is optional.", False),
            ("- Never archive drafts\n- Archive completed workstreams without human approval.", False),
            ("1. Never archive drafts\n2. Archive completed workstreams without human approval.", False),
            ("Never archive drafts\n\nArchive completed workstreams without human approval.", False),
            ("- Never archive a draft release\n  without explicit human approval.", True),
            ("Never archive without explicit human approval unless the tracker item is closed.", False),
            ("Except for local archives, never archive without explicit human approval.", False),
            ("Explicit human approval is required unless the tracker item is closed.", False),
            ("Never archive without human approval. Retain the source unless its owner approves removal.", True),
            ("Do not require explicit human approval before archiving.", False),
            ("Never archive without human approval. For local archives, skip human approval.", False),
        )
        for rule, valid in cases:
            with self.subTest(rule=rule):
                content = doc_governance_text().replace(
                    "Explicit human approval is required before archiving.", rule,
                )
                result = run_cli("--final", self.write_final(content), "--kind", "doc-governance")
                self.assertEqual(result.returncode, 0 if valid else 1, result.stdout)
                if not valid:
                    self.assertIn("requires explicit human approval", result.stdout)

    def test_doc_governance_accepts_legacy_and_explicit_workflows(self) -> None:
        legacy = doc_governance_text()
        superpowers = legacy.replace(
            "## Document Roles\n\n",
            "## Document Roles\n\nWorkflow: Superpowers\n\n",
        ).replace(
            "Reset tracking", "The archive foundation is required. Reset tracking"
        )
        matt = legacy.replace(
            "## Document Roles\n\n",
            "## Document Roles\n\nWorkflow: Matt\n\n",
        ).replace(
            "Copy materials and update "
            "the archive index before verification. If verification fails, preserve every "
            "active original. Reset tracking only when no other live workstream depends on it.",
            "Create the archive index on the first explicitly approved archive. "
            "Use remote links and preserve local sources and tracking.",
        )
        for label, content in (
            ("legacy", legacy),
            ("legacy with remote evidence", legacy + "\nRetain remote links to the release evidence in the archive index.\n"),
            ("superpowers", superpowers),
            ("matt", matt),
            ("legacy with a quoted example", legacy + "\n> Workflow: Matt\n"),
        ):
            with self.subTest(label=label):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", "doc-governance")
                self.assertEqual(result.returncode, 0, result.stdout)

        for label, content in (
            ("unknown", matt.replace("Workflow: Matt", "Workflow: Other")),
            ("indented code", matt.replace("Workflow: Matt", "    Workflow: Matt")),
            ("approval waived", matt.replace("Explicit human approval is required before archiving.",
                                              "Do not require explicit human approval before archiving.")),
            ("duplicate", matt.replace("Workflow: Matt", "Workflow: Matt\nWorkflow: Superpowers")),
            ("outside roles", matt.replace("Workflow: Matt\n\n", "") + "\nWorkflow: Matt\n"),
            ("unmarked Matt", matt.replace("Workflow: Matt\n\n", "")),
            ("lazy Superpowers", matt.replace("Workflow: Matt", "Workflow: Superpowers")),
            ("eager Matt", superpowers.replace("Workflow: Superpowers", "Workflow: Matt")),
        ):
            with self.subTest(label=label):
                path = self.write_final(content)
                result = run_cli("--final", path, "--kind", "doc-governance")
                self.assertEqual(result.returncode, 1, result.stdout)
                diagnostic = "approval" if label == "approval waived" else "workflow"
                self.assertIn(diagnostic, result.stdout.lower())

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

    def test_claude_routing_is_fixed_by_tier(self) -> None:
        mutations = (
            ("Claude workers run Opus, except that `nhk-light` runs Haiku.", "Every Claude worker runs Opus."),
            ("Claude workers run Opus, except that `nhk-light` runs Haiku.", "Claude workers run Sonnet."),
            ("`deep` uses `nhk-deep`, and `audit` uses the read-only `nhk-audit`", "`deep` and `audit` use `nhk-deep`"),
            ("`light` uses `nhk-light`, `standard` uses `nhk-standard`", "`light` and `standard` use `nhk-standard`"),
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
            "Use `nhk-deep` for every task implementation.",
            "Standard tasks use nhk-light.",
            "Judgment tasks use nhk-light.",
            "Dispatch `nhk-diagnosis` for ordinary fixes.",
            "Dispatch `nhk-audit` for ordinary fixes.",
            "Complex final review uses `nhk-deep`.",
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
