---
name: build-fix
description: Use this skill when the user invokes `/build-fix`, says the build/typecheck/compile is failing, asks to fix TypeScript, Rust, Go, Java, Python, Gradle, Maven, package, import, or CI build errors, or when an implementation hits build failures. It fixes errors incrementally with minimal diffs, reruns the build after each fix, and stops when a fix requires architecture changes or missing dependencies.
metadata:
  short-description: Fix build errors incrementally
---

# Build Fix

Use this skill to fix build, typecheck, and compile failures one root cause at a time.

## 1. Detect Build System

Inspect project files and prefer existing scripts:

| Indicator | Preferred command |
| --- | --- |
| `package.json` with build/typecheck scripts | package-manager script, then `tsc --noEmit` if TypeScript |
| `Cargo.toml` | `cargo build` or `cargo check` |
| `go.mod` | `go build ./...` |
| `pom.xml` | `mvn compile` |
| `build.gradle` / `gradlew` | `./gradlew compileJava` or project equivalent |
| `pyproject.toml` / `requirements.txt` | `python -m compileall -q .`, `pytest`, or `mypy` when configured |

Use the repository's package manager lockfile when running Node scripts.

## 2. Parse And Group Errors

Run the build command and capture the failing output. Group errors by file and root cause, then choose the first fix based on dependency order:

1. Syntax and parse errors.
2. Missing imports or modules.
3. Type/interface mismatches.
4. Generated files or config issues.
5. Logic or API incompatibilities.

Track the total error count and the number of root-cause groups after each build run so progress is explicit.

## 3. Fix Loop

For each error:

1. Read the file and surrounding context.
2. Diagnose the root cause.
3. Make the smallest change that can plausibly resolve it.
4. Rerun the relevant build/typecheck target.
5. Continue only if the error count or root-cause set improves.

## Stop Conditions

Stop and ask or report a blocker when:

- The same error remains after three targeted attempts.
- A fix introduces more errors than it resolves.
- The fix requires a new dependency, package install, schema migration, or broad architecture change.
- The build failure is unrelated to the user's requested scope.

## Final Report

Include:

- Build command(s) run.
- Errors fixed, grouped by file.
- Errors remaining.
- Original error count and final error count when available.
- New errors introduced, ideally zero.
- Recovery strategy used for unresolved errors.
- Any skipped dependency install or architectural blocker.
