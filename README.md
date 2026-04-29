# codex-skills

Local Codex plugin marketplace for reusable Codex skills.

## Install

Add this repository as a local marketplace:

```bash
codex plugin marketplace add /mnt/a/Users/anon/Desktop/deving/private-repos/codex-skills
```

The marketplace installs the `codex-skills` plugin by default. The plugin currently bundles the `skill-creator` skill from `plugins/codex-skills/skills/skill-creator`, so adding this marketplace makes that skill available through the plugin system.

## Add Skills

Future reusable skills should live under:

```text
plugins/codex-skills/skills/<skill-name>/
```

Each skill directory should keep its `SKILL.md` at the root and place optional Codex metadata, helper scripts, references, assets, and review tooling in the conventional subdirectories (`agents/`, `scripts/`, `references/`, `assets/`, and similar).

Validate bundled skills before publishing marketplace changes:

```bash
python3 plugins/codex-skills/skills/skill-creator/scripts/quick_validate.py plugins/codex-skills/skills/skill-creator
```
