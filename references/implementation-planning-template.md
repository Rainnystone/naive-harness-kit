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

- Keep outcome, constraints, architecture, and cross-task sequencing at plan level.
- Make each task the smallest independently reviewable delivery unit; keep the workflow's 2–5-minute execution steps short and exact.
- Do not turn every setup action or test command into its own task.

### Task Contract

Each task starts with these fields before the workflow's ordinary implementation detail:

```md
**Delivers:** <one observable, independently acceptable result>
**Blocked by:** <task identifiers, or None>
**Worker class:** <mechanical | standard | judgment>
```

Then retain the workflow's exact file, interface, TDD, command, expected-result, and code requirements.

- One task must fit one fresh implementer context, one test cycle, one reviewer gate, and one independent return.
- If a substep can be approved or rejected separately, promote it to a task.
- Fold setup, scaffolding, configuration, and documentation that serve only this result into the same task.
- `mechanical` covers deterministic search, transcription, or transformation; `standard` covers clear implementation or scoped review; `judgment` covers bounded work whose main difficulty is integration or design judgment.

### Dependencies and Execution

- `Blocked by` lists only real prerequisite tasks and uses `None` when there is no dependency.
- Under subagent-driven development, implementation tasks remain sequential; dependency metadata does not grant parallel-write permission.
- A dispatch brief carries the complete task body. Do not make the implementer reconstruct acceptance criteria from the rest of the plan.
- Split a task before assigning it when the result, test cycle, or review gate is not singular.

### Wide Changes

- A change expected to touch thousands of lines or many call sites is not an ordinary task.
- Structure it as expand → migrate batches → contract, with each batch independently reviewable and verified.
- When a migration batch cannot keep the shared branch green alone, name an integration branch and finish with an explicit integrate-and-verify task.
- Do not raise worker capability to compensate for an oversized migration packet.

### Plan Review

Before approval or dispatch, verify:

- every task has `Delivers`, `Blocked by`, and `Worker class`
- every task has one observable result, one fresh context, one test cycle, and one reviewer gate
- dependencies form a valid execution order and do not imply unsafe parallel writes
- wide changes use expand, migrate batches, and contract rather than one giant task
- the plan preserves the active Superpowers details and introduces no competing workflow
- a fifth failed fix/review round enters the existing systematic-debugging breaker; the plan does not schedule a sixth patch

## Final Check

- The generated file is at most 80 lines and has exactly the six required second-level headings.
- No template prompt, placeholder, model catalog, repository map, active status, or duplicated execution workflow remains.
