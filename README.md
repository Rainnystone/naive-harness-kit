# Welcome to NHK: Naive Harness Kit

**English** | [中文](README_CN.md)

NHK is a prompt-first starter kit for people who want a usable agent workspace harness without becoming full-time harness engineers first.

It is intentionally a little humble, a little self-aware, and very practical. The point is not to look clever. The point is to help you get the good tools in place, wire them together sanely, and keep a Codex or Claude Code workspace from turning into a vague little document swamp.

## What NHK Is

NHK helps with five recurring jobs that show up surprisingly fast once you start using coding agents seriously:

- getting the useful workflow tools in place, especially `superpowers` and `planning-with-files`
- lazily but safely initializing the right workspace instruction file for the current agent environment
- keeping routing, implementation-planning, and documentation-governance companions aligned with reality
- deciding whether a workstream should stay active or move to archive
- doing all of that with explicit prompts instead of opaque hooks

In other words, NHK is not trying to be magic. It is trying to be the slightly fussy friend who says: yes, let's make this easier, but let's also write the rules down so future-you is not stuck deciphering agent vibes.

This kit is for beginners, lazy pragmatists, and anyone who would rather ship than hand-roll a custom agent harness from scratch.

## What Is Included

NHK ships with four focused skills:

- `welcome-to-nhk`: the first-stop router
- `nhk-bootstrap`: first-time workspace setup
- `nhk-upkeep`: day-to-day harness maintenance
- `nhk-archive`: human-confirmed archive transition

It also ships with eight controlled references:

- `AGENTS-template.md`
- `CLAUDE-template.md`
- `coding-agent-guide-template.md`
- `implementation-planning-template.md`
- `documentation-governance-template.md`
- `archive-readme-template.md`
- `dependency-setup.md`
- `validation-scenarios.md`

The instruction templates are generation contracts, not copy-paste snacks. They tell the agent what must survive, what must be adapted, and what should quietly disappear before the final `AGENTS.md` or `CLAUDE.md` lands in a real workspace.

## Documentation Logic

NHK separates human-facing docs from agent-facing docs on purpose:

- `README.md` is the default GitHub landing page for humans
- `README_CN.md` is the Chinese companion for humans
- `AGENTS.md` is for Codex-style agents maintaining this repository
- `CLAUDE.md` is for Claude Code and imports the shared repo instructions
- the four skill folders define actual NHK behavior
- `references/` stores frozen drafting and validation assets used by the skills

This split matters. README files explain what NHK is, how to install it, and how to use it. `AGENTS.md` and `CLAUDE.md` are not tutorials; they tell coding agents how to work on the NHK repository itself without confusing repo maintenance with skill usage.

For an NHK-managed workspace, the expected document system is layered:

| Layer | File(s) | Job |
| --- | --- | --- |
| Instruction layer | canonical `AGENTS.md` or standalone `CLAUDE.md`, plus an optional thin Claude adapter | stable execution rules, verification discipline, collaboration rules |
| Routing layer | `coding-agent-guide.md` | task or symptom to first reads, likely change surfaces, and targeted verification |
| Planning layer | `implementation-planning.md` | on-demand Superpowers-compatible task sizing, dependency edges, and wide-change structure |
| Governance layer | `documentation-governance.md` | document roles, active/archive surfaces, naming/loading, and archive invariants |
| Active work layer | active `specs/`, active `plans/`, optional root `task_plan.md` / `progress.md` / `findings.md` | work in progress only |
| Archive layer | `archive/` plus root `archive/README.md` | completed specs, completed plans, completed tracking files, historical reference only |

NHK is opinionated here on purpose:

- after the canonical instruction is known, every NHK-managed workspace has five mandatory foundation surfaces: routing, implementation planning, governance, `archive/`, and `archive/README.md`
- root tracking files are conditional, not automatic
- active docs and archive docs should not be mixed
- archive transitions require human confirmation
- archived workstreams should stay discoverable through a root `archive/README.md` index

For the beginner-sized projects NHK is built for, the routing table is the shallow code map. A second codemap would mostly give newcomers two maps to get lost between, which feels ambitious in the wrong direction.

The direct source for the governance layer is `references/documentation-governance-template.md`. NHK does not treat documentation lifecycle as an implicit side effect. It expects those rules to be written down explicitly in the target workspace.

`implementation-planning.md` is deliberately narrower. It is a Superpowers overlay, not a competing planner: load it before writing, approving, or materially revising an implementation plan, then leave it closed for ordinary coding, review, and debugging. It keeps Superpowers' exact files, interfaces, TDD steps, commands, expected results, and necessary code while adding `Delivers`, `Blocked by`, and `Worker class` to make each task small enough for one fresh implementer context and one reviewer gate. NHK improves this through workspace documents; it does not patch the Superpowers plugin.

## Dependencies

NHK expects these peer workflow systems:

- [`superpowers`](https://github.com/obra/superpowers): process discipline, skill-first routing, brainstorm/spec/plan flow
- [`planning-with-files`](https://github.com/othmanadi/planning-with-files): persistent task tracking, recovery, and continuity

The pairing matters.

`superpowers` is useful because it gives agent work an actual shape instead of a vague "just keep going" spiral. It helps the model route work, choose the right workflow, and avoid improvising its own grand theory every twenty minutes.

`planning-with-files` pairs well with that because Codex and Claude Code are both a bit fuzzy about long-lived working memory in practice. External tracking files are not glamorous, but they are much better than hoping the model remembers which thread is still active, what has already been verified, or whether a half-finished workstream was supposed to stay live.

Together they give NHK a steadier foundation:
- `superpowers` gives the process shape
- `planning-with-files` gives the memory somewhere reliable to live outside the model
- NHK uses both to make `AGENTS.md` / `CLAUDE.md` setup, daily upkeep, and archive decisions less ad hoc

If one of them is missing, NHK should pause and ask whether you want to install it, enable it, or explicitly adopt its conventions manually for this NHK run. Adopt does not install anything, does not persist into later runs, and should be reported honestly. That decision is described in [`references/dependency-setup.md`](references/dependency-setup.md).

## Installation

NHK is a file-based skill bundle. There is nothing to compile.

Copy the four skill directories and their sibling `references/` directory directly under the skills root used by your agent environment:

```text
<skills-root>/
├── welcome-to-nhk/
├── nhk-bootstrap/
├── nhk-upkeep/
├── nhk-archive/
└── references/
```

From this repository, the equivalent copy command is:

```bash
cp -R welcome-to-nhk nhk-bootstrap nhk-upkeep nhk-archive references <skills-root>/
```

Replace `<skills-root>` with the real skill collection path for your environment. Do not add an extra `nhk/` directory around these five siblings.

The repository's `scripts/` and `tests/` directories are maintainer-only and are not runtime installation content. Python is not an NHK dependency. If Python 3 is already available, the zero-third-party-dependency validator is an optional file-layout check:

```bash
python3 -B scripts/validate_nhk.py --install-root <skills-root>
```

The validator confirms files and versions; it cannot confirm platform skill discovery. After copying and validating, refresh the agent session and confirm that all four skills are discoverable. Then start in the target workspace with `welcome-to-nhk`.

Maintainers can also check generated companion docs without turning the validator into a runtime dependency:

```bash
python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance
```

If you are installing NHK into a new environment and are not sure whether the dependencies are already present, that is normal. NHK is designed to stop and ask before pretending everything is ready.

## How To Use It

The shortest path is:

1. Start with `welcome-to-nhk`.
2. Let it decide whether the workspace needs `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive`.
3. Use `nhk-bootstrap` to create or adapt the workspace instruction file, the three mandatory companion docs, and the root archive surface (`archive/` plus `archive/README.md`).
4. Use `nhk-upkeep` after normal delivery cycles to repair drift; it asks about archive only when one specific workstream has completion evidence and related materials.
5. Use `nhk-archive` only after the human clearly confirms that one workstream is done and should move to archive.

If you do not know where to begin, NHK is opinionated on purpose: begin at `welcome-to-nhk` and let the router be the adult in the room.

## Codex And Claude Code

NHK is designed to work with both:

- Codex-oriented workspaces usually center on `AGENTS.md`
- Claude Code workspaces may use standalone `CLAUDE.md`, or a thin `CLAUDE.md` that imports canonical `AGENTS.md`

NHK does not guess recklessly. When both files exist and CLAUDE has a real import line exactly equal to `@AGENTS.md` or `@./AGENTS.md`, AGENTS is canonical and NHK does not ask a needless question. A lone importing CLAUDE is a broken adapter; two independent files are real ambiguity and still require a human choice.

Thin CLAUDE imports only AGENTS. The three companion docs stay as backticked literal paths and load on demand; importing them with `@` would charge every session for the full map before anyone knows whether it is needed.

## Worker Cost Policy

Leaving every worker to inherit the main thread turned out to be a wonderfully efficient way to buy premium reasoning for jobs that mostly needed competent typing. NHK therefore keeps three practical Codex preset bands. They are task-fit choice sets, not a universal model ranking, and presets within one band have no fixed internal order:

`Band 1: GPT-5.5 xhigh; GPT-5.6 Luna max; GPT-5.6 Terra high`
`Band 2: GPT-5.6 Terra xhigh; GPT-5.6 Terra max; GPT-5.6 Sol high`
`Band 3: GPT-5.6 Sol xhigh; GPT-5.6 Sol max`

Mechanical work, clear ordinary implementation, and scoped review use Band 1; multi-file integration and difficult but bounded work use Band 2; architecture, high-uncertainty bounded work, and final review use Band 3 or stay on the main thread. The main thread explicitly names model and effort, then chooses the best task fit with the lowest expected total cost inside that band instead of defaulting to its highest-effort preset. An unavailable choice is replaced inside the same band; a correctly sized but capability-limited packet may rise one band. An oversized packet is split first. The main-thread model and effort remain each worker's cost ceiling. Sol max needs no special approval when it remains within that ceiling; any configuration above the main-thread ceiling needs the human's approval.

Ultra stays outside the three bands. It reaches a worker only when the human approves one specific packet for the current run and simultaneously permits recursive delegation inside that packet. Claude standalone keeps the same lowest-cost-suitable and approval boundaries without carrying an OpenAI model list around like a tiny museum exhibit.

## When Fixes Start Going In Circles

Most gaps should close within five honest fix–verify or fix–review rounds. If the same one is still sitting there after round five, NHK stops pretending patch number six is bound to be the clever one: work must stop, `systematic-debugging` must be invoked or restarted, and those five rounds count as failed fixes. No sixth patch is allowed until root-cause and architecture reassessment is complete.

## Repo Maintenance

This repository itself includes both `AGENTS.md` and `CLAUDE.md`.

The intent is:

- `AGENTS.md` is the shared repo maintenance contract for coding agents
- `CLAUDE.md` imports `AGENTS.md` and adds only Claude-specific glue

That keeps the human-facing README separate from the agent-facing working rules, which is the least dramatic arrangement and therefore usually the best one.
