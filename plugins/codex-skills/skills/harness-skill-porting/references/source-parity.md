# Source Parity

This skill ports workflows from other agent harnesses into Codex skill surfaces.

## Source Behavior Preserved

- Trigger sources from skills, slash commands, prompt packs, Cursor/Cline/Roo rules, and repo instructions become Codex `description` trigger phrasing plus `SKILL.md` input contracts.
- Source agents become inline skill responsibilities unless they are independently reusable enough to become separate Codex skills.
- Source hooks become explicit verification steps, bundled scripts, CI recommendations, or documented limitations.
- Ambient source behavior becomes strong trigger phrasing plus an `AGENTS.md` update or manual snippet when always-on behavior is required.
- MCP, credential, and local-service assumptions are recorded in the parity ledger and marked `Direct`, `Emulated`, or `Out of scope`.

## Required Output Parity

Porting outputs must include this ledger:

```markdown
| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
```

Each source command, agent, hook, MCP assumption, ambient rule, bundled resource, and output contract gets its own row.
