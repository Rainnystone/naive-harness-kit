[[TEMPLATE_ONLY:BEGIN]]
# CLAUDE.md Generation Contract

Choose exactly one mode before producing any final content.

Thin mode:
- Use thin mode when `AGENTS.md` is the canonical instruction source and Claude Code supports importing it.
- Write `@AGENTS.md` or `@./AGENTS.md` as its own nonblank line, outside code fences, quotes, and comments.
- Add only necessary Claude-specific notes and keep the entire final file at or below 35 lines.
- Do not `@` import `coding-agent-guide.md`, `implementation-planning.md`, or `documentation-governance.md`; canonical AGENTS routes to their literal paths on demand.
- Then stop. Do not read, adapt, or copy any standalone final-producing block below.

Standalone mode:
- Use standalone mode when `CLAUDE.md` is the canonical instruction source.
- Do not import AGENTS or any companion doc. Refer to companion docs with backticked literal paths and load them only when the task requires.
- Process the final-producing blocks below and follow the standalone contract.

This source is a generation contract, not a final instruction file.

Marker protocol:
- Keep exactly these four marker types: `TEMPLATE_ONLY`, `FINAL_VERBATIM`, `FINAL_ADAPT`, and `OPTIONAL_BY_COMPLEXITY`.
- Markers must be paired, flat, ordered, and never nested.
- Apart from marker boundary lines, every nonblank semantic line in this source template must be inside one marker block.
- Every final-producing block must have a first Markdown heading, and that first heading must be unique across the template.
- Never copy marker lines or `TEMPLATE_ONLY` content into the final file.
- Copy `FINAL_VERBATIM` content exactly unless the human explicitly approves a change.
- Rewrite every `FINAL_ADAPT` block with actual workspace facts; do not leave generation prompts behind.
- Include `OPTIONAL_BY_COMPLEXITY` only when the selected complexity and real project needs justify it.

The standalone final file must use these seven top-level headings, once each and in this order:
1. Project Map
2. Execution Rules
3. Context and Documentation
4. Subagents and Packets
5. Blockers and Human Approval
6. Testing and Verification
7. Git and Delivery

Hard line limits for a standalone final file:
- simple: 100 lines
- medium: 125 lines
- complex: 150 lines

There is no minimum line count. Never add text to fill a budget. Move detailed file maps, architecture notes, commands, and lifecycle procedures into companion docs when the final file would exceed its selected limit.

Source-template hard limit: 200 lines.

Final cleanup:
- No marker, generation-contract text, placeholders, suggested content, or template instructions remain.
- All seven required top-level headings are present in order and no extra top-level heading is invented.
- Project facts are current, concise, and consistent with the companion docs.
- The selected line limit is satisfied.
[[TEMPLATE_ONLY:END]]

[[FINAL_ADAPT:BEGIN]]
## Project Map

Write two to four bullets:
- identify the project in one sentence
- state that `coding-agent-guide.md` is the canonical route from task or symptom to code entry and first-pass verification
- add at most two safety-critical boundaries that must be known before opening files

Do not include a directory tree, module inventory, active branch or workstream, inferable stack facts, or a separate codemap.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Execution Rules

- Start from the human's requested outcome and define completion before choosing an implementation path.
- Prefer the smallest direct change that resolves the request and can be verified.
- Keep validation, schema, path, reference-integrity, and persistence guarantees deterministic.
- Preserve the project's declared sources of truth and do not hand-edit generated artifacts unless the project explicitly requires it.
- When instructions, implementation, tests, and active docs disagree, resolve intended behavior first, then bring them back into sync.
- Reuse an installed or explicitly adopted peer workflow when it fits; do not pretend an unavailable workflow is installed.
- Five failed fix–verify or fix–review rounds on the same acceptance gap trigger a mandatory stop. Invoke or restart `systematic-debugging`, count those rounds as failed fixes, and forbid a sixth fix until root-cause and architecture reassessment is complete.
[[FINAL_VERBATIM:END]]

[[OPTIONAL_BY_COMPLEXITY:BEGIN]]
### Additional Project Boundaries

Include only when the selected medium or complex workspace has a safety boundary that cannot fit in the two Project Map slots. Keep it operational and route task-specific detail to `coding-agent-guide.md`.
[[OPTIONAL_BY_COMPLEXITY:END]]

[[FINAL_VERBATIM:BEGIN]]
## Context and Documentation

- `coding-agent-guide.md`, `implementation-planning.md`, `documentation-governance.md`, `archive/`, and `archive/README.md` are the stable NHK foundation.
- Treat `documentation-governance.md` as the source of truth for documentation lifecycle rules.
- Before writing, approving, or materially revising an implementation plan, read `implementation-planning.md`; do not dispatch a task that fails its packet contract.
- Do not load `implementation-planning.md` for ordinary coding, review, or debugging.
- Load the smallest active context that safely routes the task; prefer current implementation, tests, and active docs before historical material.
- Treat archive as reference material, not a default execution source.
- Keep existing plans, task lists, findings, and progress records aligned with actual status; create heavier tracking only when the work needs it.
- Use planning or execution workflows only when they are installed or explicitly adopted for the current run.
- Consider archive only for a specific workstream with completion evidence and related materials; ask before archiving and never archive automatically.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
## Subagents and Packets

- Dispatch only work that forms an independent, reviewable packet, and use the fewest workers needed to complete the task.
- Choose the lowest-cost configuration that can reliably complete the packet; the main thread's model and effort remain the cost ceiling for each worker, not a combined concurrency budget.
- If a packet contains more than one independently acceptable result, test cycle, or reviewer gate, split it before increasing worker capability.
- Obtain human approval before assigning a worker above the main-thread ceiling. If support or relative capability is unclear, keep the work on the main thread or ask; do not guess.
- Do not allow recursive delegation unless the plan and the human authorize it for a named packet.
- Run packets serially when they overlap in files, generated artifacts, mutable state, service state, or verification artifacts.
- Every dispatch brief must state the objective, read/write authority, owned scope, success criteria, verification method, forbidden actions, and expected return.
- A timeout is not proof of a blocker. Check actual progress before asking, replacing, or ending a worker, and close idle workers after their work is complete.
- The main thread owns integration, cross-packet verification, and the final result.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
## Blockers and Human Approval

- Exhaust safe, in-scope checks before declaring a blocker.
- Stop and ask before changing a public API, persistence semantics, data model, user-facing workflow, documented architecture boundary, or other contract the human did not authorize.
- Do not hide unresolved problems behind a fallback, heuristic patch, silent scope expansion, or fabricated success.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project-specific Approval Boundaries

Replace this guidance with any additional project-specific stop conditions and the smallest safe diagnostic or repair sequence. Omit the subsection if the shared rules are sufficient.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Testing and Verification

- For production behavior changes, use TDD: verify a meaningful failing test, implement the smallest fix, verify it passes, then refactor safely.
- Follow the project's existing coverage gate without raising, lowering, or bypassing it silently.
- If no coverage gate exists, report that fact and still test the changed behavior and important error paths.
- Run the strongest relevant checks available for the changed surface, including real or representative inputs when practical.
- Inspect visual or interactive output directly when the task changes it.
- Do not claim completion until required checks pass, or clearly report what could not be run and why.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project Verification Commands

Replace this guidance with the real targeted test, full test, type-check, lint, build, coverage, and smoke commands that exist. Include only applicable commands and identify the final delivery gate.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Git and Delivery

- Preserve unrelated human changes and avoid destructive Git operations unless the human explicitly requests them.
- Record only repository policies that actually exist; do not invent branch, commit-message, review, merge, or pull-request conventions.
- Keep active plans and task tracking current as work completes.
- Summarize the result, verification performed, remaining uncertainty, and any action still needed from the human.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project Git and Delivery Policy

Replace this guidance with the actual repository, canonical and active branches, protected-branch rules, commit policy, review requirements, pull-request target, and release or handoff checks. Omit unknown policies instead of guessing.
[[FINAL_ADAPT:END]]
