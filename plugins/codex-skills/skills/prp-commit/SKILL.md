---
name: prp-commit
description: Use this skill when the user invokes `/prp-commit`, asks for a smart commit, wants natural-language file targeting, needs staged/all/specific changes committed, or asks to create a conventional commit from current git changes. It interprets file selection, stages safely, writes a concise conventional commit message, and reports the commit hash and files.
metadata:
  short-description: Stage targeted changes and commit them
---

# PRP Commit

Create a focused conventional commit from current changes, optionally using natural-language file targeting.

## Workflow

### Phase 1: Assess

Run:

```bash
git status --short
```

If there are no changes, stop with "Nothing to commit."

Summarize added, modified, deleted, and untracked files.

### Phase 2: Interpret And Stage

Interpret the user's target:

| Input | Behavior |
| --- | --- |
| blank | stage all changes |
| `staged` | use already staged changes |
| glob or file path | stage matching files |
| `except tests` | stage all except test/spec files |
| `only new files` | stage untracked files only |
| natural language | match files from status/diff by area and explain why |

Show which files will be staged and why. If no files match, stop.

### Phase 3: Commit

Generate a single-line conventional commit:

```text
<type>: <imperative description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`.

Rules:

- Imperative mood.
- Lowercase after the type prefix.
- No period.
- Prefer under 72 characters.
- Describe what changed, not how.

### Phase 4: Output

Report:

- Commit hash.
- Commit message.
- Files committed.
- Suggested next step: push, `prp-pr`, or `code-review`.
