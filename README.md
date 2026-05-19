# codex-skills

Eval-backed reusable Codex skills packaged as a local Codex plugin marketplace.

This repository is a distribution surface for reusable agent workflows, not a scratchpad. Each skill is intended to be:

- **Triggerable**: the skill description says when Codex should load it.
- **Portable**: converted workflows preserve behavior from other agent harnesses where useful.
- **Validated**: converted skills include task evals, trigger evals, and source-parity notes.
- **Composable**: skills can carry helper scripts, references, assets, and lightweight UI metadata.

> Unofficial project. This repository is not affiliated with OpenAI, Codex, Anthropic, Claude, or any upstream source projects referenced in converted skills.

## Install

Clone the repository and add it as a local marketplace:

```bash
git clone https://github.com/elijj/codex-skills.git
codex plugin marketplace add ./codex-skills
```

For a fork or private checkout, point Codex at the local repository path instead:

```bash
codex plugin marketplace add /path/to/codex-skills
```

The marketplace installs the `codex-skills` plugin by default. Plugin metadata lives at:

```text
plugins/codex-skills/.codex-plugin/plugin.json
```

The bundled skills live under:

```text
plugins/codex-skills/skills/
```

## Included Skills

- `skill-creator` — create, package, test, benchmark, and improve Codex skills.
- `harness-skill-porting` — convert Claude Code, Cursor, Cline, Roo, Aider, or prompt-pack workflows into Codex-native skills with parity tracking.
- `karpathy-guidelines` — apply pragmatic code-quality guidance.
- `refactor-cleaner` — clean refactors while preserving behavior.
- `warp-worktree-fix` — repair Warp worktree configuration issues.
- `implementation-planning` — produce implementation plans before coding.
- `tdd-workflow` — use test-first implementation loops.
- `build-fix` — fix build, typecheck, and compile errors incrementally.
- `code-review` — review changes for correctness, maintainability, security, and test gaps.
- `prp-plan` — create PRP-style implementation plans.
- `prp-implement` — implement from PRP plans with report artifacts.
- `prp-pr` — prepare pull requests from PRP work.
- `prp-commit` — prepare commits from PRP work.
- `e2e-testing` — plan and execute end-to-end testing workflows.

## Repository Layout

```text
.agents/plugins/marketplace.json           # local marketplace metadata
plugins/codex-skills/.codex-plugin/        # Codex plugin metadata
plugins/codex-skills/skills/<skill>/       # individual skills
scripts/validate-skills.sh                 # repo-level validation gate
NOTICE.md                                  # attribution and license notes
PUBLICATION_CHECKLIST.md                   # pre-publication safety checklist
```

A typical skill directory may include:

```text
SKILL.md          # required skill instructions and trigger metadata
agents/           # optional display, grader, or helper-agent guidance
evals/            # task and trigger evals
references/       # longer docs loaded on demand
scripts/          # deterministic helper scripts
assets/           # templates, images, fixtures, or viewer assets
```

## Converted Skills

Converted skills preserve workflow behavior from other agent-harness surfaces while keeping `skills/` as the canonical Codex surface:

- Behavioral: `karpathy-guidelines`
- Cleanup and refactoring: `refactor-cleaner`
- Warp worktree config repair: `warp-worktree-fix`
- Planning and implementation: `implementation-planning`, `prp-plan`, `prp-implement`
- Validation and review: `tdd-workflow`, `build-fix`, `code-review`, `e2e-testing`
- GitHub workflow: `prp-commit`, `prp-pr`
- Meta conversion: `harness-skill-porting`

Each converted skill should document its source behavior in `references/source-parity.md`.

## Validate

Run the full repository validation before publishing marketplace changes:

```bash
scripts/validate-skills.sh
```

The validation script runs `quick_validate.py` for every skill, validates every eval JSON file with `python3 -m json.tool`, and checks that each converted skill has:

- `references/source-parity.md`
- `evals/evals.json`
- task eval assertions
- a 20-prompt `evals/trigger_eval_<skill>.json` split into 10 positive and 10 negative trigger prompts

Run trigger optimization with the existing `skill-creator` loop when changing a converted skill description:

```bash
python3 plugins/codex-skills/skills/skill-creator/scripts/run_loop.py \
  --eval-set plugins/codex-skills/skills/<skill>/evals/trigger_eval_<skill>.json \
  --skill-path plugins/codex-skills/skills/<skill> \
  --max-iterations 3 \
  --runs-per-query 2 \
  --results-dir /tmp/codex-skills-trigger-optimization
```

## Add Skills

Future reusable skills should live under:

```text
plugins/codex-skills/skills/<skill-name>/
```

Each skill directory should keep its `SKILL.md` at the root and place optional Codex metadata, helper scripts, references, assets, and review tooling in the conventional subdirectories (`agents/`, `scripts/`, `references/`, `assets/`, and similar).

When adding or converting a skill:

1. Keep trigger guidance in `SKILL.md` frontmatter.
2. Move long compatibility notes or examples into `references/`.
3. Add task evals and trigger evals before treating the skill as releasable.
4. Add or update `references/source-parity.md` when behavior came from another harness or upstream workflow.
5. Run `scripts/validate-skills.sh` before opening a PR.

## Before Making This Repository Public

This repository is intended to be safe to publish only after the pre-publication checklist passes. See [`PUBLICATION_CHECKLIST.md`](PUBLICATION_CHECKLIST.md).

Recommended release posture:

- Keep this private repository as the working copy.
- Publish from a clean mirror or fresh branch after history and secret scanning.
- Avoid flipping visibility directly until commit history, attribution, and private artifacts are reviewed.

## License and Attribution

Root project code and docs are licensed under the MIT License unless otherwise noted. Some bundled or converted content carries upstream notices or separate license terms. See [`NOTICE.md`](NOTICE.md) and per-skill `LICENSE.txt` / `references/source-parity.md` files for details.