# Source Parity: Codex Goal Semantics

Source: current Codex goal behavior checked with Context7 against `/openai/codex` on 2026-05-21.

Related sources:

- `https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md`
- `https://github.com/openai/codex/blob/main/codex-rs/core/templates/goals/continuation.md`

## Parity Ledger

| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| Goal objective and optional token budget | `SKILL.md` rubric and rewrite pattern | Direct | Low | Goals are graded as durable execution contracts. |
| `thread/goal/get` / `thread/goal/set` status metadata | `references/verified-goal-docs.md` | Direct | Low | Reference records known fields and API semantics. |
| Complete only when objective is achieved | `SKILL.md` Codex semantics section | Direct | Low | Explicitly enforced in grading. |
| Blocked only after three repeated blocking turns | `SKILL.md` Codex semantics section | Direct | Low | Captures continuation rule and external-state requirement. |
| Budget-limited and usage-limited statuses | `references/verified-goal-docs.md` | Direct | Low | Recorded as status values without overfitting slash UI. |
| Current slash-command UI syntax may change | `SKILL.md` source check | Emulated | Medium | Agents must verify latest docs when exact syntax matters. |
| Safety gates for destructive/external actions | `SKILL.md` rubric and evals | Direct | Low | Added as prompt-quality requirement for autonomous work. |

## Conversion Notes

This skill is not a direct port from another harness command. It packages current Codex goal semantics into a reusable grading workflow and keeps volatile docs in `verified-goal-docs.md`.
