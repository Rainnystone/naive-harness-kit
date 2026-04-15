# Documentation Governance Template

## What This Document Is For

This document defines workspace-level documentation governance.

Its job is to make these boundaries explicit:
- what counts as active documentation
- what counts as archived documentation
- where active planning and tracking files live
- when documents may move into archive
- how active and archived materials should be named
- what agents should read first and what they should avoid loading unless needed

This file is not a task-routing guide.
This file is not a full architecture spec.
This file is not a changelog.

Template usage rules:
- This file is a template, not a final `documentation-governance.md`.
- Instructional text such as `Document`, `Recommended`, `Suggested`, and similar template guidance should not remain in the final project file.
- The final project file should define the real workspace rules clearly and operationally.

## Relationship To Other Docs

Document this boundary clearly in the final project file:

- The workspace instruction file, such as `AGENTS.md` or `CLAUDE.md`, defines stable execution rules, verification rules, and collaboration discipline.
- `coding-agent-guide.md` defines quick task routing, packet landing zones, and first-pass verification.
- `documentation-governance.md` defines documentation lifecycle, active/archive boundaries, naming rules, and loading discipline.
- `docs/codemaps/` or equivalent provide deeper module and system structure only when routing docs are insufficient.
- active `specs/` and `plans/` document work still in progress.
- `archive/` stores completed or historical documentation that is no longer an active execution source.

Recommended reference:
- For `specs/` and `plans/` naming conventions, refer to `$using-superpowers`.

## Core Governance Rules

The final project file should define rules equivalent to the following.

### 1. Active and Archived Documentation Must Be Kept Separate

- Active documentation and archived documentation must not be mixed in the same working area.
- Active root tracking files should contain active work only.
- Active spec and plan directories should contain active work only.
- Archived materials should move into a dedicated archive area.

### 2. Archive Is Not An Active Execution Source

- Agents should prefer active docs first.
- Archive should be read only when historical context is actually needed.
- Archived materials are reference records, not default execution entry points.

### 3. Archival Is Never Automatic

- Do not archive active docs automatically.
- Do not assume a workstream is finished just because implementation appears complete.
- Before archiving any active plan, spec, `task_plan.md`, `progress.md`, or `findings.md`, the agent must explicitly ask the human whether the work is truly complete and ready to archive.
- If the human does not confirm completion, leave the materials in the active area.

This rule is important. Humans may consider a workstream still active even when an implementation slice appears done.

### 4. Completed Tracking Files Must Archive Together With Their Related Work

- If a workstream is confirmed complete, archive its tracking files together with the corresponding completed specs and plans.
- Do not archive plans without the related tracking files.
- Do not archive tracking files without the related plans/specs unless the project explicitly documents that exception.

### 5. Active Root Tracking Files May Be Reset Only After Human-Approved Archival

- Root-level `task_plan.md`, `progress.md`, and `findings.md` are active tracking files only.
- They may be reset or cleared only after the related work has been explicitly confirmed complete by the human and archived appropriately.
- Do not clear active tracking files early just to reduce clutter.

## Active Documentation Surfaces

Document the active documentation surfaces for the real project.

Typical examples:
- root `task_plan.md`
- root `progress.md`
- root `findings.md`
- active `docs/specs/`
- active `docs/plans/`
- active codemaps or routing docs

For each active surface, document:
- what it is for
- what kind of content is allowed there
- what kind of content should not remain there after completion

Recommended reference:
- For root tracking files such as `task_plan.md`, `progress.md`, and `findings.md`, refer to `$planning-with-files-zh`.

## Key Paths and Document Map

Document the highest-value workspace paths that agents need in order to find the active document system and major execution surfaces.

Recommended shape:

| What | Where |
| --- | --- |
| Workspace instruction file | `...` |
| Routing guide | `...` |
| Documentation governance | `...` |
| Active specs | `...` |
| Active plans | `...` |
| Root tracking files | `...` |
| Codemaps | `...` |
| Archive | `...` |

Rules:
- In simple workspaces, this map may be very short.
- In complex workspaces, prefer keeping the full key-path and document-surface inventory here instead of expanding `AGENTS.md` or `CLAUDE.md`.
- Keep the emphasis on document surfaces, active versus archived locations, and the paths that affect loading discipline and CLI retrieval.
- Leave code entry maps and production-file navigation to `coding-agent-guide.md`.

## Archive Structure

Document the archive structure for the real project.

At minimum, define:
- where completed specs go
- where completed plans go
- where completed tracking files go
- whether there are special archive areas for recovery snapshots, tracks, or legacy documentation

If the project has multiple archive categories, document the difference between them.

Good examples:
- completed specs and plans
- archived root tracking snapshots
- legacy design materials
- superseded recovery records

## Naming Rules

The final project file should define naming rules clearly.

### 1. Active Specs and Plans

- Active specs and plans should follow a consistent naming scheme.
- The naming scheme should make active work easy to sort and scan from the CLI.
- For spec and plan naming conventions, refer to `$using-superpowers`.

### 2. Archived Tracking Files Must Be Renamed

- Archived copies of `task_plan.md`, `progress.md`, and `findings.md` must not keep the same generic filenames in archive collections where many workstreams accumulate.
- Rename archived tracking files to include workstream identity so CLI search results remain usable.

Recommended examples:
- `archive-task-plan.md`
- `archive-progress.md`
- `archive-findings.md`

If the archive layout groups files by workstream directory, the project may choose a similarly clear naming pattern, but the names must still avoid producing large numbers of indistinguishable generic results in CLI workflows.

### 3. Archived Workstream Containers Should Be Distinguishable

If the project archives by workstream folder, the folder name should make the workstream easy to identify.

Good examples:
- date + topic
- date + initiative name
- date + implementation track

The goal is simple CLI retrieval, not aesthetic naming.

## Read Order and Loading Discipline

Document the loading discipline for the real project.

At minimum, define:
- what active docs should be read first
- when active tracking files must be read
- when codemaps should be loaded
- when archive may be consulted
- what not to load by default

Recommended rules to adapt:
- Start with active execution docs first.
- Load archive only when current docs are insufficient.
- Do not load historical specs or archives just because they exist.
- Keep loading scoped to the task at hand.

## Transition Rules

Document how a workstream moves from active to archived state.

The final project file should make the transition explicit:

1. Work reaches an apparent completion point.
2. Agent asks the human whether the workstream is actually complete and ready to archive.
3. Only after explicit human confirmation:
   - archive completed specs and plans
   - archive related tracking files
   - reset or clear active root tracking files if appropriate
4. Update any routing or governance docs if the active surface has changed.

If the human says the work is not complete:
- keep the workstream active
- do not archive
- do not clear root tracking files

## Suggested Sections For The Final File

The final project `documentation-governance.md` should usually contain these sections:

1. What This Document Is For
2. Relationship To Other Docs
3. Active vs Archive Rules
4. Active Documentation Surfaces
5. Key Paths and Document Map
6. Archive Structure
7. Naming Rules
8. Read Order and Loading Discipline
9. Transition Rules
10. Optional Project-Specific Exceptions

## Writing Principles

The final project file should follow these principles:

- Keep the rules operational and unambiguous.
- Separate lifecycle rules from routing guidance.
- Prefer explicit naming and storage rules over vague guidance.
- Treat archive as a deliberate human-approved state, not an automatic cleanup mechanism.
- Optimize for CLI discoverability and low-friction retrieval.
- If a rule affects searchability, naming, or context loading, write it explicitly.
- In complex workspaces, absorb file-map and document-surface detail here rather than allowing the workspace instruction file to grow past its line budget.
