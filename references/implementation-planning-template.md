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

- State that the installed or explicitly adopted Superpowers workflow remains authoritative for plan shape and execution.
- Preserve its `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code.
- Describe this document as a task-sizing overlay, not a replacement spec, ticket system, or runtime dependency.

### Plan Layers

- Keep outcome, constraints, architecture, interfaces, and cross-task sequencing at plan level.
- Make each task one worthwhile, independently acceptable delivery with a complete implementation-and-verification loop.
- Keep the workflow's 2–5-minute execution steps short and exact. A task may contain multiple necessary TDD cycles.
- Fold setup, tests, configuration, and documentation into the result they enable instead of making them separate tasks.

### Task Contract

Each task starts with these fields before the workflow's ordinary implementation detail:

```md
**Delivers:** <one observable, independently acceptable result>
**Blocked by:** <task identifiers, or None>
**Worker class:** <mechanical | standard | judgment>
```

Then retain the workflow's `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code.

- One task must fit one fresh implementer context, one coherent acceptance result, one reviewer gate, and one independent return.
- Separate independent judgment, results, or ownership boundaries. Do not split one transaction, permission decision, or recovery path across tasks.
- Batch same-shape mechanical edits when they share one acceptance result and verification loop.
- `mechanical` covers deterministic search, transcription, or transformation; `standard` covers clear implementation or scoped review; `judgment` covers bounded work whose main difficulty is integration or design judgment.

### Dependencies and Execution

- `Blocked by` lists only real prerequisite tasks and uses `None` when there is no dependency.
- Under subagent-driven development, implementation tasks remain sequential; dependency metadata does not grant parallel-write permission.
- A dispatch brief carries the complete task body, selected configuration, and binding `Files`, `Interfaces`, acceptance, authority, verification, forbidden actions, expected return, and global constraints.
- If a brief helper extracts only the task section, copy plan-level constraints into that section or attach one self-contained file handoff.
- Split a task before assigning it when its delivery, ownership boundary, or reviewer gate is not singular.
- Apply `worker-policy.md` for dispatch and review choices. Apply `execution-recovery.md` only when its triggers fire.

### Wide Changes

- A change expected to touch thousands of lines or many call sites is not an ordinary task.
- Structure it as expand → migrate batches → contract, with each batch independently reviewable and verified.
- When a migration batch cannot keep the shared branch green alone, name an integration branch and finish with an explicit integrate-and-verify task.
- Do not raise worker capability to compensate for an oversized migration packet.

### Plan Review

Before approval or dispatch, verify:

- every task has `Delivers`, `Blocked by`, and `Worker class`
- every task has one worthwhile acceptance result, one fresh context, a complete verification loop, and one reviewer gate
- dependencies form a valid execution order and do not imply unsafe parallel writes
- wide changes use expand, migrate batches, and contract rather than one giant task
- the plan preserves the active Superpowers details and introduces no competing workflow
- every extracted brief carries or attaches binding plan-level constraints and interfaces
- dispatch and recovery procedures route to their companions instead of being copied into the plan

## Final Check

- The generated file is at most 80 lines and has exactly the six required second-level headings.
- No template prompt, placeholder, model catalog, repository map, active status, or duplicated execution workflow remains.
