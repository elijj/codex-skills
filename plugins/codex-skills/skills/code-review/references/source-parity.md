# Source Parity

Source: `https://github.com/affaan-m/everything-claude-code/blob/main/commands/code-review.md`

| Source feature | Codex port |
| --- | --- |
| `/code-review` local or PR mode | Preserved through mode selection |
| GitHub CLI PR fetch/publish | Preserved with explicit fallback when `gh` is unavailable |
| Full-file review, not only diff hunks | Preserved |
| Security and quality categories | Preserved |
| Validation by project type | Preserved |
| Decision/report artifact | Adapted to Codex final report; file artifact optional unless user asks |

