---
name: welcome-to-nhk
description: Use when starting NHK work in a workspace and needing the first-stop router for dependency readiness, instruction-file state, or lifecycle stage.
---

# Welcome To NHK

NHK `welcome-to-nhk` is the first-stop router. It decides whether the workspace should go to `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive`, and it does not absorb those workflows.

If you are not sure which NHK skill should run first, start here.

## Required Dependencies

Treat `superpowers` and `planning-with-files` as peer dependencies.

- Check whether both are available before routing.
- If either one is missing, stop and ask the user whether to install, enable, or adopt the missing dependency before continuing. Here, `adopt` means manually adopting the required workflow conventions in the current workspace.
- When the user wants help with that dependency decision, use `../references/dependency-setup.md` to explain the repository source and the difference between install, enable, and adopt.
- Do not silently continue, emulate the missing workflow, or invent a substitute process.

## Detection Order

1. Check the peer dependencies first.
2. Check the workspace root for `AGENTS.md` and `CLAUDE.md`.
3. If exactly one exists, preserve that file and treat it as the active instruction file unless the user explicitly asks to migrate.
4. If both exist, treat that as ambiguity and ask the user which file is active. Do not guess, merge, delete, or migrate.
5. Consult environment signals only when neither `AGENTS.md` nor `CLAUDE.md` exists.

Environment signals may include the current coding agent, workspace conventions, and existing toolchain hints, but they are fallback signals only.

## Routing Rules

- Route to `nhk-bootstrap` when NHK is not yet established, mandatory companion docs are missing, or the user is setting up NHK for the first time.
- Route to `nhk-upkeep` when NHK already exists and the active instruction/doc-governance surface needs repair, refresh, or drift correction.
- Route to `nhk-archive` only when the user explicitly asks for archival handling or confirms that the current workstream should move to archive.

After deciding the route, hand off to the target skill. Do not perform `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive` implementation work inside `welcome-to-nhk`.

## Local References

Use local references instead of external copies:

- `../references/validation-scenarios.md`
- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/dependency-setup.md`

These frozen templates are references for the routed workflow, not blind copy targets.
