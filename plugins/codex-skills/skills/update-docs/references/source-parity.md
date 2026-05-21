# Source Parity: ECC `update-docs`

Source: `https://github.com/affaan-m/ECC/blob/main/commands/update-docs.md`

Fetched 2026-05-21.

## Parity Ledger

| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| Slash command `/update-docs` | `SKILL.md` description trigger wording | Direct | Low | Codex uses skill trigger text rather than command files. |
| Identify source-of-truth files | `SKILL.md` source discovery table | Direct | Low | Preserves scripts, env templates, OpenAPI/routes, exports, and deployment files. |
| Generate script reference | `SKILL.md` workflow step 2 | Direct | Low | Adds `Needs description` fallback instead of guessing. |
| Generate environment docs | `SKILL.md` workflow step 3 and safety rules | Direct | Low | Explicitly avoids real `.env` secrets. |
| Update contributing guide | `SKILL.md` workflow step 5 | Direct | Low | Uses generated sections. |
| Update runbook | `SKILL.md` workflow step 6 | Direct | Low | Only writes deployment details discoverable from source files. |
| Staleness check for docs older than 90 days | `SKILL.md` workflow step 1 and summary | Direct | Low | Preserved as flagging behavior. |
| Summary block with updated/flagged/skipped docs | `SKILL.md` workflow step 7 | Direct | Low | Preserved in Codex output contract. |
| Preserve manual sections and mark generated content | `SKILL.md` generated section contract | Direct | Low | Supports both Codex section markers and legacy ECC `AUTO-GENERATED` markers. |
| Do not create docs unprompted | `SKILL.md` safety rules | Direct | Low | Generic update requests update existing docs only; new files require explicit path or doc type. |

## Conversion Notes

The ECC command is a Claude-style slash command. The Codex conversion turns command behavior into a reusable documentation synchronization workflow with stronger secret-handling and marker-preservation rules.
