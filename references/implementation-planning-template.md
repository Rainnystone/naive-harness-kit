# Implementation Planning Template

## Purpose

Use this template to create `implementation-planning.md`, the on-demand packet contract for implementation plans executed through Superpowers.

This companion tightens task sizing and dependency edges. It does not replace Superpowers, create another plan format, or govern ordinary coding, review, or debugging.

## Template Contract

- Final file hard limit: 80 lines. There is no minimum.
- Replace explanatory examples with concise workspace facts and remove all template guidance.
- Keep stable planning rules here; keep project routes in `coding-agent-guide.md` and document lifecycle in `documentation-governance.md`.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import for it.
- Load it only before writing, approving, or materially revising an implementation plan.

## Required Final Shape

Start with `# Implementation Planning`, then use exactly the following second-level headings in order.

### Workflow Compatibility

- The installed or explicitly adopted Superpowers workflow supplies plan shape, test workflow, and review prompts; NHK module sizing, role routing, reuse, and waiting rules override conflicting generic defaults.
- Preserve its `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code.
- This document is a module-sizing overlay, not a replacement spec, ticket system, or runtime dependency.

### Plan Layers

- Keep outcome, constraints, architecture, interfaces, and cross-task sequencing at plan level.
- A Module is related work with a defined responsibility, prerequisites, interfaces, and complete acceptance; it need not match a file or directory. Default one Superpowers Task is one Module; independently dispatched mechanical work is the explicit exception.
- Keep concrete incremental internal steps and timely verification. A module may contain multiple necessary TDD cycles.
- Group implementation, tests, configuration, migration, and documentation for the same capability and working context.

### Task Contract

Keep Superpowers `Task N` headings. Each task starts with these fields before the workflow's ordinary implementation detail:

```md
**Delivers:** <one observable, independently acceptable result>
**Blocked by:** <task identifiers, or None>
**Worker class:** <mechanical | standard | judgment>
```

Then retain the workflow's `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code.

- One module must fit one implementer context, one complete acceptance result, one independent reviewer, and one return.
- Split at unrelated outcomes, distinct authority, unresolved cross-module dependencies, or scope one implementer and reviewer cannot reliably assess. File count, commit count, elapsed time, and independently testable internal results alone do not justify splitting. Keep one transaction, permission decision, or recovery path together.
- Internal mechanical steps stay with the module implementer; they never automatically become new dispatches. Batch independent same-shape mechanical work when it shares acceptance and verification.
- `mechanical` is for standalone deterministic low-risk work. Whole modules use `standard` for clear implementation or `judgment` for integration/design uncertainty; both route to medium under the Codex worker policy.

### Dependencies and Execution

- `Blocked by` lists only real prerequisite tasks and uses `None` when there is no dependency.
- Under subagent-driven development, implementation tasks remain sequential; dependency metadata does not grant parallel-write permission.
- A dispatch brief carries the complete task body, selected configuration, and binding `Files`, `Interfaces`, acceptance, authority, verification, forbidden actions, expected return, and global constraints.
- If a brief helper extracts only the task section, copy plan-level constraints into that section or attach one self-contained file handoff.
- Before dispatch, apply the module boundaries above; internal steps remain with their module owner.
- Apply `worker-policy.md` for dispatch and review choices. Apply `execution-recovery.md` only when its triggers fire.

### Wide Changes

- For wide migrations, preserve compatibility and safe acceptance boundaries; size modules by responsibility, not line or call-site count.
- Structure it as expand → migrate batches → contract, with each batch independently reviewable and verified.
- When a migration batch cannot keep the shared branch green alone, name an integration branch and finish with an explicit integrate-and-verify task.
- Do not raise worker capability to compensate for an oversized migration packet.

### Plan Review

Before approval or dispatch, verify:

- every task has `Delivers`, `Blocked by`, and `Worker class`
- every module has complete acceptance, one implementer context, internal verification, and one independent reviewer; mechanical exceptions are explicit
- dependencies form a valid execution order and do not imply unsafe parallel writes
- wide changes use expand, migrate batches, and contract rather than one giant task
- the plan preserves the active Superpowers details and introduces no competing workflow
- every extracted brief carries or attaches binding plan-level constraints and interfaces
- dispatch and recovery procedures route to their companions instead of being copied into the plan

## Final Check

- The generated file is at most 80 lines and has exactly the six required second-level headings.
- No template prompt, placeholder, model catalog, repository map, active status, or duplicated execution workflow remains.
