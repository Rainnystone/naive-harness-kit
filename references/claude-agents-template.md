# Claude Agents Template

## Purpose

Use this template to create the optional NHK agent definitions for a Claude Code workspace: one file per definition at `.claude/agents/<name>.md`.

`worker-policy.md` maps capability tiers to these definition names. These definitions alone carry the model and effort each tier runs at, because Claude Code sets a worker's effort only through its definition.

## Template Contract

- Offer the definitions only in a Claude Code workspace, meaning one with a canonical or thin `CLAUDE.md`. Create them only after the human agrees; recommend agreeing.
- Their presence records that agreement. Upkeep reconciles existing `nhk-*` definitions with this template and leaves an absent set absent.
- Retired definitions: `nhk-audit` succeeds `nhk-diagnosis`. When reconciling a set that still has it, upkeep creates any missing current definition and reports the retired file for the human to delete; it never deletes or renames one itself. An older `nhk-light` is a current definition and is reconciled like the others.
- Each file is one definition's frontmatter below followed by the Shared Body, and nothing else.
- Keep `model: haiku` for `nhk-light` and `model: opus` for the others, so every definition follows its current family through the alias.
- `nhk-light` needs `haiku` to resolve to Haiku 5.5 or later, the first Haiku with effort. The Anthropic API does; Amazon Bedrock, Google Cloud, Microsoft Foundry, and Claude Platform on AWS resolve it to Haiku 4.5. There, offer `nhk-light` only with the human pinning `ANTHROPIC_DEFAULT_HAIKU_MODEL` to the provider's Haiku 5.5 identifier; otherwise leave it out, and `light` work runs on `nhk-standard`.
- When a set lacks `nhk-light`, upkeep offers it under the same check and adds it only after the human agrees; it never adds `nhk-light` on its own.
- The `effort` values are calibrated once, here, for Haiku 5.5 and the current Opus generation. Recalibrate this file when an alias moves; `worker-policy.md` stays unchanged.
- The top effort level is not an Opus worker effort; it stays with the human-chosen main thread. Only the Haiku definition may use it.
- Keep each `description` a short pointer back to `worker-policy.md` so dispatch follows the policy.
- Source-template hard limit: 80 lines. Never use a Claude `@` import.
- Tell the human that creating the first file in a new `.claude/agents/` directory needs a fresh session before Claude Code discovers it.

## Definitions

### nhk-light

```yaml
---
name: nhk-light
description: NHK light tier worker. Dispatch only as routed by worker-policy.md.
model: haiku
effort: max
---
```

### nhk-standard

```yaml
---
name: nhk-standard
description: NHK standard tier worker. Dispatch only as routed by worker-policy.md.
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
