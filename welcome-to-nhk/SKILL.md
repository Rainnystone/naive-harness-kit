---
name: welcome-to-nhk
description: Route NHK work when dependency readiness, instruction topology, foundation state, or lifecycle stage is unresolved.
---

# Welcome To NHK

Use this skill as the first-stop router. It selects `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive`; it does not perform those workflows itself.

## 1. Check Peer Dependencies

Treat `superpowers` and `planning-with-files` as peer dependencies.

- Check whether both are available before inspecting or changing NHK surfaces.
- If either is missing, stop and ask the user to install, enable, or explicitly adopt it.
- Adopt is permission to follow that dependency's conventions manually for this NHK run only. It creates no persistent marker and is not installation.
- Carry adopted-dependency status into any handoff. Whichever skill delivers the result must report that the dependency was not installed and its conventions were followed manually for this NHK run; if this router ends the flow, report it here.
- If the user does not choose a mode, do not continue. Never silently emulate a missing workflow.
- Use `../references/dependency-setup.md` when the user needs the sources or decision boundaries.

## 2. Identify The Canonical Instruction Source

A valid thin import is a line whose trimmed content is exactly `@AGENTS.md` or `@./AGENTS.md`, outside fenced code, Markdown blockquotes, and comments. Mentions in prose, examples, quoted text, code fences, or comments do not count.

Claude `@` imports of `coding-agent-guide.md`, `implementation-planning.md`, or `documentation-governance.md` are not topology signals and are not valid NHK routing. Companion docs must be named by literal path and loaded only when the task requires them.

Apply this order:

1. Only `AGENTS.md` exists: it is canonical.
2. Only an ordinary `CLAUDE.md` exists: it is the standalone canonical source.
3. Both exist and `CLAUDE.md` contains a valid thin import: `AGENTS.md` is canonical and `CLAUDE.md` is its thin adapter. Do not ask which is active.
4. Only `CLAUDE.md` exists and it contains a valid thin import: this is a broken adapter. Ask whether to restore `AGENTS.md` or convert `CLAUDE.md` to standalone.
5. Both exist without a valid thin import: this is real ambiguity. Ask which source should be canonical and do not modify either file.
6. Neither exists: use environment and workspace signals only now. If they do not identify one format clearly, ask the user.

## 3. Check The NHK Foundation

After the canonical source is known, check all five foundation surfaces:

- `coding-agent-guide.md`
- `implementation-planning.md`
- `documentation-governance.md`
- `archive/`
- `archive/README.md`

If any surface is missing or the instruction topology needs the user-approved repair described above, route to `nhk-bootstrap` before considering upkeep or archive.

## 4. Select The Lifecycle Route

Only after the foundation is complete:

- Route to `nhk-archive` when the user explicitly asks to archive a completed workstream or has already clearly confirmed that transition.
- Route to `nhk-upkeep` when instruction, routing, implementation-planning, governance, archive-index, or active tracking descriptions may have drifted.
- If nothing needs setup, repair, or archive handling, report that the foundation is ready and stop.

## Router Handoff

After every decision above is resolved, return one compact handoff with exactly these fields:

- **Dependencies** — the installed, enabled, or current-run adopted state of each peer workflow
- **Instruction** — the canonical source and standalone/thin topology
- **Foundation** — which of the five required surfaces are present or missing
- **Route** — `bootstrap`, `upkeep`, `archive`, or `ready`

The handoff exists only in conversation for the current workspace and current NHK run. Do not write it to a file or reuse it after its dependency state, instruction topology, foundation state, lifecycle intent, or workspace changes. If a human choice remains unresolved, do not emit a complete handoff; stop at that choice.

Hand off only after all four fields are accurate. Do not implement another NHK skill inside this router.

When maintaining or evaluating NHK itself, read `../references/validation-scenarios.md`. Do not load that maintainer reference during ordinary workspace routing.
