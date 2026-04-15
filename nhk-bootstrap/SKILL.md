---
name: nhk-bootstrap
description: Use when a workspace needs first-time NHK setup or is missing the required instruction, routing, or documentation-governance surfaces.
---

# NHK Bootstrap

NHK `nhk-bootstrap` establishes the first usable workspace harness. It must leave the workspace with one active instruction file, the mandatory companion docs, and the root archive surface, and it must not guess through instruction-file ambiguity.

## Minimum Outputs

An NHK-managed workspace must finish `nhk-bootstrap` with:

- one active instruction file: `AGENTS.md` or `CLAUDE.md`
- `coding-agent-guide.md`
- `documentation-governance.md`
- `archive/`
- `archive/README.md`

`coding-agent-guide.md`, `documentation-governance.md`, and the root archive surface are mandatory minimum outputs even for simple repositories. Simplicity affects how short they may be, not whether they exist.

## Instruction File Decision

Check the workspace root for `AGENTS.md` and `CLAUDE.md` before creating anything.

1. If exactly one file already exists, preserve it as the active instruction file unless the user explicitly asks to migrate.
2. When exactly one file exists, adapt that file in place if needed. Do not create the other file by default.
3. If both files already exist, stop and ask the user which file is active.
4. If both files exist, do not merge, delete, migrate, or rewrite either file without explicit user direction.
5. Consult environment signals only when neither instruction file exists.
6. Environment signals may include the current coding agent, workspace conventions, or toolchain cues, but they are fallback signals only.
7. If the no-file case is still ambiguous after checking environment signals, ask the user instead of guessing.

## Build The Harness Surfaces

After the active instruction file is known:

- build or adapt the active instruction file from the matching local reference shape
- build or adapt `coding-agent-guide.md` from `../references/coding-agent-guide-template.md`
- build or adapt `documentation-governance.md` from `../references/documentation-governance-template.md`
- create `archive/` and build or adapt `archive/README.md` from `../references/archive-readme-template.md`
- establish the minimum cross-references among the core docs and archive surface so routing and governance stay connected

If `archive/README.md` is created from scratch, it should start with the standard stub shape rather than an empty file.

Treat `documentation-governance.md` as the lifecycle source of truth for:

- active versus archive boundaries
- root tracking activation and reset expectations
- active specs and plans versus archived materials
- naming and loading discipline for documentation surfaces

Do not treat repository simplicity as a reason to skip `coding-agent-guide.md` or `documentation-governance.md`.

## Root Tracking Activation

Root tracking files are conditional, not automatic. Initialize active root tracking files such as `task_plan.md`, `findings.md`, and `progress.md` only when one or more of these conditions hold:

- the work is expected to span multiple sessions
- the work requires active specs or active plans
- the work is likely to involve parallel agents or multiple implementation packets
- the work requires explicit recovery of findings and progress across turns

If none of those conditions hold, do not create root tracking files during `nhk-bootstrap`.

## Template Adaptation Rules

Use the local template files as references, not blind copy targets.

- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/archive-readme-template.md`

Required adaptation rules:

- remove template scaffolding, placeholder prompts, and instructional filler from final workspace docs
- keep verbatim-preserved blocks only where the reference explicitly requires verbatim preservation
- write project-specific routing, governance, and execution context instead of transplanting another workspace's content
- explain which local references were used and what was adapted for this workspace
- do not leave documentation lifecycle rules implied; write them explicitly into the final `documentation-governance.md`

## Local Validation Targets

Use these local references when pressure-checking the workflow:

- `../references/validation-scenarios.md`
- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/archive-readme-template.md`

The `nhk-bootstrap` workflow passes its core ambiguity check only if it preserves an already-existing single instruction file and asks the user rather than guessing when both instruction files already exist.
