# Ambient Behavior

Codex skills are trigger-based. Source behavior that was always-on in another harness must be handled explicitly so it is not silently lost.

## Conversion Options

Use one of these approaches:

1. Strong trigger phrasing in `SKILL.md` when the behavior only needs to apply to a recognizable class of user requests.
2. A compact repo-level `AGENTS.md` section when the behavior must apply before any skill triggers.
3. A bundled verification script when the source behavior was an enforcement hook.
4. A final-response snippet marked `manual repo-level install required` when the user did not ask you to edit a target repository.

## Required Ledger Treatment

Every ambient rule needs a row:

```markdown
| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| Cursor `alwaysApply` rule for no secrets in commits | `AGENTS.md` snippet | Emulated | Medium | manual repo-level install required |
```

Do not claim Codex will automatically enforce hooks, pre-tool checks, or always-on rules unless the target repository actually receives an enforcing script, CI job, or documented `AGENTS.md` instruction.

## Snippet Pattern

When a manual install is needed, provide exact text:

```markdown
## Ported Ambient Rule: [Name]

[Short instruction written for Codex agents.]

Verification:
- [Command or review step]
```
