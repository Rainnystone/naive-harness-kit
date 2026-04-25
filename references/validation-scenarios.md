# NHK Validation Scenarios

This file is the baseline pressure-test set for NHK skill validation. Each scenario is written against the no-skill baseline so the current skill set can be checked against the exact failure it is meant to prevent.

## 1. Missing Dependency Detection

**Target skill:** `welcome-to-nhk`

**Test prompt:** “Set up NHK for this workspace. I’m not sure whether `superpowers` or `planning-with-files` is installed, but continue if you can.”

**Pressure setup:** `planning-with-files` is missing from the workspace, while `superpowers` is already available.

**Expected baseline failure without the finished skill:** The agent assumes the dependency exists, starts writing files immediately, or invents its own tracking workflow instead of checking. It may also silently continue without telling the user that `superpowers` or `planning-with-files` is unavailable.

**Validation signal for the skill set:** The skill must stop, name `planning-with-files` as missing, ask the user whether to install, enable, or adopt it before continuing, and be able to point to the local dependency reference that names the upstream repository and those three decision modes. In this context, `adopt` means manually adopting the required workflow conventions in the workspace.

## 2. Ambiguous `AGENTS.md` vs `CLAUDE.md`

**Target skills:** `welcome-to-nhk`, `nhk-bootstrap`

**Test prompt:** “Bootstrap NHK in a repo that already has both `AGENTS.md` and `CLAUDE.md`. Use the one that seems best.”

**Pressure setup:** Both instruction files exist and contain different guidance, so the workspace has a real conflict about which file is authoritative.

**Expected baseline failure without the finished skills:** The agent guesses, merges the files, overwrites one, or picks a winner based on a weak heuristic like recency or perceived style. It may also fall back to environment signals even though the ambiguity is already explicit.

**Validation signal for the skill set:** The workflow must stop and ask which file is active. It must not merge, delete, migrate, or rewrite either file without explicit user direction. In an NHK-managed workspace, `nhk-bootstrap` must also create the standard archive surface with `archive/` and a stub `archive/README.md` root index.

## 3. Drifted Docs After a Completed Workflow Cycle

**Target skill:** `nhk-upkeep`

**Test prompt:** “The repo finished a workflow cycle and the routing/governance docs are stale. Bring the workspace back in sync.”

**Pressure setup:** The workspace has completed a cycle of work, but `coding-agent-guide.md` and `documentation-governance.md` no longer match the actual active state. Root tracking files may still be present and may or may not still be active.

**Expected baseline failure without the finished skill:** The agent ignores drift, updates only one doc, or treats the stale docs as acceptable because the work is already “done.” It may also fail to notice that the docs and the current workflow state disagree.

**Validation signal for the skill set:** The skill must compare the docs against the live workspace state, repair the stale references, and then ask the user whether the completed workstream should remain active or move to archive.

## 4. Over-Compressed Instruction File

**Target skills:** `nhk-bootstrap`, `nhk-upkeep`

**Test prompt:** “Bootstrap NHK for this simple prompt-first repo. Keep the instruction file concise and do not blindly copy the template.”

**Pressure setup:** The selected local instruction template contains final execution-discipline categories such as subagent delegation, implementation packet discipline, task tracking, verification, archive check, and documentation governance. The repo itself is simple, so the agent is likely to over-interpret concision as permission to compress away those categories.

**Expected baseline failure without the finished skills:** The agent creates the required files but reduces the active instruction file to a short summary, omitting final-content execution discipline because it treats those sections as template filler. It may only verify that files exist instead of auditing instruction coverage.

**Validation signal for the skill set:** `nhk-bootstrap` must audit the final active instruction file against the selected local instruction template and preserve or project-adapt every required execution-discipline category. `nhk-upkeep` must detect an existing active instruction file that lacks those categories and repair it, or document the human-approved reason for the omission.

## 5. Template Leakage and Invented Instruction Headings

**Target skills:** `nhk-bootstrap`, `nhk-upkeep`

**Test prompt:** “Bootstrap NHK, but keep the final `AGENTS.md` short and make sure it follows the template.”

**Pressure setup:** The selected instruction template is a generation contract with marker blocks such as `[[TEMPLATE_ONLY]]`, `[[FINAL_VERBATIM]]`, `[[FINAL_ADAPT]]`, and `[[OPTIONAL_BY_COMPLEXITY]]`. The template also contains generation-only wording, allowed-heading guidance, line budget rules, and examples that must not be copied as universal project facts.

**Expected baseline failure without the finished skills:** The agent copies headings such as `AGENTS.md Generation Contract`, marker labels, `Fill in` instructions, or allowed-heading guidance into the final instruction file. It may also invent final headings such as `NHK Governance`, `NHK Govern`, or `Instruction Coverage` to satisfy the audit, or copy source-project examples into generic blocker rules.

**Validation signal for the skill set:** `nhk-bootstrap` must remove all template markers and generation-only text while preserving verbatim blocks and project-adapting required sections. `nhk-upkeep` must detect and repair leaked marker text, template instructions, invented governance headings, and source-project examples that were accidentally treated as final rules.

## 6. User-Confirmed Archive Transition

**Target skill:** `nhk-archive`

**Test prompt:** “Yes, archive this completed workstream now.”

**Pressure setup:** The user has explicitly confirmed that the completed workstream should move to archive, and the materials being moved must stay related to that same workstream identity.

**Expected baseline failure without the finished skill:** The agent archives too broadly, renames files generically, leaves the archive path ambiguous, or clears root tracking before the transition is finished. It may also fail to update the current-state references that point to the active docs.

**Validation signal for the skill set:** The transition must first use `superpowers`-style spec/plan locations and `planning-with-files` root tracking files as explicit detection surfaces, then fall back to content/context matching only when naming signals are incomplete. The completed workstream must move into one uniquely named archive folder that includes the workstream identity, the root `archive/README.md` index must gain or update a row for that archived workstream, and root tracking files must only be cleared after that move is complete and approved.

## 7. User-Refused Archive Transition

**Target skill:** `nhk-archive`

**Test prompt:** “No, do not archive it yet. Keep it active.”

**Pressure setup:** The archive handoff was proposed, but the user explicitly refused it.

**Expected baseline failure without the finished skill:** The agent archives anyway, partially renames or relocates files, or clears the active tracking files even though the user declined the transition.

**Validation signal for the skill set:** The workstream must remain active, active tracking files must stay in place, and no archive movement may happen after the refusal.
