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

Use this only when the user explicitly authorizes NHK to follow the missing workflow's conventions manually for the current NHK run.

For NHK, `adopt` means:

- follow the relevant `superpowers` or `planning-with-files` conventions manually for this run
- do not create a persistent adoption marker or treat later runs as pre-authorized
- report clearly that the dependency was not installed and its conventions were followed manually

## Safety Rules

- Do not auto-install anything.
- Do not claim a dependency is installed if the environment only adopted the workflow conventions manually.
- Do not infer adopt from the user's willingness to continue; it must be an explicit choice.
- If the user declines install, enable, and adopt, stop the NHK bootstrap or upkeep flow and state which capability is missing.
- Prefer the upstream repository instructions over ad hoc local guesses.
