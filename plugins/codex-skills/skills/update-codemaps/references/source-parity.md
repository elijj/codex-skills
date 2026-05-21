# Source Parity: ECC `update-codemaps`

Source: `https://github.com/affaan-m/ECC/blob/main/commands/update-codemaps.md`

Fetched 2026-05-21.

## Parity Ledger

| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| Slash command `/update-codemaps` | `SKILL.md` description trigger wording | Direct | Low | Codex uses skill trigger text rather than command files. |
| Scan project type, source dirs, entry points | `SKILL.md` workflow steps 1-2 | Direct | Low | Preserved as repo-shape discovery. |
| Generate `docs/CODEMAPS/` or `.reports/codemaps/` | `SKILL.md` inputs and workflow | Direct | Low | Codex preserves existing location and defaults new ambiguous output to `.reports/codemaps/`. |
| Codemap file set: architecture/backend/frontend/data/dependencies | `SKILL.md` workflow step 3 | Direct | Low | Irrelevant maps are skipped with report notes. |
| Token-lean format under 1000 tokens | `SKILL.md` style and verification | Direct | Low | Preserved as target, not hard failure for large repos. |
| Diff detection over 30% requires approval | `SKILL.md` workflow step 6 | Emulated | Medium | Codex must estimate changed lines and pause; no source hook enforces it. |
| Freshness header | `SKILL.md` workflow step 4 | Direct | Low | Implemented as an HTML comment marker. |
| `.reports/codemap-diff.txt` summary | `SKILL.md` workflow step 7 | Direct | Low | Includes git-discoverable changes and staleness warnings. |
| Tips: high-level structure, paths/signatures, ASCII diagrams | `SKILL.md` codemap style | Direct | Low | Preserved as writing guidance. |

## Conversion Notes

The ECC command is a Claude-style slash command. The Codex conversion makes it a triggerable skill and adds explicit overwrite safety because Codex cannot rely on command-level hooks. No external MCP dependency is required.
