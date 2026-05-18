# Verified Goal Docs

Verified on 2026-05-18.

## Official OpenAI Docs

- Codex CLI slash commands: `https://developers.openai.com/codex/cli/slash-commands`
  - `/goal` is experimental.
  - It requires `features.goals` enabled through `/experimental` or `[features] goals = true` in `config.toml`.
  - `/goal <objective>` sets a goal.
  - `/goal` views the current goal.
  - `/goal pause`, `/goal resume`, and `/goal clear` control the active goal.
  - Expected behavior: Codex keeps the goal attached to the active thread while work continues.

- Codex "Follow a goal" use case: `https://developers.openai.com/codex/use-cases/follow-goals`
  - Use `/goal` for long-running work with a verifiable stopping condition.
  - Good goal work has one objective, one stopping condition, required context, proof commands or artifacts, checkpoints, and clear pause/resume/clear usage.
  - Avoid loose lists of unrelated work.

## Context7 Check

Context7 resolved `OpenAI Codex CLI` to `/openai/codex`. Its indexed docs covered Codex CLI usage but did not yet surface the latest `/goal` behavior as clearly as the official OpenAI pages above. Prefer official OpenAI docs for `/goal` specifics when they differ.

