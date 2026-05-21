# codex-skills

Reusable Codex skills packaged as a local Codex plugin marketplace.

This repo is a distribution surface for reusable agent workflows, not a scratchpad. Skills should be triggerable, portable, validated, and small enough to load only the context they need.

> Unofficial project. Not affiliated with OpenAI, Codex, Anthropic, Claude, or upstream source projects referenced by converted skills.

## Install

```bash
git clone https://github.com/elijj/codex-skills.git
codex plugin marketplace add ./codex-skills
```

For a local/private checkout:

```bash
codex plugin marketplace add /path/to/codex-skills
```

Plugin metadata: `plugins/codex-skills/.codex-plugin/plugin.json`

Skills: `plugins/codex-skills/skills/`

## Skills

- [`skill-creator`](plugins/codex-skills/skills/skill-creator/SKILL.md) — create, package, test, benchmark, and improve Codex skills.
- [`harness-skill-porting`](plugins/codex-skills/skills/harness-skill-porting/SKILL.md) — convert other agent-harness workflows into Codex-native skills.
- [`karpathy-guidelines`](plugins/codex-skills/skills/karpathy-guidelines/SKILL.md) — apply pragmatic code-quality guidance.
- [`refactor-cleaner`](plugins/codex-skills/skills/refactor-cleaner/SKILL.md) — remove dead code and cleanup refactors safely.
- [`warp-worktree-fix`](plugins/codex-skills/skills/warp-worktree-fix/SKILL.md) — repair Warp worktree configuration issues.
- [`implementation-planning`](plugins/codex-skills/skills/implementation-planning/SKILL.md) — produce implementation plans before coding.
- [`tdd-workflow`](plugins/codex-skills/skills/tdd-workflow/SKILL.md) — use test-first implementation loops.
- [`build-fix`](plugins/codex-skills/skills/build-fix/SKILL.md) — fix build, typecheck, and compile errors incrementally.
- [`code-review`](plugins/codex-skills/skills/code-review/SKILL.md) — review changes for correctness, security, and maintainability.
- [`goal-grader`](plugins/codex-skills/skills/goal-grader/SKILL.md) — grade and optimize Codex `/goal` prompts.
- [`update-codemaps`](plugins/codex-skills/skills/update-codemaps/SKILL.md) — refresh token-lean architecture codemaps.
- [`update-docs`](plugins/codex-skills/skills/update-docs/SKILL.md) — sync generated docs from source-of-truth files.
- [`prp-plan`](plugins/codex-skills/skills/prp-plan/SKILL.md) — create PRP-style implementation plans.
- [`prp-implement`](plugins/codex-skills/skills/prp-implement/SKILL.md) — implement from PRP plans with report artifacts.
- [`prp-pr`](plugins/codex-skills/skills/prp-pr/SKILL.md) — prepare pull requests from PRP work.
- [`prp-commit`](plugins/codex-skills/skills/prp-commit/SKILL.md) — prepare commits from PRP work.
- [`e2e-testing`](plugins/codex-skills/skills/e2e-testing/SKILL.md) — plan and execute end-to-end testing workflows.

## Layout

```text
plugins/codex-skills/.codex-plugin/        # plugin metadata
plugins/codex-skills/skills/<skill>/       # individual skills
scripts/validate-skills.sh                 # repo validation gate
NOTICE.md                                  # attribution and license notes
PUBLICATION_CHECKLIST.md                   # pre-publication safety checklist
```

Typical skill files:

```text
SKILL.md          # required instructions and trigger metadata
agents/           # optional UI/helper-agent metadata
evals/            # task and trigger evals
references/       # longer docs loaded on demand
scripts/          # deterministic helper scripts
assets/           # templates, images, fixtures, or viewer assets
```

## Validate

```bash
scripts/validate-skills.sh
```

The validator checks skill metadata, eval JSON, and release artifacts for converted skills:

- `references/source-parity.md`
- `evals/evals.json`
- task eval assertions
- 20 trigger eval prompts split 10 positive / 10 negative

## Add Or Convert Skills

1. Keep trigger guidance in `SKILL.md` frontmatter.
2. Move long compatibility notes or examples into `references/`.
3. Add task evals and trigger evals before treating a skill as releasable.
4. Add `references/source-parity.md` when behavior came from another harness or upstream workflow.
5. Run `scripts/validate-skills.sh` before opening a PR.

Do not commit task-local `.codex/prps/` plans or reports unless they are intentional fixtures.

## Publishing

See [`PUBLICATION_CHECKLIST.md`](PUBLICATION_CHECKLIST.md) before making this repository public.

## License

Root project code and docs are MIT licensed unless otherwise noted. Some bundled or converted content carries upstream notices or separate license terms. See [`NOTICE.md`](NOTICE.md) and per-skill license/source-parity files.
