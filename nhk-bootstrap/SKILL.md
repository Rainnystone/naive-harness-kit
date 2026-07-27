---
name: nhk-bootstrap
description: Bootstrap an NHK workspace when first-time setup is needed or any required instruction, routing, planning, governance, or archive surface is missing.
---

# NHK Bootstrap

Establish or repair the minimum NHK foundation. Preserve correct existing surfaces and add or repair only what is missing or explicitly selected; do not rebuild a healthy workspace from scratch.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue bootstrap.

Use the handoff's dependency state, canonical instruction source, topology, and missing foundation surfaces as the bootstrap input. Do not persist the handoff. After bootstrap changes the foundation, rerun `welcome-to-nhk` before continuing any earlier upkeep or archive intent.

## Required Foundation

The finished workspace must have:

- one canonical instruction source: standalone `AGENTS.md` or standalone `CLAUDE.md`
- optionally, a thin `CLAUDE.md` adapter importing canonical `AGENTS.md`
- `coding-agent-guide.md`
- `implementation-planning.md`
- `documentation-governance.md`
- `archive/`
- `archive/README.md`

Simple workspaces may keep these surfaces short, but may not omit them.

## Build Only Missing Surfaces

Once the canonical source is known:

- adapt the matching instruction template only when the canonical file is missing or materially incomplete
- preserve a valid thin adapter, or create one only when the decision above calls for it
- add or repair `coding-agent-guide.md` from `../references/coding-agent-guide-template.md`
- add or repair `implementation-planning.md` from `../references/implementation-planning-template.md`
- add or repair `documentation-governance.md` from `../references/documentation-governance-template.md`
- create `archive/` when missing and add or repair `archive/README.md` from `../references/archive-readme-template.md`
- connect the canonical instruction source, companion docs, and archive index with concise, accurate references

Use backticked literal paths for all three companion docs. In Claude Code, only a thin adapter may import canonical AGENTS; neither thin nor standalone CLAUDE may `@` import a companion doc.

Never overwrite correct project-specific content merely to match template wording.

## Root Tracking Is Conditional

Do not create root `task_plan.md`, `findings.md`, or `progress.md` merely because bootstrap runs. Create them only when the current work genuinely needs multi-session recovery, an active plan/spec, multiple packets, or explicit progress tracking. The archive foundation is still mandatory in a simple workspace.

## Instruction Template Audit

If bootstrap is creating or structurally repairing the instruction surface, open only the generation contract that matches the handoff's canonical source: `../references/AGENTS-template.md` or `../references/CLAUDE-template.md`. Do not load the other platform template. Do not load an instruction template when only a companion or archive surface is missing.

- Select simple, medium, or complex deliberately.
- A standalone final file must contain the seven required top-level sections in template order and stay within 100, 125, or 150 lines respectively.
- A thin `CLAUDE.md` must contain a valid import, only necessary Claude-specific notes, and no more than 35 lines; after producing thin mode, do not process standalone blocks.
- Copy `FINAL_VERBATIM` content exactly unless the user approves a change.
- Project-adapt `FINAL_ADAPT`; include `OPTIONAL_BY_COMPLEXITY` only when justified.
- Remove every marker, generation instruction, placeholder, and template-only heading.
- Do not compress away execution, context, worker, approval, testing, or delivery discipline.
- Do not expand project detail past the line budget; route it to the companion docs.
- Keep `coding-agent-guide.md` at or below 80 lines with one Task Routing table using `Task or Symptom`, `Read First`, `Likely Change Surface`, and `Targeted Verification`.
- Keep `implementation-planning.md` at or below 80 lines with `Workflow Compatibility`, `Plan Layers`, `Task Contract`, `Dependencies and Execution`, `Wide Changes`, and `Plan Review` in order.
- Keep `documentation-governance.md` at or below 100 lines and limited to document roles, active surfaces, the workspace/document map, lifecycle, naming/loading, and archive invariants.

## Foundation Verification

Before finishing:

- confirm the canonical source and any thin adapter match the topology rules
- confirm all three companion docs, `archive/`, and the archive index exist and cross-references resolve
- confirm companion docs meet their 80/80/100-line limits and CLAUDE does not auto-import them
- confirm generated instruction content meets its selected structure and line limit
- confirm no existing healthy surface was unnecessarily replaced
- if root tracking exists, record the audit there; otherwise report it in the delivery note
- if a dependency was adopted, state: it is not installed; its conventions were followed manually for this NHK run
