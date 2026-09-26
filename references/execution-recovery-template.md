# Execution Recovery Template

## Purpose

Use this template to create `execution-recovery.md`, the on-demand contract for exhausted fix loops and final-review recovery.

Ordinary bugs still use the installed or adopted Superpowers systematic-debugging workflow. This companion governs accounting, reassessment, one recovery attempt, and the mandatory stop.

## Template Contract

- Final file hard limit: 80 lines. Source-template hard limit: 140 lines. There is no minimum.
- Replace template guidance with the rules below and remove every prompt or placeholder.
- Record recovery state in the current workflow's existing authoritative execution record. SDD uses its ledger; other trackers only reference the applicable record.
- Name this file from canonical instructions with a backticked literal path. Never use a Claude `@` import.
- Stay within original scope and authority. Human approval is required to change acceptance, public contracts, or permissions.

- Refer diagnostic configuration to `worker-policy.md`; keep this document about triggers, evidence, authority, and stopping.
- Preserve the consultation contract clauses in their owning sections; adapt project facts around them.

## Required Final Shape

Start with `# Execution Recovery`, then use exactly these second-level headings in order.

### Triggers and Accounting

- Keep ordinary bugs in systematic-debugging. Its architecture check after three failed fixes still applies and is not delayed by this policy.
- Enter reassessment earlier when evidence shows architectural stagnation or an invalid shared premise; five rounds are a ceiling, not a waiting requirement.
- The ordinary limits are five fix-review rounds per task and five rounds for the same stable acceptance gap across tasks.
- A round is one fix dispatch plus its verification and review. Repeated failure of the same promise counts even when local tests pass.
- Reaching either the task-round bound or stable-gap bound stops ordinary fixing.
- Worker, session, model, commit, task rename, or replanning never resets a task or gap count.
- Use the current workflow's existing authoritative execution record. In SDD, this is the SDD ledger.
- Other workflows use their own existing record and do not create an SDD-only or parallel state system.
- Record counts, diagnostic use, clarification use, and recovery use for both the task and stable acceptance gap in that record. Other trackers only reference it.
- Worker, session, model, commit, task rename, or replanning never resets diagnostic or clarification use.
- Read-only diagnosis spends no fix round and grants no additional modification authority.

### Main-thread Reassessment

- Reassess the original intent, approved spec and public contracts, verification signal, prior attempts, and cross-task consequences.
- Classify the failure as implementation, design or ownership, spec conflict, invalid oracle, reviewer error, or external conditions.
- Before consultation, prepare the original contract, unmet acceptance, fixed revisions and relevant diff, prior attempts and observed results, counterevidence, open questions, and authoritative execution record.
- Include a provisional explanation and recovery direction if available; explicitly state when no credible hypothesis exists. A complete solution is not a prerequisite for consultation.
- Before recovery, record why prior attempts failed, how the new explanation differs from old hypotheses, and the discriminating observation.
- Name the concrete command or input, observed result, and expected before-and-after result.
- Keep reassessment and recovery within the original scope and authority. Acceptance, public-contract, or permission changes require a human decision.
- The main thread decides directly when evidence is sufficient and remains responsible for the final judgment.
- After consultation, verify key evidence and record why advice was accepted or rejected and the verification results. Agreement between agents is not causal evidence.

### Independent Diagnosis

- Use diagnosis only for competing explanations, review-versus-implementation conflict, an unverified old premise, or no credible explanation for repeated failure.
- Dispatch at most one fresh-context read-only diagnostic worker using the independent diagnosis role in `worker-policy.md` to investigate one concrete causal question.
- Recovery consultation uses the existing diagnosis allowance; if either the task or stable acceptance gap has used diagnosis, do not dispatch another diagnostic worker.
- Give the diagnostic worker the reassessment handoff and an explicit no-write boundary. Separate observations from prior hypotheses.
- Diagnosis checks source evidence and forms its own explanation before comparing the main thread's provisional explanation; it may support or overturn that explanation. Return evidence explaining previous failures or a discriminating experiment with expected outcomes; suggest a minimal recovery direction only when causal evidence supports it.
- After the report, allow at most one targeted clarification with the same diagnostic worker, limited to evidence, omissions, or disagreements about the original causal question. It uses the same diagnosis allowance and grants no new investigation scope.
- A diagnostic worker does not authorize a fix or replace the main thread's judgment; select any recovery fix and re-review for their own roles in `worker-policy.md`.
- If evidence remains insufficient after diagnosis and any clarification, present blockers and options to the human. Do not start a diagnostic chain.

### Recovery and Stop

- With sufficient causal evidence, allow at most one recovery fix wave and one independent re-review for the exhausted task or gap.
- This recovery wave may be the sixth modification and supersedes an old absolute “No sixth patch” rule.
- If recovery fails, stop automatic fixes and ask the human. Changing model, plan, or task never renews recovery.
- Final review retains one concentrated fix wave and one scoped re-review.
- An exhausted earlier gap cannot use final review as another repair allowance. Final residual blockers go to the human and never return to the ordinary loop.

## Final Check

- The generated file is at most 80 lines and uses the four required headings in order.
- Counts, gap identity, evidence, diagnostic use, clarification use, recovery use, and stop status are traceable in the authoritative execution record.
- Three-fix architecture review, five-round bounds, one diagnosis with at most one targeted clarification, one recovery wave, and one re-review retain distinct meanings.
- No template prompt, placeholder, model catalog, parallel state system, or automatic-loop reset remains.
