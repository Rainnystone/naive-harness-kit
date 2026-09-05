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

## Required Final Shape

Start with `# Worker Policy`, then use exactly these second-level headings in order.

### Dispatch Contract

- Authorization comes from the allowed role or preset for the packet, not the main thread's current model or effort. Explicit user budgets still bind.
- Select an explicitly runtime-supported model and effort; never inherit a top preset silently.
- Codex workers use `fork_turns: none`. A fresh worker receives a self-contained brief, required files, and binding global constraints.
- Send routine fixes back to the original implementer. Give a fresh replacement a self-contained file handoff.
- Handoff uses the task brief, report, and fixed diff. State objective, scope, read/write authority, acceptance, verification, forbidden actions, expected return, selected configuration, and binding interfaces and constraints.
- Recursive delegation needs separate human authorization for a named packet. Ultra authorization and recursion authorization never imply each other.
- Keep subagent-driven implementers sequential. Parallelize read-only work only when ownership, state, artifacts, services, and verification resources are independent.
- Check runtime progress and lifecycle. A timeout alone is not a blocker and does not require a nonexistent close tool.
- The main thread owns integration, cross-task verification, recovery decisions, and the final result.

### Review Gates

- Every task gets one independent read-only reviewer with separate spec-compliance and task-quality verdicts. Both must pass; self-review is not a substitute.
- Use the upstream task-reviewer, re-review, and final-review prompts. Do not maintain copied NHK review prompts.
- Give reviewers fixed BASE and HEAD revisions, binding constraints, the report, and evidence. Check implementer claims against the diff and test output.
- A scoped re-review checks prior findings and regressions from the fix. The main thread resolves every cannot-verify item before completion.
- Clear, small, low-risk initial reviews may use GPT-5.5 xhigh. Other initial Codex reviews use Band 2 or Band 3.
- GPT-5.6 Luna may perform low-risk scoped re-review, never an initial task review.
- GPT-6 Astra xhigh or max is reserved for the whole-change final review of a complex Superpowers plan. It is not an ordinary implementation, debugging, or recovery preset.
- Select post-review fixes and re-reviews for their own task. “Most capable upstream” means most capable within the task's authorization, not an Ultra override.
- Run one whole-change final review after all tasks. Follow it with at most one concentrated fix wave and one scoped re-review.

### Codex Routing

- Band 1: GPT-5.5 xhigh; GPT-5.6 Luna max.
- Band 2: GPT-5.6 Terra xhigh; GPT-5.6 Sol medium; GPT-5.6 Sol high; GPT-6 Astra low.
- Band 3: GPT-5.6 Sol xhigh; GPT-6 Astra medium; GPT-6 Astra high.
- Presets within a band are unordered task-fit choices. Band 1 fits mechanical, low-risk clear work; Band 2 fits ordinary implementation and bounded integration; Band 3 fits architecture, high uncertainty, and high risk.
- Start in the band that fits the packet; there is no mandatory Band 1 trial.
- If a preset is unavailable, choose a supported same-band substitute when possible. Treat whole-band unavailability as availability, not capability failure.
- Repair oversized packets and missing context first. Escalate one band only when evidence shows a correctly sized packet is capability-limited.
- At the ordinary Band 3 ceiling, enter execution recovery instead of borrowing special final-review presets.
- Ultra requires human approval naming the packet and current run. It never becomes a reusable project or session default.

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
