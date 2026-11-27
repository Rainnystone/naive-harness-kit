---
name: nhk-upkeep
description: Repair established NHK workspaces after NHK updates or when project instructions, companions, or tracking drift.
---

# NHK Upkeep

Use this skill only after the NHK foundation exists. It reconciles NHK-owned rules with the currently installed references and repairs active project descriptions; it does not bootstrap missing surfaces or perform an archive transition.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue upkeep.

Use the handoff's workspace workflow, workstream owner, capability, instruction, topology, and complete-foundation state as the maintenance input. Do not persist the handoff or repeat the topology decision inside upkeep. If a prior route remains pending, get a fresh handoff after changing the workflow marker or foundation; carry any still-applicable approval for the same workstream.

## Maintenance Pass

On every upkeep run, compare NHK-owned rules against the currently installed reference contracts, even when workspace documents look complete and project facts have not changed. Read the matching canonical instruction and five companion templates through the paths below. Read the archive-index template when an index exists and the agent-definition template only when NHK agent definitions exist. Reuse applicable content already read in this context only when it is unchanged. This comparison uses the installed bundle; upkeep does not fetch or install NHK updates.

1. Compare the canonical instruction and thin adapter, if present, against the live workspace and the matching `../references/AGENTS-template.md` or `../references/CLAUDE-template.md`; keep the canonical topology and applicable line budget.
2. Compare the single Task Routing table in `coding-agent-guide.md` against current routes and `../references/coding-agent-guide-template.md`; keep it at or below 80 lines.
3. Compare `implementation-planning.md` against `../references/implementation-planning-template.md`; use the workspace default's final shape and 80-line limit. Check that a differently owned active workstream can still reach its original record and the matching section of the installed template.
4. Compare `worker-policy.md` against `../references/worker-policy-template.md`; reconcile dispatch, review, and tier permissions within 100 lines, following its legacy tier migration.
5. Compare `execution-recovery.md` against `../references/execution-recovery-template.md`; reconcile diagnosis, recovery, and stop rules within 80 lines.
6. Compare `documentation-governance.md` against actual document roles and `../references/documentation-governance-template.md`; keep it at or below 100 lines and record one active `Workflow: Matt` or `Workflow: Superpowers` line under Document Roles.
7. When `archive/README.md` exists, compare it against existing archived workstreams and `../references/archive-readme-template.md`. Repair broken references where evidence identifies the correct destination. Report remote links whose target cannot be read. With a Matt default, leave archive creation to the first explicitly approved archive.
8. When `.claude/agents/nhk-*.md` definitions exist, compare them against `../references/claude-agents-template.md` and reconcile their frontmatter and shared body. Create any missing current definition in that set and report each retired definition the template names for the human to delete. An absent set stays absent; the human declined or was never offered it.
9. Inspect workstream plans, tracker references, and any existing `task_plan.md`, `progress.md`, and `findings.md` relevant to the work. Reconcile descriptions against the current authoritative source.
10. For existing Matt configuration, reconcile only verified tracker, domain, and triage references in `docs/agents/` and the shallow canonical `## Agent skills` section. Merge navigation into canonical `AGENTS.md` when `CLAUDE.md` is thin, or into standalone `CLAUDE.md` when it is canonical. Keep one navigation block and preserve necessary notes in the thin adapter. Confirm legacy `CONTEXT.md` or `CONTEXT-MAP.md` by content and retain existing paths. When the current scope needs missing Matt configuration, use the handoff: invoke `setup-matt-pocock-skills` when available, or follow its setup conventions manually under explicit current-run adoption. Reuse tracker and domain-layout choices, add triage configuration only when in use, and apply the same canonical navigation placement. Obtain authority for any remote mutation.
11. Repair inaccurate active references and status descriptions, replace any Claude companion `@` import with a literal on-demand path, then verify cross-links and instruction structure.

Reconcile atomic task sizing, planning detail, role-bound implementation/review, worker reuse, review consolidation, and the canonical waiting contract from their owning templates. Preserve declared contract clauses in their required sections so source and generated validation agree; adapt project facts around them. Keep correct facts and explicit human exceptions. Preserve completed and in-flight task identities and progress; never redispatch completed work. Re-evaluate unstarted work against the atomic task contract without resetting acceptance-gap counts.

Preserve an ordinary Codex routing exception using the bounded JSON record in `../references/worker-policy-template.md`, inside `worker-policy.md`'s Codex Routing section. Derive its exact target, path scope, role, preset, and approval reference from a confirmed existing human decision; never invent approval or use a blanket exemption. Keep the normal clauses/catalogs and separate special approvals intact. Follow the worker-policy template migration contract for legacy module-role records. Static acceptance of a record does not authenticate consent. Keep planning fields active as prescribed by the planning template; do not hide them in example fences.

## Repair Boundaries

When a Matt publishing skill needs a ready state but triage is unused, pass the tracker's existing agent-ready mapping, or Matt's default `ready-for-agent`, with its tracker instructions. Keep the triage guide conditional. Create or change a remote label only with authority for that operation.

A changed workspace default applies to the next workstream. Preserve the workflow and authoritative task source of each in-flight workstream, including tracker or plan identities, status, verification, and genuine approvals. Reapplying upkeep to unchanged workspace state should cause no further edits. Keep current work usable in its chosen workflow without bulk-converting plans or duplicating task records.

- Reconcile only NHK-owned rules. Preserve correct project facts and human-authorized exceptions; surface any conflict requiring a new human decision rather than silently overwriting it.
- Preserve the canonical source and a valid thin adapter; do not turn them back into a false two-file ambiguity.
- Restore missing required instruction categories, remove leaked template markers or generation prompts, and enforce the selected final line limit without inventing new headings.
- Update stale repository, dependency, routing, verification, active/archive, and loading-order statements.
- For an older workspace with new companions, replace only superseded NHK-owned inline policy or recovery text with the current conditional companion routes; preserve correct project facts and human-authorized exceptions.
- Do not recreate separate current-state, packet-routing, packet-checklist, code-map, default-verification, or anti-detour sections in `coding-agent-guide.md`; the routing table owns that job.
- Keep plan sizing in `implementation-planning.md`; do not duplicate its task contract in the routing or governance docs.
- Keep exact worker permissions in `worker-policy.md` and recovery procedure in `execution-recovery.md`; canonical instructions only retain their conditional routes.
- Keep production-code navigation out of `documentation-governance.md`, and keep detailed archive execution in `nhk-archive`.
- Keep stable `implementation-planning.md` active. Completed, evidenced workstream plans may enter the applicable archive transition.
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

If the workstream is ongoing, completion evidence is missing, or related materials are unclear, keep it active and do not ask the archive question. When all three are present, ask whether to archive unless the human already approved this same transition. A yes hands off to `nhk-archive`; a no leaves every file in place.

## Delivery

Complete upkeep only when every compared surface matches the current installed contract or has a recorded human-authorized exception or unresolved conflict. Report the repaired surfaces, preserved exceptions, unresolved conflicts, verification performed, and whether a workstream met the archive-question gate. If a dependency was adopted, name the missing skill and report manual use of its conventions for this NHK run.
