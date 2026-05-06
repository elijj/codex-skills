---
name: refactor-cleaner
description: "Use this skill when the user invokes `/refactor-clean` or asks to find and remove dead code, unused imports, orphaned files, duplicate logic, dead branches, or unused dependencies. It keeps cleanup cautious: classify risk, delete one item at a time, verify after each change, and stop when uncertainty appears."
metadata:
  short-description: Safely remove dead code
---

# Refactor Cleaner

Use this skill to remove dead code and duplicate clutter without turning the task into a broad refactor.

## 1. Detect dead code

Prefer project-native analysis tools when they exist. Use the analyzer that fits the stack, then fall back to text search when no analyzer is available.

| Stack | Prefer | What it finds |
| --- | --- | --- |
| JavaScript / TypeScript | `npx knip`, `npx depcheck`, `npx ts-prune` | Unused exports, files, dependencies, and TypeScript symbols |
| Python | `vulture src/` | Unused functions, classes, and variables |
| Go | `deadcode ./...` | Unused Go code |
| Rust | `cargo +nightly udeps` | Unused dependencies |
| Any stack | `rg` / `ripgrep` | Export, import, and reference traces when no analyzer fits |

If a command is unavailable, do not invent a wrapper. Use the strongest local search you can run.

## 2. Categorize findings

Sort every candidate before deleting it.

- SAFE: unused utilities, helper functions, dead branches, and test-only helpers with no external consumers.
- CAUTION: components, API routes, middleware, generated code, and symbols that could be reached dynamically.
- DANGER: config files, entry points, public exports, type definitions, and anything that may be part of a package contract.

Treat CAUTION and DANGER as "prove it first" work. If you cannot prove the item is unused, leave it alone.

## 3. Clean one item at a time

For each SAFE item:

1. Run the relevant baseline verification target first.
2. Delete exactly one item.
3. Re-run the same verification target immediately.
4. If verification fails, restore the tracked file and skip the item.
5. If verification passes, move to the next item.

Keep the deletions atomic. Do not batch several removals into one change unless they are the same dead symbol in the same file.

## 4. Handle caution items

Before touching CAUTION or DANGER items, search for:

- `import()` / `require()` / `__import__`
- string references to route names, component names, command names, or config keys
- public package exports and re-export chains
- external consumers or generated entrypoints
- test fixtures or build scripts that load the symbol indirectly

If the item might be reachable dynamically, stop and report the uncertainty instead of deleting it.

## 5. Consolidate duplicates after cleanup

After the dead-code pass is stable, look for duplicate code that can be merged safely.

- Merge near-duplicate functions only when behavior is clearly the same.
- Consolidate redundant type definitions.
- Remove wrapper functions that add no value.
- Drop re-exports that only add indirection.

Do not refactor first and clean later. Remove dead code before you simplify surviving code.

## 6. Report the cleanup

End with a concise cleanup summary.

Include:

- what was deleted
- what was skipped and why
- what verification command(s) ran
- whether the cleanup introduced any failures
- any remaining uncertainty

Use a format like:

```text
Dead Code Cleanup
Deleted: ...
Skipped: ...
Verified: ...
Remaining: ...
```

If nothing was deleted, say why and name the blocker.
