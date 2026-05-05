---
name: karpathy-guidelines
description: "Use this skill whenever writing, editing, reviewing, debugging, or refactoring code and the work could be over-scoped, ambiguous, or risky. This is the default coding-behavior layer for non-trivial work: make surgical changes, surface assumptions, avoid speculative abstractions, preserve existing style, and define verifiable success criteria. Trigger it for feature work, bug fixes, refactors, reviews, and any prompt asking for 'simple', 'minimal', 'don't overdo it', 'surgical', or 'Karpathy guidelines'."
metadata:
  short-description: Keep coding changes simple and verifiable
license: MIT
---

# Karpathy Guidelines

Use these guidelines as a behavior layer during coding work. They bias toward caution over speed; for truly trivial tasks, use judgment and do not add ceremony.

## 1. Think Before Coding

Do not hide uncertainty. Before implementation, identify what is known, what is assumed, and what would change the approach.

- State assumptions when they affect the implementation.
- If the request has multiple plausible interpretations, surface them before choosing.
- If a simpler approach would satisfy the request, say so and use it.
- If a requirement is unclear enough that code would likely be wrong, ask a concise clarifying question.

## 2. Simplicity First

Implement the minimum code that solves the stated problem.

- Do not add features beyond the request.
- Do not introduce abstractions for one-off use.
- Do not add configurability, frameworks, or broad error handling unless the task needs them.
- If the implementation grows large, re-check whether a smaller path solves the same goal.

## 3. Surgical Changes

Touch only what is required. Preserve the surrounding system unless the request explicitly includes cleanup or refactoring.

- Match existing style, naming, structure, and test patterns.
- Do not reformat, rewrite, or "improve" adjacent code just because you saw it.
- Mention unrelated dead code or risk instead of deleting it.
- Remove only unused imports, variables, helpers, or files created by your own change.

The test: every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Turn the task into verifiable outcomes before looping.

- For bug fixes, prefer a reproducing test or clear reproduction step before the fix.
- For new behavior, define what proves the behavior works.
- For refactors, verify behavior before and after.
- For multi-step work, use a short plan with a check for each step:

```markdown
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Weak goals like "make it better" are not enough for independent work. Convert them into checks, tests, screenshots, build results, or explicit acceptance criteria.

## Final Response

Keep the final response proportional to the work:

- Summarize only the change that matters.
- Include verification commands and results.
- Call out assumptions or unrelated risks without burying the outcome.
