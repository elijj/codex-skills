# Source Parity

Sources:

- `https://github.com/affaan-m/everything-claude-code/blob/main/commands/tdd.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/skills/tdd-workflow/SKILL.md`

| Source feature | Codex port |
| --- | --- |
| `/tdd` legacy shim | Trigger phrase in description |
| Canonical `tdd-workflow` skill | Converted directly as a Codex skill |
| RED -> GREEN -> REFACTOR gates | Preserved |
| 80%+ coverage expectation | Preserved with fallback when tooling is absent |
| E2E command reference | Converted to dependency on `e2e-testing` skill |
| Git checkpoint evidence | Preserved with Codex-safe caveats |

