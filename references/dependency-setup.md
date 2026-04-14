# NHK Dependency Setup Reference

This file is a local reference for dependency readiness decisions in `welcome-to-nhk`.

Use it when `superpowers` or `planning-with-files` is missing and the user asks what the options mean or wants help proceeding.

## Dependency Sources

- `superpowers`: <https://github.com/obra/superpowers>
- `planning-with-files`: <https://github.com/othmanadi/planning-with-files>

## Decision Modes

### 1. Install

Use this when the dependency is not present and the user wants the actual workflow asset added to the current environment.

- Confirm which dependency is missing.
- Point to the upstream repository.
- Follow the repository's documented installation path instead of inventing a custom shortcut.
- Ask before mutating the environment.

### 2. Enable

Use this when the dependency already exists somewhere in the environment, but it is not active in the current workspace or current tool session.

- Confirm that the dependency is already installed or available.
- Explain what needs to be enabled for the current workspace or current agent session.
- Avoid reinstalling something that already exists unless the user asks to replace or repair it.

### 3. Adopt

Use this when the user does not want installation or cannot install right now, but still wants the workspace to follow the workflow conventions manually.

For NHK, `adopt` means:

- manually following the `superpowers` workflow shape for brainstorm/spec/plan discipline
- manually following `planning-with-files` conventions for root tracking files and recovery behavior
- being explicit that the dependency is not actually installed, only imitated by documented process

## Safety Rules

- Do not auto-install anything.
- Do not claim a dependency is installed if the environment only adopted the workflow conventions manually.
- If the user declines install, enable, and adopt, stop the NHK bootstrap or upkeep flow and state which capability is missing.
- Prefer the upstream repository instructions over ad hoc local guesses.
