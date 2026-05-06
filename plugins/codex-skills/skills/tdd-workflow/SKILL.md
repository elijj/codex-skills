---
name: tdd-workflow
description: Use this skill when writing a new feature, fixing a bug, refactoring production code, adding an API endpoint, creating a component, or when the user invokes `/tdd` or asks for test-driven development. Trigger it even when the user only asks to refactor, fix, or implement something and the safest path is test-driven. It enforces RED to GREEN to REFACTOR with explicit test evidence, 80%+ coverage expectations, and unit/integration/E2E coverage scaled to risk.
metadata:
  short-description: Implement changes with strict TDD evidence
---

# TDD Workflow

Use this skill to preserve ECC `/tdd` behavior as a Codex-native skill. Tests are the control system for the change: write or update a relevant test, watch it fail for the intended reason, implement the smallest fix, then verify it passes.

## RED Gate

Before editing production code, create or update the relevant test and run it.

A valid RED state means:

- The test target compiles or the compile failure is the intended signal.
- The new or changed test is actually executed.
- The failure is caused by the intended missing behavior or bug, not broken setup or unrelated regressions.

If a RED state cannot be produced, explain why and get a different verification path before editing production code.

## GREEN Gate

Implement the smallest code change that makes the RED test pass. Re-run the same test target and record the command and result. Do not refactor before GREEN.

## REFACTOR Gate

After GREEN, clean only the code touched by the implementation. Re-run the relevant tests. Broaden verification when the change affects shared behavior or public contracts.

## Coverage Expectations

Use coverage proportional to risk:

- Unit tests for functions, helpers, and component logic.
- Integration tests for APIs, services, databases, queues, external-service boundaries, and data contracts.
- E2E tests for critical user flows. Use the `e2e-testing` skill for Playwright structure, artifacts, CI integration, and flake handling.

Aim for 80%+ coverage where the project has a coverage framework. If the repo lacks coverage tooling, add focused tests and report that coverage could not be measured.

## Git Checkpoints

If the repository is under Git and the user asked for commits or the workflow expects them, checkpoint after major stages:

- `test: add reproducer for <bug or feature>` after RED evidence.
- `fix:` or `feat:` after GREEN evidence.
- `refactor:` after optional cleanup with tests still passing.

Do not rewrite unrelated history. Verify checkpoints are on the current branch before treating them as evidence.

## Final Report

Include:

- RED command and failure reason.
- GREEN command and pass result.
- Refactor/coverage command, if run.
- Files changed.
- Any coverage gap or skipped test reason.
