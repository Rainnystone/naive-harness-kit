---
name: nhk-upkeep
description: Use when an NHK-managed workspace has completed or advanced through a work cycle and its instruction, routing, governance, or tracking surfaces may need drift repair.
---

# NHK Upkeep

Use `nhk-upkeep` only for maintenance after NHK already exists.

- If the workspace does not already have one active instruction file plus `coding-agent-guide.md` and `documentation-governance.md`, route back through `welcome-to-nhk` so the workspace can be sent to `nhk-bootstrap`.
- Do not use `nhk-upkeep` to bootstrap missing NHK foundations.
- Do not use `nhk-upkeep` to perform the archive transition itself.

## Maintenance Pass

1. Determine which instruction file is active in the workspace root.
2. Check that file against current workspace state.
3. Check `coding-agent-guide.md` against current routing reality.
4. Check `documentation-governance.md` against current active-versus-archive reality.
5. Inspect root tracking surfaces such as `task_plan.md`, `progress.md`, and `findings.md`.
6. After drift is repaired, ask the user whether the completed workstream should remain active or move to archive.

## Core Rules

- Check the active instruction file against the live workspace and current execution sources.
- If exactly one of `AGENTS.md` or `CLAUDE.md` exists, preserve it as the active instruction file unless the user explicitly asks to migrate.
- If both files exist, stop and ask the user which file is active. Do not guess, merge, delete, or rewrite either file without explicit direction.
- If neither file exists, stop and route back through `welcome-to-nhk` for `nhk-bootstrap` instead of inventing a new instruction surface inside `nhk-upkeep`.
- Check `coding-agent-guide.md` against current routing reality, not just against its previous wording.
- Check `documentation-governance.md` against the actual active/archive layout and the current naming and loading rules.
- Treat `documentation-governance.md` as the workspace lifecycle contract, and repair it when the live workspace no longer matches its documented rules.
- Check whether the active instruction file still covers the required execution-discipline categories from the matching local template.
- If categories such as subagent delegation, implementation packet discipline, verification, archive check, or documentation governance are missing, repair them or document the human-approved reason for omission.
- If the matching instruction template uses `[[FINAL_VERBATIM]]`, `[[FINAL_ADAPT]]`, `[[OPTIONAL_BY_COMPLEXITY]]`, or `[[TEMPLATE_ONLY]]` markers, check that no marker text leaked into the active instruction file.
- Repair leftover template wording such as `Fill in`, `Suggested`, `Document:`, `Template usage`, or `Generation Contract` when it appears as final instruction text.
- Repair invented instruction headings such as `NHK Governance`, `NHK Govern`, or `Instruction Coverage` unless the human explicitly approved them for that workspace.
- Check that project-adapted sections do not preserve source-template examples as universal project rules.
- Inspect root `task_plan.md`, `progress.md`, and `findings.md` as live surfaces, not permanent assumptions.
- Repair stale statements about active repositories, branches, dependencies, entry docs, routing, verification, active/archive boundaries, and loading order.
- Remove or demote docs that are no longer active execution entry points, and reflect when root tracking files are no longer active surfaces.
- Treat root `task_plan.md`, `progress.md`, and `findings.md` as conditional surfaces. If they look stale or complete, mark them as archive candidates and ask the user instead of clearing or renaming them here.
- When the docs and tracking surfaces suggest a workstream may be complete, ask the user whether it should remain active or move to archive.
- Do not archive, relocate, rename, or clear active tracking files from `nhk-upkeep`. If the user confirms archive readiness, hand off to `nhk-archive`; otherwise leave the workstream active.

## Local References

Use local frozen references where they help repair drift:

- `../references/validation-scenarios.md`
- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`

These references help re-align active docs. They are not blind copy targets and do not replace checking the live workspace first.
