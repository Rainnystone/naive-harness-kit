# Worker Policy Template

## Purpose

Use this template to create `worker-policy.md`, the on-demand dispatch and review contract for Codex and Claude workers.

This companion owns worker configuration and orchestration detail. Canonical startup instructions keep only the conditional route to this file.

## Template Contract

- Final file hard limit: 100 lines. Source-template hard limit: 140 lines. There is no minimum.
- Replace template guidance with the rules below and remove every prompt or placeholder.
- Keep common dispatch, review, and tier rules together; read only those sections and the current platform section for an orchestration run.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import.
- Preserve explicit human budgets and authorizations. Availability does not expand capability authority.

- Capability Tiers defines every tier's permissions once. Platform sections only map tiers to configurations: Codex presets live only in its tier catalog, Claude definition names only in its tier mapping.

Legacy tier migration: replace Codex Band 1-3 routes, former Claude band routes, and any GPT-6 Astra max permission with the current tier rules. Keep an exception record only when its preset is the current `light`, `standard`, or `deep` preset and its role remains permitted for that tier; otherwise record an unresolved conflict and request a human decision.

Legacy routing migration: map `module-implementation` to `task-implementation` and `initial-module-review` to `initial-task-review` only when the record still identifies the same single task, scope, and confirmed approval. Preserve its target, scope, preset, and approval evidence. If a former module splits into several tasks or the mapping is ambiguous, record an unresolved conflict and request a human decision; never copy its authorization across the new tasks. These migrations are generation guidance, not extra runtime routes.

Optional exception illustration (generation guidance, not an actual approval): after confirming an existing decision, replace this synthetic record with its real target, scope, role, preset, and evidence. Omit records when no such decision exists.

```md
- Human routing exception: {"target":"billing-task","scope":"src/billing/","role":"task-implementation","preset":"GPT-6 Luna max","approval":"decisions/billing.md#luna-route"}
```

The record must be one complete JSON object with unique keys and no trailing prose. Use a stable target identifier of up to 80 letters/digits/underscores/hyphens; literal path components may also contain spaces and dots. Unicode names are supported. Keep one record per target/scope/role, reject blanket targets (`all`, `any`, `global`, `default`, `current`, or their prefixed forms; also bare `project`, `workspace`, or `session`), and retain all normal clauses and catalogs.

## Required Final Shape

Start with `# Worker Policy`, then use exactly these second-level headings in order.

### Dispatch Contract

- In SDD, start a fresh implementer context for each atomic task or qualifying mechanical batch; preserve the chosen native workflow when SDD is not selected.
- Low-risk implementation requires clear behavior and interfaces, an established approach, reliable verification, and bounded local impact. Security, data integrity, or hidden cross-task risks require a judgment role even when the code is short.
- Optimize total delivery cost across planning, context handoff, implementation, review, and rework; do not impose model-use quotas.
- Choose capability from the remaining difficulty and impact; architecture labels and fix rounds 4-5 do not automatically select a stronger tier.
- Authorization comes from the allowed tier for the packet, not the main thread's current model or effort. Explicit user budgets still bind.
- Select an explicitly runtime-supported model and effort; never inherit a top preset silently.
- Prefer the original implementer for ordinary fixes and the original independent reviewer for scoped re-review. A lower-cost permission never requires changing worker or model.
- Use a new cheaper worker only when a self-contained repair handoff makes total overhead worthwhile; batch suitable findings into one repair packet.
- Handoff uses the task brief, report, and fixed diff. State objective, scope, read/write authority, acceptance, verification, forbidden actions, expected return, selected configuration, and binding interfaces and constraints.
- Recursive delegation needs separate human authorization for a named packet.
- Keep subagent-driven implementers sequential. Parallelize read-only work only when ownership, state, artifacts, services, and verification resources are independent.
- Check runtime progress and lifecycle. A timeout alone is not a blocker and does not require a nonexistent close tool.
- The main thread owns integration, cross-task verification, recovery decisions, and the final result.

### Review Gates

- In SDD, every atomic task or qualifying mechanical batch gets one independent read-only reviewer with separate spec-compliance and task-quality verdicts. Both must pass; self-review is not a substitute.
- Internal task steps do not dispatch separate reviewers. Native execution retains its own task verification and one independent whole-change final review, without per-task subagent reviews.
- Use the upstream task-reviewer, re-review, and final-review prompts. Do not maintain copied NHK review prompts.
- Give reviewers fixed BASE and HEAD revisions, binding constraints, the report, and evidence. Check implementer claims against the diff and test output.
- A scoped re-review checks prior findings and regressions from the fix. The main thread resolves every cannot-verify item before completion.
- A passed SDD task review may satisfy final review only for a single-task non-complex plan covering all requirements, changes, and verification evidence at identical final scope and fixed version.
- Re-evaluate consolidation when scope, version, or evidence changes; never reuse stale approval.
- All other plans, including multi-task and complex plans, retain one whole-change final review. Final review allows at most one concentrated fix wave and one scoped re-review.
- Consolidation never resets or extends task or acceptance-gap repair counts, execution recovery, or final fix-wave bounds.

### Capability Tiers

- Route each packet to one tier: `light`, `standard`, `deep`, or `audit`. Tiers determine permission; the platform section maps them to configurations, and there is no mandatory `light` trial.
- `light`: small mechanical or standard tasks meeting the low-risk implementation condition, plus local fixes and scoped re-reviews whose cause, intended behavior, approach, impact, and verification are clear without design or cross-task judgment. The plan need not supply complete implementation code; `light` never performs an initial task review.
- `standard`: the default for ordinary implementation, local design, integration, debugging, independent investigation, and initial task reviews.
- Before selecting `deep`, check packet size, interfaces, and context; repair these first. Load `implementation-planning.md` if the plan needs material revision.
- `deep`: a concrete reasoning difficulty remaining after those checks, or demonstrated `standard` capability limits. State that difficulty in one sentence in the existing brief; a known hard task may start here without a failed lower-tier trial.
- A review uses `deep` when the review itself meets that difficulty condition; assess review difficulty separately from implementation.
- `audit` is read-only: independent diagnosis (including recovery consultation) and complex whole-change final review, never implementation or recovery fixes. After a failed `deep` implementation it may be selected directly for the one independent diagnosis.
- Other whole-change final reviews use `deep`.
- First classify failures as scope, context, environment, verification, or capability. Escalate one tier only for demonstrated capability limits of a correctly sized packet; failure count alone is not a reason to escalate.
- `deep` is the ordinary ceiling: non-convergence there enters execution recovery; earlier stagnation or the five-round bound also triggers reassessment. Model changes never reset counts.
- Small line count or a review finding alone does not qualify a fix for `light`. Keep judgment and integration with the original task owner or select `standard` or `deep` under the difficulty rules.
- Select post-review fixes and re-reviews by these repair rules. “Most capable upstream” means most capable within the task's authorization.
- Report configuration unavailability as availability; it never authorizes another tier, an older model, or the `audit` configuration as fallback.

### Codex Routing

- Every fresh Codex worker uses `fork_turns: none` and receives a self-contained brief, required files, and binding global constraints.
- Runtime model IDs are `gpt-6-luna`, `gpt-6-sol`, and `gpt-6-astra`; UI Extra High maps to `xhigh`.
- `light`: GPT-6 Luna max.
- `standard`: GPT-6 Sol xhigh.
- `deep`: GPT-6 Astra medium.
- `audit`: GPT-6 Astra xhigh.
- Ultra requires human approval naming the packet and current run. It never becomes a reusable project or session default.
- Ultra authorization and recursion authorization never imply each other.

- Preserve an existing human routing exception only as an active `Human routing exception:` JSON bullet in Codex Routing with exactly `target`, `scope`, `role`, `preset`, and `approval` string fields.
- The target names one task or qualifying mechanical batch; scope is a non-root repository-relative path without wildcards or traversal. Role is `task-implementation`, `initial-task-review`, `local-fix`, or `scoped-re-review`.
- Apply the recorded `light`, `standard`, or `deep` preset only when target, scope, and role match the confirmed decision; all other work keeps the normal rules. Never turn a record into a project or session default.
- Confirm the existing human decision from its Markdown-file-and-anchor or HTTPS-and-fragment approval reference; never invent consent. Static validation checks structure, not approval authenticity.
- Records change only that preset choice, not worker class, review gates, budgets, the `audit` tier, Ultra, or recursion. Initial reviews still exclude the `light` preset.

### Claude Routing

- Every Claude worker runs Opus. When `.claude/agents/nhk-*.md` definitions exist, dispatch through them and omit the per-invocation model so each definition stays authoritative.
- Without those definitions, pass `model: opus` on every dispatch; the worker then runs at session effort, as the human chose when declining them.
- The definitions alone carry model and effort. Map tiers to definitions: `light` and `standard` use `nhk-standard`, `deep` uses `nhk-deep`, and `audit` uses the read-only `nhk-audit`.
- Delegate a packet only when it is independent and larger than the main thread finishes in a handful of tool calls; use one worker when one suffices.
- A worker report with open acceptance items and no named blocker is a report, not completion: continue that worker with the open items, at most twice. Continuations are not repair rounds; afterwards classify the failure.
- Use Fable only when the human explicitly chooses or approves it for the main thread.
- Built-in agents also receive `model: opus` explicitly, so Fable is never inherited.

## Final Check

- The generated file is at most 100 lines and uses the five required headings in order.
- Common sections and the current platform route are sufficient for every dispatch and review decision.
- Tier permissions, exact presets, review gates, the read-only `audit` tier, Ultra approval, and recursion approval retain their separate meanings.
- Claude Routing names tiers and definitions only; effort values live in the agent definitions built from `claude-agents-template.md`.
- No template prompt, placeholder, project map, active status, or copied upstream review prompt remains.
