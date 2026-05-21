---
name: update-codemaps
description: Use this skill when the user invokes `/update-codemaps`, asks to update codemaps, generate architecture maps, refresh AI-readable architecture docs, scan project structure into `docs/CODEMAPS/`, or produce token-lean codebase maps after major feature work or refactors. Converted from ECC `commands/update-codemaps.md` for Codex. The skill scans project structure, writes compact codemap documents, detects large diffs before overwriting, and records a codemap update report.
---

# Update Codemaps

Generate token-lean architecture codemaps for AI context loading. Prefer high-signal structure over implementation detail.

## Inputs

Use the current repo unless the user gives a path. If multiple apps/packages exist, map the whole workspace first, then create package-specific notes only where boundaries matter.

Default output:

- Prefer existing `docs/CODEMAPS/`.
- If `.reports/codemaps/` already exists, use it to preserve ECC generated-artifact workflows.
- If neither exists and the user did not specify a tracked docs location, create `.reports/codemaps/`.
- Also write `.reports/codemap-diff.txt` when `.reports/` can be created safely.

## Workflow

1. Scan project shape.
   - Identify project type: monorepo, single app, library, service, or mixed workspace.
   - Find source roots such as `src/`, `lib/`, `app/`, `packages/`, `apps/`, `services/`, `cmd/`, `internal/`.
   - Map entry points: `main.*`, `index.*`, app routers, package exports, CLI binaries, workers, server boot files.
   - Detect tests, migrations, generated code, docs, configs, and deployment files.
2. Build a compact architecture model.
   - Trace routes/controllers to services/repositories where possible.
   - Trace frontend routes/pages to components and state/data-fetching layers.
   - Trace database schemas, migrations, ORM models, queues, caches, and external services.
   - Capture file paths, public symbols, and responsibility boundaries. Avoid copying source bodies.
3. Prepare codemap files.
   - `architecture.md`: system overview, service boundaries, data flow, repo layout.
   - `backend.md`: API routes, middleware, jobs, services, repository/data access.
   - `frontend.md`: page tree, component hierarchy, state management, API calls.
   - `data.md`: tables/models, relationships, migrations, data stores.
   - `dependencies.md`: external services, third-party integrations, shared libraries.
   - Skip irrelevant files with a short note in the report rather than creating empty noise.
4. Add freshness metadata to each generated codemap:

   ```markdown
   <!-- codemap:freshness generated=YYYY-MM-DD source=repo-scan -->
   ```

5. Keep codemaps token-lean.
   - Target under 1000 tokens per file.
   - Prefer bullets, tables, ASCII diagrams, file paths, and function signatures.
   - Omit implementation details unless they explain architecture.
   - Mark uncertainty explicitly as `Unknown:` rather than guessing.
6. Protect existing codemaps.
   - If a codemap exists, draft the replacement first.
   - Estimate changed lines against the existing file.
   - If change is over 30%, show a concise diff summary and ask before overwriting.
   - If change is 30% or less, update in place.
7. Write `.reports/codemap-diff.txt`.
   - Files added, removed, and heavily modified since the last codemap scan when discoverable from git.
   - New dependencies or integrations detected.
   - Architecture changes: routes, services, packages, data stores, queues, workers.
   - Staleness warnings for architecture docs not updated in 90+ days.

## Codemap Style

Use this shape:

```markdown
# Backend Architecture

<!-- codemap:freshness generated=YYYY-MM-DD source=repo-scan -->

## Routes
POST /api/users -> UserController.create -> UserService.create -> UserRepo.insert
GET /api/users/:id -> UserController.get -> UserService.findById -> UserRepo.findById

## Key Files
src/services/user.ts - business rules and validation
src/repos/user.ts - database reads/writes

## Dependencies
- PostgreSQL - primary data store
- Redis - session cache and rate limiting
```

## Verification

Before finishing:

- Confirm every generated codemap has the freshness marker.
- Confirm no codemap exceeds the token-lean target unless the repo size makes that impractical.
- Run available formatting checks only if they apply to markdown.
- Report created, updated, skipped, and approval-required files.

## Source Parity

For conversion notes and ECC parity decisions, read `references/source-parity.md` only when auditing or modifying this skill.
