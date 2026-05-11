---
name: cost-aware-llm-pipeline
description: "Use this skill whenever the user is building, reviewing, debugging, or refactoring application code that spends money on LLM API calls. Trigger for OpenAI, Anthropic/Claude, Gemini, Mistral, hosted model gateways, agent workers, batch jobs, token usage, API credits, spend limits, per-user or per-tenant budgets, model routing, fallback models, prompt caching, paid retries, or reducing an LLM bill. Skip generic prompt-writing or AI explanations unless runtime API cost controls are part of the task."
metadata:
  short-description: Control LLM API spend
---

# Cost-Aware LLM Pipeline

Use this skill when LLM API usage is part of production behavior, not just a one-off prompt. The goal is to make paid model calls intentional, observable, and bounded.

Build toward five concrete surfaces:

1. A model policy that says which models are allowed and why.
2. A router that picks the cheapest adequate model from measurable task signals.
3. A budget guard that runs before paid calls and records actual usage after them.
4. A retry policy that spends money only on failures likely to recover.
5. Tests that prove expensive behavior is deliberate.

## 1. Map the Paid Path First

Before editing, find the real provider call path.

Inspect:

- provider SDKs or gateways, such as OpenAI, Anthropic, Gemini, Mistral, LiteLLM, or internal proxy clients
- model ids and where they are configured
- usage metadata returned by the provider, including input, output, cached, reasoning, or billed tokens
- retry, timeout, concurrency, queue, and batch behavior
- tenant, user, job, or request identifiers available for budget scope
- logging, metrics, tracing, and persistence patterns already used by the repo
- existing tests and fake provider clients

If pricing, model names, token semantics, or prompt caching behavior matter, verify them from current official provider docs or the repo's existing pricing config. Do not hardcode stale example prices into reusable code.

## 2. Add a Cost Policy

Prefer a single policy/config object over scattered constants.

The policy should describe:

- model profiles: provider, model id, input/output price, context limits, and supported features
- tiers: `fast`, `balanced`, `strong`, or product-specific names
- routing thresholds: token count, item count, schema complexity, tool use, modality, risk, or validation failures
- budget scopes: request, user, tenant, workspace, batch job, feature, day, or billing period
- override rules: who can force a model, when, and how that override is logged
- fallback rules: when to degrade, split a batch, escalate, or stop

Keep prices configurable. Code should still work when prices are updated without editing business logic.

## 3. Route by Measurable Complexity

Start with the cheapest tier that can satisfy the request.

Good routing signals:

- estimated input tokens or character count
- number of records in a batch
- output schema size or strictness
- tool-call or structured-output requirement
- modality, such as vision, audio, or file input
- compliance, financial, medical, or other higher-risk context
- failed cheap-model validation where escalation is allowed

Avoid vague routing based only on words like "hard" or "important" unless the product already treats them as policy.

Every route should produce a reason, for example:

```text
model=fast reason=short_extraction input_tokens=420 item_count=1
model=strong reason=large_context input_tokens=58000 threshold=32000
model=balanced reason=cheap_model_failed_schema_validation retry_of=request_abc
```

## 4. Preflight the Budget

Estimate cost before calling the provider. Use measured tokens when available and conservative estimates otherwise.

Before the call:

- compute expected input and max output cost
- include prompt cache reads/writes if the provider prices them separately
- check the relevant budget scope
- reject, degrade, chunk, or ask for explicit approval when the call would exceed budget

After the call:

- record actual usage from provider metadata
- distinguish estimated cost from billed or provider-reported cost
- update the same budget scope used during preflight
- emit metrics or logs with request id, tenant/user id, model, reason, tokens, and cost

Budget checks that only log overspend are not guardrails. The code path should prevent new paid work once the limit is reached.

## 5. Record Usage Immutably

Make spend auditable.

A useful usage record includes:

- provider and model
- request id, trace id, tenant/user/job id when available
- routing reason and any override reason
- input, output, cached, reasoning, and total tokens as supported by the provider
- estimated cost and billed cost as separate fields when both exist
- retry attempt number
- timestamp

Prefer append-only ledgers, immutable value objects, or database rows over hidden mutable totals. If the app needs a running total, derive it from records or update it transactionally with the new record.

## 6. Retry Only Recoverable Failures

Paid retries must be narrow.

Usually retry:

- network connection errors
- provider 429 rate limits
- provider 5xx errors
- retryable timeouts

Usually fail fast:

- authentication or permission errors
- invalid request, schema, or unsupported-parameter errors
- content policy failures
- deterministic parser or validator failures unless the retry changes prompt, model, or input
- budget exhausted errors

Use capped exponential backoff with jitter if the repo has a helper. Account for every paid attempt. Do not hide retry spend inside one final record.

## 7. Cache Only Stable Content

Use provider-native prompt caching or app-level result caching when correctness and privacy allow it.

Good candidates:

- long stable system prompts
- tool or schema instructions
- static retrieval context
- unchanged batch prefixes
- deterministic classification of unchanged inputs

Poor candidates:

- secrets, credentials, or private user data without clear isolation
- volatile retrieval context
- prompts affected by time, permissions, feature flags, or current account state
- outputs that must reflect fresh data

Define cache keys, TTL, invalidation, tenant/user isolation, and cached-token accounting. If the provider bills cache reads and writes differently, represent that in the cost policy.

## 8. Compose the Runtime Flow

The final code path should read like this:

1. Normalize task metadata.
2. Estimate tokens and complexity.
3. Select the cheapest adequate model from policy.
4. Preflight budget for the selected scope.
5. Build messages, including safe cached sections.
6. Call the provider through narrow retry logic.
7. Validate output.
8. Escalate, degrade, split, or stop according to policy.
9. Write usage and budget records.

Keep this flow discoverable. It can be split across helpers, but avoid burying model choice and budget enforcement in unrelated code.

## 9. Test the Expensive Edges

Use fake provider clients by default. Do not hit paid APIs in automated tests unless the repo already has explicit opt-in integration tests and budget controls.

Cover:

- simple input selects the cheap tier
- long, complex, or high-risk input selects a stronger tier
- forced model overrides still pass budget checks and are logged
- budget exceeded prevents the provider call
- retryable failures retry with a cap
- non-retryable failures do not retry
- prompt caching is applied only to stable content
- usage records distinguish estimated, cached, and billed tokens
- batch jobs chunk, degrade, or stop near budget exhaustion

If the user asked for a review, findings should call out any missing guardrail that could cause accidental spend.

## 10. Report the Result

End with:

- model tiers and routing thresholds added or changed
- budget scopes enforced
- retry taxonomy changed
- caching added or deliberately skipped
- telemetry or ledger fields added
- tests and validation run
- provider pricing or behavior assumptions that still need current-doc verification

If current provider pricing could not be verified, keep pricing configurable and say so.
