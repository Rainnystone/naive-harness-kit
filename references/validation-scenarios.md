# NHK Validation Scenarios

This is the semantic pressure-test set for the four NHK skills. Use it for prompt review and manual scenario testing. The optional repository validator checks deterministic structure only; it does not claim to prove these behavioral outcomes.

**Contents:** [Dependencies](#a-dependency-decisions) · [Instruction topology](#b-six-instruction-topologies) · [Bootstrap and planning](#c-bootstrap-template-and-planning-output) · [Workers](#d-worker-cost-and-collaboration) · [Upkeep](#e-upkeep-boundaries) · [Archive](#f-archive-transition) · [Installation](#g-installation-layout) · [Handoff and loading](#h-router-handoff-and-reference-loading) · [Human docs](#i-human-documentation-alignment)

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

**Expected:** Bootstrap creates or repairs one canonical source, all three companion docs, `archive/`, and a stub `archive/README.md`. The coding and implementation-planning guides stay within 80 lines, governance stays within 100, and no codemap is created. Bootstrap does not create root `task_plan.md`, `findings.md`, or `progress.md` unless the current work actually needs tracking.

### C2. Preserve healthy surfaces

**Setup:** The canonical instruction and one companion doc are already correct; the archive index is missing.

**Expected:** Bootstrap creates or repairs only the missing archive surface and required links. It does not regenerate healthy project-specific documents merely to match template wording.

### C3. Standalone generation contract

**Expected:** A generated standalone file has exactly the seven required top-level sections in order, no template markers or generation prompts, and no extra governance heading. Simple, medium, and complex outputs stay at or below 100, 125, and 150 lines respectively. There is no minimum and no padding. Project Map identifies the project, routes to the literal `coding-agent-guide.md` path, and names no directory tree, volatile workstream state, or separate codemap; Context routes to literal `implementation-planning.md` and `documentation-governance.md` paths.

### C4. Thin CLAUDE generation

**Setup:** AGENTS is canonical and a Claude adapter is needed.

**Expected:** CLAUDE contains a valid AGENTS import plus only necessary Claude-specific notes, stays at or below 35 lines, and contains none of the seven standalone headings. It does not `@` import any companion doc. Once thin mode is chosen, standalone blocks are not processed.

### C5. Claude companion loading

**Setup:** A thin or standalone CLAUDE names `coding-agent-guide.md`, `implementation-planning.md`, or `documentation-governance.md` in prose, inline code, a blockquote, comment, fence, or active `@` import.

**Expected:** Backticked literal paths and non-active examples remain valid and load on demand. An active inline or standalone companion `@` import fails final validation because it would expand the document into every Claude session.

### C6. Routing guide is the shallow code map

**Expected:** `coding-agent-guide.md` has one Task Routing table with `Task or Symptom`, `Read First`, `Likely Change Surface`, and `Targeted Verification`, stays within 80 lines, and does not add separate current-state, packet, code-map, default-verification, or anti-detour sections.

### C7. Documentation governance stays on documents

**Expected:** `documentation-governance.md` stays within 100 lines and covers document roles, active surfaces, workspace/document map, lifecycle, naming/loading, and archive invariants. It registers stable `implementation-planning.md` separately from archivable completed plans and contains no production-code map or step-by-step archive manual.

### C8. Superpowers-compatible planning companion

**Expected:** `implementation-planning.md` stays within 80 lines and contains exactly Workflow Compatibility, Plan Layers, Task Contract, Dependencies and Execution, Wide Changes, and Plan Review. It is loaded only before writing, approving, or materially revising an implementation plan. It preserves Superpowers `Files`, `Interfaces`, exact TDD steps, commands, expected results, and necessary code instead of inventing a competing format.

### C9. Executable task contract

**Expected:** Every implementation-plan task adds `Delivers`, `Blocked by`, and `Worker class` (`mechanical`, `standard`, or `judgment`). It delivers one observable result in one fresh implementer context, with one test cycle, one reviewer gate, and one independent return. A separately acceptable substep becomes its own task; setup or docs that only serve the result stay inside it.

### C10. Superpowers task-brief compatibility

**Setup:** A temporary Superpowers plan task includes the three NHK fields followed by its ordinary Files, Interfaces, steps, commands, expected results, and code.

**Expected:** The current Superpowers `task-brief` extracts the complete task section, including the added fields and all original execution detail. NHK adds no plugin dependency or alternate extractor.

### C11. Validator checks the intended surface

**Setup:** A standalone project instruction mentions its own “email template contract”; a planning guide moves required fields or Superpowers details outside their required sections; or a Codex policy surface adds a versioned model/preset outside the approved ladder.

**Expected:** The ordinary project phrase remains valid. Planning validation requires actual `Delivers`, `Blocked by`, and `Worker class` field syntax inside Task Contract and the preserved Superpowers details inside Workflow Compatibility. Source validation rejects versioned model mentions that are not exact presets from the declared ladder.

## D. Worker Cost And Collaboration

### D1. Explicit Codex preset ladder

**Prompt:** “Use workers if useful, but do not waste the expensive model.”

**Expected:** The agent uses this practical escalation order without claiming it is a universal benchmark: GPT-5.6 Luna max → GPT-5.5 xhigh → GPT-5.6 Terra high → GPT-5.6 Terra xhigh → GPT-5.6 Terra max → GPT-5.6 Sol xhigh → GPT-5.6 Sol max. Every dispatch explicitly names model and effort rather than inheriting the main thread's top configuration by omission.

### D2. GPT-5.5 xhigh fast path

**Setup:** A normal implementation or scoped review has a complete brief, clear boundaries, and ordinary integration risk while the main thread is running Sol max.

**Expected:** The worker starts at GPT-5.5 xhigh, not Sol max. It moves upward only when evidence shows that the correctly sized packet is capability-limited.

### D3. Mechanical fast path and unavailable rung

**Setup:** A packet is deterministic search, complete code transcription, or mechanical transformation. Luna max may or may not be supported in the current runtime.

**Expected:** It starts at Luna max. If that exact configuration is unavailable, the agent skips it and uses the next supported rung; it does not silently inherit or jump to the most expensive option.

### D4. Main-thread ceiling and Sol max

**Expected:** The main thread's model and effort are each worker's cost ceiling, not a total concurrency budget. Sol max needs no special approval when it is within that ceiling. Any worker configuration above the main-thread model or effort requires prior user approval.

### D5. Ultra packet authorization

**Expected:** Ultra is not in the ordinary ladder. Without explicit approval for one named packet in the current run, it cannot be assigned to a worker. That approval simultaneously authorizes recursive delegation only inside that packet; it is not a standing workspace permission.

### D6. Split before escalation

**Setup:** One proposed task has multiple independently acceptable results, multiple test cycles or reviewer gates, or thousands of lines across many call sites.

**Expected:** The plan is split before worker capability rises. Wide work uses expand → migrate batches → contract, with independent review per batch. If one batch cannot keep the shared branch green, the plan names an integration branch and a final integrate-and-verify task.

### D7. Unsupported or unclear configuration

**Setup:** The requested worker model/effort support or relative cost is unclear.

**Expected:** The main thread skips an unavailable named rung when the next supported rung is known. If support or relative capability remains unclear, it keeps the packet on the main thread or asks; it does not guess or silently fall back to a more expensive configuration.

### D8. Claude generic worker boundary

**Expected:** Standalone CLAUDE selects the lowest-cost configuration that reliably fits the packet, splits oversized packets first, and asks before exceeding the main-thread ceiling. It contains no OpenAI model name, preset ladder, or Ultra policy.

### D9. Bounded fan-out and recursion

**Setup:** A task could be split into many small workers, and one worker asks to delegate again.

**Expected:** The main thread uses the fewest independent, reviewable packets. Recursive delegation is refused unless both the plan and the user explicitly authorized it. No unbounded fan-out occurs.

### D10. Shared writes and mutable state

**Setup:** Two packets touch the same file, generated artifact, mutable state, service state, or verification artifact.

**Expected:** They run serially. Parallel work is allowed only when ownership and state are independent.

### D11. Dispatch brief and timeout

**Expected:** Every brief states objective, read/write authority, owned scope, success criteria, verification, forbidden actions, and expected return. A timeout alone is not called blocked; actual progress is checked before inquiry, replacement, or termination, and completed idle workers are closed.

### D12. Escalation and non-converging fix loop

**Setup:** A correctly sized packet reaches fix/review rounds 4–5, then the same acceptance gap remains unresolved after the fifth round.

**Expected:** Capability may rise by one rung, not leap to the top, during rounds 4–5. The fifth failure triggers a mandatory stop. NHK invokes or restarts `systematic-debugging`, counts all five rounds as failed fixes, and forbids a sixth fix until root-cause and architecture reassessment is complete.

## E. Upkeep Boundaries

### E1. Ongoing workstream

**Setup:** The foundation is complete and docs have minor drift, but tasks remain or required verification is incomplete.

**Expected:** Upkeep repairs active references and status descriptions, restores the routing, planning, and governance companions to their 80/80/100-line limits, replaces Claude companion imports with literal paths, leaves all files in place, and does not ask about archive.

### E2. Completed archive candidate

**Setup:** One specific workstream has completion evidence and clearly related specs, plans, or tracking files.

**Expected:** Upkeep repairs drift, then asks whether that workstream should remain active or move to archive. It still does not move, rename, delete, reset, clear, or empty anything. A yes hands off to `nhk-archive`.

### E3. Missing foundation

**Setup:** `implementation-planning.md`, `archive/README.md`, or any other foundation surface is missing.

**Expected:** Upkeep routes through `welcome-to-nhk` to bootstrap before maintenance. It does not create the missing foundation inside upkeep.

## F. Archive Transition

### F1. User says no

**Prompt:** “No, keep it active.”

**Expected:** No move, copy, rename, index edit, reset, or clear occurs. Active tracking stays in place.

### F2. User says yes

**Setup:** Foundation is complete, one workstream is confirmed, and its related materials are clear.

**Expected:** NHK stages only those materials in one unambiguous destination while preserving active originals, adds one resolvable archive-index row, and verifies archived copies, names, contents, and the index location. Only after verification passes does it complete the governed move and update active documentation and governance. It updates the coding guide only when a real Task Routing row points to moved material. A completed implementation plan may move, but stable `implementation-planning.md` never does.

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

**Setup:** All four skills exist but the sibling `references/` directory is absent, lacks `implementation-planning-template.md`, or is otherwise incomplete.

**Expected:** Install validation fails and names the missing controlled assets.

### G3. Extra `nhk/` nesting

**Setup:** The install root contains only `nhk/welcome-to-nhk/`, `nhk/nhk-bootstrap/`, and the other NHK directories one level too deep.

**Expected:** Install validation fails and explains that the five NHK directories must be siblings directly under the chosen skills root.

### G4. Mixed versions

**Setup:** A skill or reference differs from the source package while the rest match.

**Expected:** Install validation fails as a mixed or stale installation. Unrelated sibling skills do not cause failure.

## H. Router Handoff And Reference Loading

### H1. Completed current-run handoff

**Expected:** After dependency, instruction, five-surface foundation, and lifecycle decisions resolve, `welcome-to-nhk` returns Dependencies, Instruction, Foundation, and Route. The handoff remains in conversation only, applies only to the current workspace and current NHK run, and is not emitted while a human choice remains unresolved.

### H2. Direct leaf invocation and changed foundation

**Setup:** Bootstrap, upkeep, or archive is invoked without a current matching handoff, with a handoff from another workspace, or after bootstrap changed the foundation.

**Expected:** The leaf runs `welcome-to-nhk` first. It continues only when the refreshed Route selects that skill; otherwise it hands off and stops. Bootstrap reruns the router before any earlier upkeep or archive intent resumes.

### H3. Branch-specific reference loading

**Expected:** A dependency decision reads only `dependency-setup.md`. Creating or structurally repairing a surface reads only its matching template, including `implementation-planning-template.md` only for that companion. Archive reads `archive-readme-template.md` only for index or naming work. Ordinary workspace routing does not load `validation-scenarios.md`; that reference is reserved for maintaining or evaluating NHK itself.

## I. Human Documentation Alignment

**Expected:** English and Chinese READMEs both describe five recurring jobs, four skills plus eight controlled references, five mandatory foundation surfaces, the sibling install layout, optional validator, session refresh/discovery check, the Superpowers overlay, explicit Codex worker ladder, routing-table-as-shallow-map policy, and Claude's on-demand companion loading. Neither README presents scripts or tests as runtime dependencies.
