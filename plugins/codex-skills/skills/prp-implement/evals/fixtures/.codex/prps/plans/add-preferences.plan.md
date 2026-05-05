# Plan: Add Preferences

## Summary
Add notification preference storage.

## Metadata
- PRD: docs/notifications.prd.md#phase-1

## Files to Change
| Path | Change | Reason |
| --- | --- | --- |
| `src/preferences.ts` | Add preference model | Store user choices |

## Step-by-Step Tasks
### Task 1: Add model
- Files: `src/preferences.ts`
- Action: Add preference model.
- Verify: `npm test -- src/preferences.test.ts`

## Validation Commands
- `npm test -- src/preferences.test.ts`

## Acceptance Criteria
- Preferences can be read and saved.
