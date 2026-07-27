---
name: nhk-upkeep
description: Repair NHK drift when an established workspace's instruction, routing, planning, governance, archive index, or tracking descriptions no longer match reality.
---

# NHK Upkeep

Use this skill only after the NHK foundation exists. It repairs active references and state descriptions; it does not bootstrap missing surfaces or perform an archive transition.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue upkeep.

Use the handoff's dependency, instruction, topology, and complete-foundation state as the maintenance input. Do not persist the handoff or repeat the topology decision inside upkeep.

## Maintenance Pass

1. Compare the canonical instruction source and any thin adapter with the live workspace. If its structure needs repair, open only the matching `../references/AGENTS-template.md` or `../references/CLAUDE-template.md`.
2. Compare the single Task Routing table in `coding-agent-guide.md` with current task routes, likely change surfaces, and targeted verification; keep the file at or below 80 lines. Open `../references/coding-agent-guide-template.md` only when this surface needs structural repair.
3. Compare `implementation-planning.md` with the Superpowers-compatible task contract; keep it at or below 80 lines and load it only for plan work. Open `../references/implementation-planning-template.md` only when this surface needs structural repair.
4. Compare `documentation-governance.md` with actual document roles, active surfaces, workspace/document map, lifecycle, naming/loading rules, and archive invariants; keep it at or below 100 lines. Open `../references/documentation-governance-template.md` only when this surface needs structural repair.
5. Verify `archive/README.md` remains a resolvable index of existing archived workstreams. Open `../references/archive-readme-template.md` only when its shape or row contract needs repair.
6. Inspect existing implementation plans, task lists, `task_plan.md`, `progress.md`, and `findings.md` as active surfaces, not permanent assumptions.
7. Repair inaccurate active references and status descriptions, replace any Claude companion `@` import with a literal on-demand path, then verify cross-links and instruction structure.

## Repair Boundaries

- Preserve the canonical source and a valid thin adapter; do not turn them back into a false two-file ambiguity.
- Restore missing required instruction categories, remove leaked template markers or generation prompts, and enforce the selected final line limit without inventing new headings.
- Update stale repository, dependency, routing, verification, active/archive, and loading-order statements.
- Do not recreate separate current-state, packet-routing, packet-checklist, code-map, default-verification, or anti-detour sections in `coding-agent-guide.md`; the routing table owns that job.
- Keep plan sizing in `implementation-planning.md`; do not duplicate its task contract in the routing or governance docs.
- Keep production-code navigation out of `documentation-governance.md`, and keep detailed archive execution in `nhk-archive`.
- Keep stable `implementation-planning.md` active; only completed implementation plans may become archive candidates.
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
