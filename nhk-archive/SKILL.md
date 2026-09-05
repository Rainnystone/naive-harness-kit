---
name: nhk-archive
description: Archive one completed NHK workstream when the human has explicitly approved its active-to-archive transition.
---

# NHK Archive

Use this skill only for the active-to-archive transition of one completed workstream.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue archive.

Use the handoff's dependency, instruction, topology, and complete-foundation state as the archive input. Do not persist the handoff. A bootstrap route must finish and rerun `welcome-to-nhk` before archive may resume.

## Human Archive Gate

- If the current context does not already contain a clear yes for this specific workstream, ask whether to archive it now.
- Do not move, rename, copy into archive, reset, or clear anything before that yes.
- If the user declines or remains ambiguous, keep the workstream active and stop.

## Workstream Identity And Materials

Choose one stable identity already supported by the active materials, such as a dated topic slug, plan/spec name, initiative, or user-provided name. If multiple identities remain plausible, ask.

Select related materials in this order:

1. active spec and plan surfaces used by the installed or explicitly adopted planning workflow
2. active root tracking such as `task_plan.md`, `progress.md`, and `findings.md`
3. filenames, directories, dates, and topic slugs matching the chosen identity
4. file content and current context when naming signals are incomplete

Archive only materials that clearly belong to that identity. Completed implementation plans may move with their workstream, but the stable companions `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, and `documentation-governance.md` never do. Do not archive unrelated live plans, shared instruction or governance docs, or tracking still used by another workstream.

## Naming And Index Contract

When creating or repairing the archive index row, read `../references/archive-readme-template.md`. Do not load unrelated instruction or companion templates during archive.

- Prefer one unique archive container such as `archive/<date>-<topic>/`.
- If files share a flat archive directory, include the workstream identity in every archived plan, spec, and tracking filename.
- Never accumulate indistinguishable generic tracking filenames in a shared archive.
- Add or update exactly one resolvable row in `archive/README.md` with identity, date, location, included materials, and an optional short note.

## Transition And Verification Order

1. Record the confirmed workstream identity and exact related-material set.
2. Create the uniquely named archive destination and stage copies of the selected completed materials without removing the active originals.
3. Update the archive index row.
4. Verify every expected archived copy exists, is readable, belongs to the workstream, and uses an unambiguous name.
5. Verify the index row resolves to the real archive location and accurately lists the included materials.
6. Verify no other live workstream depends on any active original or root tracking file selected for transition.
7. Only after steps 4-6 pass, complete the governed move by removing active originals when required, then update active documentation and `documentation-governance.md` while keeping historical records intact. Update `coding-agent-guide.md` only when a real Task Routing row points to material that moved.
8. Only after that verified move may root tracking for this workstream be reset or cleared, and only when workspace governance calls for reuse.

If archive copy, naming, content, or index verification fails, preserve every active original and root tracking file, repair the archive result, and rerun verification first. Never remove an active original before the staged archive and index have passed verification.

## Delivery

Report the confirmed identity, archived location, included materials, index update, verification performed, current active surface, and whether root tracking was reset. If a dependency was adopted, say it was not installed and was followed manually for this NHK run.
