---
name: nhk-archive
description: Use when an NHK-managed workspace is at the formal archive handoff for one completed workstream.
---

# NHK Archive

Use `nhk-archive` only for the active-to-archive transition of one completed workstream.

## Archive Gate

- If the current context does not already include a clear yes, ask the user explicitly whether this workstream should move to archive now.
- Do not move, rename, reset, or clear anything until the user gives a clear yes.
- If the user declines or stays ambiguous, keep the workstream active, keep active tracking files in place, and stop.

## Workstream Identity

Define the workstream identity before selecting materials.

- Prefer a stable identity already present in the active materials, such as a date-plus-topic slug, plan or spec name, initiative name, or an explicit user-provided workstream name.
- If multiple identities are plausible, ask the user which workstream is being archived.
- Use the chosen workstream identity to decide both relatedness and archive naming.

## Detection Priority

Determine related materials in this order:

1. Look for active spec/plan surfaces that follow `superpowers`-style naming and placement conventions, such as `docs/specs/`, `docs/plans/`, `specs/`, or `plans/`.
2. Look for active root tracking files that follow `planning-with-files` conventions, especially root `task_plan.md`, `progress.md`, and `findings.md`.
3. Use the established workstream identity to match filenames, directory names, and obvious date-plus-topic slugs.
4. If naming or placement signals are incomplete, fall back to content and context: read enough of the candidate files to determine whether they primarily describe the same workstream.
5. If filename signals, document contents, and current conversation context still do not converge on one clear set of related materials, ask the user before archiving.

## Related Materials

Archive only materials that belong to the same workstream identity.

Related materials normally include:

- completed specs and plans whose names, locations, or contents point to the same workstream
- root `task_plan.md`, `progress.md`, and `findings.md` only when their names or active contents primarily track that same workstream
- workstream-specific folders or notes already scoped to that identity

Do not archive:

- unrelated active plans, specs, or tracking files for another live workstream
- the active instruction file, `coding-agent-guide.md`, or `documentation-governance.md` themselves
- shared docs that still describe live work, except for updating their current-state references after the transition

## Naming Rules

- Archive the workstream into one uniquely named container, preferably a workstream folder such as `<date>-<topic>/`.
- If the archive layout does not use a workstream folder, rename every archived spec, plan, and tracking file to include the workstream identity, such as `<workstream>-spec.md`, `<workstream>-plan.md`, `<workstream>-task-plan.md`, `<workstream>-progress.md`, and `<workstream>-findings.md`.
- Never leave archived tracking files under indistinguishable generic names in a shared archive collection.

## Transition Order

1. Ask for and receive explicit user confirmation to archive this workstream.
2. Resolve the workstream identity.
3. Gather only the related materials for that identity.
4. Move the completed specs, plans, and related tracking records into the uniquely named archive container.
5. Ensure `archive/README.md` exists and add or update one row for the archived workstream.
6. The root archive index row should record:
   - workstream identity
   - archival date
   - archive location
   - main included materials
   - a short note only if needed
7. Update `coding-agent-guide.md` current execution state so it no longer presents the archived workstream as active and so it points to the remaining active surface, if any.
8. Update `documentation-governance.md` current-state or active-versus-archive references so the archive location and active/archive boundary remain accurate.
9. Only after the archive move is complete and the archived copies are named clearly may root `task_plan.md`, `progress.md`, and `findings.md` be cleared or reset.
10. Clear root tracking files only when they were the active surface for the archived workstream and no other live workstream still depends on them.

## Local References

Use local references to keep the transition aligned:

- `../references/validation-scenarios.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/archive-readme-template.md`
- `../references/dependency-setup.md`

These references are local alignment aids, not blind copy targets.
