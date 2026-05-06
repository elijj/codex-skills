# codex-skills

Local Codex plugin marketplace for reusable Codex skills.

## Install

Add this repository as a local marketplace:

```bash
codex plugin marketplace add /mnt/a/Users/anon/Desktop/deving/private-repos/codex-skills
```

The marketplace installs the `codex-skills` plugin by default. The plugin currently bundles:

- `skill-creator` from `plugins/codex-skills/skills/skill-creator`
- `harness-skill-porting` from `plugins/codex-skills/skills/harness-skill-porting`
- `karpathy-guidelines` from `plugins/codex-skills/skills/karpathy-guidelines`
- `refactor-cleaner` from `plugins/codex-skills/skills/refactor-cleaner`
- `warp-worktree-fix` from `plugins/codex-skills/skills/warp-worktree-fix`
- `implementation-planning` from `plugins/codex-skills/skills/implementation-planning`
- `tdd-workflow` from `plugins/codex-skills/skills/tdd-workflow`
- `build-fix` from `plugins/codex-skills/skills/build-fix`
- `code-review` from `plugins/codex-skills/skills/code-review`
- `prp-plan` from `plugins/codex-skills/skills/prp-plan`
- `prp-implement` from `plugins/codex-skills/skills/prp-implement`
- `prp-pr` from `plugins/codex-skills/skills/prp-pr`
- `prp-commit` from `plugins/codex-skills/skills/prp-commit`
- `e2e-testing` from `plugins/codex-skills/skills/e2e-testing`

Adding this marketplace makes those skills available through the plugin system.

## Converted Skills

These skills preserve converted workflow behavior from other agent-harness surfaces while keeping `skills/` as the canonical Codex surface:

- Behavioral: `karpathy-guidelines`
- Cleanup and refactoring: `refactor-cleaner`
- Warp worktree config repair: `warp-worktree-fix`
- Planning and implementation: `implementation-planning`, `prp-plan`, `prp-implement`
- Validation and review: `tdd-workflow`, `build-fix`, `code-review`, `e2e-testing`
- GitHub workflow: `prp-commit`, `prp-pr`
- Meta conversion: `harness-skill-porting`

## Add Skills

Future reusable skills should live under:

```text
plugins/codex-skills/skills/<skill-name>/
```

Each skill directory should keep its `SKILL.md` at the root and place optional Codex metadata, helper scripts, references, assets, and review tooling in the conventional subdirectories (`agents/`, `scripts/`, `references/`, `assets/`, and similar).

Validate bundled skills before publishing marketplace changes:

```bash
scripts/validate-skills.sh
```

The validation script runs `quick_validate.py` for every skill, validates every eval JSON file with `python3 -m json.tool`, and checks that each converted skill has `references/source-parity.md`, `evals/evals.json`, task eval assertions, and a 20-prompt `evals/trigger_eval_<skill>.json` split into 10 positive and 10 negative trigger prompts.

Run trigger optimization with the existing `skill-creator` loop when changing a converted skill description:

```bash
python3 plugins/codex-skills/skills/skill-creator/scripts/run_loop.py \
  --eval-set plugins/codex-skills/skills/<skill>/evals/trigger_eval_<skill>.json \
  --skill-path plugins/codex-skills/skills/<skill> \
  --max-iterations 3 \
  --runs-per-query 2 \
  --results-dir /tmp/codex-skills-trigger-optimization
```
