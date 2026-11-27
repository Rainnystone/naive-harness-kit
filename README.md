# Welcome to NHK: Naive Harness Kit

**English** | [中文](README_CN.md)

NHK is a prompt-first starter kit that sets up your Codex or Claude Code workspace, then keeps it tidy, so you can spend your attention on the actual project.

You do not need to become a harness engineer first. NHK makes a few sensible decisions for you, writes them down where both you and the agent can see them, and asks before doing anything you would want a say in. It is not magic. Think of it as the slightly fussy friend who helps you move house and insists on labelling the boxes, so future-you is not stuck deciphering agent vibes.

## In 30 Seconds

NHK takes care of five recurring jobs that show up surprisingly fast once you use coding agents seriously:

- choosing the project's workflow and connecting its tracker or plan
- setting up the right instruction file (`AGENTS.md` or `CLAUDE.md`) for your agent, lazily but safely
- keeping the project's routing, planning, worker, recovery, and governance notes in step with reality
- deciding whether a workstream stays active or moves to archive
- doing all of it through explicit prompts rather than hidden hooks

It is built for beginners, lazy pragmatists, and anyone who would rather ship than hand-roll an agent harness. Experts are welcome too; nobody here is checking credentials.

## Quick Start

**1. Choose the workflow for this project.** For a new project we recommend [Matt Pocock Skills](https://github.com/mattpocock/skills). [Superpowers](https://github.com/obra/superpowers) is an equally supported choice. NHK checks the capabilities your project needs. An existing Superpowers project keeps its workflow.

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
| `welcome-to-nhk` | Always first | Finds the canonical instructions and project workflow, checks what this operation needs, and picks the next skill. |
| `nhk-bootstrap` | First setup, or when a required piece is missing | Connects the instruction file, five guides, and the selected workflow’s records. |
| `nhk-upkeep` | After a delivery cycle, or after updating NHK | Repairs drift between your documents and the current NHK rules. It asks about archive only when one workstream has clear completion evidence. |
| `nhk-archive` | You ask about readiness, approve an archive, or check a previous archive | Checks the records. With your approval, it indexes originals or verifies local copies before moving them. |

Updated your installed copy of NHK? Run `welcome-to-nhk` in an existing project and ask for upkeep. It compares the project against the new templates even when everything still looks tidy, keeps your project facts and approved exceptions, and sends any missing foundation piece through bootstrap first. Updating the bundle by itself never rewrites project documents.

## What Ends Up In Your Project

After choosing a canonical instruction file, NHK connects five stable guides. Superpowers also starts with `archive/` and its index. A Matt workspace creates them on its first approved archive. The tracker and domain rules live in `docs/agents/`.

| Layer | File(s) | Job |
| --- | --- | --- |
| Instruction | canonical `AGENTS.md` or standalone `CLAUDE.md`, plus an optional thin Claude adapter | stable execution rules, verification discipline, collaboration rules |
| Routing | `coding-agent-guide.md` | from a task or symptom to what to read first, what probably changes, and how to check it |
| Planning | `implementation-planning.md` | task sizing, dependencies, and wide-change structure, loaded only while planning |
| Workers and recovery | `worker-policy.md`, `execution-recovery.md`, optional Claude `.claude/agents/nhk-*.md` | choosing helpers, reviewing their work, and knowing when to stop repeating fixes |
| Governance | `documentation-governance.md` | document roles, active versus archived material, naming, and loading |
| Active work | Matt spec and tickets in the configured tracker, or a Superpowers spec, plan and execution ledger | acceptance, dependencies, evidence and remaining work |
| Archive | `archive/README.md` | links to verified local materials or original tracker records |

A few opinions come baked in:

- Root tracking files appear only when the work needs them, not by default.
- Approve the named workstream once. Matt links its original records in the index. Superpowers verifies copies before moving the originals. Retrying reuses the same index entry.
- For the beginner-sized projects NHK is built for, the routing table is the shallow code map. A second codemap would mostly give newcomers two maps to get lost between.
- Documentation lifecycle is written down explicitly, following `references/documentation-governance-template.md`, rather than left to guesswork.

The companions stay out of the way until needed. `implementation-planning.md` comes out when a plan is being written or revised, `worker-policy.md` when work is handed to a helper, and `execution-recovery.md` when fixes start going in circles. Most days, none of them needs to sit open on the desk.

## Why It Is Designed This Way

Every choice in NHK follows from a few plain observations about how coding agents actually behave:

- **Prompts, not hooks.** Each step is a prompt you can read, so nothing happens behind your back, and when something goes wrong you can see which instruction caused it. It also keeps NHK working the same way in Codex and Claude Code.
- **Short always-on instructions, details on demand.** The agent rereads the main instruction file constantly, which costs tokens and attention every time. So that file holds only stable rules and pointers, and the companion guides load when a task actually needs them.
- **Resume from the work itself.** The tracker or execution ledger preserves progress and verification for the next session. Add `planning-with-files` only when the current record cannot support the tracking you need.
- **Approved implementation keeps moving.** The main agent resolves reversible engineering choices, fixes failures and completes the agreed checks. It asks you when a remaining action needs new authority, changes the goal, or the recovery limit leaves no viable path. Archiving, recursive delegation and Fable on the Claude main thread retain their approval rules.
- **Helpers sized to the job.** Every helper costs time and tokens, so the default is a capable-enough helper, and going heavier needs a stated reason. Difficulty earns stronger help; habit does not.
- **A repeated failure calls for a new explanation.** When fixes keep bouncing off the same problem, another patch rarely helps. NHK caps the loop and asks for a fresh look instead.
- **Beginner-sized on purpose.** A small fixed foundation and one routing table are enough for the projects NHK is aimed at. More structure would mostly mean more to keep in sync.

## Choosing and combining workflows

- **Matt.** Run Matt’s project setup when its tracker or domain configuration is missing. It maintains an `## Agent skills` navigation section in the canonical instruction file. In an `AGENTS.md` + thin `CLAUDE.md` workspace, keep that section only in AGENTS. It points to `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` when triage is configured. A local tracker uses `.scratch/<feature>/spec.md` and one file per ticket under `issues/`. A remote tracker keeps native IDs, discussions and dependency links.
- **Superpowers.** Its spec, implementation plan and execution ledger own the workstream. A team can also use Matt’s `GLOSSARY.md`, `GLOSSARY-MAP.md` or ADRs for shared language and decisions. These are durable knowledge, created as terms or decisions emerge. Inspect legacy `CONTEXT.md` before treating it as an old glossary.

Record the default once in `documentation-governance.md` as `Workflow: Matt` or `Workflow: Superpowers`. Each workstream keeps one owner and one authoritative progress record. Changing the default applies to new work; active work resumes from its existing record. When a required capability is missing, choose installation, enablement, or explicit manual adoption for this run. [Dependency setup](references/dependency-setup.md) · [Optional planning-with-files](https://github.com/othmanadi/planning-with-files)

## Codex Or Claude Code?

NHK works with both. The shared rules (reviews, waiting, recovery, and your approvals) are identical. What differs is the controls each platform gives NHK to work with:

| | Codex | Claude Code |
| --- | --- | --- |
| Main instruction file | `AGENTS.md` | a standalone `CLAUDE.md`, or a thin `CLAUDE.md` that imports `AGENTS.md` |
| Companion guides | read from their file paths when needed | the same; never pulled in with `@` imports |
| Helper models | four capability tiers, each mapped to one preset in the [worker policy template](references/worker-policy-template.md) | one definition per tier: Haiku for light, Opus for standard, deep, and read-only audit |
| How helper effort is set | picked for each helper when it is dispatched | through optional `.claude/agents/nhk-*.md` files that bootstrap offers; otherwise your session's effort |
| Needs your explicit approval | Helpers delegating further | Fable on the main thread, and helpers delegating further |

Why the difference? Both platforms share the same four tiers and the same permissions; only the mapping differs. Codex lets the main agent choose both model and effort for every helper it dispatches, so each tier maps to one preset. Claude Code lets the main agent choose a helper's model, but sets effort only through an agent definition file. NHK therefore ships four ready-made definitions, one per tier: light work runs on the small, cheap Haiku family at its highest effort, and the other three run Opus and vary only how hard each one thinks.

**Which instruction file wins.** NHK does not guess recklessly. When both files exist and `CLAUDE.md` has a real import line exactly equal to `@AGENTS.md` or `@./AGENTS.md`, AGENTS is canonical and nobody gets asked a needless question. A `CLAUDE.md` that imports a missing AGENTS is a broken adapter; two independent files are real ambiguity, and then NHK asks you to choose.

Thin CLAUDE imports only AGENTS. The five companion docs stay as backticked literal paths and load on demand; importing them with `@` would charge every session for the full map before anyone knows whether it is needed.

**Which model for the main conversation?** One suggestion per platform:

For a Codex main thread, we suggest GPT-6.2 Astra xhigh for coordination, integration and delivery. This is a human-facing suggestion only. You choose the main-thread model and effort, and NHK worker permissions do not depend on that choice. [OpenAI model guidance](https://learn.chatgpt.com/docs/models)

For a Claude Code main thread, we suggest Opus high during implementation, one level above its default, because the main thread carries the coordination. Treat it the same way: a suggestion for you, not a rule, and helper tiers stay the same whatever you pick. See [Anthropic effort guidance](https://platform.claude.com/docs/en/build-with-claude/effort) for current options.

## Helpers, Reviews, And Knowing When To Stop

You can use NHK without reading this section. It is here so you know what the agent is doing on your behalf when it hands work to helpers.

The short version:

- **Helpers are matched to the job.** Everyday work goes to a sensible default, clear low-risk tasks can go lighter, and genuinely hard work goes heavier, with the difficulty written down.
- **Review follows the workflow.** Superpowers SDD reviews each task; native execution keeps its independent final review. Matt reviews the integrated change against the project standards and originating spec.
- **The main agent waits politely.** No nagging helpers every few minutes.
- **Fixes going in circles trigger a rethink.** After five rounds on the same problem, the next move is a better explanation, not patch number six.
- **You control permissions.** Archiving, recursive delegation and Fable on a Claude main thread require explicit approval. On Codex, a single read-only consultation is already authorized during implementation.

<details>
<summary>The fine print, for the curious</summary>

### Capability tiers

**Picking helpers.** NHK sorts helper work into four capability tiers with permissions tied to the role, defined once for both platforms. `standard` is the default for ordinary implementation, local design, integration, debugging, independent investigation, and initial task reviews. `light` can implement and test a small, clear, low-risk feature as well as mechanical work: behavior and interfaces are clear, the approach is established, verification is reliable, and impact stays local. The plan need not contain complete implementation code. Security, data integrity, and hidden cross-task risks require more judgment even when the code is short. Before choosing `deep`, check scope, interfaces, and context; use it only for a remaining reasoning difficulty or demonstrated `standard` limits, and name the difficulty in the brief. `deep` is the ceiling for implementation. The read-only `audit` tier handles complex final review. Claude also uses it for independent recovery diagnosis. Architecture labels and later fix rounds do not automatically raise the tier. Local repairs and scoped re-reviews qualify for `light` only when cause, behavior, approach, impact, and verification are clear without design or cross-task judgment. Your budget still binds.

The [worker policy template](references/worker-policy-template.md) defines the tiers, maps them to each platform, and creates `worker-policy.md`. Optimize total delivery cost: planning, context handoff, implementation, review, and rework. Atomic boundaries should make clear work suitable for `light` and keep remaining judgment bounded for `standard`. If many tasks need `deep`, revisit the plan; there is no model-use quota. Failures are classified before escalation, and an unavailable configuration is reported rather than silently swapped for another tier or an older model. Non-convergence at `deep`, earlier stagnation, or the five-round bound leads to execution recovery.

### Codex only

**Tier presets.** `light` uses Terra xhigh. `standard`, `deep` and read-only `audit` use Sol xhigh. The main thread may separately ask one fresh Astra xhigh consultant for an independent opinion on a consequential question. The consultant is read-only. Luna is available for a single mechanical batch when you explicitly name it. Automatic routing uses the tiers above. See the [worker policy template](references/worker-policy-template.md) for exact model IDs.

### Claude Code only

**Tier definitions.** Claude's light helper runs Haiku, and every other Claude helper runs Opus. Claude Code sets a helper's effort only through an agent definition, so in a Claude Code workspace `nhk-bootstrap` offers four optional files under `.claude/agents/`, built from the [agent definitions template](references/claude-agents-template.md): `nhk-light` runs Haiku 5.5 at max effort for `light` work, `nhk-standard` runs Opus at its default medium effort for `standard` work, `nhk-deep` thinks harder, and the read-only `nhk-audit` thinks hardest. Haiku 5.5 is priced far below Opus, so even at its top effort it is an economical fit for the small, clear work `light` allows; the tier rules themselves do not change. We recommend accepting; if you decline, every helper runs Opus at your session's effort. A new `.claude/agents/` directory needs a fresh session before Claude Code discovers it. Fable stays on the main thread, and only when you choose or approve it. A recovery diagnosis goes to a helper that can be resumed, never a one-shot built-in explorer, so its one allowed follow-up question reaches the same helper; if that helper can no longer be resumed, the follow-up is dropped rather than handed to a new one.

### Both platforms

**Special permissions.** Recursive delegation requires approval for the specific task and run. The Astra consultation is available once per task or stable acceptance gap and shares the independent diagnosis allowance with recovery. It grants no additional fix round, fallback model, or final-review credit.

**Reusing helpers.** Ordinary fixes go back to the original implementer, and scoped re-review prefers the original independent reviewer. Being allowed a cheaper configuration does not mean changing workers; a fresh cheaper worker is worth it only when a self-contained handoff justifies the overhead, and suitable findings travel together in one repair packet.

**Reviews.** In SDD, each atomic task or qualifying mechanical batch has one independent, read-only reviewer with separate specification and quality verdicts; both must pass. Initial reviews default to `standard`, moving to `deep` only for difficulty in the review itself. Whole-change final review uses `deep`, or `audit` for a complex plan. Internal steps stay within their task. Reviews use fixed revisions, binding constraints, the actual diff, and test evidence. A passed SDD task review can serve as final review only for a single-task non-complex plan covering every requirement and change at the identical final scope, version, and evidence. Changes invalidate that reuse; multi-task and complex plans retain whole-change review. Native execution uses its own task verification and one independent whole-change final review, without per-task subagent reviews. Consolidation never extends repair or recovery allowances.

**Waiting.** In Superpowers SDD, allow at least 30 minutes between unsolicited checks after dispatch or resumption. Completion, questions, concrete failure and user messages are handled immediately. Silence alone does not justify interrupting or replacing a worker. Keep the identity, evidence and repair count when resuming work.

**Decisions you already made.** Existing human decisions can be kept as narrow ordinary-routing exceptions in `worker-policy.md`. The [worker policy template](references/worker-policy-template.md) defines a single JSON bullet naming the target, repository-relative scope, role, a `light`, `standard`, or `deep` preset, and a specific approval reference. Bootstrap and upkeep must confirm the decision and keep its scope; they never invent approval. Normal rules and the catalog stay in place, and the record changes only the matched preset choice. It cannot waive worker classes, review gates, budgets, the `audit` tier, or recursion. The optional validator checks the record's structure, not whether you actually consented; unrecorded conflicts and malformed or blanket records still fail.

**Planning.** `implementation-planning.md` describes the project default. An active workstream under the other workflow uses its original records and the matching section of the installed planning template. The Superpowers overlay uses the smallest independently testable deliveries worth their own review. Matt creates verifiable vertical slices with acceptance criteria and blocking edges in its tracker. `implement-spec` can run independent ready tickets in isolated worktrees, then integrate and review the branch against Standards and Spec. An in-flight plan keeps its original workflow after a default change.

Superpowers plans preserve Files, Interfaces, concrete TDD steps, boundary examples, commands, expected results, and necessary code examples; the worker supplies local implementation rather than transcribing a mandatory complete code listing. Worker class describes the work, not its model. SDD starts a fresh implementer context for each task or qualifying batch and keeps implementation sequential; native execution remains a separate choice. Use upstream brief, report, diff package, and ledger files, carrying binding global constraints and relevant interfaces even when a helper extracts only the task section. NHK atomic sizing, planning detail, role routing, reuse, and timing override conflicting generic defaults without patching the plugin. Planning fields remain active text.

**Updating older workspaces.** Upkeep replaces NHK-owned whole-module defaults with the atomic contract while preserving project facts and approved exceptions. Legacy `module-implementation` / `initial-module-review` records become `task-implementation` / `initial-task-review` only for the same single task, scope, and confirmed approval. A module split or ambiguous mapping is reported for a human decision; permission never spreads automatically to the new tasks. Band-based routing from earlier versions becomes the tier rules; an exception record survives only when its preset is still a `light`, `standard`, or `deep` preset its role allows, and anything else waits for your decision. In Claude Code, upkeep moves an older `nhk-light` definition to Haiku, adds any missing current definition such as `nhk-audit` beside a retired `nhk-diagnosis`, and asks you to delete the retired `nhk-diagnosis` file, because upkeep never deletes files itself. Installing the updated bundle alone does not rewrite project documents.

**When fixes go in circles.** Use the selected workflow’s debugging method. The five-round limit applies to each task and the same unresolved problem across tasks. Record attempts in the original tracker or execution ledger. At the limit, reassess the cause and continue independent work.

For a consequential unresolved question in either workflow, the main agent may use one fresh read-only consultation. Codex can do this during approved implementation with Astra xhigh. During recovery Claude uses its existing resumable diagnostic role. Provide the acceptance criteria, evidence, counterevidence and specific question. On Codex, the same allowance applies before and during recovery.

The consultant checks source evidence, forms its own explanation, and then compares the main agent's view. It may support or overturn that view, returning evidence that explains past failures or a discriminating experiment with expected outcomes. One targeted clarification with the same consultant may address evidence, omissions, or disagreements about the original question; it shares the diagnosis allowance and adds no investigation scope. Diagnostic and clarification use are tracked against both the task and the same unresolved gap in the existing execution record; changing workers, sessions, models, commits, task names, or plans does not reset them.

The main agent verifies the evidence, decides and continues. New evidence that explains earlier failures permits one recovery fix and one independent re-review. Superpowers retains its architecture check after three failed fixes. Ask for a decision only when the remaining action requires new authority, changes acceptance, or recovery is exhausted with no viable path. [Recovery template](references/execution-recovery-template.md)

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

For archive governance, the CLI checks the section structure and any declared workflow marker. It accepts legacy files without a marker. The router resolves their workflow during use. Test approval, file moves and retries by running the archive scenarios in [Validation Scenarios](references/validation-scenarios.md#f-archive-transition).

The size tests use identical project facts to compare generated `AGENTS.md` and standalone `CLAUDE.md` examples with the baseline from before the detailed rules moved into companions. Both must contain at least 20% fewer always-loaded English words, and shuffling line breaks does not count. This measures instruction size, not a promised reduction in your bill. It is a maintainer check, not homework for installing NHK.
