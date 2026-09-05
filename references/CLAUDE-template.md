[[TEMPLATE_ONLY:BEGIN]]
# CLAUDE.md Generation Contract

Choose one mode before producing final content.

Thin mode:
- Use thin mode when `AGENTS.md` is canonical and Claude Code supports importing it.
- Put `@AGENTS.md` or `@./AGENTS.md` on its own active line. Add only necessary Claude-specific notes.
- Keep the complete file at or below 35 lines, then stop without processing standalone blocks.
- Never `@` import `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, or `documentation-governance.md`.

Standalone mode:
- Use standalone mode when `CLAUDE.md` is canonical. Do not import AGENTS or companion docs.
- Refer to companions with backticked literal paths and load them only under their stated conditions.

Marker protocol:
- Keep exactly `TEMPLATE_ONLY`, `FINAL_VERBATIM`, `FINAL_ADAPT`, and `OPTIONAL_BY_COMPLEXITY` markers.
- Markers are paired, flat, ordered, and never nested. Keep every semantic source line inside one block.
- Copy `FINAL_VERBATIM` exactly unless the human approves a change. Replace `FINAL_ADAPT` with workspace facts.
- Include `OPTIONAL_BY_COMPLEXITY` only for a real medium or complex need.
- Remove every marker, template instruction, prompt, and placeholder from the final file.

Use these seven top-level headings once each and in order: Project Map; Execution Rules; Context and Documentation; Subagents and Packets; Blockers and Human Approval; Testing and Verification; Git and Delivery.

Standalone line limits:
- simple: 100 lines
- medium: 125 lines
- complex: 150 lines

There is no minimum line count. Keep this source at or below 200 lines.
[[TEMPLATE_ONLY:END]]

[[FINAL_ADAPT:BEGIN]]
## Project Map

Write two to four bullets that identify the project and route coding work to `coding-agent-guide.md`. Add only safety-critical boundaries needed before opening files.

Omit directory trees, inventories, active status, inferable stack facts, and a separate codemap.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Execution Rules

- Start from the human's requested outcome and define completion before choosing an implementation path.
- Prefer the smallest direct change that resolves the request and can be verified.
- Keep validation, schema, path, reference-integrity, and persistence guarantees deterministic.
- Preserve declared sources of truth. Change generated artifacts only through the project's required process.
- Resolve intended behavior when instructions, implementation, tests, and active docs disagree, then restore consistency.
- Use an installed or explicitly adopted workflow when it fits. Do not claim an unavailable workflow.
- Use ordinary systematic debugging for bugs. Read `execution-recovery.md` when its stop or recovery triggers apply.
[[FINAL_VERBATIM:END]]

[[OPTIONAL_BY_COMPLEXITY:BEGIN]]
### Additional Project Boundaries

Include only a real safety boundary that cannot fit in Project Map. Route task-specific detail to `coding-agent-guide.md`.
[[OPTIONAL_BY_COMPLEXITY:END]]

[[FINAL_VERBATIM:BEGIN]]
## Context and Documentation

- The stable foundation includes `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, `documentation-governance.md`, `archive/`, and `archive/README.md`.
- Read `coding-agent-guide.md` to route a task or symptom to code and first-pass verification.
- Read `implementation-planning.md` before writing, approving, or materially revising an implementation plan.
- Read `worker-policy.md` only when orchestrating, dispatching, or reviewing workers. Load its common sections and the current platform section.
- Read `execution-recovery.md` only when a documented recovery trigger or exhausted review path applies.
- Treat `documentation-governance.md` as the source of truth for documentation lifecycle rules.
- Load the smallest active context that safely routes the task. Prefer implementation, tests, and active docs before history.
- Keep active plans and tracking aligned with actual status. Create heavier tracking only when the work needs it.
- Consider archive only for a completed, identifiable workstream. Ask before archiving and never archive automatically.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
## Subagents and Packets

- Dispatch only an independent, reviewable packet and use the fewest workers needed.
- Before dispatch or review, apply `worker-policy.md`; reuse unchanged rules already loaded for the current orchestration run.
- Keep each dispatch brief self-contained with its binding constraints, acceptance, authority, verification, and return contract.
- Run writes sequentially when files, generated artifacts, mutable state, services, or verification resources overlap.
- Check actual worker progress and lifecycle before acting on a timeout or replacing a worker.
- The main thread owns integration, cross-packet verification, and the final result.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
## Blockers and Human Approval

- Exhaust safe, in-scope checks before declaring a blocker.
- Ask before changing an unauthorized public contract, persistence meaning, data model, user workflow, or architecture boundary.
- Keep unresolved problems visible. Continue only within the accepted scope, evidence, and authority.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project-specific Approval Boundaries

Replace this block with additional project stop conditions and the smallest safe diagnostic path. Omit it when shared rules are sufficient.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Testing and Verification

- For production behavior changes, use TDD: establish a meaningful failure, implement the smallest fix, and verify it passes.
- Follow the existing coverage gate without silently changing or bypassing it.
- If no gate exists, report that fact and test the changed behavior and important error paths.
- Run the strongest relevant checks, including representative inputs and direct visual inspection when applicable.
- Claim completion only after required checks pass, or report exactly what could not be verified and why.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project Verification Commands

Replace this block with real targeted and final verification commands. Include only applicable commands and identify the delivery gate.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Git and Delivery

- Preserve unrelated human changes and use destructive Git operations only with explicit authorization.
- Record only repository policies that exist; omit unknown branch, commit, review, merge, or release conventions.
- Keep active plans and task tracking current as work completes.
- Report the result, verification, remaining uncertainty, and any action still needed from the human.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project Git and Delivery Policy

Replace this block with verified repository, branch, review, and release facts. Omit unknown policies instead of guessing.
[[FINAL_ADAPT:END]]
