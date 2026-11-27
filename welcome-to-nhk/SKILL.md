---
name: welcome-to-nhk
description: Route NHK work when dependency readiness, instruction topology, foundation state, or lifecycle stage is unresolved.
---

# Welcome To NHK

Use this skill as the first-stop router. It selects `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive`; it does not perform those workflows itself.

## 1. Identify The Canonical Instruction Source

A valid thin import is a line whose trimmed content is exactly `@AGENTS.md` or `@./AGENTS.md`, outside fenced code, Markdown blockquotes, and comments. Mentions in prose, examples, quoted text, code fences, or comments do not count.

Claude `@` imports of any companion doc are not topology signals and are not valid NHK routing. Companion docs must be named by literal path and loaded only when the task requires them.

Apply this order:

1. Only `AGENTS.md` exists: it is canonical.
2. Only an ordinary `CLAUDE.md` exists: it is the standalone canonical source.
3. Both exist and `CLAUDE.md` contains a valid thin import: `AGENTS.md` is canonical and `CLAUDE.md` is its thin adapter. Do not ask which is active.
4. Only `CLAUDE.md` exists and it contains a valid thin import: this is a broken adapter. Ask whether to restore `AGENTS.md` or convert `CLAUDE.md` to standalone.
5. Both exist without a valid thin import: this is real ambiguity. Ask which source should be canonical and do not modify either file.
6. Neither exists: use environment and workspace signals only now. If they do not identify one format clearly, ask the user.

## 2. Identify The Workspace Default And Workstream Owner

First inspect `documentation-governance.md`, the canonical instruction, and existing workstream evidence. One active line whose trimmed text is `Workflow: Matt` or `Workflow: Superpowers` under governance's Document Roles records the workspace default. Ignore examples in fences, blockquotes, and comments. Correct malformed or duplicate markers using a confirmed choice or unambiguous existing evidence. Ask only when the choice remains unresolved. Honor an explicit change of default for the next workstream.

- For a workspace without a recorded default, continue a clearly established workflow. Treat configured Matt tracker and domain routes, Matt specs or tickets in their actual tracker, and existing Superpowers specs or plans as evidence when their content confirms how work is run. A glossary by itself does not identify the workflow. Installed skills, a directory name, and generic tracking files alone do not establish a choice.
- For a new workspace without an established workflow, recommend Matt. Use a clear existing user choice when available. Ask once if a choice is needed, including when both workflows are plausible and prior evidence does not identify a default. Bootstrap or upkeep records the resolved default in `documentation-governance.md`.
- If a workstream is already active, keep the workflow that owns its plan, task state, and completion evidence. Resolve ownership from the actual records or, if conflicting, ask for the one authoritative source. Use the workspace default for new workstreams. In a mixed workstream, one workflow owns implementation and task tracking. A Matt glossary or supplemental skill can serve a Superpowers implementation without taking over task ownership.

## 3. Check The Foundation And Select The Lifecycle Route

Check the five stable companions:

- `coding-agent-guide.md`
- `implementation-planning.md`
- `worker-policy.md`
- `execution-recovery.md`
- `documentation-governance.md`

For a Superpowers workspace default, also require `archive/` and `archive/README.md` as the legacy archive foundation. With a Matt default, an absent archive directory or index is normal until the first explicitly approved archive. Record any existing archive surfaces in the handoff.

For a read-only archive question, report any missing prerequisite without running repairs. Select the route in this order:

1. Route to `nhk-bootstrap` when the canonical instruction or a required foundation surface is missing or needs the approved topology repair. Complete bootstrap and reroute any outstanding intent.
2. Route to `nhk-upkeep` to record a newly resolved or changed workspace default or repair its marker in otherwise complete governance. Preserve any explicit archive approval for the named workstream and reroute that intent after the marker is recorded.
3. Route to `nhk-archive` when the user asks about archive readiness for a named workstream, approves its archive, or asks to verify or retry its archive. A readiness or verification request is read-only.
4. Route to `nhk-upkeep` when the user requests upkeep, after an NHK update needs workspace reconciliation, when current NHK work requires repository setup for Matt in an otherwise complete workspace, or when workspace descriptions or existing archive links may have drifted.
5. Otherwise, select `ready` and report the foundation status.

## 4. Check Capability Readiness

Check only capabilities required by the selected route and workstream. Use the selected workflow's actual skills for workflow actions. Matt setup or tracker capabilities apply when their work is in scope. Superpowers planning or execution capabilities apply when their work is in scope. `planning-with-files` applies only when the current work needs its file-based tracking and the authoritative records do not already cover that need. NHK-only document maintenance and archive retrieval do not require unrelated authoring or execution skills. Require tracker access for archive only when completion or identity evidence must be retrieved from it. When that evidence and a canonical URL are already confirmed, limited remote access is reported during archive verification.

- Verify a required skill can be invoked in the current session through native discovery or an explicitly invokable installed entrypoint. Finding a folder, plugin, or cached file alone does not establish availability.
- If a required capability is missing, use `../references/dependency-setup.md` and ask for install, enable, or explicit current-run adoption, as applicable. If the user has not chosen, stop that route at the missing capability.
- Adoption permits manual conventions for this NHK run only. Carry the adopted state in the handoff and have the delivering skill report it as manual use of a missing dependency. Record the workspace workflow separately from capability readiness. Never persist adoption or treat it as installation.

## Router Handoff

After every decision above is resolved, return one compact handoff with exactly these fields:

- **Workflow** — the workspace default and the current workstream owner if different
- **Dependencies** — each required capability and its available, enabled, or current-run adopted state
- **Instruction** — the canonical source and standalone/thin topology
- **Foundation** — required surfaces present or missing and the state of the archive surfaces
- **Route** — `bootstrap`, `upkeep`, `archive`, or `ready`

The handoff exists only in conversation for the current workspace and current NHK run. Do not write it to a file or reuse it after its workflow selection, capability state, instruction topology, foundation state, lifecycle intent, or workspace changes. If a human choice remains unresolved, do not emit a complete handoff; stop at that choice.

Hand off only after all five fields are accurate. Do not implement another NHK skill inside this router.

When maintaining or evaluating NHK itself, read `../references/validation-scenarios.md`. Do not load that maintainer reference during ordinary workspace routing.
