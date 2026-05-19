# Publication Checklist

Use this checklist before making this repository, a mirror, or a release artifact public.

## Recommended Publishing Strategy

Prefer publishing from a clean mirror instead of flipping the working private repository public.

Recommended flow:

```bash
# from a clean local checkout
git clone git@github.com:elijj/codex-skills.git codex-skills-public
cd codex-skills-public

# inspect, scrub, and validate before pushing to a public remote
scripts/validate-skills.sh
```

## Required Checks

- [ ] Run a secret scanner on the full working tree and git history.
- [ ] Review commit history for private paths, usernames, internal hostnames, customer names, credentials, tokens, API keys, and proprietary source text.
- [ ] Review `.codex/`, `.agents/`, `evals/fixtures/`, `references/`, generated reports, and archived PRP files for private or project-local content.
- [ ] Confirm all upstream-derived skills have `references/source-parity.md`.
- [ ] Confirm copied upstream content preserves required license notices.
- [ ] Confirm `NOTICE.md` is up to date.
- [ ] Confirm `README.md` install paths use clone-relative or placeholder paths, not local workstation paths.
- [ ] Run `scripts/validate-skills.sh`.
- [ ] Run `git diff --check`.
- [ ] Inspect all large files and binary assets.
- [ ] Confirm no generated caches, benchmark workspaces, local `.env` files, or credentialed configs are tracked.

## Suggested Secret Scans

Use at least one history-aware scanner. Examples:

```bash
# gitleaks example
gitleaks detect --source . --redact --verbose

# trufflehog example
trufflehog git file://$PWD --only-verified
```

If a real secret is found, rotate it. Do not rely on deletion from a later commit; public history can preserve leaked values.

## Review Areas That Commonly Leak Private Context

- Absolute local paths, especially under `/Users/`, `/mnt/c/Users/`, `/mnt/a/Users/`, `C:\Users\`, or `AppData`.
- Agent logs and evaluation outputs.
- Generated implementation reports and PRP archives.
- Fixture PRDs that accidentally describe real private work.
- Source-parity files that include private repository URLs.
- Screenshots, SVGs, and binary assets with embedded metadata.
- CI config that names private services, secrets, or internal package registries.

## Release Decision

Only make the repo public when:

1. The repository passes the validation script.
2. Secret scanning passes on the full history or the public mirror is created with clean history.
3. Attribution and licenses are complete enough for the upstream content included.
4. The README clearly presents this as an unofficial reusable Codex skills marketplace.

If any of those are uncertain, keep the working repository private and publish only a curated subset.