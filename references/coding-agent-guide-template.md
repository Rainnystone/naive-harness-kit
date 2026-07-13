# Coding Agent Guide Template

## Purpose

Use this template to create `coding-agent-guide.md`, the shortest practical route from an incoming coding task to the right first files and verification.

The routing table is the workspace's shallow code map. Do not create a second directory-based map, architecture manual, workstream tracker, or copy of the canonical instruction file.

## Template Contract

- Final file hard limit: 80 lines. There is no minimum.
- Replace every example with current project facts and remove all template guidance.
- Keep only routes that materially reduce blind browsing or failed verification attempts.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import for it.
- Put active work status in active plans or tracking, and documentation lifecycle rules in `documentation-governance.md`.

## Relationship to Other Files

- Canonical `AGENTS.md` or standalone `CLAUDE.md` defines execution, collaboration, approval, testing, and delivery rules.
- A thin `CLAUDE.md` may import canonical AGENTS; it does not import this guide.
- `coding-agent-guide.md` routes coding work.
- `documentation-governance.md` governs active and archived documentation.
- `archive/README.md` indexes historical workstreams and is consulted only when history is relevant.

## Required Final Shape

Start with `# Coding Agent Guide` and one sentence explaining that this file routes coding tasks. Then write the required routing table.

### Task Routing

Use exactly these columns:

| Task or Symptom | Read First | Likely Change Surface | Targeted Verification |
| --- | --- | --- | --- |
| `<incoming task or observable symptom>` | `<smallest useful first-read paths>` | `<probable owned files or directories>` | `<fastest relevant command or direct check>` |

Write rows from the user's task or symptom toward code, never from directory names toward descriptions.

- `Read First` names the smallest context that can confirm the route.
- `Likely Change Surface` is a starting boundary, not permission to edit every listed file.
- `Targeted Verification` gives the first useful feedback loop; canonical instructions still govern final delivery checks.
- Combine routes that lead to the same first files and verification.

### Shared Entry Points

Include this optional section only when a few files or commands genuinely serve several task types. Use a compact list; do not repeat routing-table rows.

### Search and Boundary Hints

Include this optional section only for high-value searches or non-obvious routing boundaries that prevent common detours. Deeper architecture belongs in existing project documentation, not a new NHK codemap.

## Final Check

- The file is at most 80 lines.
- The Task Routing table has all four required columns.
- Every path and command exists or is clearly marked as conditional project policy.
- No generated-file warning, safety boundary, or verification rule conflicts with canonical instructions.
- No template prompt, placeholder, volatile workstream status, full directory tree, or duplicated lifecycle procedure remains.
