# Source Parity

Source: `https://github.com/affaan-m/everything-claude-code/blob/main/commands/prp-pr.md`

| Source feature | Codex port |
| --- | --- |
| `/prp-pr` command | Trigger phrase in description |
| Base branch and `--draft` parsing | Preserved |
| Git state validation | Preserved |
| PR template discovery | Preserved |
| Commit/file/PRP artifact analysis | Preserved, using `.codex/prps` paths |
| `gh pr create` and verification | Preserved with fallback when `gh` unavailable |
| Follow-up `/prp-commit` and `/code-review` | Converted to dependencies on `prp-commit` and `code-review` |

