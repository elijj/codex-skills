---
name: update-docs
description: Use this skill when the user invokes `/update-docs`, asks to sync documentation from source-of-truth files, refresh generated docs, update command/env/API/contributing/runbook docs from code, or check docs for staleness after code changes. Converted from ECC `commands/update-docs.md` for Codex. The skill derives docs from scripts, schemas, routes, exports, env templates, and deployment files while preserving manual prose.
---

# Update Docs

Sync documentation from source-of-truth files. Treat code, schemas, configs, and route definitions as authoritative; preserve manual documentation sections.

## Source Discovery

Scan the repo for source-of-truth files:

| Source | Generated Documentation |
| --- | --- |
| `package.json`, `Makefile`, `Cargo.toml`, `pyproject.toml`, task files | commands/scripts reference |
| `.env.example`, `.env.template`, `.env.sample` | environment variable reference |
| `openapi.yaml`, `openapi.json`, route files, controllers | API endpoint reference |
| public exports, CLI entry points, library modules | public API reference |
| `Dockerfile`, `docker-compose.yml`, deployment configs | infrastructure and runbook notes |

If sources are missing, skip that section and explain why. Do not invent commands, env vars, routes, or deployment procedures.

## Generated Section Contract

Only replace content inside generated markers. Support both Codex section markers and legacy ECC markers.

```markdown
<!-- BEGIN GENERATED: section-name -->
...
<!-- END GENERATED: section-name -->
```

```markdown
<!-- AUTO-GENERATED -->
...
<!-- /AUTO-GENERATED -->
```

If a file exists without markers, preserve all prose and ask before rewriting broad sections. If a needed doc file is missing, create it only when the user explicitly requested that new file or doc type. For a generic "update docs" request, update existing docs only and report missing docs as skipped.

## Workflow

1. Build an inventory.
   - Identify available source files and existing docs.
   - Note stale docs: documentation files older than 90 days that overlap recently changed source areas.
   - Decide target docs based on discovered sources and user scope.
2. Generate command reference.
   - Extract scripts/tasks/commands from package and build files.
   - Prefer descriptions from adjacent comments, script names, existing docs, or conventional meanings.
   - Mark unknown descriptions as `Needs description` rather than guessing.
3. Generate environment reference.
   - Read env templates, never secret `.env` files.
   - Categorize variables as required vs optional when defaults or comments make that clear.
   - Document expected format, valid values, and safe examples.
4. Generate API or public surface reference.
   - Prefer OpenAPI files when present.
   - Otherwise summarize route files/controllers or exported modules.
   - Include method/path, handler, auth requirement when discoverable, and source file.
5. Update contributor docs.
   - Prefer the repo's existing contributor guide: `CONTRIBUTING.md`, `docs/CONTRIBUTING.md`, or equivalent.
   - Update generated sections for prerequisites, install, scripts, tests, lint/format, and PR checklist.
6. Update runbook docs.
   - Prefer the repo's existing runbook: `RUNBOOK.md`, `docs/RUNBOOK.md`, `docs/operations.md`, or equivalent.
   - Update generated sections for deploy steps, health checks, monitoring, rollback, and escalation only when source files reveal them.
7. Show a concise summary:

   ```text
   Documentation Update
   Updated: docs/CONTRIBUTING.md (scripts table)
   Updated: docs/ENV.md (3 new variables)
   Flagged: docs/DEPLOY.md (142 days stale)
   Skipped: docs/API.md (no route source found)
   ```

## Safety Rules

- Never read or copy real secret values from `.env`, local credential files, keychains, or deployment secrets.
- Preserve manual sections outside generated markers.
- Do not create broad new docs unless the user explicitly asks for new docs or names the missing doc type/path.
- Do not document behavior not supported by source files.
- Keep generated docs concise and easy to diff.

## Verification

Before finishing:

- Confirm generated markers are balanced.
- Confirm no secrets or local-only values were copied.
- Run markdown formatting or link checks if the repo already provides them.
- Report updated, created, skipped, and flagged docs.

## Source Parity

For conversion notes and ECC parity decisions, read `references/source-parity.md` only when auditing or modifying this skill.
