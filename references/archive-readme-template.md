# Archive Index Template

## What This File Is For

This file is the root archive index for the workspace.

Its job is to make archived workstreams easy to find without turning `documentation-governance.md` or `coding-agent-guide.md` into archive catalogs.

This file is not:
- the active execution entrypoint
- the full archive policy
- a priority ranking of archived work

Template usage rules:
- This file is a template, not a final `archive/README.md`.
- Instructional text such as `Document`, `Recommended`, and similar guidance should not remain in the final file.
- Keep the final file short and index-oriented.

## Recommended Bootstrap Stub

The initial root archive README should already contain:

- a title
- one sentence stating that the file indexes archived workstreams and is not the active execution surface
- the archived-workstreams table with headers in place

Recommended minimum stub:

```md
# Archive

This file indexes archived workstreams. It is a retrieval surface, not the active execution entrypoint.

| Workstream | Archived On | Location | Included Materials | Notes |
| --- | --- | --- | --- | --- |
```

## Archived Workstreams

Use a flat table rather than nested archive narration.

Recommended shape:

| Workstream | Archived On | Location | Included Materials | Notes |
| --- | --- | --- | --- | --- |
| `...` | `YYYY-MM-DD` | `archive/...` | `spec, plan, findings` | `optional short note` |

Write each row so a coding agent can quickly decide whether to open that archived workstream.

## Maintenance Rule

- `nhk-bootstrap` should create this file as part of the standard archive surface.
- `nhk-archive` should add or update one row after each human-approved archive transition.
- Keep this file as a flat index. Do not grow it into an archive policy doc or a narrative history.
