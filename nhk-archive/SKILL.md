---
name: nhk-archive
description: Archive one completed NHK workstream when the human has explicitly approved its active-to-archive transition.
---

# NHK Archive

Use this skill only for the active-to-archive transition of one completed workstream.

## Router Handoff

Reuse a `welcome-to-nhk` handoff only when it is for the current workspace and current NHK run, and its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, hand off and do not continue archive.

Use the handoff's workspace workflow, workstream owner, capability, instruction, topology, and complete-foundation state as the archive input. Apply the archive transition of the workflow that owns this workstream. Do not persist the handoff. Any preceding bootstrap or upkeep route must finish and rerun `welcome-to-nhk` before archive may resume.

## Human Archive Gate

- Confirm the named workstream and evidence that it met its required completion and verification gates before proposing the transition.
- If the current context does not already contain a clear yes for this specific workstream, ask whether to archive it now.
- Do not move, rename, copy into archive, reset, or clear anything before that yes.
- If the user declines or remains ambiguous, keep the workstream active and stop.

## Workstream Identity And Materials

Choose one stable identity already supported by the active materials, such as a dated topic slug, plan/spec name, initiative, or user-provided name. If multiple identities remain plausible, ask.

Select related materials in this order:

1. the workstream's authoritative spec, plan, or tracker records, including its completion and verification evidence
2. workstream-specific recovery or progress records, including applicable `task_plan.md`, `progress.md`, and `findings.md`
3. named supporting materials whose content and identity associate them with the completed workstream

Archive only materials that clearly belong to that identity. Completed implementation plans may follow their owning workflow's transition. Keep `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, and `documentation-governance.md`, canonical instructions, shared domain docs, and `docs/agents/` as stable active references. Keep unrelated live plans and shared tracking in use.

## Naming And Index Contract

When creating or repairing the archive index row, read `../references/archive-readme-template.md`. Add or update one row in `archive/README.md` for the confirmed identity, with the date, location, verified materials, and an optional short note. Reuse a matching row on retry. Preserve unrelated entries. In a Matt workspace, create `archive/` and its index when first needed for an explicitly approved archive.

## Matt Transition

1. Record the confirmed identity, the authoritative source paths or URLs, and the completion and verification evidence to retain.
2. Prepare the index row with Markdown links to the actual local records (relative to the index) or the canonical tracker URLs. Locate any additional related evidence through this row. Keep local source files and tracking in place. Reference remote items by URL only, with no duplicated issue material or tracker changes.
3. Verify local references and report any remote access that remains unverified. Verify the row from its staged location and match each local path or confirmed URL to its recorded identity. Use read-only tracker access where available. If permissions or connectivity prevent reading a confirmed remote URL, note that limit in the index and delivery; local verification does not prove remote access. If a reference is ambiguous or points to the wrong material, resolve it before recording the transition.
4. Save the verified row and recheck its local references from `archive/README.md`. Update active descriptions and governance references for the completion as needed while preserving the evidence, original tracker state, and any tracking still in use.

## Superpowers Transition

1. Record the confirmed identity and exact related material. Prefer a unique container such as `archive/<date>-<topic>/`; in a flat archive include the identity in each archived plan, spec, and tracking filename.
2. Stage copies without removing the active originals, then update the index row.
3. Verify each archived copy is readable, belongs to the workstream, and uses an unambiguous name. Verify the index resolves to the real destination and accurately lists the materials.
4. Confirm no other live workstream depends on any active original or tracking file selected for transition.
5. After these checks pass, complete the governed move by removing active originals when required. Update active descriptions and `documentation-governance.md` while retaining historical records. Update `coding-agent-guide.md` only if a Task Routing row actually points to moved material.
6. Reset or clear root tracking only after a verified move and only when it is no longer shared and workspace governance calls for reuse.

If a copy, link, identity, or index fails verification, preserve every active original and tracking file. Repair the staged archive and verify it before marking the transition complete.

## Delivery

Report the confirmed identity, index location and referenced or copied materials, verification performed and its limits, and the current active surfaces and tracking state. If a dependency was adopted, name the missing skill and report manual use of its conventions for this NHK run.
