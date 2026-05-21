---
name: goal-grader
description: Use this skill when the user asks to grade, review, score, improve, rewrite, harden, sanity-check, or optimize a Codex `/goal` prompt or any long-running autonomous Codex objective. Trigger for phrases like "grade this /goal", "is this a good goal", "optimize my goal", "score my autonomous task", "goal grader", or when a prompt starts with `/goal` and the user wants feedback before running it. The skill grades execution readiness, identifies blockers, and returns a safer optimized `/goal` rewrite.
---

# Goal Grader

Grade a Codex `/goal` prompt as an execution contract for long-running autonomous work. Reward prompts that make progress measurable, safe, bounded, and resumable across automatic continuations.

## Source Check

If the user asks for latest behavior, exact `/goal` semantics, or a docs-backed review, consult current Codex docs first. Use Context7 for `/openai/codex` when available, then read `references/verified-goal-docs.md` for the core semantics to apply.

## Workflow

1. Extract the proposed goal text. If the user pasted surrounding commentary, isolate the actual objective.
2. Run the helper when useful for a first-pass score:

   ```bash
   python3 scripts/grade_goal.py --text "<goal text>"
   ```

   Use `--file <path>` for long prompts. Treat script output as a baseline, not a substitute for judgment.
3. Apply the rubric below. Penalize vague, unsafe, unbounded, or unverifiable prompts even when they sound plausible.
4. Identify true blockers: missing repo/input, impossible end state, unsafe side effects without approval, destructive commands, credential exposure, external posting/messaging/spend/deployments, or no measurable stop condition.
5. Provide the grade, highest-impact fixes, and an optimized `/goal` rewrite unless the user explicitly asks only for critique.

## Rubric

Score each category from 0 to 10. Average to 100.

| Category | What Good Looks Like |
| --- | --- |
| Objective clarity | One concrete objective with specific verbs, target repo/system, and no unrelated bundles. |
| Verifiable end state | Explicit done condition: tests pass, metric threshold, file exists, PR created, report written, or other observable output. |
| Scope boundaries | Names in-scope and out-of-scope areas; says what not to change. |
| Deliverables | Defines expected files, commits, reports, issues, PRs, configs, dashboards, or summaries. |
| Validation loop | Gives commands, evals, checks, measurement cadence, or manual verification steps. |
| Context and dependencies | Points to repos, docs, issues, inputs, credentials, environments, constraints, and assumptions. |
| Checkpoints | Requests progress updates, phase boundaries, or after-each-step verification for long work. |
| Stop and block rules | Says when to pause, ask, stop, or escalate; respects Codex blocked/complete semantics. |
| Safety and permissions | Protects secrets, destructive actions, external writes, deployments, purchases, auth, user data, and account settings. |
| Autonomy fit | Bigger than one prompt, smaller than an open-ended backlog; suitable for repeated continuations. |

Grade bands:

- `A` = 90-100: Ready to run.
- `B` = 80-89: Good, minor tightening.
- `C` = 65-79: Usable after edits.
- `D` = 50-64: Risky, rewrite before running.
- `F` = 0-49: Not safe or executable as a goal.

## Output Format

Use this structure:

````markdown
Grade: [A-F] ([score]/100)

Blocking Issues:
- [Use "None" if there are no true blockers.]

Scorecard:
| Category | Score | Feedback |
| --- | ---: | --- |

Highest-Impact Fixes:
1. [Specific edit]
2. [Specific edit]
3. [Specific edit]

Optimized /goal:
```text
/goal [rewritten objective]
```

Notes:
- [Docs checked, assumptions, or why a risk matters.]
````

Keep feedback direct. Do not bury the grade. Do not rewrite one broad goal into many parallel goals unless the original is too broad; instead pick the first executable goal and list follow-up goals separately.

## Rewrite Pattern

Use this pattern unless the user's domain needs something more specific:

```text
/goal Complete [one objective] in [repo/path/system] without changing [boundaries]. First read [required context]. Work in checkpoints, keep a short progress log, and after each checkpoint run [validation]. Done when [verifiable end state]. Pause and ask before [risky action].
```

For external side effects, add:

```text
Do not post, delete, buy, deploy, rotate secrets, message users, change account settings, or expose credentials without explicit approval.
```

For eval, benchmark, or prompt-optimization goals, add:

```text
After each change, run [eval command], inspect failures, keep edits minimal, and stop when [target score] is reached or further gains require product guidance.
```

## Codex Goal Semantics To Enforce

- Mark complete only when the objective is actually achieved and no required work remains.
- Mark blocked only after the same blocking condition recurs for at least three consecutive goal turns and progress requires user input or an external state change.
- Do not call a goal blocked merely because work is hard, slow, uncertain, or would benefit from clarification.
- Do not mark complete or blocked only because the token budget is low.
- A strong `/goal` prompt should make those decisions unambiguous before Codex starts.
