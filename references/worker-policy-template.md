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

- Keep named Astra xhigh/max declarations in the final-review reservation; refer to that reservation by role elsewhere rather than adding alternate preset permissions.

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
- Runtime model IDs are `gpt-5.6-luna` and `gpt-6-astra`; UI Light / Extra High map to `low` / `xhigh`.
- Band 1: GPT-5.6 Luna max; GPT-6 Astra low.
- Band 2: GPT-6 Astra medium.
- Presets within a band are unordered task-fit choices; roles determine permission, and there is no mandatory Band 1 trial.
- Whole module implementation, internal debugging, tests, integration, and initial independent module review use GPT-6 Astra medium (Band 2).
- Standalone mechanical work must be independent, deterministic, clearly specified, and low-risk; it may use Band 1.
- Initial review of standalone mechanical work may use GPT-6 Astra low. Other initial reviews use Band 2.
- Local fixes and scoped re-reviews may use Band 1 only when cause, intended behavior, approach, impact, and verification are clear and no design or cross-module judgment is needed.
- Small line count or a review finding alone does not qualify a fix. Keep judgment and integration with the original module owner or Band 2.
- GPT-5.6 Luna may perform low-risk scoped re-review, never an initial task review.
- Band 1 may substitute an available same-band preset only within the role's permissions.
- At the ordinary Band 2 ceiling, non-convergence enters execution recovery. Report medium unavailability as availability; never downgrade a module or use special final-review presets as fallback.
- GPT-6 Astra xhigh and GPT-6 Astra max are reserved for whole-change final review of a complex Superpowers plan, not ordinary implementation, debugging, or recovery.
- Select post-review fixes and re-reviews by the bounded repair role above. “Most capable upstream” means most capable within the task's authorization.
- Ultra requires human approval naming the packet and current run. It never becomes a reusable project or session default.
- Ultra authorization and recursion authorization never imply each other.

### Claude Routing

- Use Sonnet for ordinary implementation and review. Use Opus for difficult work, debugging, architecture, final review, and a recommended complex main thread.
- Use Fable only when the human explicitly chooses or approves it for the main thread.
- Specify Sonnet or Opus for every worker so Fable is never inherited.
- Use available versions and configurations. Do not add a Haiku band or maintain a version-pinned catalog.

## Final Check

- The generated file is at most 100 lines and uses the four required headings in order.
- Common sections and the current platform route are sufficient for every dispatch and review decision.
- Exact presets, review gates, special final-review reservation, Ultra approval, and recursion approval retain their separate meanings.
- No template prompt, placeholder, project map, active status, or copied upstream review prompt remains.
