---
name: nhk-archive
description: Use when an NHK-managed workspace is at the human-approved archive handoff for one completed workstream.
---

# NHK Archive

Use this skill only for the active-to-archive transition of one completed workstream.

## Prerequisite Order

1. Confirm `superpowers` and `planning-with-files` are installed, enabled, or explicitly adopted for this NHK run. Adopt is temporary manual authorization, not installation.
2. Resolve the canonical instruction topology. A valid thin import is a non-quoted, non-comment, non-fenced line exactly `@AGENTS.md` or `@./AGENTS.md` after trimming.
3. Confirm `coding-agent-guide.md`, `documentation-governance.md`, `archive/`, and `archive/README.md` all exist.

If instruction topology is ambiguous or broken, ask for the required choice and route through `welcome-to-nhk`. If any foundation surface is missing, route through `welcome-to-nhk` to `nhk-bootstrap`. Do not begin archive movement first.

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

Archive only materials that clearly belong to that identity. Do not archive unrelated live plans, shared instruction or governance docs, or tracking still used by another workstream.

## Naming And Index Contract

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

## Local References

- `../references/validation-scenarios.md`
- `../references/AGENTS-template.md`
- `../references/CLAUDE-template.md`
- `../references/coding-agent-guide-template.md`
- `../references/documentation-governance-template.md`
- `../references/archive-readme-template.md`
- `../references/dependency-setup.md`
