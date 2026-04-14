# Coding Agent Guide Template

## What This Guide Is For

This file is a task-routing and entry-point guide for coding agents who are new to the workspace.

Its job is to help a manager thread or subagent answer these questions quickly:
- what should I read first
- which area does this task belong to
- where should the first implementation packet land
- what verification should I run first

This file is not a replacement for the workspace instruction file such as `AGENTS.md` or `CLAUDE.md`.
This file is not a full architecture spec.
This file is not a changelog, roadmap, or archive summary.

Use this file to route work quickly.
Use deeper docs such as codemaps, active specs, and active plans only when this guide is not enough.

Template usage rules:
- This file is a template, not a final `coding-agent-guide.md`.
- Instructional text such as `Fill in`, `Document`, `Suggested`, `Recommended reference`, and similar template guidance should not remain in the final project `coding-agent-guide.md`.
- The final project `coding-agent-guide.md` should be concise, route-oriented, and project-specific.
- If a section becomes long-form explanation, move the detail into companion docs and leave only the routing summary here.
- In NHK-managed workspaces, this file is mandatory even for simple projects.

## Relationship To Other Docs

Document this boundary clearly in the final project guide:

- The workspace instruction file, such as `AGENTS.md` or `CLAUDE.md`, defines stable execution rules, verification discipline, and collaboration rules.
- `coding-agent-guide.md` defines quick task routing, entry files, packet landing zones, and first-pass verification.
- `documentation-governance.md` defines documentation lifecycle, active/archive boundaries, naming rules, archival rules, and loading discipline.
- `docs/codemaps/` or equivalent explain deeper module relationships when routing alone is not enough.
- active `specs/` and `plans/` describe work that is still in progress.
- `archive/` stores completed plans, completed specs, and completed tracking records.

Recommended reference:
- For `task_plan.md`, `findings.md`, and `progress.md`, refer to `$planning-with-files-zh`.
- For active `specs/` and `plans/` workflow conventions, refer to `$using-superpowers`.

## Suggested Sections For The Final Guide

The final project `coding-agent-guide.md` should usually contain the following sections.

### 1. What This Guide Is For

Write a short definition of:
- what this guide helps an agent do
- when an agent should read it
- what it does not try to cover

Keep this short. Its purpose is orientation.

### 2. First Read Order

List the first-pass reading order for a new coding agent.

Include:
- the workspace instruction file such as `AGENTS.md` or `CLAUDE.md`
- this `coding-agent-guide.md`
- `documentation-governance.md`
- current active tracking files
- active codemaps if needed
- any active plan/spec entry points if the project depends on them

Also document:
- which historical docs are optional follow-up reading
- which deeper docs should only be loaded when the first pass is insufficient

This section should answer: what do I read first, in what order, and why.

### 3. Current Execution State

Document the current execution state of the workspace.

Examples:
- which previous phases or initiatives are already complete and archived
- what the current active tracking surface is
- whether the current workstream is still active or already human-confirmed for archival
- whether any previously important docs are no longer active execution entry points

This section exists to stop agents from treating old plans as active work.

### 4. Task Routing

Provide a routing table for common task types.

Recommended shape:

| Task Type | Read Here First |
| --- | --- |
| `<task type>` | `<paths>` |
| `<task type>` | `<paths>` |

Write task categories from the perspective of incoming work, not from the perspective of directory names.

Good examples:
- a page or route behavior problem
- persistence or reload inconsistency
- background worker or sidecar behavior
- package creation or import flow
- API boundary issue

This section should answer: for this kind of problem, where do I look first.

### 5. High-Frequency Packet Routing

For frequent bug classes or feature areas, document where the first implementation packet should land.

Recommended shape:

| Symptom / Goal | First Packet Owned Files | Default Verification | Parallel Hint |
| --- | --- | --- | --- |
| `<symptom>` | `<files>` | `<command>` | `<note>` |

This section should answer:
- what files should the first packet own
- what is the default targeted verification
- is the work likely serial or parallel-safe

Keep this practical. It should help packet planning immediately.

### 6. Implementation Packet Checklist

Document what a valid implementation packet must declare in this project.

Recommended checklist:
- `Packet Goal`
- `Owned Files`
- `Verification`
- `Parallel?`
- `Reviewer Focus`

If the project has stronger packet rules, summarize them here and point to the workspace instruction file, such as `AGENTS.md` or `CLAUDE.md`, for the stable execution discipline.

This section should answer: what must be clear before dispatch or implementation begins.

### 7. Quick File Map

Provide a compact file and directory map for the highest-value entry points only.

Use a lightweight tree or grouped list.
Do not try to mirror the whole repository.

Include:
- top-level docs and routing files
- major source roots
- persistence, runtime, frontend, backend, or worker entry areas
- archive and tooling locations when relevant

This section should answer: what are the main entry points in this repository.

### 8. Search Hints

If the project is large enough to justify it, provide high-value `rg` searches.

Only include searches that materially reduce blind directory browsing.
Do not dump every possible keyword.

This section should answer: what searches help a new agent find the right area quickly.

### 9. Key Architectural Boundaries

Summarize the architectural boundaries that most often affect routing and implementation safety.

Recommended shape:

| Boundary | Rule |
| --- | --- |
| `<boundary>` | `<operational rule>` |

Examples may include:
- content vs system logic
- UI vs persistence writes
- authoring state vs runtime state
- server-owned creation vs browser-owned editing
- packet boundaries that should not be mixed

Keep this section short and operational.
If it starts turning into a full architecture writeup, move the detail into codemaps.

### 10. Default Verification

Document the default verification baseline for the project.

Split it into:
- minimum verification for common production-path changes
- extra verification for boundary-sensitive changes
- targeted suites for frequent task classes

This section should answer:
- what should I run by default
- what should I run for this kind of change
- what targeted command lets me iterate quickly

### 11. Anti-Detour Advice

Capture the most valuable routing and execution advice that helps agents avoid common mistakes.

Examples:
- which surface to inspect first for UX issues
- when to start with persistence/state rather than UI
- when archive should be consulted
- how to avoid mixing multiple surfaces into one packet too early

This section should answer: what mistakes should a new agent avoid in this workspace.

## Writing Principles

The final project `coding-agent-guide.md` should follow these principles:

- Optimize for first-pass routing, not completeness.
- Prefer tables and compact lists over long prose.
- Write from task type to code entry, not from directory to description.
- Keep architecture notes short and operational.
- Prefer entry files and first-hop directories over exhaustive module inventories.
- If a section grows too large, split detail into `docs/codemaps/` or another companion doc.
- Keep documentation lifecycle rules in `documentation-governance.md` or an equivalent dedicated doc rather than expanding them here.

## Companion Doc Guidance

If the project is simple:
- the workspace instruction file, `coding-agent-guide.md`, and `documentation-governance.md` should still exist.
- `coding-agent-guide.md` can stay very short.

If the project is medium complexity:
- add task routing
- add packet routing
- add default verification

If the project is complex:
- maintain `documentation-governance.md` or an equivalent dedicated doc
- maintain `docs/codemaps/` or equivalent deeper maps
- maintain active `specs/` and `plans/`
- maintain active root tracking files if the workflow requires them
- archive completed plans, specs, and tracking records together

Do not let this guide become a second architecture manual.
Its job is to shorten the path from task description to correct first action.
