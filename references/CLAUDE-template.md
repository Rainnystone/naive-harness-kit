# Claude Code Project Instructions Template

## 1. Purpose and Scope

This file defines stable execution rules, collaboration discipline, verification expectations, and project-specific navigation guidance for coding agents working in this workspace.

Keep this file focused on:
- stable execution rules
- document loading and context discipline
- verification expectations
- only the minimum project context needed to execute safely

Do not turn this file into a changelog, implementation diary, or long-form architecture spec. If the project becomes too complex, move detailed routing, codemaps, and evolving plans into companion documents and keep this file as the stable control layer.

Template usage rules:
- This file is a template, not a final `CLAUDE.md`.
- Guidance-only text such as `Fill in this section with`, `Document:`, `Suggested categories:`, `If the project is complex`, and similar template instructions must not remain in the final project `CLAUDE.md`.
- Fill-in sections must be rewritten for the actual workspace; they are not copy-paste blocks.
- Any subsection explicitly marked as verbatim-preserved content must be copied into the final project `CLAUDE.md` without changing a single word unless the human explicitly approves a change.
- Final line budget:
  - simple workspace target: usually no more than 100 lines
  - complex workspace hard cap: 185 lines
- If the file starts approaching the line budget, move document-system maps and loading detail to `documentation-governance.md`, and move code/file maps plus task-routing or implementation detail to `coding-agent-guide.md` instead of expanding this file.

## 2. Project-Specific Fill-in Sections

The following sections must exist, but their content must be written for the actual project rather than copied from another workspace.

### Project Overview

Fill in this section with:
- what this project is for
- the primary user-facing goal
- the current active repository and canonical branch
- the current implementation stack
- whether there are legacy repos, mirrors, or archived references
- which materials are historical reference only, not active execution sources

Keep this section short. The goal is orientation, not a full product brief.

### Workspace Navigation

Fill in this section with:
- the first documents or files an agent should read
- the preferred routing order for common task types
- where detailed codemaps, task-routing guides, or recovery docs live
- which historical materials should only be consulted when current docs are insufficient

If the workspace is simple, this section may include a very short inline key-path or file-map summary.

If the workspace is complex, this section should stay brief and point to companion docs such as:
- `coding-agent-guide.md`
- `docs/codemaps/`
- recovery files like `task_plan.md`, `findings.md`, `progress.md`

In complex workspaces, do not keep a large file map in `CLAUDE.md`.

### Architecture

Fill in this section with the minimum architecture description needed for safe execution:
- the major loops, pipelines, or subsystems
- the core domain boundaries
- the main coordination points
- any strict separation that agents must preserve

If the project has multiple operational loops or modes, describe them separately.

If the project is simple, keep this section brief and only document boundaries that matter for implementation safety.
If the project is complex, keep this section as a boundary summary only and move operational detail into companion docs.

## 3. Mandatory Execution Rules

### 3. Immutable Data Patterns
- Never mutate state objects. Always return new copies.
- `const newState = { ...oldState, field: newValue }`
- Array operations: `slice`, `map`, `filter` — never `splice`, `push`, `sort` in-place.

### 2. Deterministic Boundaries Must Stay Deterministic

- Validation, schema checks, path checks, reference integrity, and persistence guarantees should be handled by deterministic code.
- Do not delegate deterministic validation to heuristic or probabilistic flows unless the human explicitly approves that tradeoff.

### 3. Keep Rules, Code, Tests, and Active Docs in Sync

- If code, tests, and active project documents disagree, resolve intended behavior first.
- Then bring implementation, tests, and active docs back into sync.

### 4. Task Tracking Discipline

- If the workspace maintains a todo list, task list, checklist, plan, or other active tracking surface, update it when each task is completed.
- Do not batch all task-list updates at the very end if task-by-task updates are practical.
- If the workspace uses `task_plan.md`, `progress.md`, or `findings.md`, keep them aligned with actual task status rather than letting them drift.

### 5. Workflow Completion and Archive Check

- After a full `superpowers` workflow cycle or another clearly bounded implementation cycle, check whether the active docs and tracking surfaces suggest that a workstream may be complete.
- If the workspace is NHK-managed and the workstream looks complete, ask whether `nhk-archive` should be invoked.
- If the workspace is not NHK-managed, ask whether the project's equivalent archive transition should be invoked.
- Do not archive automatically.

### 6. Project-Specific Architecture Discipline

If the project has important architecture-specific execution boundaries, summarize them here instead of copying rules from another workspace.

Examples may include:
- module dependency discipline
- adapter or bridge responsibility boundaries
- orchestration layer boundaries
- LLM vs code responsibility boundaries
- persistence or write-path restrictions

Rules for writing this subsection:
- Only add it if the project actually has these boundaries.
- Do not add or expand it without explicit human approval.
- Keep it concise, operational, and project-specific.
- Combined token budget for all project-specific architecture-discipline subsections inside `CLAUDE.md`: max 800 tokens.
- If more detail is needed, move it to a companion doc and link to that doc instead of expanding this file.

## 4. Documentation Governance and Context Loading

Use a dedicated companion doc such as `documentation-governance.md` for detailed documentation lifecycle rules.

This `CLAUDE.md` section should keep only the minimum execution-facing summary.

### 1. Documentation Governance Source Of Truth

- The project should define a dedicated documentation governance doc, such as `documentation-governance.md`, for active/archive rules, naming rules, archival rules, and documentation lifecycle management.
- `CLAUDE.md` should not duplicate the full governance policy.
- If a governance doc exists, it is the primary source for documentation lifecycle rules.

### 2. Active vs Historical Documents

- Active execution should prefer current code, current tests, and active docs first.
- Archive should be treated as reference material, not as the default execution source.
- Archived materials must not silently override direct human instructions or active execution sources.

### 3. Active Planning and Recovery Files

- If the project uses root tracking files such as `task_plan.md`, `findings.md`, and `progress.md`, document that they are active work surfaces only.
- For structure and operating discipline, refer to `$planning-with-files-zh`.

### 4. Context Loading Discipline

- Start with the smallest active document set that can route the current task safely.
- Load codemaps, plans, specs, or archive only when the current task genuinely needs them.
- If the project defines task-specific loading order, summarize it here briefly and point to `coding-agent-guide.md` or `documentation-governance.md` for detail.

### 5. Spec and Context Budget

- Spec text budget: max 40,000 tokens per session.
- If spec or design materials exceed that budget, summarize or route through companion docs instead of loading everything into the main execution context.
- Do not let `CLAUDE.md` become a substitute for detailed specs, codemaps, or governance records.
- For active `specs/` and `plans/` conventions, refer to `$using-superpowers`.

### 6. Sync Discipline

- If active plans, specs, tests, and implementation drift apart, resolve intended behavior first.
- Then update the active source of truth and bring dependent materials back into sync.

## 5. Subagent and Packet Discipline

The implementation packet subsection below is intentionally copied verbatim from the source workspace and should remain unchanged in derivative versions of this template unless the human explicitly approves a change.

The subagent subsection is Claude-specific and should be adapted to current Claude Code capabilities rather than copied from a Codex-oriented template.

### 7. Subagent Delegation Discipline

#### Dispatch

- For complex work, prefer decomposing the implementation into bounded tasks and dispatching subagents rather than keeping the whole execution on the main thread.
- Subagent dispatch must follow `subagent-driven-development`; do not improvise a parallel workflow outside that discipline when the task has already been decomposed.
- Choose the Claude subagent model according to task complexity instead of defaulting to the largest model.
- Prefer Claude Code model aliases over hardcoded dated model strings unless the project explicitly requires version pinning.
- Valid Claude Code model aliases currently include:
  - `haiku`
  - `sonnet`
  - `opus`
- If the workspace uses a default subagent model, document it through `CLAUDE_CODE_SUBAGENT_MODEL`.
- If the workspace uses a more specific Claude Code configuration surface for subagent model or effort control, document that mechanism explicitly and keep it aligned with current Anthropic docs.
- Supported effort levels are currently `low`, `medium`, `high`, and `max`.
- Official Claude Code docs currently describe `effort` support for Opus 4.6 and Sonnet 4.6, with `max` available on Opus 4.6 only.
- Recommended deployment guidance:
  - `haiku` with `low` or `medium` for lightweight read-only scans, keyword discovery, and mechanical support work
  - `sonnet` with `medium` or `high` for most implementation packets, review packets, and balanced codebase work
  - `opus` with `medium` or `high` for high-risk debugging, architecture, or synthesis-heavy tasks
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

### 8. Implementation Packet Discipline

- Decompose implementation work into bounded packets before dispatch.
- Prefer one primary objective, one main module or surface area, and one verification path per packet.
- The default implementation packet should be the smallest unit that can complete one TDD loop and one review/fix/re-review loop without widening scope mid-flight.
- Each packet should explicitly declare its user-facing goal, owned files, default verification command, and whether it is safe to run in parallel with other packets.
- Prefer dispatching subagent packets that can own their focused tests, implement against them, run targeted verification, and return a reviewable result.
- If two packets share the same primary production file or the same primary test file, default to serial execution unless the plan explains why parallel work is still safe.
- If a packet grows across unrelated concerns, long execution chains, or multiple verification paths, split it again.

## 7. Blocker Protocol
When blocked during implementation:

1. Field missing producer → add the producer.
2. Output has no downstream entry → add to nearest shared contract.
3. Code forced to understand semantics → convert to LLM three-stage pattern.
4. Naming conflict → prefer the current branch canonical name, then sync code/spec/tests.

STOP and wait for human if the fix would change:

- Author-visible control model or Editor Page boundaries.
- Core domain object boundaries (Scene, Phase, Beat).
- Public API semantics or the Deterministic Bridge persistence flow.

## 8. Testing and Verification

- **TDD mandatory**: write test → RED → implement → GREEN.
- Coverage minimum: 80%.
- If the project has fixtures, packaged content, or externalized data, define the project-specific anti-hardcoding rule for test assertions here.
- Prefer targeted suites while iterating, and list the project-specific commands here:
  - `<test command>`
  - `<test command>`
  - `<test command>`
  - `<type-check command>`
  - `<simulation or integration command>`
- If the work touches route integrity, subsystem boundaries, prompt projection, persistence flow, or environment-specific verification harnesses, include the relevant project-specific verification suite in the loop.
- Run `<build command>` for app-surface changes before calling work complete.
- Run `<full test command>` before calling work complete.

## 9. Companion Docs

In NHK-managed workspaces, the following companion docs are mandatory even for simple projects:

- `coding-agent-guide.md`
- `documentation-governance.md`

They may stay minimal in a simple repository, but they should still exist as stable routing and governance surfaces.

Complexity still matters for heavier companion materials.

File-map guidance:
- Simple workspaces may keep a very short key-path summary inline in `CLAUDE.md` if the file remains within the line budget.
- Complex workspaces should move document-surface maps and key-path inventories into `documentation-governance.md` or another dedicated companion doc.
- Code/file maps, task-routing detail, and implementation-oriented guidance should live in `coding-agent-guide.md`, not here.

For medium-complexity or complex projects, consider adding:
- `task_plan.md`, `findings.md`, `progress.md` for multi-session continuity
- `docs/codemaps/` for module relationships
- `docs/specs/` or equivalent for active design specs
- `docs/plans/` or equivalent for execution plans
- dedicated simulation, tooling, or environment guides
- a small architecture map for subsystem boundaries

Recommended reference:
- For `task_plan.md`, `findings.md`, and `progress.md`, refer to `$planning-with-files-zh`.
- For `docs/specs/`, `docs/plans/`, and related superpowers-oriented workflow structure, refer to `$using-superpowers`.

## 10. Git and Delivery

Fill in:
- active repository
- active development branch
- whether `main` is primary, mirrored, or protected
- default PR target branch

General rules:
- Commit format: `<type>: <description>` (e.g., `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).
- PRs should target `<active development branch>` unless the human explicitly says otherwise.
- Human review required before merge.
- When working from a Plan in `<plan directory>`, check off tasks as you complete them.
- If the workspace uses a todo list outside the plan system, update it as each task completes.
- Do not treat code changes as complete until the required verification commands have passed
