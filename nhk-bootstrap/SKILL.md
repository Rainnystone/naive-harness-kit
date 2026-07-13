---
name: nhk-bootstrap
description: Use when a workspace needs first-time NHK setup or is missing a required instruction, routing, documentation-governance, or archive surface.
---

# NHK Bootstrap

Establish or repair the minimum NHK foundation. Preserve correct existing surfaces and add or repair only what is missing or explicitly selected; do not rebuild a healthy workspace from scratch.

## Prerequisite

Confirm that `superpowers` and `planning-with-files` are installed, enabled, or explicitly adopted for this NHK run. Adopt is temporary manual authorization, not installation, and must not create a persistent marker. If the user has not selected a mode for a missing dependency, stop.

## Required Foundation

The finished workspace must have:

- one canonical instruction source: standalone `AGENTS.md` or standalone `CLAUDE.md`
- optionally, a thin `CLAUDE.md` adapter importing canonical `AGENTS.md`
- `coding-agent-guide.md`
- `documentation-governance.md`
- `archive/`
- `archive/README.md`

Simple workspaces may keep these surfaces short, but may not omit them.

## Canonical Instruction Decision

A valid thin import is a line whose trimmed content is exactly `@AGENTS.md` or `@./AGENTS.md`, outside fenced code, Markdown blockquotes, and comments.

1. Only `AGENTS.md`: preserve it as canonical. Do not create `CLAUDE.md` unless a thin adapter is already present, needed by the environment, or requested by the user.
2. Only ordinary `CLAUDE.md`: preserve it as standalone canonical.
3. Both plus a valid thin import in `CLAUDE.md`: preserve `AGENTS.md` as canonical and `CLAUDE.md` as the thin adapter; do not ask which is active.
4. Only `CLAUDE.md` plus a valid thin import: ask whether to restore `AGENTS.md` or convert `CLAUDE.md` to standalone. Make only the selected repair.
5. Both without a valid thin import: ask which source should be canonical. Do not merge, delete, migrate, or rewrite either file until the user decides.
6. Neither: use environment and workspace signals. If they remain inconclusive, ask rather than guessing.

An import mentioned only in prose, fenced code, a blockquote, or a comment does not make a thin adapter.

## Build Only Missing Surfaces

Once the canonical source is known:

- adapt the matching instruction template only when the canonical file is missing or materially incomplete
- preserve a valid thin adapter, or create one only when the decision above calls for it
- add or repair `coding-agent-guide.md` from `../references/coding-agent-guide-template.md`
- add or repair `documentation-governance.md` from `../references/documentation-governance-template.md`
- create `archive/` when missing and add or repair `archive/README.md` from `../references/archive-readme-template.md`
- connect the canonical instruction source, companion docs, and archive index with concise, accurate references

Use backticked literal paths for both companion docs. In Claude Code, only a thin adapter may import canonical AGENTS; neither thin nor standalone CLAUDE may `@` import a companion doc.

Never overwrite correct project-specific content merely to match template wording.

## Root Tracking Is Conditional

Do not create root `task_plan.md`, `findings.md`, or `progress.md` merely because bootstrap runs. Create them only when the current work genuinely needs multi-session recovery, an active plan/spec, multiple packets, or explicit progress tracking. The archive foundation is still mandatory in a simple workspace.

## Instruction Template Audit

Use `../references/AGENTS-template.md` or `../references/CLAUDE-template.md` as a generation contract, not a copy target.

- Select simple, medium, or complex deliberately.
- A standalone final file must contain the seven required top-level sections in template order and stay within 100, 125, or 150 lines respectively.
- A thin `CLAUDE.md` must contain a valid import, only necessary Claude-specific notes, and no more than 35 lines; after producing thin mode, do not process standalone blocks.
- Copy `FINAL_VERBATIM` content exactly unless the user approves a change.
- Project-adapt `FINAL_ADAPT`; include `OPTIONAL_BY_COMPLEXITY` only when justified.
- Remove every marker, generation instruction, placeholder, and template-only heading.
- Do not compress away execution, context, worker, approval, testing, or delivery discipline.
- Do not expand project detail past the line budget; route it to the companion docs.
- Keep `coding-agent-guide.md` at or below 80 lines with one Task Routing table using `Task or Symptom`, `Read First`, `Likely Change Surface`, and `Targeted Verification`.
- Keep `documentation-governance.md` at or below 100 lines and limited to document roles, active surfaces, the workspace/document map, lifecycle, naming/loading, and archive invariants.

## Foundation Verification

Before finishing:

- confirm the canonical source and any thin adapter match the topology rules
- confirm both companion docs, `archive/`, and the archive index exist and cross-references resolve
- confirm companion docs meet their 80/100-line limits and CLAUDE does not auto-import them
- confirm generated instruction content meets its selected structure and line limit
- confirm no existing healthy surface was unnecessarily replaced
- if root tracking exists, record the audit there; otherwise report it in the delivery note
- if a dependency was adopted, state: it is not installed; its conventions were followed manually for this NHK run

## Local References

- `../references/validation-scenarios.md`
- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/archive-readme-template.md`
- `../references/dependency-setup.md`
