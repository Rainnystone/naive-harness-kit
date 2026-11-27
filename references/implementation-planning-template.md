# Implementation Planning Template

## Purpose

Use this template to create `implementation-planning.md`, the on-demand contract for work planned through Superpowers or Matt. Keep the chosen workflow's own planning artifacts and execution method.

## Template Contract

- Select one final shape and keep its `Workflow: Superpowers` or `Workflow: Matt` line active under `Workflow Compatibility`. Start with `# Implementation Planning` and promote the six selected headings to second level.
- For Superpowers, keep the three Task Contract field declarations active and adapt only their right-hand placeholders.
- Keep stable planning rules here; keep project routes in `coding-agent-guide.md` and document lifecycle in `documentation-governance.md`.
- Load it before writing, approving or revising a plan or ticket breakdown. Generate the workspace default from the governance marker. Link the guide by literal path and load it on demand.

## Required Final Shape

### Workflow Compatibility

Workflow: Superpowers

- If the current workstream has a different owner, use its original spec, tickets or plan and the matching workflow section in the installed NHK package’s `references/implementation-planning-template.md`. Keep the workspace guide on its default.
- Choose one primary workflow per workstream. Other skills may contribute without replacing the primary workflow or duplicating its artifacts.
- The installed or explicitly adopted Superpowers workflow supplies plan shape, test workflow, and review prompts; NHK atomic task sizing, planning detail, role routing, reuse, and waiting rules override conflicting generic defaults.
- Preserve its `Files`, `Interfaces`, concrete TDD steps, commands, expected results, and necessary code examples. Specify behavior, boundaries, and verification; workers own local implementation without a mandatory complete code listing in the plan.
- This document is an atomic task-sizing overlay for both Codex and Claude Code; preserve the user's chosen SDD or native execution method.

### Plan Layers

- Keep outcome, constraints, architecture, interfaces, and cross-task sequencing at plan level.
- An atomic task is the smallest independently testable delivery with a complete verification loop worth its own review. Split where a reviewer could accept one result and reject its neighbor, including within the same feature.
- Keep Superpowers' small execution steps inside their task. A task may contain multiple necessary TDD cycles.
- Group implementation, tests, configuration, migration, and documentation required for that task's acceptance.
- Define the delivery before choosing a model; reduce independent decisions and context burden without moving all local implementation into the main thread.

### Task Contract

Keep Superpowers `Task N` headings. Each task starts with these fields before the workflow's ordinary implementation detail:

**Delivers:** <one observable, independently acceptable result>
**Blocked by:** <task identifiers, or None>
**Worker class:** <mechanical | standard | judgment>

Then retain the workflow's `Files`, `Interfaces`, concrete TDD steps, commands, expected results, and necessary code examples.

- One task fits one bounded working context, one observable acceptance result, and one independent return; SDD adds one independent reviewer.
- Separate independently acceptable outcomes and judgments; connect dependent tasks through explicit interfaces. Keep one transaction, permission decision, or recovery path together.
- File count, code size, and elapsed time are clues, not task-size thresholds. A task may span files; a feature may span tasks.
- Batch same-shape mechanical changes only with one transformation rule, an explicit file list, shared verification, and no separate judgment. Internal execution steps do not become separate dispatches.
- `mechanical` describes deterministic transformations, `standard` clear implementation, and `judgment` local design, integration, or debugging decisions. Worker class is not a model tier; a small standard task can meet the low-risk implementation condition in `worker-policy.md`.

### Dependencies and Execution

- `Blocked by` lists only real prerequisite tasks and uses `None` when there is no dependency.
- Under subagent-driven development, implementation tasks remain sequential; dependency metadata does not grant parallel-write permission.
- A dispatch brief carries the complete task body, selected configuration, and binding `Files`, `Interfaces`, acceptance, authority, verification, forbidden actions, expected return, and global constraints.
- If a brief helper extracts only the task section, copy plan-level constraints into that section or attach one self-contained file handoff.
- Use upstream brief, report, diff-package, and ledger artifacts; pass relevant interfaces and evidence rather than accumulated session history.
- Before increasing capability, separate independent deliveries and decisions and resolve missing interfaces or context; preserve tightly coupled logic and its verification.
- Split investigation only when it delivers a verifiable conclusion, interface contract, or reusable decision; otherwise keep local understanding with implementation. Independent investigation starts at the default implementation role unless its own difficulty justifies more capability.
- Apply `worker-policy.md` for dispatch and review choices. Apply `execution-recovery.md` only when its triggers fire.

### Wide Changes

- For wide migrations, preserve compatibility and safe acceptance boundaries; each batch remains an independently verifiable delivery.
- Structure it as expand → migrate batches → contract, with each batch independently reviewable and verified.
- When a migration batch cannot keep the shared branch green alone, name an integration branch and finish with an explicit integrate-and-verify task.
- Do not raise worker capability to compensate for an oversized migration packet.

### Plan Review

Before approval or dispatch, verify:

- every task has `Delivers`, `Blocked by`, and `Worker class`
- every task has one independently acceptable delivery, a bounded context, and a complete verification loop; mechanical batches meet the shared-rule condition
- When many tasks need higher capability, recheck boundaries and shared constraints; use no fixed quota and preserve irreducible difficult tasks.
- dependencies form a valid execution order and do not imply unsafe parallel writes
- wide changes use expand, migrate batches, and contract rather than one giant task
- the plan preserves the active Superpowers details and introduces no competing workflow
- every extracted brief carries or attaches binding plan-level constraints and interfaces
- dispatch and recovery procedures route to their companions instead of being copied into the plan

## Matt Final Shape

### Workflow Compatibility

Workflow: Matt

- If the current workstream has a different owner, use its original spec, tickets or plan and the matching workflow section in the installed NHK package’s `references/implementation-planning-template.md`. Keep the workspace guide on its default.
- Choose one primary workflow per workstream. Other skills may contribute without replacing the primary workflow or duplicating its artifacts.
- Use `to-spec` for the shared spec and `to-tickets` for implementation tickets in Matt's configured tracker. Use native blocking edges where available or one Markdown file per ticket with the local tracker. Without triage, pass the configured ready-state mapping or Matt's default `ready-for-agent` to the publishing skill.

### Plan Layers

- Keep shared outcomes, constraints, decisions, and testing seams in the spec. Make each vertical slice independently testable through the affected layers and small enough for one fresh context.

### Task Contract

- State end-to-end behavior, observable acceptance criteria, and blocking edges on each ticket. Carry binding constraints and decisions through pointers to the spec and ticket.

### Dependencies and Execution

- For a local tracker, give each helper read access to the spec and ticket in their authoritative checkout, including untracked files. The primary thread owns tracker updates.
- Give `implement-spec` the spec and ticket references. Use separate branches and isolated worktrees, one of each per ticket. Independent tickets with resolved blockers may run concurrently when write boundaries are safe. Use Matt's `tdd` for each ticket, then merge its result into the integration branch before unblocking dependent tickets.
- Keep ticket state in the configured tracker and link to it from NHK workstream records. Apply `worker-policy.md` for dispatch and review choices and `execution-recovery.md` when its triggers fire.

### Wide Changes

- For a wide refactor that cannot land green as vertical slices, expand, migrate in verifiable batches, then contract. If batches cannot stay green alone, keep the sequence on an integration branch and finish with an integrate-and-verify ticket.

### Plan Review

- Check spec coverage, slice size, acceptance criteria, and blocking edges before execution. Run Matt's `code-review` on the integration branch for Standards and Spec, then verify integrated acceptance before closing tickets.

## Final Check

- The generated file is at most 80 lines and has exactly the six required second-level headings.
- No template prompt, placeholder, model catalog, repository map, active status, or duplicated execution workflow remains.
