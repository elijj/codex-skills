# Verified Codex Goal Semantics

Checked with Context7 against `/openai/codex` on 2026-05-21.

Sources returned by Context7:

- `https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md`
- `https://github.com/openai/codex/blob/main/codex-rs/core/templates/goals/continuation.md`

## Operational Model

Codex goals are thread-level objectives with status and usage metadata. The app-server API exposes `thread/goal/set` for creating or updating a goal and `thread/goal/get` for reading it.

Known goal fields from current docs:

- `objective`: goal text.
- `tokenBudget`: optional token budget for the thread goal.
- `status`: includes `active`, `blocked`, `budgetLimited`, and `usageLimited` in app-server docs.
- `tokensUsed`, `timeUsedSeconds`, `createdAt`, `updatedAt`: returned metadata.

The user-facing `/goal` command maps conceptually to creating a long-running objective. Exact slash-command UI syntax can change; verify current docs when the precise invocation matters.

## Completion Rule

Mark a goal complete only when the objective has actually been achieved and no required work remains. Do not mark complete because the budget is nearly exhausted or because work is stopping.

## Blocked Rule

Mark a goal blocked only when:

- The same blocking condition has repeated for at least three consecutive goal turns.
- The count includes the original user-triggered turn and automatic continuations.
- Progress is truly at an impasse and requires user input or an external state change.

If a blocked goal is resumed, restart the blocked audit. Do not use `blocked` for work that is merely difficult, slow, uncertain, incomplete, or likely to benefit from clarification.

## Prompt Implications

Good `/goal` prompts should define:

- A single objective.
- Verifiable done criteria.
- Validation commands or measurement loops.
- Safe boundaries and approval gates.
- Stop/block rules that align with the three-turn blocked audit.
- Context needed to resume after continuations without rediscovery.
