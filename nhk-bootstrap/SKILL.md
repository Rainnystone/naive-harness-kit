---
name: nhk-bootstrap
description: Bootstrap an NHK workspace when first-time setup is needed or any required instruction, routing, planning, governance, or workflow-required archive surface is missing.
---

# NHK Bootstrap

Establish or repair the minimum NHK foundation. Preserve correct existing surfaces and add or repair only what is missing or explicitly selected; do not rebuild a healthy workspace from scratch.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue bootstrap.

Use the handoff's workspace workflow, workstream owner, capability state, canonical instruction source, topology, and missing foundation surfaces as the bootstrap input. Do not persist the handoff. After bootstrap changes the foundation, rerun `welcome-to-nhk` before continuing any earlier upkeep or archive intent.

## Required Foundation

The finished workspace must have:

- one canonical instruction source: standalone `AGENTS.md` or standalone `CLAUDE.md`
- optionally, a thin `CLAUDE.md` adapter importing canonical `AGENTS.md`
- `coding-agent-guide.md`
- `implementation-planning.md`
- `worker-policy.md`
- `execution-recovery.md`
- `documentation-governance.md`

Create the archive foundation only when the workspace default is Superpowers. That foundation consists of `archive/` and `archive/README.md`. In a Matt workspace, the first explicitly approved archive creates those surfaces when needed. Preserve existing archive material.

## Build Only Missing Surfaces

Once the canonical source is known:

- adapt the matching instruction template only when the canonical file is missing, materially incomplete, or retains superseded NHK-owned inline policy or recovery rules alongside the new companions
- preserve a valid thin adapter, or create one only when the decision above calls for it
- add or repair `coding-agent-guide.md` from `../references/coding-agent-guide-template.md`
- add or repair `implementation-planning.md` from the workspace default's shape in `../references/implementation-planning-template.md`; the guide points differently owned workstreams to their original records and the matching installed shape
- add or repair `worker-policy.md` from `../references/worker-policy-template.md`
- add or repair `execution-recovery.md` from `../references/execution-recovery-template.md`
- add or repair `documentation-governance.md` from `../references/documentation-governance-template.md`; record exactly one active `Workflow: Matt` or `Workflow: Superpowers` line under Document Roles
- for a Superpowers default, create `archive/` if missing and add or repair `archive/README.md` from `../references/archive-readme-template.md`
- connect the canonical source and companions with concise references, and link any existing archive index
- in a Claude Code workspace (canonical or thin `CLAUDE.md`) without `.claude/agents/nhk-*.md`, offer the optional NHK agent definitions from `../references/claude-agents-template.md`, recommend them, and create them only after the human agrees; they stay outside the required foundation

Use backticked literal paths for all five companion docs. In Claude Code, only a thin adapter may import canonical AGENTS; neither thin nor standalone CLAUDE may `@` import a companion doc.

Never overwrite correct project-specific content merely to match template wording.

When an older workspace has the new companions but still keeps superseded NHK-owned inline model-catalog or recovery-procedure text in its canonical instruction, make a minimal semantic repair: replace only that NHK text with the current explicit companion routes. Preserve correct project facts and human-authorized exceptions.

Reconcile atomic task sizing, planning detail, role-bound implementation/review, worker reuse, review consolidation, and the canonical waiting contract from their owning templates. Preserve declared contract clauses in their required sections so source and generated validation agree; adapt project facts around them. Keep correct facts and explicit human exceptions. Preserve completed and in-flight task identities and progress; never redispatch completed work. Re-evaluate unstarted work against the atomic task contract without resetting acceptance-gap counts.

Preserve an ordinary Codex routing exception using the bounded JSON record in `../references/worker-policy-template.md`, inside `worker-policy.md`'s Codex Routing section. Derive its exact target, path scope, role, preset, and approval reference from a confirmed existing human decision; never invent approval or use a blanket exemption. Keep the normal clauses/catalogs and separate special approvals intact. Follow the worker-policy template migration contract for legacy module-role records. Static acceptance of a record does not authenticate consent. Keep planning fields active as prescribed by the planning template; do not hide them in example fences.

## Configure Matt Only When Needed

When current Matt work needs repository configuration, inspect existing routes. Invoke `setup-matt-pocock-skills` when available; with explicit current-run adoption, follow its setup conventions manually. Reuse an existing tracker and prior user choices. Apply new tracker or domain-layout choices only when the work needs them. Before a remote mutation, establish authority for that specific operation.

- Record tracker navigation in `docs/agents/issue-tracker.md` and domain loading rules in `docs/agents/domain.md` when those capabilities are configured. Add `docs/agents/triage-labels.md` only when the triage skill and configured triage actually use it. Use the native setup templates where applicable.
- Also reconcile existing navigation when setup configuration is already complete. Put the shallow `## Agent skills` navigation in canonical `AGENTS.md` or standalone `CLAUDE.md`. With a thin adapter, override the native setup's preference to edit `CLAUDE.md` and merge existing navigation into canonical `AGENTS.md`. Keep a single block and link only configured routes.
- Create `GLOSSARY.md`, a multi-context `GLOSSARY-MAP.md` only where warranted, and ADR files only when actual terms or decisions call for them. Recognize `CONTEXT.md` or `CONTEXT-MAP.md` as legacy domain docs only when their content confirms that role. Preserve their existing paths absent a separate approved migration.

When a Matt publishing skill needs a ready state but triage is unused, pass the tracker's existing agent-ready mapping, or Matt's default `ready-for-agent`, with its tracker instructions. Keep the triage guide conditional. Create or change a remote label only with authority for that operation.

## Root Tracking Is Conditional

Create root `task_plan.md`, `findings.md`, or `progress.md` only when genuine multi-session recovery, packet coordination, or an explicit request needs them. Apply `planning-with-files` when that capability is needed. Use the workflow's own plan or tracker as the authority for tasks and statuses; use any additional tracking to link to that record and carry distinct recovery context.

## Instruction Template Audit

Superseded NHK-owned orchestration or waiting clauses also trigger the matching canonical template audit and minimal semantic repair.

If bootstrap is creating, structurally repairing, or making the specific semantic policy/recovery migration above, open only the generation contract that matches the handoff's canonical source: `../references/AGENTS-template.md` or `../references/CLAUDE-template.md`. Do not load the other platform template. Do not load an instruction template when only a companion or archive surface is missing and the canonical instruction has no superseded NHK-owned policy or recovery text.

- Select simple, medium, or complex deliberately.
- A standalone final file must contain the seven required top-level sections in template order and stay within 100, 125, or 150 lines respectively. Add the optional shallow Agent skills navigation only as specified by the matching template.
- A thin `CLAUDE.md` must contain a valid import, only necessary Claude-specific notes, and no more than 35 lines; after producing thin mode, do not process standalone blocks.
- Copy `FINAL_VERBATIM` content exactly unless the user approves a change.
- Project-adapt `FINAL_ADAPT`; include `OPTIONAL_BY_COMPLEXITY` only when justified.
- Remove every marker, generation instruction, placeholder, and template-only heading.
- Do not compress away execution, context, worker, approval, testing, or delivery discipline.
- Do not expand project detail past the line budget; route it to the companion docs.
- Keep `coding-agent-guide.md` at or below 80 lines with one Task Routing table using `Task or Symptom`, `Read First`, `Likely Change Surface`, and `Targeted Verification`.
- Keep `implementation-planning.md` at or below 80 lines with `Workflow Compatibility`, `Plan Layers`, `Task Contract`, `Dependencies and Execution`, `Wide Changes`, and `Plan Review` in order.
- Keep `worker-policy.md` at or below 100 lines with its dispatch, review, capability-tier, Codex, and Claude sections in order.
- Keep `execution-recovery.md` at or below 80 lines with its accounting, reassessment, diagnosis, and recovery sections in order.
- Keep `documentation-governance.md` at or below 100 lines and limited to document roles, active surfaces, the workspace/document map, lifecycle, naming/loading, and archive invariants.

## Foundation Verification

Before finishing:

- confirm the canonical source and any thin adapter match the topology rules
- confirm all five companions exist and their cross-references resolve, the workflow marker matches the handoff, and the required Superpowers archive foundation or existing Matt archive links are accurate
- when Matt configuration is in scope, confirm the configured paths and the canonical location of Agent skills navigation
- confirm companion docs meet their 80/80/100/80/100-line limits and CLAUDE does not auto-import them
- confirm generated instruction content meets its selected structure and line limit
- confirm any semantic migration replaced only superseded NHK-owned policy or recovery text and preserved project facts and authorized exceptions
- confirm no existing healthy surface was unnecessarily replaced
- if NHK agent definitions were created, confirm they match their template and tell the human that a new `.claude/agents/` directory needs a fresh session
- if root tracking exists, record the audit there; otherwise report it in the delivery note
- if a dependency was adopted, name the missing skill and report manual use of its conventions for this NHK run
