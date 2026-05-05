---
name: implementation-planning
description: Use this skill whenever the user asks to plan before coding, uses `/plan`, requests an implementation plan, wants requirements restated, needs risks assessed, has ambiguous requirements, or is starting a complex feature, architecture change, multi-file refactor, migration, or high-risk change. Trigger it even when the user only describes the work and does not explicitly say "plan". This skill must produce a concrete implementation plan and stop for explicit confirmation before modifying code.
metadata:
  short-description: Plan complex code changes before editing
---

# Implementation Planning

Use this skill to preserve the ECC `/plan` behavior in Codex: analyze first, write a useful implementation plan, and wait for explicit user confirmation before touching code.

## Confirmation Gate

When this skill is active, do not edit files, run write commands, or implement the feature until the user explicitly confirms with language such as "yes", "proceed", "implement", or a modified plan. If the user asks for a change to the plan, revise the plan and wait again.

Read-only exploration is allowed when it is needed to make the plan concrete.

## Workflow

1. Restate requirements in clear terms.
2. Surface assumptions, ambiguities, and any clarification questions that block a reliable plan.
3. Inspect the codebase for relevant patterns, entry points, tests, configuration, and similar implementations.
4. Break work into phases that can be implemented and verified incrementally.
5. Identify dependencies, risks, and mitigations.
6. Define testing and success criteria.
7. Present the plan and stop for confirmation.

## Plan Format

Use this structure:

```markdown
# Implementation Plan: [Feature Name]

## Requirements Restatement
- [What the user is asking for]

## Assumptions
- [Assumption or "None"]

## Architecture Changes
- [File/path/component]: [planned change]

## Implementation Phases
### Phase 1: [Name]
1. **[Step]** (`path/to/file`)
   - Action: [specific action]
   - Why: [reason]
   - Dependencies: [none or prior step]
   - Risk: [Low/Medium/High]
   - Verify: [test/check]

## Testing Strategy
- Unit:
- Integration:
- E2E/manual:

## Risks & Mitigations
- **Risk:** [description]
  - Mitigation: [response]

## Success Criteria
- [ ] [verifiable criterion]

**WAITING FOR CONFIRMATION:** Proceed with this plan? Reply "proceed", "modify: ...", or "different approach: ...".
```

## Follow-On Skills

After confirmation, use these Codex skills when the work requires them:

- `tdd-workflow` for test-first implementation.
- `build-fix` when build, typecheck, or compile failures appear.
- `code-review` when implementation is complete or when reviewing a PR.
- `prp-plan` for artifact-producing plans with deeper codebase analysis.
- `prp-implement` to execute an existing plan with validation loops.

## Parity Notes

The Claude command delegated to a `planner` agent. In Codex, the planner role is embedded directly in this skill so the workflow does not depend on a source-harness agent. Optional subagent delegation may be used only when the current runtime and user authorization allow it; the skill must still work inline.
