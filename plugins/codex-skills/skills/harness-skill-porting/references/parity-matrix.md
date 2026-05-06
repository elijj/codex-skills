# Harness Feature Parity Matrix

Use this reference while converting source skills, commands, and agent workflows into Codex skills. Load only the sections relevant to the source artifacts you found.

## Claude Code To Codex

| Claude Code feature | Codex equivalent | Porting guidance |
| --- | --- | --- |
| `SKILL.md` frontmatter | Codex `SKILL.md` frontmatter | Preserve `name`; rewrite `description` to be trigger-oriented and Codex-specific. Keep unsupported metadata only if harmless. |
| Skill body instructions | Codex `SKILL.md` body | Rephrase tool and runtime assumptions for Codex. Keep workflow, examples, constraints, and output contract. |
| `.claude/commands/*.md` slash commands | Skill trigger description, workflow sections, optional project docs | Fold reusable command behavior into the skill. Preserve argument conventions as an input contract. Create command shims only for explicit compatibility needs. |
| `.claude/agents/*.md` subagents | Inline review guidance, `agents/*.md` reference guidance, or Codex subagents when authorized | Do not assume delegation is available. Convert the role into a checklist or optional delegated task. |
| Hooks | Verification steps, bundled scripts, test commands, project setup notes | Codex cannot guarantee the same hook enforcement. Preserve the behavior as an explicit check and script when possible. |
| `CLAUDE.md` project instructions | Repository `AGENTS.md` or skill reference | Keep project-specific policy in `AGENTS.md`; put reusable workflow behavior in the skill. |
| MCP server assumptions | Codex MCP tools or fallback instructions | Verify the MCP exists in the current runtime before relying on it. Add fallback behavior for missing MCP servers. |
| Memories | Skill instructions, project docs, or user memory when appropriate | Avoid copying personal memories into reusable skills unless the user explicitly wants that behavior generalized. |
| Plan mode / approvals | Codex planning updates and permission policy | Translate into explicit planning and verification steps. Do not instruct Codex to request approvals that the current runtime cannot support. |

## Cursor, Cline, Roo, Aider, And Rule Packs

| Source feature | Codex equivalent | Porting guidance |
| --- | --- | --- |
| `.cursorrules`, `.cursor/rules/*` | `AGENTS.md` for project policy or `SKILL.md` for reusable workflow | Separate coding standards from task workflows. Avoid putting broad always-on rules into a specialized skill. |
| Cline/Roo custom mode | Skill workflow plus optional reference file | Convert role identity into concrete steps, allowed tools, file boundaries, and output contract. |
| Aider conventions | Skill instructions and verification commands | Preserve edit/test/commit workflow, but remove Aider-only command syntax. |
| Prompt pack | Skill body with examples | Keep examples that demonstrate decisions. Remove roleplay boilerplate that does not affect outcomes. |
| Tool allowlist | Codex runtime assumptions and fallback notes | State required tools plainly. Do not claim a tool is available unless it is part of the current environment or the skill's compatibility requirements. |

## Parity Risk Levels

Use these labels in parity notes:

- **Low:** Direct text or workflow translation; behavior should carry over naturally.
- **Medium:** Requires Codex to remember an explicit checklist or run a bundled script because automatic source-harness enforcement is unavailable.
- **High:** Depends on unavailable tools, credentials, event hooks, long-lived background services, or strict command interception.

For high-risk rows, either ask the user before accepting reduced parity or include a limitation with a concrete next step.

## Conversion Patterns

### Slash command to skill trigger

Source:

```markdown
/release-notes --from v1.2 --to v1.3
```

Codex conversion:

- Add trigger phrases such as "generate release notes", "port `/release-notes`", and "from tag to tag" to the skill description.
- Add an input contract section describing `from` and `to` refs.
- Add a workflow that runs `git log`, groups changes, and writes the requested output.

### Hook to verification script

Source:

```json
{"event": "PreCommit", "command": "npm run secret-scan"}
```

Codex conversion:

- Bundle or reference the secret scan command.
- Add a "Before commit" verification step.
- Report the command result in the final response.
- Document that Codex does not install an automatic blocking hook unless the user asks for repository hook setup.

### Subagent to optional review pass

Source:

```markdown
Use security-reviewer after edits.
```

Codex conversion:

- Add a security review checklist to the skill.
- If the current Codex runtime and user authorization allow subagents, delegate a bounded review task.
- Otherwise, run the checklist inline and report residual risk.

