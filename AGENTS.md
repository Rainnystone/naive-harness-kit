# NHK Repository Agent Instructions

This file is for coding agents working on the `nhk` repository itself.

It is not the end-user manual for NHK. Human-facing usage belongs in `README.md` and `README_CN.md`. Skill behavior belongs in the four skill folders. Frozen drafting assets belong in `references/`.

## Repo Scope

Treat this repository as the clean publishable NHK package:

- repo-facing docs for humans
- agent-facing maintenance instructions
- four NHK skills
- frozen local references used by those skills

Do not turn this repository into a scratchpad for local planning artifacts from outside the package.

## Documentation Roles

- `README.md`: default GitHub landing page, English-first, written for humans
- `README_CN.md`: Chinese companion, written for humans, must stay aligned with `README.md`
- `AGENTS.md`: shared repository instructions for Codex-style agents
- `CLAUDE.md`: Claude Code entrypoint, should remain thin and import this file
- `welcome-to-nhk/`, `nhk-bootstrap/`, `nhk-upkeep/`, `nhk-archive/`: actual skill behavior
- `references/`: frozen reference assets, not casual dumping grounds

Do not mix these roles. If a change is meant to teach humans how to use NHK, put it in the READMEs. If a change is meant to guide an agent maintaining this repository, put it here or in `CLAUDE.md`.

## Editing Rules

- Keep NHK prompt-first, not hook-first.
- Preserve the current four-skill split unless there is a clear design reason to change it.
- Treat `references/` as controlled assets. Update them deliberately, not casually.
- If a reference or template explicitly says a subsection is verbatim-preserved, do not rewrite that subsection unless the human explicitly approves it.
- Do not silently remove the English/中文 cross-links between the two READMEs.

## Required Sync Surfaces

When changing dependency behavior, review and sync:

- `welcome-to-nhk/SKILL.md`
- `README.md`
- `README_CN.md`
- `references/dependency-setup.md`
- `references/validation-scenarios.md`

When changing archive behavior, review and sync:

- `nhk-archive/SKILL.md`
- `README.md`
- `README_CN.md`
- `references/validation-scenarios.md`
- any affected governance-related references

When changing template policy, review and sync:

- affected files under `references/`
- any skill that points to those references
- the READMEs if the user-visible workflow changes

## Validation Standard

Before claiming the repo is updated:

- verify the relevant READMEs still align
- verify any changed skill still points to the right local references
- verify any changed behavior is reflected in `references/validation-scenarios.md`
- verify the repo root still presents the right human/agent split: READMEs for humans, instruction files for agents

Prefer the smallest change that keeps the package self-consistent.
