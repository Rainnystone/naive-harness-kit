---
name: nhk-upkeep
description: Use when an NHK-managed workspace has advanced through a work cycle and its instruction, routing, governance, archive-index, or tracking descriptions may need drift repair.
---

# NHK Upkeep

Use this skill only after the NHK foundation exists. It repairs active references and state descriptions; it does not bootstrap missing surfaces or perform an archive transition.

## Prerequisite And Topology Check

Confirm that `superpowers` and `planning-with-files` are installed, enabled, or explicitly adopted for this NHK run. A temporary adopt is not installation and creates no persistent marker.

Resolve the canonical instruction topology before maintenance:

- only `AGENTS.md`: AGENTS is canonical
- only ordinary `CLAUDE.md`: CLAUDE is standalone canonical
- both, with a real non-quoted, non-comment, non-fenced line exactly `@AGENTS.md` or `@./AGENTS.md` after trimming: AGENTS is canonical and CLAUDE is thin; do not ask
- only CLAUDE with such an import: broken adapter; ask restore AGENTS versus convert to standalone
- both without such an import: real ambiguity; ask and do not modify either file
- neither: route through `welcome-to-nhk` to `nhk-bootstrap`

Then confirm all four foundation surfaces exist: `coding-agent-guide.md`, `documentation-governance.md`, `archive/`, and `archive/README.md`. If any is missing, route through `welcome-to-nhk` to `nhk-bootstrap` before doing upkeep.

## Maintenance Pass

1. Compare the canonical instruction source and any thin adapter with the live workspace and selected local template.
2. Compare `coding-agent-guide.md` with current task routing, entry points, and verification reality.
3. Compare `documentation-governance.md` with actual active/archive boundaries, naming, and loading rules.
4. Verify `archive/README.md` remains a resolvable index of existing archived workstreams.
5. Inspect existing plans, task lists, `task_plan.md`, `progress.md`, and `findings.md` as active surfaces, not permanent assumptions.
6. Repair inaccurate active references and status descriptions, then verify cross-links and instruction structure.

## Repair Boundaries

- Preserve the canonical source and a valid thin adapter; do not turn them back into a false two-file ambiguity.
- Restore missing required instruction categories, remove leaked template markers or generation prompts, and enforce the selected final line limit without inventing new headings.
- Update stale repository, branch, dependency, entry-doc, routing, verification, active/archive, and loading-order statements.
- Update existing tracking status when it no longer reflects reality.
- Never delete, move, rename, archive, reset, clear, or empty a file in `nhk-upkeep`.
- Never demote a document by removing it from the workspace; only correct whether active docs describe it as an active execution source.
- If archive is appropriate, hand off to `nhk-archive`; do not perform any part of that transition here.

## Conditional Archive Question

Ask whether to archive only when all three are present:

1. one specific, identifiable workstream
2. concrete completion evidence, including its required verification or other declared completion gate
3. specs, plans, tracking files, or other materials that clearly belong to that workstream

If the workstream is ongoing, completion evidence is missing, or related materials are unclear, keep it active and do not ask the archive question. When all three are present, ask whether it should remain active or move to archive. A yes hands off to `nhk-archive`; a no leaves every file in place.

## Delivery

Report the repaired surfaces, verification performed, and whether a workstream met the archive-question gate. If a dependency was adopted, state that it was not installed and its conventions were followed manually for this NHK run.

## Local References

- `../references/validation-scenarios.md`
- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/archive-readme-template.md`
- `../references/dependency-setup.md`
