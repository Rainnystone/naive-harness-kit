# Worker Policy Template

## Purpose

Use this template to create `worker-policy.md`, the on-demand dispatch and review contract for Codex and Claude workers.

This companion owns worker configuration and orchestration detail. Canonical startup instructions keep only the conditional route to this file.

## Template Contract

- Final file hard limit: 100 lines. Source-template hard limit: 140 lines. There is no minimum.
- Replace template guidance with the rules below and remove every prompt or placeholder.
- Keep common dispatch and review rules together; read only those sections and the current platform section for an orchestration run.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import.
- Preserve explicit human budgets and authorizations. Availability does not expand capability authority.

- Keep presets in the band catalog and special-role declarations below; use band or role names for other routing rules.

Optional exception illustration (generation guidance, not an actual approval): after confirming an existing decision, replace this synthetic record with its real target, scope, role, preset, and evidence. Omit records when no such decision exists.

```md
- Human routing exception: {"target":"billing-module","scope":"src/billing/","role":"module-implementation","preset":"GPT-6 Luna max","approval":"decisions/billing.md#luna-route"}
```

The record must be one complete JSON object with unique keys and no trailing prose. Use a stable target identifier of up to 80 letters/digits/underscores/hyphens; literal path components may also contain spaces and dots. Unicode names are supported. Keep one record per target/scope/role, reject blanket targets (`all`, `any`, `global`, `default`, `current`, or their prefixed forms; also bare `project`, `workspace`, or `session`), and retain all normal clauses and catalogs.

## Required Final Shape

Start with `# Worker Policy`, then use exactly these second-level headings in order.

### Dispatch Contract

- Authorization comes from the allowed role or preset for the packet, not the main thread's current model or effort. Explicit user budgets still bind.
- Select an explicitly runtime-supported model and effort; never inherit a top preset silently.
- Prefer the original implementer for ordinary fixes and the original independent reviewer for scoped re-review. A lower-cost permission never requires changing worker or model.
- Use a new cheaper worker only when a self-contained repair handoff makes total overhead worthwhile; batch suitable findings into one repair packet.
- Handoff uses the task brief, report, and fixed diff. State objective, scope, read/write authority, acceptance, verification, forbidden actions, expected return, selected configuration, and binding interfaces and constraints.
- Recursive delegation needs separate human authorization for a named packet.
- Keep subagent-driven implementers sequential. Parallelize read-only work only when ownership, state, artifacts, services, and verification resources are independent.
- Check runtime progress and lifecycle. A timeout alone is not a blocker and does not require a nonexistent close tool.
- The main thread owns integration, cross-task verification, recovery decisions, and the final result.

### Review Gates

- Every module or standalone mechanical task gets one independent read-only reviewer with separate spec-compliance and task-quality verdicts. Both must pass; self-review is not a substitute.
- Internal module steps do not dispatch separate reviewers.
- Use the upstream task-reviewer, re-review, and final-review prompts. Do not maintain copied NHK review prompts.
- Give reviewers fixed BASE and HEAD revisions, binding constraints, the report, and evidence. Check implementer claims against the diff and test output.
- A scoped re-review checks prior findings and regressions from the fix. The main thread resolves every cannot-verify item before completion.
- A passed module review may satisfy final review only for a single-module non-complex plan covering all requirements, changes, and verification evidence at identical final scope and fixed version.
- Re-evaluate consolidation when scope, version, or evidence changes; never reuse stale approval.
- All other plans, including multi-module and complex plans, retain one whole-change final review. Final review allows at most one concentrated fix wave and one scoped re-review.
- Consolidation never resets or extends module or acceptance-gap repair counts, execution recovery, or final fix-wave bounds.

### Codex Routing

- Every fresh Codex worker uses `fork_turns: none` and receives a self-contained brief, required files, and binding global constraints.
- Runtime model IDs are `gpt-6-luna` and `gpt-6-astra`; UI Extra High maps to `xhigh`.
- Band 1: GPT-6 Luna max.
- Band 2: GPT-6 Astra medium.
- Band 3: GPT-6 Astra xhigh.
- Presets within a band are unordered task-fit choices; roles determine permission, and there is no mandatory Band 1 trial.
- Default module implementation, internal debugging, tests, and integration to Band 2.
- Standalone mechanical work must be independent, deterministic, clearly specified, and low-risk; it may use Band 1.
- Before selecting Band 3, check packet size, interfaces, and context; repair these first. Load `implementation-planning.md` if the plan needs material revision.
- Select Band 3 only for a concrete reasoning difficulty remaining after sizing and context checks, or demonstrated Band 2 capability limits. State that difficulty in one sentence in the existing brief; a known hard task may start here without a failed lower-band trial.
- First classify failures as scope, context, environment, verification, or capability. Escalate one band only for demonstrated capability limits of a correctly sized packet; failure count alone is not a reason to escalate.
- Initial independent reviews default to Band 2; use Band 3 when the review itself meets its difficulty condition. Assess review difficulty separately from implementation.
- Local fixes and scoped re-reviews may use Band 1 only when cause, intended behavior, approach, impact, and verification are clear and no design or cross-module judgment is needed.
- Small line count or a review finding alone does not qualify a fix. Keep judgment and integration with the original module owner or select Band 2/3 under the difficulty rules.
- GPT-6 Luna may perform low-risk scoped re-review, never an initial task review.
- Report preset unavailability as availability; it does not authorize a different band, an older model, or a special-role preset as fallback.
- At the ordinary Band 3 ceiling, non-convergence enters execution recovery; earlier stagnation or the five-round bound also triggers reassessment. Model changes never reset counts.
- Independent diagnosis and complex whole-change final review use Band 3, or GPT-6 Astra max when deeper reasoning is needed. Max is limited to these read-only roles; after a failed Band 3 implementation it may be selected directly for the one independent diagnosis.
- Other whole-change final reviews default to Band 2 and use Band 3 when the review meets its difficulty condition.
- Select post-review fixes and re-reviews by the bounded repair role above. “Most capable upstream” means most capable within the task's authorization.
- Ultra requires human approval naming the packet and current run. It never becomes a reusable project or session default.
- Ultra authorization and recursion authorization never imply each other.

- Preserve an existing human routing exception only as an active `Human routing exception:` JSON bullet in Codex Routing with exactly `target`, `scope`, `role`, `preset`, and `approval` string fields.
- The target names one packet or module; scope is a non-root repository-relative path without wildcards or traversal. Role is `module-implementation`, `initial-module-review`, `local-fix`, or `scoped-re-review`.
- Apply the ordinary catalog preset only when target, scope, and role match the confirmed decision; all other work keeps the normal rules. Never turn a record into a project or session default.
- Confirm the existing human decision from its Markdown-file-and-anchor or HTTPS-and-fragment approval reference; never invent consent. Static validation checks structure, not approval authenticity.
- Records change only ordinary preset choice, not worker class, review gates, budgets, special-role permissions, Ultra, or recursion. Initial reviews still exclude Luna.

### Claude Routing

- Every Claude worker runs Opus. When `.claude/agents/nhk-*.md` definitions exist, dispatch through them and omit the per-invocation model so each definition stays authoritative.
- Without those definitions, pass `model: opus` on every dispatch; the worker then runs at session effort, as the human chose when declining them.
- The definitions alone carry model and effort. Route by band name: `nhk-light`, `nhk-standard`, `nhk-deep`, or `nhk-diagnosis`.
- `nhk-light`: standalone mechanical work, and local fixes or scoped re-reviews whose cause, intended behavior, approach, impact, and verification are clear without design or cross-module judgment. Initial reviews start at `nhk-standard`.
- `nhk-standard`: the default for module implementation, internal debugging, tests, integration, initial reviews, and other whole-change final reviews.
- `nhk-deep`: a concrete reasoning difficulty that remains after sizing and context checks, stated in one sentence in the brief, or demonstrated `nhk-standard` limits. Reviews meeting that difficulty condition also use it.
- `nhk-diagnosis`: read-only independent diagnosis and complex whole-change final review. The highest effort levels stay with the human-chosen main thread.
- Delegate a packet only when it is independent and larger than the main thread finishes in a handful of tool calls; use one worker when one suffices.
- A worker report with open acceptance items and no named blocker is a report, not completion: continue that worker with the open items, at most twice. Continuations are not repair rounds; afterwards classify the failure.
- Use Fable only when the human explicitly chooses or approves it for the main thread.
- Built-in agents also receive `model: opus` explicitly, so Fable is never inherited.

## Final Check

- The generated file is at most 100 lines and uses the four required headings in order.
- Common sections and the current platform route are sufficient for every dispatch and review decision.
- Exact presets, review gates, special-role permissions, Ultra approval, and recursion approval retain their separate meanings.
- Claude Routing names bands only; effort values live in the agent definitions built from `claude-agents-template.md`.
- No template prompt, placeholder, project map, active status, or copied upstream review prompt remains.
