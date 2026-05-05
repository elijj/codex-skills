---
name: e2e-testing
description: Use this skill when creating, updating, debugging, or reviewing Playwright end-to-end tests, browser user flows, Page Object Models, CI E2E setup, flaky test handling, screenshots, traces, videos, or when a workflow invokes `/e2e`. It covers stable selectors, artifact management, critical flow coverage, and test reports.
metadata:
  short-description: Build stable Playwright E2E coverage
---

# E2E Testing

Use this skill for Playwright E2E coverage that behaves like production users and produces useful diagnostics when it fails.

## Workflow

1. Identify the critical user journey and its acceptance criteria.
2. Inspect existing Playwright config, test layout, fixtures, and selector conventions.
3. Add or update tests using resilient locators: roles, labels, text, and `data-testid` where appropriate.
4. Prefer Page Object Models for repeated page interactions.
5. Wait for specific UI, network, or route conditions rather than arbitrary timeouts.
6. Run the smallest relevant E2E target first, then broaden if the flow is critical.
7. Capture and report artifacts: HTML report, screenshots, videos, traces, console/network notes when relevant.

## Recommended Layout

```text
tests/
  e2e/
    auth/
    features/
    api/
  fixtures/
  pages/
playwright.config.ts
```

## Playwright Practices

- Use `await expect(locator).toBeVisible()` or semantic assertions instead of implementation details.
- Use `page.waitForResponse()` only when the response is a meaningful user-flow signal.
- Avoid fixed sleeps unless validating debounce behavior and no better signal exists.
- Configure retries in CI, not as a substitute for fixing race conditions.
- Use `trace: "on-first-retry"`, failure screenshots, and retained videos for diagnostic value.

## Config And CI Defaults

- Prefer explicit reporters that preserve an HTML report and machine-readable output in CI.
- Configure `use.screenshot`, `use.video`, and `use.trace` so failures leave useful diagnostics.
- Add `webServer` when the app must run locally for tests.
- In CI, upload `playwright-report/` and other failure artifacts so failures can be inspected later.

## Flake Handling

When a test is flaky:

1. Re-run with `--repeat-each` or retries to characterize the failure.
2. Identify the common failure point and likely race.
3. Replace brittle selectors or timing assumptions.
4. Quarantine with `test.fixme()` only when the flow cannot be stabilized immediately, and include the issue/reason.

## Report Format

```markdown
# E2E Test Report

Status: PASSING | FAILING
Command: `<command>`

Summary:
- Total:
- Passed:
- Failed:
- Flaky:
- Skipped:

Artifacts:
- HTML report:
- Screenshots:
- Videos:
- Traces:

Failures:
- `<test>` (`path:line`): <error and recommended fix>
```
