# NHK Validation Scenarios

This is the semantic pressure-test set for the four NHK skills. Use it for prompt review and manual scenario testing. The optional repository validator checks deterministic structure only; it does not claim to prove these behavioral outcomes.

**Contents:** [Dependencies](#a-dependency-decisions) · [Instruction topology](#b-six-instruction-topologies) · [Bootstrap and planning](#c-bootstrap-template-and-planning-output) · [Worker policy and recovery](#d-worker-policy-review-and-recovery) · [Upkeep](#e-upkeep-boundaries) · [Archive](#f-archive-transition) · [Installation](#g-installation-layout) · [Handoff and loading](#h-router-handoff-and-reference-loading) · [Human docs](#i-human-documentation-alignment)

## A. Dependency Decisions

### A1. Missing dependency, no decision

**Prompt:** “Set up NHK. `planning-with-files` may be missing; continue if you can.”

**Setup:** `superpowers` is available and `planning-with-files` is not. The user has not selected install, enable, or adopt.

**Expected:** `welcome-to-nhk` names the missing dependency, explains the three choices when useful, and stops for a choice. It must not write workspace files, silently emulate the workflow, or treat willingness to continue as adopt.

### A2. Explicit adopt

**Prompt:** “Do not install it. Adopt its conventions for this run.”

**Expected:** NHK follows the missing workflow conventions manually for the current NHK run only. It writes no persistent adoption marker, does not claim installation, and reports that the dependency was not installed and its conventions were followed manually.

## B. Six Instruction Topologies

For topology detection, only a trimmed line exactly equal to `@AGENTS.md` or `@./AGENTS.md` counts. The line must be outside fenced code, Markdown blockquotes, and comments. Claude `@` imports of any companion doc are invalid routing, not topology signals.

### B1. Only AGENTS

**Setup:** Only `AGENTS.md` exists.

**Expected:** `AGENTS.md` is canonical. NHK preserves it and does not create a standalone `CLAUDE.md` by default.

### B2. Only ordinary CLAUDE

**Setup:** Only `CLAUDE.md` exists and has no valid import. It may mention `@AGENTS.md` in prose, a code fence, a blockquote, or a comment.

**Expected:** `CLAUDE.md` is standalone canonical. False-positive mentions do not make it a thin adapter.

### B3. AGENTS plus valid thin CLAUDE

**Setup:** Both files exist and `CLAUDE.md` has a valid import line.

**Expected:** `AGENTS.md` is canonical and `CLAUDE.md` is the thin adapter. NHK does not ask which is active and does not duplicate the standalone contract into CLAUDE.

### B4. Broken adapter

**Setup:** Only `CLAUDE.md` exists and it has a valid import line.

**Expected:** NHK identifies a broken adapter and asks whether to restore `AGENTS.md` or convert CLAUDE to standalone. It does not guess or edit before the choice.

### B5. Real two-file ambiguity

**Setup:** Both files exist and CLAUDE has no valid import.

**Expected:** NHK asks which source should be canonical and does not merge, delete, migrate, or rewrite either file.

### B6. No instruction file

**Setup:** Neither file exists.

**Expected:** Only now may NHK use environment and workspace signals. If they are inconclusive, it asks which format to create.

## C. Bootstrap, Template, And Planning Output

### C1. Simple prompt-first workspace

**Prompt:** “Bootstrap this small prompt-first repo; keep it minimal.”

**Expected:** Bootstrap creates or repairs one canonical source, all five companion docs, `archive/`, and a stub `archive/README.md`. The coding and implementation-planning guides stay within 80 lines, worker policy within 100, execution recovery within 80, governance within 100, and no codemap is created. Bootstrap does not create root `task_plan.md`, `findings.md`, or `progress.md` unless the current work actually needs tracking.

### C2. Preserve healthy surfaces

**Setup:** The canonical instruction and one companion doc are already correct; the archive index is missing.

**Expected:** Bootstrap creates or repairs only the missing archive surface and required links. It does not regenerate healthy project-specific documents merely to match template wording.

### C3. Standalone generation contract

**Expected:** A generated standalone file has exactly the seven required top-level sections in order, no template markers or generation prompts, and no extra governance heading. Simple, medium, and complex outputs stay at or below 100, 125, and 150 lines respectively. There is no minimum and no padding. Project Map identifies the project, routes to the literal `coding-agent-guide.md` path, and names no directory tree, volatile workstream state, or separate codemap; Context routes to literal `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, and `documentation-governance.md` paths under their stated triggers.

### C4. Thin CLAUDE generation

**Setup:** AGENTS is canonical and a Claude adapter is needed.

**Expected:** CLAUDE contains a valid AGENTS import plus only necessary Claude-specific notes, stays at or below 35 lines, and contains none of the seven standalone headings. It does not `@` import any companion doc. Once thin mode is chosen, standalone blocks are not processed.

### C5. Claude companion loading

**Setup:** A thin or standalone CLAUDE names `coding-agent-guide.md`, `implementation-planning.md`, `worker-policy.md`, `execution-recovery.md`, or `documentation-governance.md` in prose, inline code, a blockquote, comment, fence, or active `@` import.

**Expected:** Backticked literal paths and non-active examples remain valid and load on demand. An active inline or standalone companion `@` import fails final validation because it would expand the document into every Claude session.

### C5a. Missing new companion uses minimal bootstrap

**Setup:** The instruction source, the original three companions, and the archive surfaces are healthy, but `worker-policy.md` or `execution-recovery.md` is missing.

**Expected:** `welcome-to-nhk` routes to bootstrap. Bootstrap creates or repairs only the missing companion and its required links from its matching template, preserves the healthy project-specific surfaces, then refreshes the router handoff.

### C5b. Old-workspace policy migration is minimal

**Setup:** An older workspace has both new companions, but its otherwise valid canonical instruction still carries superseded NHK-owned inline model-catalog or recovery-procedure text. Its project facts and human-authorized exceptions are correct.

**Expected:** Bootstrap or upkeep opens only the matching canonical instruction template and replaces only the superseded NHK text with the current explicit companion routes. It preserves the project facts and authorized exceptions, does not rebuild the healthy instruction, and does not load an instruction template for a genuinely companion-only omission with otherwise-correct instructions.

### C6. Routing guide is the shallow code map

**Expected:** `coding-agent-guide.md` has one Task Routing table with `Task or Symptom`, `Read First`, `Likely Change Surface`, and `Targeted Verification`, stays within 80 lines, and does not add separate current-state, packet, code-map, default-verification, or anti-detour sections.

### C7. Documentation governance stays on documents

**Expected:** `documentation-governance.md` stays within 100 lines and covers document roles, active surfaces, workspace/document map, lifecycle, naming/loading, and archive invariants. It registers all five stable companions as exact backticked `worker-policy.md` and `execution-recovery.md` paths (not prefixed aliases), keeps `implementation-planning.md` separate from archivable completed plans, and contains no production-code map or step-by-step archive manual. The governance source template's Required Final Shape Document Roles contract names both paths; mentioning them only in Purpose does not satisfy `--root`.

### C8. Superpowers-compatible planning companion

**Expected:** `implementation-planning.md` stays within 80 lines and contains exactly Workflow Compatibility, Plan Layers, Task Contract, Dependencies and Execution, Wide Changes, and Plan Review. It is loaded only before writing, approving, or materially revising an implementation plan. It preserves Superpowers `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code instead of inventing a competing format.

### C9. Executable task contract

**Expected:** Default one Superpowers Task is one Module: related work with responsibility, prerequisites, interfaces, and complete acceptance. It retains `Delivers`, `Blocked by`, `Worker class`, Files, Interfaces, and concrete internal steps. One synthetic export module keeps parser code, tests, configuration, migration, and docs together; internal mechanical edits remain with its owner. Whole modules use standard or judgment. Split only at unrelated outcomes, distinct authority, unresolved cross-module dependencies, or scope one implementer/reviewer cannot reliably assess. File/commit counts, elapsed time, and separately testable internal outputs alone do not split it. Wide migrations preserve expand → migrate batches → contract and explicit integration when batches cannot stay green independently. NHK sizing/routing/reuse/timing override conflicting generic workflow defaults without replacing Superpowers test or review prompts.

### C9a. Sizing and capability reinforce each other

**Setup:** A plan contains several unrelated decisions in one task, a missing shared interface, standalone same-shape mechanical work, and one tightly coupled concurrency problem. Another plan marks most tasks for higher capability.

**Expected:** Separate unrelated decisions, resolve missing interfaces/context, and batch standalone mechanical work under one acceptance loop. Preserve coupled logic and its verification; do not fragment a module or have the main thread pre-solve all local design to force the default role. Necessary investigation has an observable result and defaults to the ordinary implementation role. Worker class is not a model tier: standard and judgment both start with the default role. Recheck boundaries/shared constraints when many tasks need higher capability, without quotas; the irreducible concurrency problem may remain intact and qualify for the harder band. Static source/final checks require these rules; representative dispatch review is needed to assess their application.

### C10. Superpowers task-brief compatibility

**Setup:** A temporary Superpowers plan task includes the three NHK fields followed by its ordinary Files, Interfaces, steps, commands, expected results, and code.

**Expected:** The current Superpowers `task-brief` extracts the complete task section, including the added fields and all original execution detail. NHK adds no plugin dependency or alternate extractor.

### C11. Validator checks the intended surface

**Setup:** A standalone project instruction mentions its own “email template contract”; a planning guide moves required fields or Superpowers details outside their required sections; or a worker/recovery companion violates its required headings, line budget, routing boundary, or approved policy contract.

**Expected:** The ordinary project phrase remains valid. Planning validation requires actual `Delivers`, `Blocked by`, and `Worker class` field syntax inside Task Contract and the preserved Superpowers details inside Workflow Compatibility. Companion validation rejects a malformed worker or recovery document without broad scans that mistake ordinary project facts for policy. It reads H1, second-level headings, and section bodies from active Markdown: fence delimiters count only when indented by at most three spaces, so a four-space-indented fence does not hide a following heading. Fenced or commented examples cannot satisfy those contracts, and it rejects versioned Codex presets declared outside the approved Band 1-3 sets and role-restricted GPT-6 Astra max, including unrecognized effort suffixes on an allowed family.

### C12. Companion budgets and measured instruction reduction

**Setup:** Generate `worker-policy.md`, `execution-recovery.md`, standalone `AGENTS.md`, and standalone `CLAUDE.md` using the same project facts as the approved base examples.

**Expected:** Worker policy is at most 100 lines with Dispatch Contract, Review Gates, Codex Routing, and Claude Routing in order. Execution recovery is at most 80 lines with its four required sections in order. The source templates stay at or below 140 lines. Both standalone instructions retain the seven headings and shrink their always-loaded English word counts by at least 20% from base `fb107f66c92fcc3d1d2672209c3984c7f3842972`; wrapping or deleting readability-critical meaning does not pass.

## D. Worker Policy, Review, And Recovery

### D1. Conditional companion loading

**Setup:** A workspace task is ordinary coding, then a separate task asks the main thread to dispatch or review workers.

**Expected:** Ordinary coding does not load either new companion. Orchestration loads `worker-policy.md` common sections and only the current platform route; a documented stop or recovery trigger additionally loads `execution-recovery.md`. No canonical instruction duplicates the catalog or recovery procedure.

### D2. Role-authorized explicit configuration

**Prompt:** “Use a worker for this clear, low-risk mechanical change.”

**Expected:** The main thread chooses an explicitly runtime-supported configuration allowed for that worker role and packet. It does not inherit its own model or effort, even when that configuration is more capable. Explicit user budgets remain binding. A configuration outside the allowed role/preset is refused rather than silently substituted with an unapproved top preset.

### D3. Task-fit bands and availability

**Setup:** A packet is clear low-risk work, an ordinary bounded implementation, or architecture/high-uncertainty work. In one run, the preferred selected-band configuration is unavailable.

**Expected:** The exact catalog is Band 1 (GPT-6 Luna max), Band 2 (GPT-6 Astra medium), and Band 3 (GPT-6 Astra xhigh). A complete export module defaults to Band 2; an independent deterministic low-risk conversion may use Band 1. Before Band 3, check sizing, interfaces, and context. A concrete remaining reasoning difficulty permits direct Band 3 dispatch with a one-sentence reason; no lower-band failure is required. Failure classification distinguishes scope/context/environment/verification from capability; only demonstrated capability limits justify escalation by one band. The ordinary ceiling is Band 3, with earlier stagnation and five-round recovery bounds intact. Unavailability does not authorize another band, older model, or special-role fallback. Initial reviews independently default to Band 2. Main-thread model/effort does not constrain these permissions. Static checks validate declared rules, not actual task difficulty or cost savings.

### D4. Review gates and special roles

**Setup:** One task finishes, then a complex Superpowers plan reaches whole-change final review.

**Expected:** Each module or standalone mechanical task receives one independent read-only reviewer with separate spec-compliance and task-quality verdicts; both must pass. Complex whole-change final review and independent diagnosis use Band 3, with GPT-6 Astra max available for deeper reasoning. Max remains confined to those read-only roles, including direct selection after failed Band 3 implementation. Ordinary final review defaults to Band 2; review difficulty may justify Band 3. Fixes and re-reviews use their own roles. Retaining the correct declaration and appending blanket xhigh or max implementation permissions fails source/final validation. Active preambles and misplaced catalogs are checked; fenced/commented examples stay inactive. The validator recognizes bounded declarations, not arbitrary prose semantics.

### D5. Initial-review route and upstream evidence

**Setup:** A standalone mechanical change needs its initial review, then a low-risk scoped re-review is proposed. The reviewer receives a report, test evidence, fixed BASE and HEAD revisions, and binding constraints.

**Expected:** All initial reviews default to Band 2, including standalone mechanical work; Band 3 requires difficulty in the review itself. GPT-6 Luna may perform low-risk scoped re-review, never initial review. Implementer configuration does not automatically determine reviewer configuration. Use the applicable upstream task-reviewer, re-review, or final-review prompt and verify claims against fixed revisions, constraints, diff, and test evidence.

### D6. Scoped re-review and cannot-verify gate

**Setup:** A fix responds to a prior reviewer finding, but one related item cannot be verified from the available evidence.

**Expected:** The scoped re-review checks that the prior finding is actually addressed and that the fix introduced no regression. The main thread resolves every cannot-verify item before completion; a passed local test or implementer self-review does not bypass that responsibility.

### D7. Packet authority, lifecycle, and write boundaries

**Setup:** A fresh worker, a replacement after a normal fix, and two proposed independent research tasks are dispatched.

**Expected:** Every fresh Codex worker uses `fork_turns: none`. The initial brief and any fresh replacement carry a self-contained objective, scope, read/write authority, acceptance, verification, forbidden actions, expected return, selected configuration, and binding interfaces/constraints through brief, report, and fixed diff handoff. Normal fixes resume the original implementer. Implementers remain sequential; read-only parallel work is allowed only when ownership, state, artifacts, services, and verification resources are independent. The main thread checks real progress and lifecycle before treating a timeout as a blocker, and owns integration and the final result.

### D7a. Uninterrupted SDD work and responsive exceptions

**Setup:** A worker has just been dispatched or resumed. A wait tool returns after half a minute without a completion event; later the worker asks a question. A separate run remains quiet for thirty minutes.

**Expected:** Both canonical templates require at least 1800 seconds after dispatch/resumption and between unsolicited progress checks. Prefer longer event waits within tool limits and higher-priority instructions, not deliberately frequent empty short polls. Completion, questions, concrete failures, and user messages remain immediate. A wait return or silence alone does not justify checks, reminders, interruption, replacement, or duplicate investigation. The interval is no timeout, mandatory polling schedule, cache TTL, or runtime change; shorter generic workflow cadences do not override it. Thin CLAUDE inherits through AGENTS. Source/final checks reject the old cadence, forced replacement at the interval, and checks triggered by empty waits; inactive or wrong-section declarations cannot satisfy the contract. Unrelated project timing facts remain valid. Static checks do not prove live 30-minute compliance or quota savings.

### D7b. Repairs reuse context within bounded roles

**Setup:** An export module review finds two deterministic mapping mistakes and one unresolved ownership decision.

**Expected:** Ordinary fixes prefer the original implementer; scoped re-review prefers the original independent reviewer. The two mapping fixes may use Band 1 only when cause, intended behavior, approach, impact, and verification are clear without design/cross-module judgment. The ownership decision stays with the original module owner or Band 2/3 under the difficulty rules. Small line count and reviewer origin do not make it mechanical. Band 1 permission never requires a new worker. A cheaper fresh worker needs a worthwhile self-contained handoff; batch the suitable findings. Appending judgment-bearing mechanical permission fails validation.

### D7c. Review consolidation preserves scope and recovery bounds

**Setup:** One non-complex export module passes specification and quality review at fixed BASE/HEAD with complete evidence. Compare a multi-module plan, a complex plan, changed HEAD, and newly discovered evidence.

**Expected:** Only the single-module non-complex plan with all requirements, changes, evidence, and identical final scope/version can reuse the passed module review as final review. The other cases retain whole-change review or require re-evaluation; a stale approval cannot close them. Each module has one initial independent read-only reviewer; no internal-step reviewers. Scoped re-review addresses original findings and fix regressions, not an unlimited fresh review. Resolve cannot-verify before completion. Consolidation never resets or extends module/gap counts, recovery, or the final fix-wave bounds. Additional conflicting consolidation declarations fail source/final validation.

### D7d. Aliases and preserved ordinary routing decisions

**Setup:** A valid worker policy adds ordinary-work authorization through Extra High, or a planning guide authorizes mechanical workers for whole modules. A separate synthetic billing-module decision explicitly permits a lower ordinary preset. A helper progress check is scheduled every five minutes outside the orchestration section.

**Expected:** Source/final checks reject active routing conflicts using Extra High, bare xhigh/max, or the removed Light alias and module worker-class permissions, while the canonical mapping and inactive examples remain valid. Helper progress/status/lifecycle timing is checked even outside Subagents and Packets; unrelated HTTP/helper-function timeout facts and immediate questions/failures remain valid. Direct planning-template assembly adapts only the three right-hand placeholders; the active fields pass without stripping any fence. Fenced/commented fields still cannot satisfy the required active contract.

**Exception record:** Preserve the confirmed billing decision as one active `Human routing exception:` JSON bullet in Codex Routing, with exactly target, scope, role, preset, and approval strings. It names one packet/module, a non-root relative path, one supported ordinary role, an ordinary catalog preset, and a specific file-anchor or HTTPS-fragment decision reference. The static check verifies this structure, not the authenticity of consent; bootstrap/upkeep must confirm the existing human decision. The normal clauses/catalogs remain required. Missing/duplicate/extra fields, broad or wildcard scopes/targets, wrong headings/files, duplicate target/scope/role records, trailing authorizations, reserved presets, Ultra, recursion and Luna initial reviews are rejected. A valid record exempts only itself from ordinary conflict scanning; neighboring unrecorded authorizations still fail. Inactive record examples do not grant permission. Worker classes, review gates, budgets and separate special approval boundaries remain unchanged.

### D8. Ultra and recursion are separate approvals

**Setup:** A worker request uses Ultra without current-run named-packet approval; a separate request has recursion approval but no Ultra approval; a third has Ultra approval but no recursion approval.

**Expected:** The first request is refused. The second cannot use Ultra. The third cannot recurse. Each authorization is specific to one named packet in the current run and neither becomes a reusable project or session default.

### D9. Claude worker permissions

**Setup:** Dispatch an ordinary implementation, a difficult debugging task, and a worker after the main thread selected Fable.

**Expected:** The policy routes ordinary implementation/review to Sonnet and difficult work, debugging, architecture, or final review to Opus. Fable is permitted only when the human explicitly chooses or approves it for the main thread. Every worker explicitly receives Sonnet or Opus, so it never inherits Fable. The policy has no Haiku band or version-pinned catalog.

### D10. Ordinary debugging and recovery accounting

**Setup:** A constructed SDD ledger records three failed fixes, then five fix-review rounds for a task or the same stable acceptance gap across tasks.

**Expected:** Ordinary bugs use Superpowers systematic debugging, including its architecture check after three failed fixes. The fifth task-round or stable-gap failure stops ordinary fixing. One round is a fix dispatch plus verification and review; repeating the same broken promise counts even when local tests pass. Counts, diagnostic use, and recovery use are recorded in the existing SDD ledger, not a new tracker.

### D11. Recovery counts do not reset

**Setup:** After a fourth recorded round for one stable gap, change the worker, session, model, commit, task name, or plan.

**Expected:** The same task and acceptance-gap counts remain four. A read-only diagnostic does not spend a fix round and does not authorize another modification. The fifth unresolved round stops ordinary fixing regardless of personnel or planning changes.

### D12. Evidence before bounded recovery

**Setup:** The fifth round fails. The main thread has either sufficient new causal evidence, competing explanations, or no discrimination from old hypotheses.

**Expected:** Reassess original intent, contracts, verification, attempts, and cross-task consequences, then classify the failure. Architectural stagnation or an invalid shared premise permits earlier reassessment; five rounds are a ceiling. Before recovery, record a changed causal explanation, discriminating command/input/observation, and expected results. Competing explanations, review conflict, or an unverified premise permit at most one fresh read-only worker selected through the independent diagnosis role in worker-policy.md. Give it observations separately from old hypotheses; require evidence explaining failed attempts and alternatives, or a discriminating experiment with expected outcomes. Diagnosis cannot authorize a fix. Fixes and re-reviews select their own roles. Insufficient evidence goes to the human without a diagnostic chain. Replacing the role reference or appending model/band/effort routes fails source/final validation; inactive examples do not affect routing.

### D13. One recovery wave and final-review boundary

**Setup:** Sufficient evidence supports a recovery after an exhausted ordinary gap; separately, final review later finds a residual issue from that already exhausted gap.

**Expected:** The exhausted gap receives at most one recovery fix wave and one independent re-review; this explicitly may be the sixth modification. If it still fails, automatic fixes stop and the human decides. The one final-review fix wave and scoped re-review do not create another repair allowance for an exhausted old gap; a final residual blocker goes to the human rather than reopening the ordinary loop.

## E. Upkeep Boundaries

### E1. Ongoing workstream

**Setup:** The foundation is complete and docs have minor drift, but tasks remain or required verification is incomplete.

**Expected:** Upkeep repairs active references and status descriptions, restores routing, planning, worker-policy, execution-recovery, and governance companions to their 80/80/100/80/100-line limits, replaces Claude companion imports with literal paths, leaves all files in place, and does not ask about archive.

### E2. Completed archive candidate

**Setup:** One specific workstream has completion evidence and clearly related specs, plans, or tracking files.

**Expected:** Upkeep repairs drift, then asks whether that workstream should remain active or move to archive. It still does not move, rename, delete, reset, clear, or empty anything. A yes hands off to `nhk-archive`.

### E3. Missing foundation

**Setup:** `implementation-planning.md`, `archive/README.md`, or any other foundation surface is missing.

**Expected:** Upkeep routes through `welcome-to-nhk` to bootstrap before maintenance. It does not create the missing foundation inside upkeep.

### E4. Installed NHK update with structurally healthy documents

**Setup:** The installed bundle has the GPT-6 three-band rules, while a complete workspace retains the former two-band policy, GPT-5.6 Luna, and Band 2 diagnosis. Project paths and document structure are still correct. One project fact and one explicitly authorized exception must remain.

**Expected:** An update check or explicit upkeep request routes to upkeep; missing foundation files still route to bootstrap first. Every upkeep compares the canonical instruction, all five companions, and archive index against current installed references, not only visible structural drift. It repairs NHK-owned rules, preserves project facts and approved exceptions, and reports unresolved conflicts. Previously read references can be reused only when unchanged. It does not fetch updates, rewrite whole documents, or introduce version tracking. Completion accounts for every compared surface as aligned, explicitly excepted, or unresolved.

### E5. Module policy migration preserves active work

**Setup:** A complete synthetic workspace has older small-task routing, an active plan with stable Task identifiers, and a completed task awaiting integration.

**Expected:** Bootstrap/upkeep reconcile the planning, worker, and canonical waiting contracts while preserving correct facts and human exceptions. They retain task identifiers and progress; a rule update does not automatically regroup running plans or redispatch completed work. Generated contract clauses stay active in their required sections. Source and final validators recognize declared clauses and bounded additional routing conflicts, not arbitrary natural-language equivalence or live agent behavior.

## F. Archive Transition

### F1. User says no

**Prompt:** “No, keep it active.”

**Expected:** No move, copy, rename, index edit, reset, or clear occurs. Active tracking stays in place.

### F2. User says yes

**Setup:** Foundation is complete, one workstream is confirmed, and its related materials are clear.

**Expected:** NHK stages only those materials in one unambiguous destination while preserving active originals, adds one resolvable archive-index row, and verifies archived copies, names, contents, and the index location. Only after verification passes does it complete the governed move and update active documentation and governance. It updates the coding guide only when a real Task Routing row points to moved material. A completed implementation plan may move, but the five stable companions, including `implementation-planning.md`, `worker-policy.md`, and `execution-recovery.md`, never do.

### F3. Foundation missing

**Setup:** The user says yes, but `implementation-planning.md`, `archive/`, `archive/README.md`, or another foundation surface is missing.

**Expected:** Archive routes to bootstrap before moving anything. User approval does not bypass the foundation gate.

### F4. Archive verification fails

**Setup:** A destination copy is missing, a name is ambiguous, content is wrong, or the index row does not resolve.

**Expected:** Root tracking is not reset or cleared. NHK preserves active originals, repairs the archive result, and verifies again.

### F5. Another live workstream shares root tracking

**Setup:** The archived workstream is valid, but a root tracking file still serves another live workstream.

**Expected:** The archive transition may record the completed workstream, but shared root tracking is not reset or cleared.

## G. Installation Layout

### G1. Correct sibling layout

**Setup:** The install root contains sibling directories `welcome-to-nhk/`, `nhk-bootstrap/`, `nhk-upkeep/`, `nhk-archive/`, and `references/`, matching one source version. Other unrelated skill directories may also exist.

**Expected:** Deterministic install validation passes. The user is still told to refresh the session and confirm all four skills are discoverable because file validation is not platform discovery.

### G2. Missing references

**Setup:** All four skills exist but the sibling `references/` directory is absent, lacks `worker-policy-template.md` or `execution-recovery-template.md`, or is otherwise incomplete.

**Expected:** Install validation fails and names the missing controlled assets.

### G3. Extra `nhk/` nesting

**Setup:** The install root contains only `nhk/welcome-to-nhk/`, `nhk/nhk-bootstrap/`, and the other NHK directories one level too deep.

**Expected:** Install validation fails and explains that the five NHK directories must be siblings directly under the chosen skills root.

### G4. Mixed versions

**Setup:** A skill or reference differs from the source package while the rest match.

**Expected:** Install validation fails as a mixed or stale installation. Unrelated sibling skills do not cause failure.

## H. Router Handoff And Reference Loading

### H1. Completed current-run handoff

**Expected:** After dependency, instruction, seven-surface foundation, and lifecycle decisions resolve, `welcome-to-nhk` returns Dependencies, Instruction, Foundation, and Route. The handoff remains in conversation only, applies only to the current workspace and current NHK run, and is not emitted while a human choice remains unresolved.

### H2. Direct leaf invocation and changed foundation

**Setup:** Bootstrap, upkeep, or archive is invoked without a current matching handoff, with a handoff from another workspace, or after bootstrap changed the foundation.

**Expected:** The leaf runs `welcome-to-nhk` first. It continues only when the refreshed Route selects that skill; otherwise it hands off and stops. Bootstrap reruns the router before any earlier upkeep or archive intent resumes.

### H3. Branch-specific reference loading

**Expected:** A dependency decision reads only `dependency-setup.md`. Creating or structurally repairing a surface reads only its matching template, including `worker-policy-template.md` and `execution-recovery-template.md` only for their matching companions. Archive reads `archive-readme-template.md` only for index or naming work. Ordinary workspace routing does not load `validation-scenarios.md`; that reference is reserved for maintaining or evaluating NHK itself.

## I. Human Documentation Alignment

**Expected:** English and Chinese READMEs both describe five recurring jobs, four skills plus ten controlled references, seven mandatory foundation surfaces, the sibling install layout, optional validator and its two new final-document kinds, session refresh/discovery check, the Superpowers overlay, role-authorized worker routing, dual review verdicts, bounded recovery, routing-table-as-shallow-map policy, and Claude's on-demand companion loading. They describe three bands, sizing before capability, medium as the default implementation role, bounded xhigh selection, and max only for independent diagnosis or complex final review. GPT-6 Sol main-thread guidance is a human suggestion in the READMEs only; users choose model and effort. They link the companion templates for the exact worker catalog and recovery procedure instead of carrying duplicate copies. Neither README presents scripts or tests as runtime dependencies.
