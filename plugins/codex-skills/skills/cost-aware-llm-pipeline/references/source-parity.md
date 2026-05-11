# Source Parity

Source: `https://github.com/affaan-m/everything-claude-code/blob/main/skills/cost-aware-llm-pipeline/SKILL.md`

| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| ECC skill frontmatter and activation guidance | `SKILL.md` frontmatter description | Direct | Low | Trigger wording is expanded for Codex phrases around LLM API cost, budgets, model routing, token accounting, retries, prompt caching, hosted gateways, agent workers, and batch jobs. |
| "When to Activate" cases for LLM API apps, batches, budgets, and cost-quality optimization | `SKILL.md` description and overview | Direct | Low | Preserves the source activation surface in Codex-native trigger language. |
| Model routing by task complexity | `SKILL.md` cost policy and routing sections | Direct | Low | Preserves cheap-versus-strong routing and adds measurable routing signals, logging, and override handling. |
| Source Claude model constants | `SKILL.md` cost policy section | Emulated | Medium | Replaced hardcoded source examples with configurable provider/model profiles because model ids and prices change. |
| Immutable cost tracking with frozen records | `SKILL.md` usage recording section | Direct | Low | Preserves immutable ledger behavior and extends it with provider, trace id, cached-token, estimate/billed, routing reason, retry attempt, and timestamp fields. |
| Budget limit and over-budget guard | `SKILL.md` budget preflight section | Direct | Low | Preserves fail-before-overspend behavior and generalizes scope to request, user, tenant, workspace, batch, billing period, and workflow budgets. |
| Narrow retry logic for transient errors only | `SKILL.md` retry section | Direct | Low | Preserves retryable versus non-retryable classification and adds budget accounting for paid retry attempts. |
| Prompt caching for stable long prompts | `SKILL.md` caching section | Direct | Low | Preserves provider caching guidance and adds cache keys, TTLs, invalidation, privacy boundaries, tenant isolation, and cached-token accounting. |
| Composition example combining routing, budget, retry, caching, and tracking | `SKILL.md` runtime flow section | Direct | Low | Converts the Python snippet into a language-neutral runtime flow for Codex implementation work. |
| 2025-2026 static pricing table | `SKILL.md` paid-path and cost-policy sections | Emulated | Medium | Replaced with current-doc/config verification guidance to avoid stale pricing inside the reusable skill. |
| Best practices | `SKILL.md` sections 2 through 10 | Direct | Low | Preserved as concrete implementation guardrails and reporting requirements. |
| Anti-patterns | `SKILL.md` sections 2 through 9 | Direct | Low | Preserved by instructing against scattered model names, vague routing labels, retrying permanent failures, mutable hidden state, and cache misuse. |
| Python-only source snippets | `SKILL.md` language-neutral workflow | Emulated | Low | Codex should adapt the pattern to the repository language and local SDK helpers instead of copying Python into every project. |
| Source had no scripts, hooks, agents, assets, or evals | `evals/` and no runtime scripts | Direct | Low | Added Codex evals for trigger and task behavior; no runtime dependency closure needed beyond the single source skill. |
