# Dependency Closure

Use this checklist when a source workflow references other commands, agents, hooks, rules, MCP servers, scripts, templates, memories, or follow-on workflows.

## Trace Order

1. Start with the user-provided source artifact.
2. List every referenced file, command, agent, hook, rule, MCP, script, template, and generated output path.
3. Follow each reference once. Stop when the dependency is either fully understood, clearly external, or project-local policy.
4. Classify each dependency:
   - Required runtime dependency: convert, embed, or replace with a deterministic Codex equivalent.
   - Follow-on workflow dependency: convert separately when the user asked for full workflow parity.
   - Optional alternative: document or convert only when omitting it would break the workflow.
   - Project-local policy: install in `AGENTS.md` or existing project docs instead of the reusable skill.
   - External unavailable service: mark `Out of scope` or `Emulated` with the required setup.
5. Add one parity-ledger row per dependency. Do not collapse commands, agents, hooks, and MCP assumptions into a generic note.

## Common Omissions

- Slash command argument parsing that should become an input contract.
- Claude subagent responsibilities that must become inline skill instructions when Codex child agents are unavailable.
- Hooks that provided enforcement and now need explicit verification steps or bundled scripts.
- Cursor/Cline/Roo ambient rules that will not trigger from a skill description alone.
- MCP servers, credentials, or local services that the target runtime may not have.
- Templates, scripts, and assets that outputs depend on.
- Follow-on command recommendations that would point users at missing source-harness files.

## Ledger Status

- `Direct`: Codex has a real equivalent surface and the behavior is preserved.
- `Emulated`: Codex lacks the source mechanism, but explicit instructions, scripts, evals, or repo-level guidance reproduce the behavior.
- `Out of scope`: The behavior needs unavailable credentials, private services, host automation, or runtime features. State exactly what would be needed for full parity.
