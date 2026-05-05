# Source Parity

Source: `https://github.com/affaan-m/everything-claude-code/blob/main/commands/prp-implement.md`

| Source feature | Codex port |
| --- | --- |
| `/prp-implement` command | Trigger phrase in description |
| Plan loading and validation loops | Preserved |
| Package manager and validation detection | Preserved |
| Git state preparation | Preserved with Codex user-change safeguards |
| `.claude/PRPs/reports` artifact path | Adapted to `.codex/prps/reports` |
| PRD progress update and completed-plan archive | Preserved with `.codex/prps/archive` path and safe-edit fallback |
| Follow-up `/code-review` and `/prp-pr` | Converted to dependencies on `code-review` and `prp-pr` skills |
