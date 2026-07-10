[[TEMPLATE_ONLY:BEGIN]]
# AGENTS.md Generation Contract

Use this template to produce a standalone `AGENTS.md` for an NHK-managed workspace. It is a generation contract, not a final instruction file.

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

Hard line limits for the final file:
- simple: 100 lines
- medium: 125 lines
- complex: 150 lines

There is no minimum line count. Never add text to fill a budget. Move detailed file maps, architecture notes, commands, and lifecycle procedures into companion docs when the final file would exceed its selected limit.

Source-template hard limit: 190 lines.

Final cleanup:
- No marker, generation-contract text, placeholders, suggested content, or template instructions remain.
- All seven required top-level headings are present in order and no extra top-level heading is invented.
- Project facts are current, concise, and consistent with the companion docs.
- The selected line limit is satisfied.
[[TEMPLATE_ONLY:END]]

[[FINAL_ADAPT:BEGIN]]
## Project Map

Replace this guidance with the shortest useful map of the actual workspace:
- purpose, active repository, canonical branch, and implementation or content type
- first-read paths and the source of truth for the current task
- only the subsystem, write, generated-artifact, and active/archive boundaries needed for safe work

Point to `coding-agent-guide.md` for detail. Do not turn this section into a product brief or full file inventory.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Execution Rules

- Start from the human's requested outcome and define completion before choosing an implementation path.
- Prefer the smallest direct change that resolves the request and can be verified.
- Keep validation, schema, path, reference-integrity, and persistence guarantees deterministic.
- Preserve the project's declared sources of truth and do not hand-edit generated artifacts unless the project explicitly requires it.
- When instructions, implementation, tests, and active docs disagree, resolve intended behavior first, then bring them back into sync.
- Reuse an installed or explicitly adopted peer workflow when it fits; do not pretend an unavailable workflow is installed.
[[FINAL_VERBATIM:END]]

[[FINAL_ADAPT:BEGIN]]
### Project-specific Boundaries

Replace this guidance with only the real data, state, module, dependency, write-path, or deterministic-versus-heuristic rules for this workspace. Omit rules that do not apply and route deeper architecture detail to `coding-agent-guide.md`.
[[FINAL_ADAPT:END]]

[[FINAL_VERBATIM:BEGIN]]
## Context and Documentation

- `coding-agent-guide.md`, `documentation-governance.md`, `archive/`, and `archive/README.md` are the stable NHK foundation.
- Treat `documentation-governance.md` as the source of truth for documentation lifecycle rules.
- Load the smallest active context that safely routes the task; prefer current implementation, tests, and active docs before historical material.
- Treat archive as reference material, not a default execution source.
- Keep existing plans, task lists, findings, and progress records aligned with actual status; create heavier tracking only when the work needs it.
- Use planning or execution workflows only when they are installed or explicitly adopted for the current run.
- Consider archive only for a specific workstream with completion evidence and related materials; ask before archiving and never archive automatically.
[[FINAL_VERBATIM:END]]

[[OPTIONAL_BY_COMPLEXITY:BEGIN]]
### Additional Context for Medium or Complex Workspaces

Name only the active plans, specs, codemaps, recovery files, or environment guides that actually exist and materially improve routing. Keep their lifecycle rules in `documentation-governance.md`.
[[OPTIONAL_BY_COMPLEXITY:END]]

[[FINAL_VERBATIM:BEGIN]]
## Subagents and Packets

- Dispatch only work that forms an independent, reviewable packet, and use the fewest workers needed to complete the task.
- The main thread's model and reasoning effort are the default cost ceiling for each worker, not a combined concurrency budget.
- A lower-cost configuration may be used only when it is known to support the task and is unlikely to increase total cost through retries.
- Obtain human approval before any known increase in model cost or reasoning effort. If support or relative cost is unclear, inherit the current configuration, keep the work on the main thread, or ask; do not guess.
- Do not allow recursive delegation unless both the plan and the human explicitly authorize it.
- Run packets serially when they overlap in files, generated artifacts, mutable state, service state, or verification artifacts.
- Every dispatch brief must state the objective, read/write authority, owned scope, success criteria, verification method, forbidden actions, and expected return.
- A timeout is not proof of a blocker. Check actual progress before asking, replacing, or ending a worker, and close idle workers after their work is complete.
- The main thread owns integration, cross-packet verification, and the final result.
[[FINAL_VERBATIM:END]]

[[FINAL_VERBATIM:BEGIN]]
### Codex Worker Boundary

- Ultra is reserved for main-thread orchestration and must never be assigned to a worker.
- Do not turn current model catalogs or effort tables into standing project instructions.
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
