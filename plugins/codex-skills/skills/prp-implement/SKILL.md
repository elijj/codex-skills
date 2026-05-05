---
name: prp-implement
description: Use this skill when the user invokes `/prp-implement`, provides a `.codex/prps/plans/*.plan.md` or other implementation plan file, asks to execute a plan step-by-step, or wants rigorous validation loops while implementing. It loads the plan, prepares git state, executes each task incrementally, runs validation after each meaningful change, writes an implementation report, and recommends `code-review` or `prp-pr` next.
metadata:
  short-description: Execute PRP plans with validation loops
---

# PRP Implement

Execute a plan artifact step by step. The central rule is simple: never accumulate broken state. If validation fails, fix it before moving to the next task or clearly report the blocker.

## Input

Expected input is a plan path, usually:

```text
.codex/prps/plans/{name}.plan.md
```

If no valid plan exists, ask the user to run `prp-plan <feature>` first.

## Workflow

### Phase 0: Detect Project Commands

Identify package manager and validation commands from project files:

- Node: lockfile and `package.json` scripts.
- Python: `pyproject.toml`, `requirements.txt`, test/type tools.
- Rust: `Cargo.toml`.
- Go: `go.mod`.
- Java/Kotlin: Maven/Gradle files.

Record typecheck, lint, test, build, and integration commands when available.

### Phase 1: Load Plan

Read the plan and extract:

- Summary.
- Mandatory reading.
- Patterns to mirror.
- Files to change.
- Step-by-step tasks.
- Validation commands.
- Acceptance criteria.

### Phase 2: Prepare

Check:

- Current branch.
- `git status --porcelain`.
- Whether uncommitted user work exists.
- Whether the plan requires new dependencies or services.

Do not overwrite unrelated user changes.

### Phase 3: Execute Per Task

For each task:

1. Read relevant files.
2. Apply the smallest coherent change.
3. Run the task's validation command or the nearest relevant check.
4. Fix failures immediately.
5. Record deviations from the plan.

When the plan's validation commands are placeholders, infer the best available project command and note the substitution.

### Phase 4: Full Validation

Run the broadest reasonable validation set for the changed surface:

- Static analysis/typecheck.
- Unit/integration tests.
- Build.
- E2E/manual checks when applicable.

### Phase 5: Report Artifact

Write:

```text
.codex/prps/reports/{kebab-case-feature}.implementation.md
```

Include:

- Summary.
- Assessment vs plan.
- Tasks completed.
- Validation results.
- Files changed.
- Deviations.
- Issues encountered.
- Tests written.
- Next steps.

### Phase 6: PRD Progress And Archive

When the plan links to a PRD or phase:

- Update the PRD phase status to `complete` if acceptance criteria are satisfied.
- Add the implementation report path beside the phase.
- If acceptance criteria are not complete, mark the phase `in progress` or report the exact manual update instead of overstating completion.

Archive the executed plan by moving or copying it to:

```text
.codex/prps/archive/{kebab-case-feature}.plan.md
```

If archiving would obscure active work or the user did not want file movement, leave the plan in place and report that archive was skipped.

## Final Response

Report status, validation summary, changed files, report path, PRD update/archive status, deviations, and next step. Recommend `code-review` before commit/merge and `prp-pr` when the branch is ready for a pull request.
