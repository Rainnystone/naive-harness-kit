---
name: nhk-upkeep
description: Repair established NHK workspaces after NHK updates or when project instructions, companions, or tracking drift.
---

# NHK Upkeep

Use this skill only after the NHK foundation exists. It reconciles NHK-owned rules with the currently installed references and repairs active project descriptions; it does not bootstrap missing surfaces or perform an archive transition.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue upkeep.

Use the handoff's dependency, instruction, topology, and complete-foundation state as the maintenance input. Do not persist the handoff or repeat the topology decision inside upkeep.

## Maintenance Pass

On every upkeep run, compare NHK-owned rules against the currently installed reference contracts, even when workspace documents look complete and project facts have not changed. Read the matching canonical instruction template, all five companion templates, and the archive-index template through the paths below. Reuse applicable content already read in this context only when it is unchanged. This comparison uses the installed bundle; upkeep does not fetch or install NHK updates.

1. Compare the canonical instruction and thin adapter, if present, against the live workspace and the matching `../references/AGENTS-template.md` or `../references/CLAUDE-template.md`; keep the canonical topology and applicable line budget.
2. Compare the single Task Routing table in `coding-agent-guide.md` against current routes and `../references/coding-agent-guide-template.md`; keep it at or below 80 lines.
3. Compare `implementation-planning.md` against `../references/implementation-planning-template.md`; keep its Superpowers-compatible task contract and 80-line limit.
4. Compare `worker-policy.md` against `../references/worker-policy-template.md`; reconcile dispatch and review permissions within 100 lines.
5. Compare `execution-recovery.md` against `../references/execution-recovery-template.md`; reconcile diagnosis, recovery, and stop rules within 80 lines.
6. Compare `documentation-governance.md` against actual document roles and `../references/documentation-governance-template.md`; keep it at or below 100 lines.
7. Compare `archive/README.md` against existing archived workstreams and `../references/archive-readme-template.md`; keep every index entry resolvable.
8. Inspect existing implementation plans, task lists, `task_plan.md`, `progress.md`, and `findings.md` as active surfaces, not permanent assumptions.
9. Repair inaccurate active references and status descriptions, replace any Claude companion `@` import with a literal on-demand path, then verify cross-links and instruction structure.

Reconcile module sizing, role-bound implementation/review, worker reuse, review consolidation, and the canonical waiting contract from their owning templates. Preserve declared contract clauses in their required sections so source and generated validation agree; adapt project facts around them. Keep correct facts and explicit human exceptions. Updating rules does not automatically regroup a running plan or redispatch completed work; preserve stable task identifiers and progress when reconciling active surfaces.

## Repair Boundaries

- Reconcile only NHK-owned rules. Preserve correct project facts and human-authorized exceptions; surface any conflict requiring a new human decision rather than silently overwriting it.
- Preserve the canonical source and a valid thin adapter; do not turn them back into a false two-file ambiguity.
- Restore missing required instruction categories, remove leaked template markers or generation prompts, and enforce the selected final line limit without inventing new headings.
- Update stale repository, dependency, routing, verification, active/archive, and loading-order statements.
- For an older workspace with new companions, replace only superseded NHK-owned inline policy or recovery text with the current conditional companion routes; preserve correct project facts and human-authorized exceptions.
- Do not recreate separate current-state, packet-routing, packet-checklist, code-map, default-verification, or anti-detour sections in `coding-agent-guide.md`; the routing table owns that job.
- Keep plan sizing in `implementation-planning.md`; do not duplicate its task contract in the routing or governance docs.
- Keep exact worker permissions in `worker-policy.md` and recovery procedure in `execution-recovery.md`; canonical instructions only retain their conditional routes.
- Keep production-code navigation out of `documentation-governance.md`, and keep detailed archive execution in `nhk-archive`.
- Keep stable `implementation-planning.md` active; only completed implementation plans may become archive candidates.
- Keep all five companions active; none is an archive candidate.
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

Complete upkeep only when every compared surface matches the current installed contract or has a recorded human-authorized exception or unresolved conflict. Report the repaired surfaces, preserved exceptions, unresolved conflicts, verification performed, and whether a workstream met the archive-question gate. If a dependency was adopted, state that it was not installed and its conventions were followed manually for this NHK run.
