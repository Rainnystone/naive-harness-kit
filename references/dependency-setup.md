# NHK Workflow Capability Setup

Use this reference when the current NHK route or workstream needs a workflow capability that cannot be invoked. Use the workspace default and current workstream ownership established by `welcome-to-nhk`.

## Workflow Sources

- Matt Pocock's engineering skills: <https://github.com/mattpocock/skills>
- Superpowers: <https://github.com/obra/superpowers>
- Planning with Files: <https://github.com/othmanadi/planning-with-files>

## Which Capability To Check

| Current work | Capability to check |
| --- | --- |
| Matt repository setup | `setup-matt-pocock-skills` when the work needs new or incomplete Matt configuration. Reuse verified existing configuration. |
| Matt domain, spec, ticketing, triage, or engineering work | The specific skill needed and the configured tracker access when the task reads or writes tracker records. |
| Superpowers spec, plan, or implementation work | The specific Superpowers skills needed to run that workflow. |
| File-based workstream tracking | `planning-with-files` only when the authoritative plan or tracker cannot meet a genuine tracking or recovery need. Keep one authoritative task state. |
| NHK-only documentation repair or archive retrieval | The tools needed to inspect and update local artifacts. Require read-only tracker access when identity or completion evidence is missing locally. A confirmed remote link may be recorded with an explicit remote access limit. |

A visible skill is ready when the harness can invoke it in this session. A discovered install, cached skill file, or documented upstream link can help locate it. Confirm invocation through the harness or its supported explicit installed-skill entrypoint.

## Decision Modes

### 1. Install

When the required skill is absent and the user wants a native install, identify the missing skill, use its upstream documentation and the platform's install mechanism, and obtain authorization before environment changes.

### 2. Enable

When the skill is installed but unavailable in the active environment, explain how to enable it in this workspace or start the session that can invoke it. Verify that it becomes available.

### 3. Adopt

When the user explicitly authorizes manual use of a missing skill's conventions, follow the conventions for this NHK run only. Keep adoption in the conversational handoff, with no persistent adoption marker or effect on future runs. Report that the dependency was missing and its conventions were followed manually. The persisted workspace workflow records a default, independent of install or adoption state.

If the required capability remains unavailable and the user has not chosen or has declined these options, stop the affected route. A separate authorization is still required for any environment change or tracker mutation outside the current task.
