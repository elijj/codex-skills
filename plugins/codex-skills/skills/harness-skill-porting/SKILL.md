---
name: harness-skill-porting
description: Use this skill only when the user wants to convert, migrate, port, translate, adapt, or get parity for a skill, prompt, command, agent, hook, rule, MCP config, or workflow from another agent harness into a Codex skill. This applies to Claude Code skills and slash commands, Cursor/Cline/Roo/Aider rules, prompt packs, and AGENTS/CLAUDE instructions. Trigger for phrases like "make this work in Codex", "full parity", "convert this skill", or "bring over this Claude workflow". Do not use for native Codex planning, PRP, TDD, build-fix, code review, PR, commit, E2E, packaging, or docs tasks unless the user is porting them from another harness.
metadata:
  short-description: Convert other harness workflows into Codex skills
---

# Harness Skill Porting

## Overview

Use this skill to convert workflows from another AI coding harness into a Codex-native skill without losing behavior that came from harness-specific features. The goal is not a literal file translation; it is operational parity: Codex should know when to trigger the skill, what context to inspect, which tools to use, what outputs to produce, and how to compensate for features Codex does not share with the source harness.

Start by identifying the source harness and reading the source artifacts. If the user pasted a source skill or workflow in the conversation, treat that as the source of truth; otherwise search the provided path or repo for files like `SKILL.md`, `CLAUDE.md`, `.claude/commands/*`, `.claude/agents/*`, hooks, rules, MCP configs, and bundled scripts.

## Porting Workflow

### 1. Inventory the source behavior

Create a concise source inventory before writing the Codex skill:

- **Trigger surface:** how the source workflow is invoked, including skill descriptions, slash commands, prompt phrases, file types, and repo contexts.
- **Required inputs:** files, URLs, user answers, environment variables, credentials, local services, or MCP servers.
- **Behavioral steps:** the actual workflow, decision points, validations, retries, review loops, and expected stopping conditions.
- **Harness features:** agents, hooks, slash commands, memories, plan modes, approval modes, MCP tools, browser tools, sandboxes, or background tasks.
- **Bundled resources:** scripts, templates, assets, examples, reference docs, tests, and generated artifacts.
- **Output contract:** final response shape, files to create, metadata to preserve, package format, and verification evidence.

If the source mixes reusable behavior with one project's local policy, separate them. Put general reusable behavior in the skill and keep project-specific rules in the target repository's `AGENTS.md` or existing docs.

When a source artifact references other commands, agents, skills, hooks, or rules, trace the dependency closure before deciding scope. Classify each reference as:

- **Required runtime dependency:** the source workflow cannot run without it. Convert or embed it.
- **Follow-on workflow dependency:** the source tells users to use it next. Convert it as a separate skill when the user asked for full workflow parity.
- **Optional alternative:** the source mentions it as a deeper or adjacent path. Convert only if full parity would otherwise leave a broken reference.
- **Project-local policy:** keep in `AGENTS.md` or existing project docs rather than a reusable skill.

For a deeper dependency tracing checklist, read `references/dependency-closure.md`.

For ambient behavior from source harnesses, such as Cursor `alwaysApply` rules or Claude project guidance, note that a Codex skill is trigger-based. Preserve the behavior with strong trigger phrasing and, when true always-on behavior is required, recommend placing a compact version in the target repo's `AGENTS.md`.

When ambient behavior is required for parity, do one of these:

- Add or update a repo-level `AGENTS.md` section when the user has asked you to install the behavior into a specific repository.
- Otherwise, include an exact `AGENTS.md` snippet in the final response and mark the ledger row as `Emulated` with the note `manual repo-level install required`.

For examples of converting always-on source behavior, read `references/ambient-behavior.md`.

### 2. Build a parity ledger

Use a parity ledger to avoid silently dropping source-harness behavior:

```markdown
| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| Claude slash command `/foo` | `SKILL.md` description and input contract | Direct | Low | Slash invocation becomes trigger wording plus normal user prompt handling. |
| Claude hook before commit | `SKILL.md` verification checklist or bundled script | Emulated | Medium | Codex cannot enforce the hook automatically; run the check before commit. |
```

For common feature mappings, read `references/parity-matrix.md`. Load only the relevant sections for the source harness and features you found.

Classify each row:

- **Direct:** Codex has an equivalent surface, such as a skill body, `agents/openai.yaml`, bundled resources, project `AGENTS.md`, or MCP tool.
- **Emulated:** Codex lacks the exact feature, but the behavior can be reproduced through explicit instructions, scripts, evals, or a review checklist.
- **Out of scope:** the behavior depends on unavailable runtime capabilities, credentials, private services, or host-specific automation. Preserve the requirement in a limitation note and ask before omitting it.

### 3. Design the Codex-native shape

Choose the smallest set of Codex surfaces that preserves behavior:

- `SKILL.md`: trigger description, workflow, decision rules, verification, and output contract.
- `agents/openai.yaml`: display metadata only; do not put trigger logic here.
- `references/`: longer conversion notes, source-specific mappings, examples, schemas, or policies loaded on demand.
- `scripts/`: deterministic checks, converters, package builders, or repeated mechanical steps that should not be reimplemented by the model every run.
- `assets/`: templates, images, boilerplate, fixtures, or other files to copy into outputs.
- `evals/`: realistic prompts that prove the converted skill triggers and preserves source behavior.

Do not create `commands/` shims unless the target project explicitly needs compatibility with a command surface. Codex skills should be the canonical workflow surface.

When a source command delegates to an agent, prefer embedding the agent's reusable behavior into the target skill unless the agent has enough standalone value to become its own skill. Do not leave a Codex skill depending on a source-harness agent file that will not exist for the user.

### 4. Rewrite for Codex behavior

When drafting the target `SKILL.md`:

- Put all trigger guidance in the frontmatter `description`; Codex decides whether to load a skill from name plus description.
- Write instructions for a Codex coding agent that shares a filesystem with the user. Avoid source-harness terms unless they are part of the input being converted.
- Replace source-only control flow with Codex-operable steps. For example, turn a hook into a verification step, a slash command into trigger phrasing and an input contract, and a source subagent into either inline review guidance or a Codex multi-agent note only when the runtime permits delegation.
- Preserve why each step exists. Parity is more reliable when the model understands the failure mode a step prevents.
- Keep the body under about 500 lines. Move large compatibility tables, examples, schemas, and source-specific details into references.
- Include explicit fallback behavior for headless environments, missing tools, unavailable MCP servers, and absent source files.

Avoid promising automatic enforcement for capabilities Codex cannot enforce. Say "run this check before committing" or "verify this condition" rather than implying an unavailable hook will block the action.

### 5. Preserve resources and tests

Port bundled resources deliberately:

- Copy deterministic scripts when they still apply; patch paths and assumptions for the Codex skill directory.
- Convert source-specific config examples into references unless Codex will execute them directly.
- Keep templates and assets intact when licensing allows it.
- Add or adapt eval prompts that represent the source workflow's core promises. Include at least one eval for a harness-specific feature that required emulation.

For each converted skill, create `evals/evals.json` with realistic prompts and expected outputs. If the source had tests, map them to Codex-friendly checks rather than dropping them.

### 6. Validate and report parity

Before handing off a converted skill:

1. Run the skill validator if available, usually:
   ```bash
   python3 <skill-creator>/scripts/quick_validate.py <converted-skill-path>
   ```
2. Inspect the final diff and confirm no source secrets or private credentials were copied.
3. Check that every parity-ledger row is direct, emulated, or explicitly documented as a limitation.
4. Report the created or changed files, verification commands, and any remaining parity gaps.

## Output Format

When the user asks you to port a skill, finish with:

```markdown
Converted `<source-name>` to `<target-skill-name>`.

Changed files:
- <path>

Parity ledger:
| Source feature/dependency | Target surface/file | Status | Risk | Note |
| --- | --- | --- | --- | --- |
| <source behavior> | <target path or Codex surface> | Direct/Emulated/Out of scope | Low/Medium/High | <note> |

Verification:
- <command>: <result>
```

If you cannot verify full parity, say exactly which source feature is not covered and what would be needed to cover it.

## Review Checklist

Use this checklist before finalizing:

- The target skill's `description` names the source contexts and real user phrases that should trigger it.
- The skill body explains the workflow and fallback behavior without relying on unsupported source harness mechanics.
- Every source command, agent, hook, memory, tool, resource, and output expectation has a parity-ledger decision.
- Ambient or always-on source behavior has either a repo-level `AGENTS.md` update or an exact snippet marked as requiring manual repo-level install.
- Scripts and assets are copied only when needed and safe to redistribute.
- Tests or eval prompts cover the core workflow and at least one emulated feature.
- Validation passes, or failures are explained with next steps.
