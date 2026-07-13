# Archive Index Template

## Purpose

Use this template to create `archive/README.md`, the retrieval index for completed workstreams. It is not an active execution source or an archive procedure.

## Final Shape

Generate this minimum shape, then add verified rows as workstreams are archived:

```md
# Archive

This file indexes archived workstreams. It is a retrieval surface, not the active execution entrypoint.

| Workstream | Archived On | Location | Included Materials | Notes |
| --- | --- | --- | --- | --- |
```

## Row Contract

- Keep one resolvable row per archived workstream.
- Use a stable workstream identity and a `YYYY-MM-DD` archive date.
- Point `Location` to the real, uniquely named archive destination.
- List only materials confirmed in the verified archive copy.
- Keep `Notes` optional and short.
- Do not duplicate archive policy, active status, cleanup steps, or narrative history here.
