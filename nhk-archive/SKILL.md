---
name: nhk-archive
description: Archive one completed NHK workstream with the human’s approval, or verify its existing archive on retry.
---

# NHK Archive

## Router Handoff

Reuse a `welcome-to-nhk` handoff only for the current workspace and current NHK run when its **Route** selects this skill. If the handoff is absent, unresolved, or stale, run `welcome-to-nhk` first. If it selects another route, do not continue archive. Complete that route and rerun the router.

## Before writing

Identify the workstream, its owning workflow, its records, and the evidence that its required checks passed. On a retry, consult its existing row in `archive/README.md` for materials already moved.

Archive only with the human’s explicit approval for this workstream. Reuse approval already given for the same transition. If the work is complete and consent is unclear, ask once and leave the files and tracker as they are. A decline leaves the work active.

Select only records belonging to that workstream. Keep the canonical instructions, domain docs, `docs/agents/`, and the five companions active: `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, and `documentation-governance.md`.

## Record the archive

Use the owning workflow even when the workspace default differs. Read `../references/archive-readme-template.md` for the row format. Reuse the existing identity, row, archive date and destination on retry. Preserve unrelated entries.

### Matt

1. Prepare one row linking the spec, tickets and completion evidence for `archive/README.md`. Create the index on the first approved archive in a Matt workspace. Keep local sources and tracking in place. Link remote tracker items by canonical URL and leave their contents and status intact.
2. Open local links relative to the index and check they lead to the named records. Verify remote identities with read-only access when available. If a confirmed URL is inaccessible, record that limit in the row and delivery. Save the row once its targets and completion evidence identify this workstream.

### Superpowers

1. Copy the selected spec, plan and workstream-specific evidence to a uniquely named destination. Keep the active originals while staging. On retry, reuse existing copies after checking their identity and contents.
2. Link the destination and list its materials in the index. Open the links from the index and compare each copy with its active original while that original is available. If verification fails, preserve the originals and repair the staged archive before proceeding.
3. Once the copies and index are verified, remove active originals only as workspace governance requires and only when other work no longer needs them. Reset root tracking only after the verified move, when governance calls for reuse and no live workstream shares it.

## Finish

Check that the identity has one retrievable index row. Update active references affected by the transition. Report the row, materials, verification limits, and what stayed active. Report any manual use of an adopted dependency.
