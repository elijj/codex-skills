---
name: prp-plan
description: Use this skill when the user invokes `/prp-plan`, asks for a PRP, wants an artifact-producing implementation plan, provides a PRD or feature description that needs codebase analysis, pattern extraction, validation commands, acceptance criteria, and a self-contained plan file. Use this for deeper planning than conversational `/plan`, especially when `prp-implement` will execute the result later.
metadata:
  short-description: Create self-contained PRP implementation plans
---

# PRP Plan

Create a self-contained implementation plan artifact with enough context for a later implementation pass to execute without rediscovering basic patterns.

## Output Location

Write plans under:

```text
.codex/prps/plans/{kebab-case-feature}.plan.md
```

Use `.codex/prps/` instead of the source harness `.claude/PRPs/` path unless the target repo already standardizes on another location.

## Workflow

### Phase 0: Detect Input

- Path to `*.prd.md`: parse the PRD, find the next pending phase, and plan that phase.
- Path to another markdown/reference file: read it as context.
- Free-form text: treat as the feature request.
- Empty input: ask what feature to plan.

### Phase 1: Parse Requirements

Identify:

- What is being built.
- Why it matters.
- Who or what uses it.
- Where it fits in the codebase.
- Complexity: Small, Medium, Large, or XL.

If requirements are too ambiguous for a self-contained plan, ask targeted questions before writing the artifact.

### Phase 2: Explore Codebase

Use `rg`, file reads, and project config inspection to capture:

- Similar features and patterns.
- Relevant entry points, APIs, services, models, components, and tests.
- Naming, error handling, logging, repository, service, and test conventions.
- Validation commands available in package/config files.

Record file paths and key observations in the plan.

### Phase 3: Research External Docs

When the implementation depends on a library, framework, or external service whose APIs may have changed, use current official docs or the available documentation tools. Capture direct links and only the details needed for implementation.

### Phase 4: Design

Define:

- Problem -> solution.
- Files to change.
- Patterns to mirror.
- Tasks in dependency order.
- Testing strategy.
- Validation commands.
- Risks, acceptance criteria, and explicit non-goals.

### Phase 5: Generate Plan

Use this structure:

```markdown
# Plan: [Feature Name]

## Summary
## User Story
## Problem -> Solution
## Metadata
- Complexity:
- Source input:
- Created:

## Mandatory Reading
- `path`: why it matters

## External Documentation
- [name](url): why it matters

## Patterns to Mirror
### NAMING_CONVENTION
### ERROR_HANDLING
### LOGGING_PATTERN
### TEST_STRUCTURE

## Files to Change
| Path | Change | Reason |
| --- | --- | --- |

## NOT Building

## Step-by-Step Tasks
### Task 1: [Name]
- Files:
- Action:
- Dependencies:
- Verify:

## Testing Strategy
## Validation Commands
## Acceptance Criteria
## Risks
## Notes
```

## Final Response

Report:

- Plan path.
- Feature summary.
- Key risks.
- Next step: use `prp-implement <plan-path>` when ready.

## PRD Back-Reference

When the input was a PRD or PRD phase, update the PRD if it is safe to edit:

- Mark the planned phase as `planned` or add a note that a plan was created.
- Add a link or path to `.codex/prps/plans/{kebab-case-feature}.plan.md`.
- Preserve existing PRD formatting and do not rewrite unrelated sections.

If the PRD is read-only, outside the workspace, or ambiguous to update, do not guess. Report the exact back-reference snippet the user should add.
