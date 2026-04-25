# CLAUDE.md Generation Contract

[[TEMPLATE_ONLY:BEGIN]]
This file is a generation contract for an NHK-managed Claude Code instruction file. It is not a final `CLAUDE.md`.

Prefer a thin `CLAUDE.md` when the workspace also has `AGENTS.md`:
- import or point to `AGENTS.md` as the shared instruction source when the platform supports it
- add only Claude-specific rules that cannot live in `AGENTS.md`
- avoid duplicating the full shared instruction set unless the human explicitly wants `CLAUDE.md` to be the active standalone instruction file

Template markers:
- `[[TEMPLATE_ONLY]]` content is generation guidance only and must not appear in the final `CLAUDE.md`.
- `[[FINAL_VERBATIM]]` content must be copied into the final `CLAUDE.md` without changing a single word unless the human explicitly approves a change.
- `[[FINAL_ADAPT]]` content must appear in the final `CLAUDE.md`, but it must be rewritten for the actual workspace.
- `[[OPTIONAL_BY_COMPLEXITY]]` content appears only when the workspace complexity justifies it.
- Marker boundary lines and the bracket labels themselves must never appear in the final `CLAUDE.md`.

Final line budget:
- thin adapter target: 15-35 lines
- simple standalone target: 110-130 lines
- medium standalone target: 130-160 lines
- complex standalone hard cap: 185 lines

Allowed final top-level headings for standalone mode:
- Project Overview
- Workspace Navigation
- Architecture
- Execution Rules
- Context Loading
- Subagents and Packets
- Blockers
- Testing and Verification
- Companion Docs
- Git and Delivery

Do not add final headings such as `NHK Governance`, `NHK Govern`, `Instruction Coverage`, `Template Notes`, or `Claude Code Project Instructions Template` unless the human explicitly asks for them.

Final cleanup checklist:
- No template markers remain.
- No `Fill in`, `Suggested`, `Document:`, `Template usage`, or similar generation-only wording remains.
- Required `[[FINAL_VERBATIM]]` blocks are unchanged.
- Required `[[FINAL_ADAPT]]` sections are present and project-specific.
- Final line count meets the selected budget unless the human explicitly approves an exception.
[[TEMPLATE_ONLY:END]]

[[FINAL_ADAPT:BEGIN]]
## Project Overview

Write 3-6 bullets or short sentences covering only:
- what this workspace is for
- the current active repository and canonical branch
- the implementation stack or content type
- active versus historical materials
- any non-obvious project constraint an agent must know before editing
[[FINAL_ADAPT:END]]

[[FINAL_ADAPT:BEGIN]]
## Workspace Navigation

Write the first-read order for this workspace.

For simple workspaces, include only a short key-path summary.
For medium or complex workspaces, point to `coding-agent-guide.md`, `documentation-governance.md`, active plans, codemaps, or recovery files instead of expanding this section.
[[FINAL_ADAPT:END]]

[[FINAL_ADAPT:BEGIN]]
## Architecture

Summarize only the boundaries needed for safe execution:
- core subsystems or document surfaces
- write boundaries
- deterministic versus heuristic responsibilities
- active/archive boundaries that affect implementation
[[FINAL_ADAPT:END]]

## Execution Rules

[[FINAL_ADAPT:BEGIN]]
### Data and State Discipline

Write project-specific data mutation rules only when they apply.

For JavaScript, TypeScript, React, reducers, or state-heavy apps, include immutable update rules such as returning new objects and avoiding in-place array mutation.

For documentation-only, prompt-first, static-site, or script-light workspaces, replace this with concise rules about preserving source-of-truth files, generated artifacts, and deterministic writes.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
### Deterministic Boundaries Must Stay Deterministic

- Validation, schema checks, path checks, reference integrity, and persistence guarantees should be handled by deterministic code.
- Do not delegate deterministic validation to heuristic or probabilistic flows unless the human explicitly approves that tradeoff.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
### Keep Rules, Code, Tests, and Active Docs in Sync

- If code, tests, and active project documents disagree, resolve intended behavior first.
- Then bring implementation, tests, and active docs back into sync.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
### Task Tracking Discipline

- If the workspace maintains a todo list, task list, checklist, plan, or other active tracking surface, update it when each task is completed.
- Do not batch all task-list updates at the very end if task-by-task updates are practical.
- If the workspace uses `task_plan.md`, `progress.md`, or `findings.md`, keep them aligned with actual task status rather than letting them drift.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
### Workflow Completion and Archive Check

- After a full `superpowers` workflow cycle or another clearly bounded implementation cycle, check whether the active docs and tracking surfaces suggest that a workstream may be complete.
- If the workspace is NHK-managed and the workstream looks complete, ask whether `nhk-archive` should be invoked.
- If the workspace is not NHK-managed, ask whether the project's equivalent archive transition should be invoked.
- Do not archive automatically.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project-Specific Architecture Discipline

Add this subsection only when the workspace has real architecture-specific boundaries. Keep it under 800 tokens and link to `coding-agent-guide.md` for deeper detail.
[[FINAL_ADAPT:END]]

## Context Loading

[[FINAL_VERBATIM:BEGIN]]
- If a governance doc exists, it is the source of truth for documentation lifecycle rules.
- Prefer current code, current tests, and active docs first; treat archive as reference material rather than a default execution source.
- Start with the smallest active document set that can route the task safely, and load codemaps, plans, specs, or archive only when the task genuinely needs them.
- Spec text budget: max 40,000 tokens per session.
- If active plans, specs, tests, and implementation drift apart, resolve intended behavior first, then bring the active source of truth and dependent materials back into sync.
- For root tracking discipline, refer to `$planning-with-files-zh`.
- For active `specs/` and `plans/` conventions, refer to `$using-superpowers`.
[[FINAL_VERBATIM:END]]

## Subagents and Packets

[[FINAL_VERBATIM:BEGIN]]
### Subagent Delegation Discipline

#### Dispatch

- For complex work, prefer decomposing the implementation into bounded tasks and dispatching subagents rather than keeping the whole execution on the main thread.
- Subagent dispatch must follow `subagent-driven-development`; do not improvise a parallel workflow outside that discipline when the task has already been decomposed.
- Choose the Claude subagent model according to task complexity instead of defaulting to the largest model.
- Prefer Claude Code model aliases over hardcoded dated model strings unless the project explicitly requires version pinning.
- Valid Claude Code model aliases currently include:
  - `sonnet`
  - `opus`
- If the workspace uses a default subagent model, document it through `CLAUDE_CODE_SUBAGENT_MODEL`.
- If the workspace uses a more specific Claude Code configuration surface for subagent model or effort control, document that mechanism explicitly and keep it aligned with current Anthropic docs.
- Supported effort levels are model-dependent. Official Claude Code docs currently list:
  - Opus 4.7: `low`, `medium`, `high`, `xhigh`, `max`
- Other Claude Code models expose model-dependent subsets; check current Anthropic docs before pinning an effort level.
- If an unsupported effort level is configured, Claude Code falls back to the highest supported level at or below that setting.
- Recommended deployment guidance:
  - `sonnet` with `max` for implementation packets, review packets, and balanced codebase work when Sonnet is the chosen subagent model
  - `opus` with `medium` or `high` for high-risk debugging, architecture, or synthesis-heavy tasks
  - `opus` with `xhigh` for most difficult coding and agentic tasks where extra reasoning is useful but `max` may overthink
  - `opus` with `max` only for the most difficult bounded tasks where extra latency and cost are justified
- Dispatch instructions must explicitly tell the worker that it is a subagent, not the main thread.
- Prefer giving the subagent a clean task brief, file boundary, and success criteria instead of forwarding raw main-thread conversation history.
- Each dispatch should clearly state:
  - whether the subagent is read-only review or write-authorized implementation
  - which files or modules it owns
  - which actions are forbidden, especially spawning more subagents, reverting unrelated work, or broadening scope without approval

#### Waiting and Inquiry

- The first `wait_agent` call must use `timeout_ms=120000`.
- If the first wait times out but there is new output, such as new replies, `git diff` changes, or changes in owned files, the next wait must use `timeout_ms=180000`.
- If the second wait also times out and new output is still appearing, the next wait must use `timeout_ms=300000`.
- `timed_out` is not the same as `blocked`; a timeout only means that the current wait window ended without a final result, not that the subagent is stalled, invalid, or ready to terminate.
- Status inquiry is allowed only after two consecutive rounds with both no new output and no file changes.
- Status inquiry must be phrased as “report progress and blockers only, without pausing the current task”; it must not ask the subagent to stop implementation, pause work, immediately hand over, or abandon its current context.

#### Replacement and Termination

- Do not close a subagent just because a wait timed out.
- Before replacing or closing a subagent, first confirm its actual work status, current progress, latest conclusion, and whether keeping it alive still reduces risk or rework.
- Replace or close a subagent only after three rounds with no output and a status inquiry that also confirms there is no meaningful progress.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
### Implementation Packet Discipline

- Decompose implementation work into bounded packets before dispatch.
- Prefer one primary objective, one main module or surface area, and one verification path per packet.
- The default implementation packet should be the smallest unit that can complete one TDD loop and one review/fix/re-review loop without widening scope mid-flight.
- Each packet should explicitly declare its user-facing goal, owned files, default verification command, and whether it is safe to run in parallel with other packets.
- Prefer dispatching subagent packets that can own their focused tests, implement against them, run targeted verification, and return a reviewable result.
- If two packets share the same primary production file or the same primary test file, default to serial execution unless the plan explains why parallel work is still safe.
- If a packet grows across unrelated concerns, long execution chains, or multiple verification paths, split it again.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
## Blockers

Write a project-specific blocker protocol. Do not copy domain objects from another workspace.

Include:
- the smallest safe repair sequence for common implementation blockers
- exact changes that require stopping for human approval
- public API, persistence, data model, user-facing workflow, or architecture boundaries that must not be changed silently
[[FINAL_ADAPT:END]]

[[FINAL_ADAPT:BEGIN]]
## Testing and Verification

Required baseline:
- TDD is mandatory for production behavior changes: write a failing test, verify RED, implement, verify GREEN, then refactor.
- Default coverage minimum is 80%. If the project already has a higher baseline, use the higher baseline.
- Coverage is a completion gate, not proof of test quality. Do not satisfy coverage with empty assertions, shallow smoke tests, or tests that only verify mocks.
- If the project has no coverage tooling yet, document the human-approved exception or add the smallest suitable coverage command before claiming coverage compliance.

List the real project commands:
- targeted test command
- coverage command
- type-check or lint command
- build command when app or package surfaces change
- full verification command before delivery
[[FINAL_ADAPT:END]]

## Companion Docs

[[FINAL_VERBATIM:BEGIN]]
In NHK-managed workspaces, the following companion docs are mandatory even for simple projects:

- `coding-agent-guide.md`
- `documentation-governance.md`

They may stay minimal in a simple repository, but they should still exist as stable routing and governance surfaces.

Complexity still matters for heavier companion materials.
[[FINAL_VERBATIM:END]]

[[OPTIONAL_BY_COMPLEXITY:BEGIN]]
For medium-complexity or complex projects, consider adding:
- `task_plan.md`, `findings.md`, `progress.md` for multi-session continuity
- `docs/codemaps/` for module relationships
- `docs/specs/` or equivalent for active design specs
- `docs/plans/` or equivalent for execution plans
- dedicated simulation, tooling, or environment guides
- a small architecture map for subsystem boundaries
[[OPTIONAL_BY_COMPLEXITY:END]]

[[FINAL_ADAPT:BEGIN]]
## Git and Delivery

Write the active repository, active development branch, protected branch rules, and PR target.

General rules to preserve:
- Commit format: `<type>: <description>` such as `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, or `chore:`.
- PRs should target the active development branch unless the human explicitly says otherwise.
- Human review is required before merge.
- When working from a plan, check off tasks as they complete.
- Do not treat code changes as complete until required verification commands have passed.
[[FINAL_ADAPT:END]]
