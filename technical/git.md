# Git Best Practices & Commit Conventions (AI Context)

## Commit Convention

- This repository follows **Conventional Commits**.
- Commit messages **MUST** comply with the Conventional Commit specification:
    - Format:  
      `<type>(optional scope): <short description>`
    - Examples:
        - `feat(auth): add JWT token refresh`
        - `fix: handle null response from API`

### Priority Rule

- If the repository contains a **pre-commit hook, commit-msg hook, or any tool**
  (e.g. commitlint, husky, lefthook) enforcing commit rules:
    - **Always follow the repository’s enforced rules**
    - These rules take precedence over any generic Conventional Commit guideline

## Commit Description Rules

- The commit description (body + subject combined) **MUST NOT exceed 2 lines**
- Prefer:
    - One concise subject line
    - Optional second line only if strictly necessary
- Avoid long explanations, bullet lists, or markdown in commit messages

## General Git Best Practices

- Make small, focused commits
- One logical change per commit
- Do not mix formatting, refactoring, and behavior changes in one commit
- Commit only relevant files
- Ensure the working tree is clean before committing

## AI Agent Behavior

- Never generate commits that violate:
    - Existing repository hooks
    - Conventional Commit structure
    - The 2-line description limit
- When unsure, default to the **simplest valid conventional commit**
