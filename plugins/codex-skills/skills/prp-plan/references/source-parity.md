# Source Parity

Source: `https://github.com/affaan-m/everything-claude-code/blob/main/commands/prp-plan.md`

| Source feature | Codex port |
| --- | --- |
| `/prp-plan` command | Trigger phrase in description |
| PRD/free-form/reference input detection | Preserved |
| PRD phase status/back-reference update | Preserved when the PRD is safely editable; otherwise report exact manual snippet |
| Codebase search and pattern extraction | Preserved |
| External documentation capture | Preserved; use current official docs when needed |
| Plan template and validation sections | Preserved and condensed |
| `.claude/PRPs/plans` artifact path | Adapted to `.codex/prps/plans` |
| Next step `/prp-implement` | Converted to dependency on `prp-implement` skill |
