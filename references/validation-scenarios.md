# NHK Validation Scenarios

This is the semantic pressure-test set for the four NHK skills. Use it for prompt review and manual scenario testing. The optional repository validator checks deterministic structure only; it does not claim to prove these behavioral outcomes.

## A. Dependency Decisions

### A1. Missing dependency, no decision

**Prompt:** “Set up NHK. `planning-with-files` may be missing; continue if you can.”

**Setup:** `superpowers` is available and `planning-with-files` is not. The user has not selected install, enable, or adopt.

**Expected:** `welcome-to-nhk` names the missing dependency, explains the three choices when useful, and stops for a choice. It must not write workspace files, silently emulate the workflow, or treat willingness to continue as adopt.

### A2. Explicit adopt

**Prompt:** “Do not install it. Adopt its conventions for this run.”

**Expected:** NHK follows the missing workflow conventions manually for the current NHK run only. It writes no persistent adoption marker, does not claim installation, and reports that the dependency was not installed and its conventions were followed manually.

## B. Six Instruction Topologies

For topology detection, only a trimmed line exactly equal to `@AGENTS.md` or `@./AGENTS.md` counts. The line must be outside fenced code, Markdown blockquotes, and comments. Claude `@` imports of either companion doc are invalid routing, not topology signals.

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

## C. Bootstrap And Template Output

### C1. Simple prompt-first workspace

**Prompt:** “Bootstrap this small prompt-first repo; keep it minimal.”

**Expected:** Bootstrap creates or repairs one canonical source, both companion docs, `archive/`, and a stub `archive/README.md`. The coding guide stays within 80 lines, governance stays within 100, and no codemap is created. Bootstrap does not create root `task_plan.md`, `findings.md`, or `progress.md` unless the current work actually needs tracking.

### C2. Preserve healthy surfaces

**Setup:** The canonical instruction and one companion doc are already correct; the archive index is missing.

**Expected:** Bootstrap creates or repairs only the missing archive surface and required links. It does not regenerate healthy project-specific documents merely to match template wording.

### C3. Standalone generation contract

**Expected:** A generated standalone file has exactly the seven required top-level sections in order, no template markers or generation prompts, and no extra governance heading. Simple, medium, and complex outputs stay at or below 100, 125, and 150 lines respectively. There is no minimum and no padding. Project Map identifies the project, routes to the literal `coding-agent-guide.md` path, and names no directory tree, volatile workstream state, or separate codemap; Context routes to the literal `documentation-governance.md` path.

### C4. Thin CLAUDE generation

**Setup:** AGENTS is canonical and a Claude adapter is needed.

**Expected:** CLAUDE contains a valid AGENTS import plus only necessary Claude-specific notes, stays at or below 35 lines, and contains none of the seven standalone headings. It does not `@` import either companion doc. Once thin mode is chosen, standalone blocks are not processed.

### C5. Claude companion loading

**Setup:** A thin or standalone CLAUDE names `coding-agent-guide.md` or `documentation-governance.md` in prose, inline code, a blockquote, comment, fence, or active `@` import.

**Expected:** Backticked literal paths and non-active examples remain valid and load on demand. An active inline or standalone companion `@` import fails final validation because it would expand the document into every Claude session.

### C6. Routing guide is the shallow code map

**Expected:** `coding-agent-guide.md` has one Task Routing table with `Task or Symptom`, `Read First`, `Likely Change Surface`, and `Targeted Verification`, stays within 80 lines, and does not add separate current-state, packet, code-map, default-verification, or anti-detour sections.

### C7. Documentation governance stays on documents

**Expected:** `documentation-governance.md` stays within 100 lines and covers document roles, active surfaces, workspace/document map, lifecycle, naming/loading, and archive invariants. It contains no production-code map or step-by-step archive manual.

## D. Worker Cost And Collaboration

### D1. Per-worker cost ceiling

**Prompt:** “Use workers if useful, but keep costs bounded.”

**Expected:** The main thread's model and effort are treated as each worker's default ceiling, not a total concurrency budget. A known lower-cost supported configuration is allowed only when retries are unlikely to raise total cost. A known cost or effort increase requires prior user approval.

### D2. Unsupported or unclear configuration

**Setup:** The requested worker model/effort support or relative cost is unclear.

**Expected:** The main thread inherits the current configuration, keeps the packet on the main thread, or asks. It does not guess, rely on a stale static table, or silently fall back to a more expensive configuration.

### D3. Ultra boundary

**Expected:** The Codex/AGENTS contract reserves Ultra for main-thread orchestration and never assigns it to a worker. The CLAUDE template contains neither Ultra nor a static model or effort catalog.

### D4. Bounded fan-out and recursion

**Setup:** A task could be split into many small workers, and one worker asks to delegate again.

**Expected:** The main thread uses the fewest independent, reviewable packets. Recursive delegation is refused unless both the plan and the user explicitly authorized it. No unbounded fan-out occurs.

### D5. Shared writes and mutable state

**Setup:** Two packets touch the same file, generated artifact, mutable state, service state, or verification artifact.

**Expected:** They run serially. Parallel work is allowed only when ownership and state are independent.

### D6. Dispatch brief and timeout

**Expected:** Every brief states objective, read/write authority, owned scope, success criteria, verification, forbidden actions, and expected return. A timeout alone is not called blocked; actual progress is checked before inquiry, replacement, or termination, and completed idle workers are closed.

### D7. Non-converging fix loop

**Setup:** The same acceptance gap remains unresolved after five fix–verify or fix–review rounds.

**Expected:** The fifth failure triggers a mandatory stop. NHK invokes or restarts `systematic-debugging`, counts all five rounds as failed fixes, and forbids a sixth fix until root-cause and architecture reassessment is complete.

## E. Upkeep Boundaries

### E1. Ongoing workstream

**Setup:** The foundation is complete and docs have minor drift, but tasks remain or required verification is incomplete.

**Expected:** Upkeep repairs active references and status descriptions, restores the single routing table and 80/100-line companion limits, replaces Claude companion imports with literal paths, leaves all files in place, and does not ask about archive.

### E2. Completed archive candidate

**Setup:** One specific workstream has completion evidence and clearly related specs, plans, or tracking files.

**Expected:** Upkeep repairs drift, then asks whether that workstream should remain active or move to archive. It still does not move, rename, delete, reset, clear, or empty anything. A yes hands off to `nhk-archive`.

### E3. Missing foundation

**Setup:** `archive/README.md` or any other foundation surface is missing.

**Expected:** Upkeep routes through `welcome-to-nhk` to bootstrap before maintenance. It does not create the missing foundation inside upkeep.

## F. Archive Transition

### F1. User says no

**Prompt:** “No, keep it active.”

**Expected:** No move, copy, rename, index edit, reset, or clear occurs. Active tracking stays in place.

### F2. User says yes

**Setup:** Foundation is complete, one workstream is confirmed, and its related materials are clear.

**Expected:** NHK stages only those materials in one unambiguous destination while preserving active originals, adds one resolvable archive-index row, and verifies archived copies, names, contents, and the index location. Only after verification passes does it complete the governed move and update active documentation and governance. It updates the coding guide only when a real Task Routing row points to moved material.

### F3. Foundation missing

**Setup:** The user says yes, but `archive/` or `archive/README.md` is missing.

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

**Setup:** All four skills exist but the sibling `references/` directory is absent or incomplete.

**Expected:** Install validation fails and names the missing controlled assets.

### G3. Extra `nhk/` nesting

**Setup:** The install root contains only `nhk/welcome-to-nhk/`, `nhk/nhk-bootstrap/`, and the other NHK directories one level too deep.

**Expected:** Install validation fails and explains that the five NHK directories must be siblings directly under the chosen skills root.

### G4. Mixed versions

**Setup:** A skill or reference differs from the source package while the rest match.

**Expected:** Install validation fails as a mixed or stale installation. Unrelated sibling skills do not cause failure.

## H. Human Documentation Alignment

**Expected:** English and Chinese READMEs both describe five recurring jobs, four skills plus seven controlled references, the sibling install layout, optional validator, session refresh/discovery check, worker cost boundary, routing-table-as-shallow-map policy, and Claude's on-demand companion loading. Neither README presents scripts or tests as runtime dependencies.
