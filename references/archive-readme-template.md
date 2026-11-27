# Archive Index Template

## Purpose

Use this template to create `archive/README.md`, the retrieval index for completed workstreams. Create the empty index during Superpowers bootstrap. In a Matt workspace, create it on the first explicitly approved archive.

## Final Shape

Generate this minimum shape, then add verified rows as workstreams are archived:

```md
# Archive

This file indexes archived workstreams. Use it for historical retrieval.

| Workstream | Archived On | Location | Included Materials | Notes |
| --- | --- | --- | --- | --- |
```

## Row Contract

- Keep one row per archived workstream, using a stable workstream identity and a `YYYY-MM-DD` archive date.
- For a Superpowers move, link to the real, uniquely named archive destination and list only materials confirmed in the archive copy.
- For a Matt archive, link to the actual local source paths from this index and list the referenced materials. Use confirmed tracker URLs as remote references. Keep referenced local files in place.
- Keep Notes short. If authorized access to a confirmed remote reference could not be verified, distinguish that from verified local links and copies.
- Use the row to retrieve the archived workstream. Keep policy, active status, cleanup steps, and narrative history in their owning surfaces.
