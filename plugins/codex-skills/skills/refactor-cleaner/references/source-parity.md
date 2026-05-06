# Source Parity

Source: `https://github.com/affaan-m/everything-claude-code/blob/main/commands/refactor-clean.md`

| Source feature | Codex port | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| `/refactor-clean` slash command | `SKILL.md` trigger description and cleanup workflow | Direct | Low | Slash invocation becomes trigger wording plus normal user prompt handling. |
| Dead code / unused imports / orphaned files / duplicate logic / dead branches / unused dependencies scope | `SKILL.md` overview and detection section | Direct | Low | Preserves the cleanup target set from the source command. |
| Analysis tools table (`knip`, `depcheck`, `ts-prune`, `vulture`, `deadcode`, `cargo +nightly udeps`) | `SKILL.md` detection table | Direct | Low | Keeps the same optional analyzers with a fallback to `rg`. |
| SAFE / CAUTION / DANGER triage | `SKILL.md` categorization section | Direct | Low | Preserves the source safety tiers. |
| One-item-at-a-time deletion loop | `SKILL.md` cleanup loop | Direct | Low | Keeps atomic deletions and easy rollback. |
| Verify after each deletion | `SKILL.md` cleanup loop and report section | Direct | Low | Same verify-after-change behavior. |
| Dynamic-import / string-reference / external-consumer checks | `SKILL.md` caution handling section | Direct | Low | Preserves the source guardrails before deleting public-facing code. |
| Duplicate consolidation after cleanup | `SKILL.md` post-cleanup section | Direct | Low | Keeps the "clean first, refactor later" ordering. |
| Summary of removed/skipped/verified items | `SKILL.md` report section | Direct | Low | Matches the source summary contract. |
