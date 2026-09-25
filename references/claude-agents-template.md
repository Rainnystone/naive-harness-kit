# Claude Agents Template

## Purpose

Use this template to create the optional NHK agent definitions for a Claude Code workspace: one file per definition at `.claude/agents/<name>.md`.

`worker-policy.md` maps capability tiers to these definition names. These definitions alone carry the model and effort each tier runs at, because Claude Code sets a worker's effort only through its definition.

## Template Contract

- Offer the definitions only in a Claude Code workspace, meaning one with a canonical or thin `CLAUDE.md`. Create them only after the human agrees; recommend agreeing.
- Their presence records that agreement. Upkeep reconciles existing `nhk-*` definitions with this template and leaves an absent set absent.
- Retired definitions: `nhk-audit` succeeds `nhk-diagnosis`, and `nhk-light` has no successor. When reconciling a set that still has them, upkeep creates any missing current definition and reports each retired file for the human to delete; it never deletes or renames one itself.
- Each file is one definition's frontmatter below followed by the Shared Body, and nothing else.
- Keep `model: opus` so every definition follows the current Opus through its alias.
- The `effort` values are calibrated once, here, for the current Opus generation. Recalibrate this file when the Opus alias moves; `worker-policy.md` stays unchanged.
- The top effort level is not a worker effort; it stays with the human-chosen main thread.
- Keep each `description` a short pointer back to `worker-policy.md` so dispatch follows the policy.
- Source-template hard limit: 80 lines. Never use a Claude `@` import.
- Tell the human that creating the first file in a new `.claude/agents/` directory needs a fresh session before Claude Code discovers it.

## Definitions

### nhk-standard

```yaml
---
name: nhk-standard
description: NHK standard worker for the light and standard tiers. Dispatch only as routed by worker-policy.md.
model: opus
effort: medium
---
```

### nhk-deep

```yaml
---
name: nhk-deep
description: NHK deep tier worker. Dispatch only as routed by worker-policy.md.
model: opus
effort: high
---
```

### nhk-audit

```yaml
---
name: nhk-audit
description: NHK read-only audit tier worker. Dispatch only as routed by worker-policy.md.
model: opus
effort: xhigh
disallowedTools: Write, Edit, NotebookEdit
---
```

## Shared Body

```md
You run one NHK packet from a self-contained brief sent by the main thread. Your final message ends your run and becomes your report, so return when the packet's acceptance criteria are met, or when only the main thread or the human can unblock the rest. Lead the report with the outcome, then the verification evidence, then each open item with what blocks it.
```
