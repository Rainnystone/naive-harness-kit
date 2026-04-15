# Welcome to NHK: Naive Harness Kit

**English** | [中文](README_CN.md)

NHK is a prompt-first starter kit for people who want a usable agent workspace harness without becoming full-time harness engineers first.

It is intentionally a little humble, a little self-aware, and very practical. The point is not to look clever. The point is to help you get the good tools in place, wire them together sanely, and keep a Codex or Claude Code workspace from turning into a vague little document swamp.

## What NHK Is

NHK helps with four recurring jobs that show up surprisingly fast once you start using coding agents seriously:

- getting the useful workflow tools in place, especially `superpowers` and `planning-with-files`
- lazily but safely initializing the right workspace instruction file for the current agent environment
- keeping `coding-agent-guide.md` and `documentation-governance.md` aligned with reality
- deciding whether a workstream should stay active or move to archive
- doing all of that with explicit prompts instead of opaque hooks

In other words, NHK is not trying to be magic. It is trying to be the slightly fussy friend who says: yes, let's make this easier, but let's also write the rules down so future-you is not stuck deciphering agent vibes.

This kit is for beginners, lazy pragmatists, and anyone who would rather ship than hand-roll a custom agent harness from scratch.

## What Is Included

NHK ships with four focused skills:

- `welcome-to-nhk`: the first-stop router
- `nhk-bootstrap`: first-time workspace setup
- `nhk-upkeep`: day-to-day harness maintenance
- `nhk-archive`: human-confirmed archive transition

It also ships with frozen local references:

- `AGENTS-template.md`
- `CLAUDE-template.md`
- `coding-agent-guide-template.md`
- `documentation-governance-template.md`
- `dependency-setup.md`
- `validation-scenarios.md`

## Documentation Logic

NHK separates human-facing docs from agent-facing docs on purpose:

- `README.md` is the default GitHub landing page for humans
- `README_CN.md` is the Chinese companion for humans
- `AGENTS.md` is for Codex-style agents maintaining this repository
- `CLAUDE.md` is for Claude Code and imports the shared repo instructions
- the four skill folders define actual NHK behavior
- `references/` stores frozen drafting and validation assets used by the skills

This split matters. README files explain what NHK is, how to install it, and how to use it. `AGENTS.md` and `CLAUDE.md` are not tutorials; they tell coding agents how to work on the NHK repository itself without confusing repo maintenance with skill usage.

For an NHK-managed workspace, the expected document system is layered:

| Layer | File(s) | Job |
| --- | --- | --- |
| Instruction layer | `AGENTS.md` or `CLAUDE.md` | stable execution rules, verification discipline, collaboration rules |
| Routing layer | `coding-agent-guide.md` | quick task routing, entry files, packet landing zones, first-pass verification |
| Governance layer | `documentation-governance.md` | active vs archive rules, naming rules, loading discipline, archival transition rules |
| Active work layer | active `specs/`, active `plans/`, optional root `task_plan.md` / `progress.md` / `findings.md` | work in progress only |
| Archive layer | `archive/` or equivalent | completed specs, completed plans, completed tracking files, historical reference only |

NHK is opinionated here on purpose:

- every NHK-managed workspace should have the instruction layer, routing layer, and governance layer
- root tracking files are conditional, not automatic
- active docs and archive docs should not be mixed
- archive transitions require human confirmation

The direct source for the governance layer is `references/documentation-governance-template.md`. NHK does not treat documentation lifecycle as an implicit side effect. It expects those rules to be written down explicitly in the target workspace.

## Dependencies

NHK expects these peer workflow systems:

- [`superpowers`](https://github.com/obra/superpowers): process discipline, skill-first routing, brainstorm/spec/plan flow
- [`planning-with-files`](https://github.com/othmanadi/planning-with-files): persistent task tracking, recovery, and continuity

The pairing matters.

`superpowers` is useful because it gives agent work an actual shape instead of a vague "just keep going" spiral. It helps the model route work, choose the right workflow, and avoid improvising its own grand theory every twenty minutes.

`planning-with-files` pairs well with that because Codex and Claude Code are both a bit fuzzy about long-lived working memory in practice. External tracking files are not glamorous, but they are much better than hoping the model remembers which thread is still active, what has already been verified, or whether a half-finished workstream was supposed to stay live.

Together they give NHK a steadier foundation:
- `superpowers` gives the process shape
- `planning-with-files` gives the memory somewhere reliable to live outside the model
- NHK uses both to make `AGENTS.md` / `CLAUDE.md` setup, daily upkeep, and archive decisions less ad hoc

If one of them is missing, NHK should pause and ask whether you want to install it, enable it, or just adopt its conventions manually. That decision is described in [`references/dependency-setup.md`](references/dependency-setup.md).

## Installation

NHK is a file-based skill bundle. There is nothing to compile.

1. Copy the `nhk/` directory into the local skill collection used by your agent environment.
2. Preserve the directory structure exactly, especially `references/` and each skill folder.
3. Make sure `superpowers` and `planning-with-files` are available, or be prepared to adopt their conventions manually.
4. In the target workspace, start with `welcome-to-nhk` so NHK can lazily initialize `AGENTS.md` or `CLAUDE.md` without guessing recklessly.

If you are installing NHK into a new environment and are not sure whether the dependencies are already present, that is normal. NHK is designed to stop and ask before pretending everything is ready.

## How To Use It

The shortest path is:

1. Start with `welcome-to-nhk`.
2. Let it decide whether the workspace needs `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive`.
3. Use `nhk-bootstrap` to create or adapt the workspace instruction file plus the two mandatory companion docs.
4. Use `nhk-upkeep` after normal delivery cycles to repair drift and ask whether a workstream should remain active.
5. Use `nhk-archive` only after the human clearly confirms that one workstream is done and should move to archive.

If you do not know where to begin, NHK is opinionated on purpose: begin at `welcome-to-nhk` and let the router be the adult in the room.

## Codex And Claude Code

NHK is designed to work with both:

- Codex-oriented workspaces usually center on `AGENTS.md`
- Claude Code workspaces usually center on `CLAUDE.md`

NHK does not guess recklessly. If a workspace already has one of those files, it preserves it. If it has both, NHK asks the human which one is active instead of playing philosopher-king.

## Repo Maintenance

This repository itself includes both `AGENTS.md` and `CLAUDE.md`.

The intent is:

- `AGENTS.md` is the shared repo maintenance contract for coding agents
- `CLAUDE.md` imports `AGENTS.md` and adds only Claude-specific glue

That keeps the human-facing README separate from the agent-facing working rules, which is the least dramatic arrangement and therefore usually the best one.
