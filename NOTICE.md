# Notice and Attribution

This repository bundles reusable Codex skills and converted workflow guidance. The root project is licensed under the MIT License unless a file or directory says otherwise.

## Upstream and Third-Party Content

Some skills were adapted from, inspired by, or converted from upstream workflow surfaces. When a skill has an upstream source, it should include a `references/source-parity.md` file that identifies the source and explains what behavior was preserved or changed.

Known upstream notes:

- `plugins/codex-skills/skills/skill-creator/` includes a separate `LICENSE.txt` notice for Anthropic, PBC under the Apache License 2.0.
- Converted skills under `plugins/codex-skills/skills/*/references/source-parity.md` may reference upstream Claude Code commands, slash-command packs, rules, or workflow examples.
- The `everything-claude-code` command sources referenced by some parity files are upstream materials and should retain their original license and attribution when copied or adapted.

## Attribution Requirements for New Skills

When adding a skill that copies, converts, or adapts existing material:

1. Add `references/source-parity.md` with the upstream URL or source path.
2. Preserve the upstream license file when required.
3. Note whether behavior was copied directly, adapted, or only used as inspiration.
4. Keep project-local or private policy out of reusable public skills.
5. Do not include private credentials, customer data, internal URLs, or proprietary source text unless the repository is intentionally private.

## Trademark and Product Names

Product names such as Codex, Claude, Anthropic, OpenAI, Cursor, Cline, Roo, Aider, Warp, and GitHub are used only to describe compatibility, source workflows, or integration surfaces. This repository is unofficial and unaffiliated with those product owners.