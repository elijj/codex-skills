---
name: prp-pr
description: Use this skill when the user invokes `/prp-pr`, asks to create a GitHub pull request from the current branch, wants commits analyzed into a PR title/body, needs PR templates discovered, wants the branch pushed with upstream tracking, or wants PRP plan/report artifacts referenced in a PR. It validates git state, uses GitHub CLI when available, and recommends `prp-commit` or `code-review` as needed.
metadata:
  short-description: Create GitHub PRs from current branch
---

# PRP Pull Request

Create a GitHub pull request from the current branch with a useful title, body, testing section, and references to PRP artifacts.

## Inputs

Accept optional base branch and flags:

- Base branch, default `main`.
- `--draft` to create a draft PR.

## Workflow

### Phase 1: Validate

Run:

```bash
git branch --show-current
git status --short
git log origin/<base>..HEAD --oneline
```

Check:

- Current branch is not the base branch.
- Working tree is clean enough to PR. If not, suggest `prp-commit`.
- Branch has commits ahead of base.
- No existing PR for the branch, using `gh pr list --head <branch>` when available.

### Phase 2: Discover Context

- Locate PR templates in `.github/PULL_REQUEST_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/pull_request_template.md`, or `docs/pull_request_template.md`.
- Analyze commits with `git log origin/<base>..HEAD --format="%h %s" --reverse`.
- Analyze files with `git diff origin/<base>..HEAD --stat` and `--name-only`.
- Include related `.codex/prps/plans/`, `.codex/prps/reports/`, and `.codex/prps/prds/` artifacts when they exist.

### Phase 3: Push

Use:

```bash
git push -u origin HEAD
```

If remote has diverged, fetch and rebase only when safe. If conflicts occur, stop and report.

### Phase 4: Create PR

Use `gh pr create` when GitHub CLI is installed and authenticated. Preserve PR template sections; fill unknown sections with `N/A` rather than deleting them.

Default body when no template exists:

```markdown
## Summary

## Changes

## Files Changed

## Testing

## Related Issues

## PRP Artifacts
```

### Phase 5: Verify

Run:

```bash
gh pr view --json number,url,title,state,baseRefName,headRefName,additions,deletions,changedFiles
gh pr checks --json name,status,conclusion 2>/dev/null || true
```

## Final Response

Include PR number, title, URL, branch/base, change stats, CI status, artifacts referenced, and next steps. Recommend `code-review <number>` before merge when review has not already happened.
