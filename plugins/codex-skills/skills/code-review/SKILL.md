---
name: code-review
description: Use this skill when the user invokes `/code-review`, asks for a code review, wants local uncommitted changes reviewed, provides a GitHub PR number, PR URL, or branch name, asks whether code is safe to merge, or after implementation before commit. It reviews correctness, security, type safety, tests, performance, and maintainability, runs applicable validation, and reports findings by severity before summaries.
metadata:
  short-description: Review local changes or GitHub PRs
---

# Code Review

Use this skill for local diffs and GitHub PR reviews. Findings come first, ordered by severity, with file and line references where possible.

## Mode Selection

- If the input includes a PR number, PR URL, branch name, or `--pr`, use PR review mode.
- Otherwise, review local changes.

## Local Review Mode

1. Run `git diff --name-only HEAD` or inspect staged/unstaged changes.
2. If no files changed, stop with "Nothing to review."
3. Read changed files in full when feasible, not just diff hunks.
4. Review for the categories below.
5. Run applicable validation commands based on project type.
6. Report findings first.

## PR Review Mode

1. Use `gh pr view` and `gh pr diff` when GitHub CLI is available and authenticated.
2. For branch-name input, find the PR with `gh pr list --head <branch>`.
3. Fetch PR metadata, branch names, changed files, and full file contents at the PR head when needed.
4. Read PR description, linked issues, and any related plan/report artifacts.
5. Review changed files and run relevant validation locally when possible.
6. Publish with `gh pr review` only if the user requested posting; otherwise report locally.

If `gh` is unavailable, fall back to local diff review and explain the limitation.

## Review Categories

| Category | Examples |
| --- | --- |
| Correctness | logic errors, edge cases, null handling, races |
| Security | secrets, injection, XSS, SSRF, authz/authn gaps, path traversal |
| Type safety | unsafe casts, `any`, missing generics, schema mismatch |
| Pattern compliance | project conventions, file structure, error handling, imports |
| Performance | N+1 queries, unbounded loops, missing indexes, large payloads |
| Completeness | missing tests, incomplete migrations, missing docs |
| Maintainability | deep nesting, long functions, dead code, unclear naming |

Severity:

- **CRITICAL:** security vulnerability, data loss, or production-breaking risk.
- **HIGH:** likely user-visible bug, failed validation, or unsafe behavior.
- **MEDIUM:** quality issue or missing best-practice coverage.
- **LOW:** style, clarity, or optional improvement.

## Validation

Detect and run applicable commands:

- Node/TypeScript: typecheck, lint, test, build scripts when present.
- Rust: `cargo clippy`, `cargo test`, `cargo build`.
- Go: `go vet ./...`, `go test ./...`, `go build ./...`.
- Python: configured test and type commands when present.

Record pass/fail/skipped. Do not invent results.

## Report Format

```markdown
## Findings

### CRITICAL
- [file:line] Issue. Impact. Suggested fix.

### HIGH
- None

### MEDIUM
- None

### LOW
- None

## Validation Results
| Check | Result |
| --- | --- |

## Open Questions
- [Only if needed]

## Summary
[Brief overall assessment]
```
