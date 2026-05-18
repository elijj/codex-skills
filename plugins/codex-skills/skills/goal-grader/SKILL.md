---
name: goal-grader
description: Use this skill whenever the user asks to grade, review, score, improve, rewrite, harden, sanity-check, or give feedback on a Codex `/goal` prompt or any long-running agent objective. Trigger for phrases like "grade this /goal", "is this a good goal", "make this goal better", "goal grader", "score my autonomous task", or when a prompt starts with `/goal` and the user wants feedback before running it. This skill grades the goal, explains risks, and provides a safer improved `/goal` rewrite.
metadata:
  short-description: Grade and improve Codex /goal prompts
---

# Goal Grader

Grade a long-running Codex `/goal` prompt as an execution contract, not as ordinary prose. A good goal should be durable enough for Codex to keep working across turns and precise enough to know when to stop.

## When To Use

Use this skill when the user wants feedback before running a `/goal`, or when a user supplies a long-running objective and asks whether it is clear, safe, bounded, measurable, or ready for autonomous work.

Do not use this skill for normal one-turn prompts unless the user explicitly asks to turn them into a goal.

## Source Of Truth

If the user asks for "latest" `/goal` behavior, or if the goal depends on a newly changed Codex feature, verify current docs first:

- Official Codex CLI slash commands: `https://developers.openai.com/codex/cli/slash-commands`
- Official Codex "Follow a goal" use case: `https://developers.openai.com/codex/use-cases/follow-goals`
- Use Context7 for `/openai/codex` when available, but prefer official OpenAI docs if Context7 lags.

Bundled reference: `references/verified-goal-docs.md`.

## Grading Workflow

1. Extract the goal text. Preserve the original wording enough that the user can map feedback to it.
2. Grade the goal with the rubric below. Use the bundled script when a deterministic pass is useful:

   ```bash
   python3 scripts/grade_goal.py --text "<goal text>"
   ```

3. Treat security, credential handling, destructive actions, and social-platform automation as blockers when they appear without explicit approval gates.
4. Give concise feedback. Focus on changes that improve execution reliability.
5. Provide an improved `/goal` rewrite unless the user asked only for a score.

## Rubric

Score each category from 0 to 10, then average to 100:

| Category | What Good Looks Like |
| --- | --- |
| Objective clarity | One concrete objective with specific verbs and target system. |
| Verifiable end state | Clear "done when" condition with tests, metrics, files, or observable output. |
| Scope boundaries | Says what is in scope and what not to change. |
| Deliverables | Names expected artifacts such as files, reports, PRs, commits, dashboards, or configs. |
| Validation loop | Defines commands, evals, checks, measurement cadence, or manual verification. |
| Context and dependencies | Points to repos, docs, issues, inputs, credentials needed, or setup assumptions. |
| Checkpoints | Requests progress log, phases, or after-each-step checks for long work. |
| Stop/block rules | Says when to pause, ask, stop, or escalate. |
| Safety and permissions | Protects secrets, destructive commands, external writes, posts, payments, auth, and user data. |
| Autonomy fit | Bigger than one prompt, smaller than an open-ended backlog, not a loose bundle of unrelated tasks. |

Grade bands:

- `A` = 90-100: Ready to run.
- `B` = 80-89: Good, minor tightening.
- `C` = 65-79: Usable after edits.
- `D` = 50-64: Risky, rewrite before running.
- `F` = 0-49: Not a safe or executable goal.

## Required Output

Use this format:

```markdown
Grade: [A-F] ([score]/100)

Blocking Issues:
- [Only include true blockers. Use "None" if none.]

Scorecard:
| Category | Score | Feedback |
| --- | ---: | --- |

Highest-Impact Fixes:
1. [Specific edit]
2. [Specific edit]
3. [Specific edit]

Improved /goal:
```text
/goal ...
```

Notes:
- [Important assumptions, docs checked, or why a risk matters.]
```

Keep the report direct. Do not bury the grade. Do not rewrite the goal into multiple goals unless the original is too broad; in that case say which first goal should run now and which should become follow-up goals.

## Rewrite Guidance

Strong rewrite pattern:

```text
/goal Complete [one objective] in [repo/path/system] without changing [boundaries]. First read [required context]. Work in checkpoints, keep a short progress log, and after each checkpoint run [validation]. Done when [verifiable end state]. Pause and ask before [risky action].
```

For social, auth, payments, deployment, data deletion, or external side effects:

```text
Do not post, delete, buy, deploy, rotate secrets, message users, or change account settings without explicit approval.
```

For eval/prompt optimization:

```text
After each change, run [eval command], inspect failing cases, keep edits minimal, and stop when [target score] is met or when further gains require product guidance.
```

