# Source Parity

Sources:

- `https://github.com/affaan-m/everything-claude-code/blob/main/commands/plan.md`
- `https://github.com/affaan-m/everything-claude-code/blob/main/agents/planner.md`

| Source feature | Codex port |
| --- | --- |
| `/plan` slash command | Trigger phrases in the skill description, including `/plan` |
| Delegation to `planner` agent | Planner instructions embedded inline |
| Read/Grep/Glob codebase inspection | Codex read-only file exploration using local tools such as `rg`, `sed`, and file reads |
| Stable markdown plan format | Preserved and made explicit |
| Wait for explicit confirmation before coding | Preserved as a hard confirmation gate |
| Follow-on commands `/tdd`, `/build-fix`, `/code-review`, `/prp-plan`, `/prp-implement` | Converted into separate Codex skills and referenced by name |

