# Welcome to NHK: Naive Harness Kit

**English** | [中文](README_CN.md)

NHK is a prompt-first starter kit that sets up your Codex or Claude Code workspace, then keeps it tidy, so you can spend your attention on the actual project.

You do not need to become a harness engineer first. NHK makes a few sensible decisions for you, writes them down where both you and the agent can see them, and asks before doing anything you would want a say in. It is not magic. Think of it as the slightly fussy friend who helps you move house and insists on labelling the boxes, so future-you is not stuck deciphering agent vibes.

## In 30 Seconds

NHK takes care of five recurring jobs that show up surprisingly fast once you use coding agents seriously:

- getting the useful workflow tools in place, especially `superpowers` and `planning-with-files`
- setting up the right instruction file (`AGENTS.md` or `CLAUDE.md`) for your agent, lazily but safely
- keeping the project's routing, planning, worker, recovery, and governance notes in step with reality
- deciding whether a workstream stays active or moves to archive
- doing all of it through explicit prompts rather than hidden hooks

It is built for beginners, lazy pragmatists, and anyone who would rather ship than hand-roll an agent harness. Experts are welcome too; nobody here is checking credentials.

## Quick Start

**1. Install the two helpers NHK leans on.** They are [`superpowers`](https://github.com/obra/superpowers) and [`planning-with-files`](https://github.com/othmanadi/planning-with-files). Not sure whether you already have them? That is fine: NHK checks and asks before pretending everything is ready.

**2. Copy NHK into your agent's skills folder.** There is nothing to compile. The four skill folders and `references/` sit side by side:

```text
<skills-root>/
├── welcome-to-nhk/
├── nhk-bootstrap/
├── nhk-upkeep/
├── nhk-archive/
└── references/
```

From this repository:

```bash
cp -R welcome-to-nhk nhk-bootstrap nhk-upkeep nhk-archive references <skills-root>/
```

Replace `<skills-root>` with your agent's real skills folder (for Claude Code, usually `~/.claude/skills/`). Keep the five folders as direct siblings; an extra wrapping `nhk/` folder hides them from the agent.

**3. Refresh the agent session** and check that all four skills are discoverable.

**4. Open your project and start with `welcome-to-nhk`.** It looks around and hands you to the right next step. That is genuinely the whole routine.

<details>
<summary>Optional: double-check the install with Python</summary>

If Python 3 happens to be around, a zero-dependency validator can check the file layout:

```bash
python3 -B scripts/validate_nhk.py --install-root <skills-root>
```

It confirms files and versions; it cannot confirm that your agent actually discovers the skills, so the refresh in step 3 still matters. The repository's `scripts/` and `tests/` folders are maintainer tools and not runtime content, and Python is not an NHK dependency.

</details>

## The Four Skills

| Skill | When it shows up | What it does |
| --- | --- | --- |
| `welcome-to-nhk` | Always first | The router. It checks dependencies and your instruction files, then picks one of the three below. When in doubt, start here and let it be the adult in the room. |
| `nhk-bootstrap` | First setup, or when a required piece is missing | Writes the main instruction file, five companion guides, and a home for finished work. You review; you do not write from scratch. |
| `nhk-upkeep` | After a delivery cycle, or after updating NHK | Repairs drift between your documents and the current NHK rules. It asks about archive only when one workstream has clear completion evidence. |
| `nhk-archive` | Only after you say a workstream is done | Moves that finished workstream into `archive/` and keeps its index findable. |

Updated your installed copy of NHK? Run `welcome-to-nhk` in an existing project and ask for upkeep. It compares the project against the new templates even when everything still looks tidy, keeps your project facts and approved exceptions, and sends any missing foundation piece through bootstrap first. Updating the bundle by itself never rewrites project documents.

## What Ends Up In Your Project

Once the main instruction file is chosen, NHK sets up seven required pieces: the routing, planning, worker, recovery, and governance guides, plus `archive/` and `archive/README.md`. Here is how they fit together:

| Layer | File(s) | Job |
| --- | --- | --- |
| Instruction | canonical `AGENTS.md` or standalone `CLAUDE.md`, plus an optional thin Claude adapter | stable execution rules, verification discipline, collaboration rules |
| Routing | `coding-agent-guide.md` | from a task or symptom to what to read first, what probably changes, and how to check it |
| Planning | `implementation-planning.md` | task sizing, dependencies, and wide-change structure, loaded only while planning |
| Workers and recovery | `worker-policy.md`, `execution-recovery.md`, optional Claude `.claude/agents/nhk-*.md` | choosing helpers, reviewing their work, and knowing when to stop repeating fixes |
| Governance | `documentation-governance.md` | document roles, active versus archived material, naming, and loading |
| Active work | active `specs/` and `plans/`, optional root `task_plan.md` / `progress.md` / `findings.md` | work in progress only |
| Archive | `archive/` plus root `archive/README.md` | finished specs, plans, and tracking, kept for reference |

A few opinions come baked in:

- Root tracking files appear only when the work needs them, not by default.
- Active and archived documents live apart, and archiving always waits for your confirmation.
- For the beginner-sized projects NHK is built for, the routing table is the shallow code map. A second codemap would mostly give newcomers two maps to get lost between.
- Documentation lifecycle is written down explicitly, following `references/documentation-governance-template.md`, rather than left to guesswork.

The companions stay out of the way until needed. `implementation-planning.md` comes out when a plan is being written or revised, `worker-policy.md` when work is handed to a helper, and `execution-recovery.md` when fixes start going in circles. Most days, none of them needs to sit open on the desk.

## Why It Is Designed This Way

Every choice in NHK follows from a few plain observations about how coding agents actually behave:

- **Prompts, not hooks.** Each step is a prompt you can read, so nothing happens behind your back, and when something goes wrong you can see which instruction caused it. It also keeps NHK working the same way in Codex and Claude Code.
- **Short always-on instructions, details on demand.** The agent rereads the main instruction file constantly, which costs tokens and attention every time. So that file holds only stable rules and pointers, and the companion guides load when a task actually needs them.
- **Written down beats remembered.** Agents forget between sessions and sometimes within one. Files do not. That is why NHK pairs with `planning-with-files`, and why routing, planning, and archive rules live in documents instead of in the model's head.
- **You keep the decisions that are hard to undo.** Archiving, top-tier modes, helpers hiring their own helpers, and anything ambiguous wait for your explicit yes. NHK would rather ask one extra question than guess wrong on your behalf.
- **Helpers sized to the job.** Every helper costs time and tokens, so the default is a capable-enough helper, and going heavier needs a stated reason. Difficulty earns stronger help; habit does not.
- **A repeated failure calls for a new explanation.** When fixes keep bouncing off the same problem, another patch rarely helps. NHK caps the loop and asks for a fresh look instead.
- **Beginner-sized on purpose.** A small fixed foundation and one routing table are enough for the projects NHK is aimed at. More structure would mostly mean more to keep in sync.

## Why Those Two Dependencies

- `superpowers` gives agent work a shape: brainstorm, spec, plan, then build, instead of a vague "just keep going" spiral where the model reinvents its methodology every twenty minutes.
- `planning-with-files` gives memory a reliable home outside the model. Codex and Claude Code are both a bit fuzzy about long-lived working memory, and a few plain tracking files beat hoping the model remembers what was verified and which workstream is still live.

NHK uses both to make instruction setup, daily upkeep, and archive decisions less ad hoc. If one is missing, NHK pauses and asks whether to install it, enable it, or adopt its conventions manually for this run only. Adopting installs nothing and does not carry over to later runs, and NHK says so plainly. The details live in [`references/dependency-setup.md`](references/dependency-setup.md).

## Codex Or Claude Code?

NHK works with both. The shared rules (reviews, waiting, recovery, and your approvals) are identical. What differs is the controls each platform gives NHK to work with:

| | Codex | Claude Code |
| --- | --- | --- |
| Main instruction file | `AGENTS.md` | a standalone `CLAUDE.md`, or a thin `CLAUDE.md` that imports `AGENTS.md` |
| Companion guides | read from their file paths when needed | the same; never pulled in with `@` imports |
| Helper models | three bands, with exact models in the [worker policy template](references/worker-policy-template.md) | Opus only, in four bands |
| How helper effort is set | picked for each helper when it is dispatched | through optional `.claude/agents/nhk-*.md` files that bootstrap offers; otherwise your session's effort |
| Needs your explicit approval | Ultra, and helpers delegating further | Fable on the main thread, and helpers delegating further |

Why the difference? Codex lets the main agent choose both model and effort for every helper it dispatches, so NHK keeps a small catalog of presets and picks from it. Claude Code lets the main agent choose a helper's model, but sets effort only through an agent definition file. NHK therefore ships four ready-made definitions, keeps one capable model family, and varies only how hard each band thinks.

**Which instruction file wins.** NHK does not guess recklessly. When both files exist and `CLAUDE.md` has a real import line exactly equal to `@AGENTS.md` or `@./AGENTS.md`, AGENTS is canonical and nobody gets asked a needless question. A `CLAUDE.md` that imports a missing AGENTS is a broken adapter; two independent files are real ambiguity, and then NHK asks you to choose.

Thin CLAUDE imports only AGENTS. The five companion docs stay as backticked literal paths and load on demand; importing them with `@` would charge every session for the full map before anyone knows whether it is needed.

**Which model for the main conversation?** One suggestion per platform:

For a long-running Codex main thread, we suggest GPT-6 Sol, with xhigh for demanding coordination and max when deeper reasoning is worthwhile. This is a human-facing suggestion only: you choose the main-thread model and effort, and NHK worker permissions do not depend on that choice. See [OpenAI model guidance](https://learn.chatgpt.com/docs/models) for current options.

For a Claude Code main thread, we suggest Opus at its default effort, one level higher for long, demanding coordination, and the top levels only where you have seen them pay off. Treat it the same way: a suggestion for you, not a rule, and helper bands stay the same whatever you pick. See [Anthropic effort guidance](https://platform.claude.com/docs/en/build-with-claude/effort) for current options.

## Helpers, Reviews, And Knowing When To Stop

You can use NHK without reading this section. It is here so you know what the agent is doing on your behalf when it hands work to helpers.

The short version:

- **Helpers are matched to the job.** Everyday work goes to a sensible default, clear low-risk tasks can go lighter, and genuinely hard work goes heavier, with the difficulty written down.
- **Delegated tasks get an independent check.** SDD reviews each atomic task; native execution keeps its own checks and a final independent review. Both specification and quality verdicts must pass.
- **The main agent waits politely.** No nagging helpers every few minutes.
- **Fixes going in circles trigger a rethink.** After five rounds on the same problem, the next move is a better explanation, not patch number six.
- **The big permissions stay with you.** Top-tier modes, helpers hiring their own helpers, and archiving all need your explicit yes.

<details>
<summary>The fine print, for the curious</summary>

### Codex only

**Picking helpers.** NHK uses three practical Codex bands with permissions tied to the role. Ordinary implementation, local design, integration, debugging, and independent investigation default to medium. The lighter band can implement and test a small, clear, low-risk feature as well as mechanical work: behavior and interfaces are clear, the approach is established, verification is reliable, and impact stays local. The plan need not contain complete implementation code. Security, data integrity, and hidden cross-task risks require more judgment even when the code is short. Before choosing the harder band, check scope, interfaces, and context; use it only for a remaining reasoning difficulty or demonstrated medium limits, and name the difficulty in the brief. Architecture labels and later fix rounds do not automatically raise the model. Local repairs and scoped re-reviews qualify for the lighter band only when cause, behavior, approach, impact, and verification are clear without design or cross-task judgment. Your budget still binds.

The exact model list and role permissions live in the [worker policy template](references/worker-policy-template.md), which creates `worker-policy.md`. Optimize total delivery cost: planning, context handoff, implementation, review, and rework. Atomic boundaries should make clear work suitable for lighter workers and keep remaining judgment bounded for the default role. If many tasks need the harder band, revisit the plan; there is no model-use quota. Failures are classified before escalation, and an unavailable model is reported rather than silently swapped for another band or an older model. Non-convergence at the ordinary ceiling, earlier stagnation, or the five-round bound leads to execution recovery.

### Claude Code only

**Picking helpers.** Every Claude helper runs Opus, sorted into four bands by role: light for small mechanical or standard tasks meeting the same low-risk condition, standard as the default for ordinary implementation and initial reviews, deep for a named reasoning difficulty, and read-only diagnosis for independent diagnosis and complex final review. Claude Code sets a helper's effort only through an agent definition, so in a Claude Code workspace `nhk-bootstrap` offers four optional files under `.claude/agents/`, built from the [agent definitions template](references/claude-agents-template.md). We recommend accepting; if you decline, helpers still run Opus at your session's effort. A new `.claude/agents/` directory needs a fresh session before Claude Code discovers it. Fable stays on the main thread, and only when you choose or approve it.

### Both platforms

**Special permissions.** Where a platform offers Ultra, Ultra and letting a helper delegate further are two separate permissions: each needs your approval for the specific task and current run.

**Reusing helpers.** Ordinary fixes go back to the original implementer, and scoped re-review prefers the original independent reviewer. Being allowed a cheaper configuration does not mean changing workers; a fresh cheaper worker is worth it only when a self-contained handoff justifies the overhead, and suitable findings travel together in one repair packet.

**Reviews.** In SDD, each atomic task or qualifying mechanical batch has one independent, read-only reviewer with separate specification and quality verdicts; both must pass. Initial reviews default to the middle band, with higher capability only for difficulty in the review itself. Complex whole-change final review uses the harder band, with max available for deeper reasoning; otherwise max is limited to independent diagnosis. Internal steps stay within their task. Reviews use fixed revisions, binding constraints, the actual diff, and test evidence. A passed SDD task review can serve as final review only for a single-task non-complex plan covering every requirement and change at the identical final scope, version, and evidence. Changes invalidate that reuse; multi-task and complex plans retain whole-change review. Native execution uses its own task verification and one independent whole-change final review, without per-task subagent reviews. Consolidation never extends repair or recovery allowances.

**Waiting.** After dispatch or resumption, and between unsolicited progress checks, the main agent waits at least 30 minutes. It prefers longer event waits within tool limits and higher-priority instructions, and responds immediately to completion, questions, concrete failures, and your messages. Empty waits or silence do not justify status checks, reminders, interruption, replacement, or duplicate investigation. This interval is neither a timeout nor a polling schedule, cache TTL, or runtime setting. Rule updates preserve completed and in-flight task identities and progress. Unstarted work is reassessed against the atomic contract, without redispatching completed work or resetting recovery counts.

**Decisions you already made.** Existing human decisions can be kept as narrow ordinary-routing exceptions in `worker-policy.md`. The [worker policy template](references/worker-policy-template.md) defines a single JSON bullet naming the target, repository-relative scope, role, ordinary preset, and a specific approval reference. Bootstrap and upkeep must confirm the decision and keep its scope; they never invent approval. Normal rules and the catalog stay in place, and the record changes only the matched preset choice. It cannot waive worker classes, review gates, budgets, special-role permissions, Ultra, or recursion. The optional validator checks the record's structure, not whether you actually consented; unrecorded conflicts and malformed or blanket records still fail.

**Planning.** `implementation-planning.md` is a Superpowers overlay loaded before writing, approving, or materially revising a plan. Both platforms use atomic tasks: the smallest independently testable deliveries worth their own review. Split where a reviewer could accept one result and reject its neighbor, including within one feature. Keep each task's implementation, tests, and necessary configuration, migration, and docs together. A task may span files; a feature may span tasks. Keep tightly coupled transactions, permission decisions, and recovery paths intact. Internal execution steps stay inside their task, while same-shape mechanical changes may share one batch with an explicit file list and common verification. Separate investigation only for a verifiable conclusion, interface contract, or reusable decision; otherwise local understanding stays with implementation.

Plans preserve Files, Interfaces, concrete TDD steps, boundary examples, commands, expected results, and necessary code examples; the worker supplies local implementation rather than transcribing a mandatory complete code listing. Worker class describes the work, not its model. SDD starts a fresh implementer context for each task or qualifying batch and keeps implementation sequential; native execution remains a separate choice. Use upstream brief, report, diff package, and ledger files, carrying binding global constraints and relevant interfaces even when a helper extracts only the task section. NHK atomic sizing, planning detail, role routing, reuse, and timing override conflicting generic defaults without patching the plugin. Planning fields remain active text.

**Updating older workspaces.** Upkeep replaces NHK-owned whole-module defaults with the atomic contract while preserving project facts and approved exceptions. Legacy `module-implementation` / `initial-module-review` records become `task-implementation` / `initial-task-review` only for the same single task, scope, and confirmed approval. A module split or ambiguous mapping is reported for a human decision; permission never spreads automatically to the new tasks. Installing the updated bundle alone does not rewrite project documents.

**When fixes go in circles.** Ordinary bugs keep using Superpowers systematic debugging. When the same problem survives round five, NHK asks the main agent to revisit its explanation before reaching for patch six. The five-round limit applies to each task and to the same unresolved problem across tasks; renaming the task does not wipe the slate. Counts stay in the workflow's existing record.

If new causal evidence explains why earlier attempts failed, NHK allows one recovery fix and one independent re-review. Competing explanations can get at most one fresh, read-only diagnosis using the harder configuration or max as needed; it separates observations from old hypotheses and returns evidence or a discriminating experiment. Fixes and re-reviews use their own role permissions. Five rounds is a ceiling: the three-fix architecture check and earlier signs of stagnation still apply. If the evidence stays inconclusive, or recovery fails, the next decision is yours. The [recovery template](references/execution-recovery-template.md) defines the evidence and stopping rules.

**Missing or outdated companions.** If a companion is missing, `nhk-bootstrap` adds it from its template and leaves existing project details in place. If older NHK rules are still sitting in the main instruction file, bootstrap or upkeep replaces just those outdated passages with pointers to the companions. Your project facts and explicitly approved exceptions stay intact.

</details>

## What Is In This Repository

Four skills, each in its own folder: `welcome-to-nhk`, `nhk-bootstrap`, `nhk-upkeep`, and `nhk-archive`.

It also ships with eleven controlled references, which the skills read when they need them:

- `AGENTS-template.md` and `CLAUDE-template.md`: how to generate the main instruction file
- `coding-agent-guide-template.md`, `implementation-planning-template.md`, `worker-policy-template.md`, `execution-recovery-template.md`, `documentation-governance-template.md`: the five companion guides
- `archive-readme-template.md`: the archive index
- `claude-agents-template.md`: the optional Claude Code helper definitions
- `dependency-setup.md`: what to do when a dependency is missing
- `validation-scenarios.md`: the scenarios NHK is checked against

The instruction templates are generation contracts, not copy-paste snacks. They tell the agent what must survive, what must be adapted, and what should quietly disappear before the final `AGENTS.md` or `CLAUDE.md` lands in a real workspace.

Human-facing and agent-facing docs are kept apart on purpose. `README.md` and `README_CN.md` are for people. `AGENTS.md` is for coding agents maintaining this repository, and `CLAUDE.md` imports it for Claude Code. The skill folders define NHK's behavior, and `references/` holds the frozen templates and validation material they use.

## Maintaining NHK Itself

This part is for people changing NHK, not for people using it. The repository has its own `AGENTS.md` (the shared maintenance contract) and a thin `CLAUDE.md` that imports it and adds only Claude-specific glue. That keeps working rules away from this README, which is the least dramatic arrangement and therefore usually the best one.

The optional validator can also check generated companion files:

```bash
python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <worker-policy.md> --kind worker-policy
python3 -B scripts/validate_nhk.py --final <execution-recovery.md> --kind execution-recovery
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance
```

The size tests use identical project facts to compare generated `AGENTS.md` and standalone `CLAUDE.md` examples with the baseline from before the detailed rules moved into companions. Both must contain at least 20% fewer always-loaded English words, and shuffling line breaks does not count. This measures instruction size, not a promised reduction in your bill. It is a maintainer check, not homework for installing NHK.
