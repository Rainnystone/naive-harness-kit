# Documentation Governance Template

## Purpose

Use this template to create `documentation-governance.md`, the workspace contract for the selected workflow, active documentation, loading, and archive transitions. Production routes belong in `coding-agent-guide.md`, task sizing in `implementation-planning.md`, worker rules in `worker-policy.md`, and recovery rules in `execution-recovery.md`.

## Template Contract

- Final file hard limit: 100 lines. There is no minimum.
- Replace examples with real workspace paths and remove all template guidance.
- Keep durable rules and current document surfaces. Active status and archive rows belong in their own records.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import for it.

## Required Final Shape

Start with `# Documentation Governance`, then use the following second-level headings in order.

### Document Roles

Record exactly one active line, `Workflow: Matt` or `Workflow: Superpowers`, for the workspace default confirmed by routing. Keep workstream ownership in its plan or tracker. A changed default applies to the next workstream. Manual adoption belongs in the current run, outside this file.

Define the canonical instruction source, `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, this governance companion, and configured active and archive surfaces. State that companion paths load on demand. A thin `CLAUDE.md` may import canonical `AGENTS.md`; use literal paths for the companions.

### Active Documentation Surfaces

List existing active specs, plans, trackers, recovery records, and other on-demand docs with their purpose. Identify the authoritative record for task state. Describe optional root tracking only when it exists and serves a genuine need.

For configured Matt capabilities, identify relevant `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and optional `docs/agents/triage-labels.md`. Domain docs and ADRs are created when actual content warrants them. Record a legacy domain file only when its content confirms the role.

### Workspace and Document Map

Map instruction, routing, active documentation, optional tracking, and existing archive paths. State the archive condition for the selected workflow. Keep production modules in the coding route.

### Lifecycle Rules

- Keep all five stable companions active; archive completed implementation plans and recovery records under their owning workflow's transition.
- Prefer current implementation, tests, and active docs. Start historical retrieval at `archive/README.md` when it exists.
- Ask about archive only for one identifiable workstream with completion evidence and related materials. Explicit approval is required for its transition.
- Upkeep may repair descriptions and links. File moves, removal, archive, and tracking resets belong to authorized transitions.

### Naming and Loading

- Use consistent, searchable names for specs and plans. Include the workstream identity in archive container names and tracking copies when making a copy.
- Load the smallest active context that safely answers the task. Load worker and recovery companions only under the conditions in canonical instructions.

### Archive Transition Invariants

Preserve the invariant about explicit human approval and use the rules for the recorded default. A workstream already owned by the other workflow uses that workflow's transition.

- **Both workflows.** Obtain explicit human approval before archiving the named workstream.
- **Matt.** Create the archive index on the first explicitly approved archive. Verify local references and preserve local sources and tracking. Use remote links for tracker items and record any limits on remote verification.
- **Superpowers.** The archive foundation is required. Copy selected materials and update the archive index before verification and removal of active originals. If verification fails, preserve every active original and repair the staged archive first. Reset or clear tracking only after the verified move and when no other live workstream depends on it.

### Project-Specific Exceptions

Include this optional final section only for a real exception. Name the genuine authorization for the exception.

## Final Check

- The final file meets the line limit, heading order, workflow marker, and applicable archive rules.
- Every documented surface exists or is explicitly conditional. Links and identities remain traceable.
- All five companions remain distinct, active, literal-path surfaces.
- The file contains only the workspace document map and durable governance rules.
