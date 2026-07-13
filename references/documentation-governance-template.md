# Documentation Governance Template

## Purpose

Use this template to create `documentation-governance.md`, the workspace contract for where active documentation lives, how it is loaded, and when completed material may move to archive.

This file maps documentation surfaces, not production modules. Coding routes belong in `coding-agent-guide.md`; detailed archive execution belongs to `nhk-archive` when that skill is available or explicitly adopted.

## Template Contract

- Final file hard limit: 100 lines. There is no minimum.
- Replace examples with real workspace paths and remove all template guidance.
- Keep durable rules and current document surfaces; do not copy active task status or an archive log into this file.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import for it.

## Relationship to Other Files

- Canonical `AGENTS.md` or standalone `CLAUDE.md` defines stable working rules.
- A thin `CLAUDE.md` may import canonical AGENTS; it does not import this document.
- `coding-agent-guide.md` routes coding tasks to code and targeted verification.
- Active plans, specs, and optional root tracking hold work in progress.
- `archive/` stores historical material, and `archive/README.md` is its resolvable index.

## Required Final Shape

Start with `# Documentation Governance`, then use the following second-level headings in order.

### Document Roles

Define the canonical instruction source, routing guide, this governance file, active work surfaces, archive root, and archive index in a compact table or list. State that ordinary companion paths are loaded on demand rather than imported into Claude startup context.

### Active Documentation Surfaces

List only active specs, plans, tracking, recovery, or environment docs that really exist. For each surface, state its purpose and what must leave it after human-approved archival. Root tracking remains optional.

### Workspace and Document Map

Map only instruction, routing, active documentation, optional tracking, archive, and archive-index paths. Do not list production modules, entry files, or a repository tree.

### Lifecycle Rules

- Keep active and archived documentation separate.
- Prefer current implementation, tests, and active docs; archive is not a default execution source.
- Never infer completion or archive automatically.
- Ask about archive only for one identifiable workstream with completion evidence and related materials.
- Upkeep may repair descriptions and links but never move, rename, delete, clear, reset, or archive files.

### Naming and Loading

- Give active specs and plans a consistent, searchable naming scheme.
- Archived containers and tracking copies include a workstream identity; do not accumulate indistinguishable generic filenames.
- Load the smallest active context that safely answers the task.
- Start historical lookup at `archive/README.md`, then open only the relevant archive location.

### Archive Transition Invariants

The final file must preserve these rules without expanding them into an operating manual:

- Explicit human approval is required before archiving the named workstream.
- Copy the selected materials and update the archive index before verification and before removing active originals.
- If verification fails, preserve every active original and repair the staged archive first.
- Reset or clear tracking only when the verified move is complete and no other live workstream depends on it.

### Project-Specific Exceptions

Include this optional final section only for a real exception that changes the rules above. Name who or what authorizes the exception; never invent one to make cleanup easier.

## Final Check

- The file is at most 100 lines and uses the required headings in order.
- Every documented surface exists or is explicitly conditional.
- Active/archive links resolve, names remain distinguishable, and the archive index is not duplicated here.
- No production code map, detailed archive procedure, template prompt, placeholder, or stale workstream status remains.
