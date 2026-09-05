# Welcome to NHK: Naive Harness Kit

**English** | [中文](README_CN.md)

NHK is a prompt-first starter kit for people who want a usable agent workspace harness without becoming full-time harness engineers first.

It is intentionally a little humble, a little self-aware, and very practical. The point is not to look clever. The point is to help you get the good tools in place, wire them together sanely, and keep a Codex or Claude Code workspace from turning into a vague little document swamp.

## What NHK Is

NHK helps with five recurring jobs that show up surprisingly fast once you start using coding agents seriously:

- getting the useful workflow tools in place, especially `superpowers` and `planning-with-files`
- lazily but safely initializing the right workspace instruction file for the current agent environment
- keeping the workspace's routing, planning, worker, recovery, and governance notes aligned with reality
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

It also ships with ten controlled references:

- `AGENTS-template.md`
- `CLAUDE-template.md`
- `coding-agent-guide-template.md`
- `implementation-planning-template.md`
- `worker-policy-template.md`
- `execution-recovery-template.md`
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
| Worker and recovery layer | `worker-policy.md`, `execution-recovery.md` | choosing helpers, reviewing their work, and knowing when to pause repeated fixes |
| Governance layer | `documentation-governance.md` | document roles, active/archive surfaces, naming/loading, and archive invariants |
| Active work layer | active `specs/`, active `plans/`, optional root `task_plan.md` / `progress.md` / `findings.md` | work in progress only |
| Archive layer | `archive/` plus root `archive/README.md` | completed specs, completed plans, completed tracking files, historical reference only |

NHK is opinionated here on purpose:

- once the main instruction file is chosen, NHK sets up seven required pieces: the routing, planning, worker, recovery, and governance guides, plus `archive/` and `archive/README.md`
- root tracking files are conditional, not automatic
- active docs and archive docs should not be mixed
- archive transitions require human confirmation
- archived workstreams should stay discoverable through a root `archive/README.md` index

For the beginner-sized projects NHK is built for, the routing table is the shallow code map. A second codemap would mostly give newcomers two maps to get lost between, which feels ambitious in the wrong direction.

The direct source for the governance layer is `references/documentation-governance-template.md`. NHK does not treat documentation lifecycle as an implicit side effect. It expects those rules to be written down explicitly in the target workspace.

`implementation-planning.md` is deliberately narrower. It is a Superpowers overlay, not a competing planner: load it before writing, approving, or materially revising an implementation plan, then leave it closed for ordinary coding, review, and debugging. It keeps Superpowers' exact files, interfaces, TDD steps, commands, expected results, and necessary code while adding `Delivers`, `Blocked by`, and `Worker class` to make each task small enough for one fresh implementer context and one reviewer gate. NHK improves this through workspace documents; it does not patch the Superpowers plugin.

`worker-policy.md` helps the main agent choose a helper, explain the job, and arrange a review. It is read when there is work to delegate or review. `execution-recovery.md` comes out when fixes keep circling: after five failed rounds on one task or the same problem, or sooner if there is reason to question the design. Most of the time, neither needs to sit open on the desk.

If either file is missing, `nhk-bootstrap` adds it from the [worker policy template](references/worker-policy-template.md) or the [recovery template](references/execution-recovery-template.md), leaving existing project details in place. If older NHK rules are still sitting in the main instruction file, bootstrap or upkeep replaces just those outdated passages with links to the companions. Your project facts and explicitly approved exceptions stay intact.

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

If you are installing NHK into a new environment and are not sure whether the dependencies are already present, that is normal. NHK is designed to stop and ask before pretending everything is ready.

## How To Use It

The shortest path is:

1. Start with `welcome-to-nhk`.
2. Let it decide whether the workspace needs `nhk-bootstrap`, `nhk-upkeep`, or `nhk-archive`.
3. Let `nhk-bootstrap` prepare the main instruction file, the five companion guides, and a home for finished work (`archive/` plus `archive/README.md`). You do not need to write these from scratch.
4. Use `nhk-upkeep` after normal delivery cycles to repair drift; it asks about archive only when one specific workstream has completion evidence and related materials.
5. Use `nhk-archive` only after the human clearly confirms that one workstream is done and should move to archive.

If you do not know where to begin, NHK is opinionated on purpose: begin at `welcome-to-nhk` and let the router be the adult in the room.

## Codex And Claude Code

NHK is designed to work with both:

- Codex-oriented workspaces usually center on `AGENTS.md`
- Claude Code workspaces may use standalone `CLAUDE.md`, or a thin `CLAUDE.md` that imports canonical `AGENTS.md`

NHK does not guess recklessly. When both files exist and CLAUDE has a real import line exactly equal to `@AGENTS.md` or `@./AGENTS.md`, AGENTS is canonical and NHK does not ask a needless question. A lone importing CLAUDE is a broken adapter; two independent files are real ambiguity and still require a human choice.

Thin CLAUDE imports only AGENTS. The five companion docs stay as backticked literal paths and load on demand; importing them with `@` would charge every session for the full map before anyone knows whether it is needed.

## Picking Helpers And Knowing When To Pause

Letting every worker inherit the main thread's settings turned out to be a remarkably effective way to pay for deep thought about very small edits. NHK uses three practical Codex bands, with no ranking inside a band: clear, low-risk jobs; ordinary implementation and bounded integration; and difficult design or high-risk work. The main agent starts with the band that fits the job and explicitly selects a configuration allowed for the task. Your budget still counts.

The current model list, availability rules, and conditions for using a stronger model live in the [worker policy template](references/worker-policy-template.md), which creates your workspace's `worker-policy.md`. Keeping one list gives us fewer opportunities to disagree with ourselves. It also spells out which configurations are reserved for the final review of a complex plan.

Every helper gets the job, relevant context, and permission boundaries in its brief. Each task also gets an independent, read-only reviewer. It checks whether the work meets the requirements and whether the implementation is sound; both checks must pass.

Claude helpers use Sonnet or Opus. Fable stays on the main thread, and only when you choose or approve it. Ultra and letting a helper delegate further are two separate permissions: each needs your approval for the specific task and current run.

For ordinary bugs, keep using Superpowers systematic debugging. When the same problem survives round five, NHK asks the main agent to revisit its explanation before reaching for patch six. The five-round limit applies to each task and to the same unresolved problem across tasks; renaming the task does not give it a clean slate. Counts stay in the workflow's existing record.

If new causal evidence explains why earlier attempts failed, NHK allows one recovery fix and one independent re-review. When explanations conflict, it may first ask one fresh, read-only helper to examine the evidence. If the evidence is still inconclusive, or recovery fails, the next decision is yours. The [recovery template](references/execution-recovery-template.md) covers the earlier design checks, the evidence needed to try again, and the limits that still apply at final review.

## Repo Maintenance

This repository itself includes both `AGENTS.md` and `CLAUDE.md`.

The intent is:

- `AGENTS.md` is the shared repo maintenance contract for coding agents
- `CLAUDE.md` imports `AGENTS.md` and adds only Claude-specific glue

That keeps the human-facing README separate from the agent-facing working rules, which is the least dramatic arrangement and therefore usually the best one.

If you are maintaining NHK itself, you can also check generated companion files with the optional validator:

```bash
python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <worker-policy.md> --kind worker-policy
python3 -B scripts/validate_nhk.py --final <execution-recovery.md> --kind execution-recovery
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance
```

The size tests use identical project facts to compare generated `AGENTS.md` and standalone `CLAUDE.md` examples with the baseline from before the detailed rules moved into companions. Both must contain at least 20% fewer always-loaded English words; moving line breaks around does not count. This measures instruction size, not a promised reduction in your bill. It is a maintainer check, not homework for installing NHK.
