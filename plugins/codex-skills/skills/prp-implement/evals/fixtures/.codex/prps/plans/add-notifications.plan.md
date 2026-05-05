# Plan: Add Notifications

## Summary
Add in-app notification delivery when watched markets resolve.

## Mandatory Reading
- `src/markets/resolution.ts`
- `src/notifications/store.ts`

## Files to Change
| Path | Change | Reason |
| --- | --- | --- |
| `src/notifications/store.ts` | Add notification persistence helper | Existing notification pattern |
| `src/markets/resolution.ts` | Enqueue notification on resolution | Hook into resolution flow |
| `src/notifications/store.test.ts` | Cover persisted notification | RED/GREEN evidence |

## Step-by-Step Tasks
### Task 1: Add notification persistence test
- Files: `src/notifications/store.test.ts`
- Verify: `npm test -- src/notifications/store.test.ts`

### Task 2: Persist notification from resolution path
- Files: `src/notifications/store.ts`, `src/markets/resolution.ts`
- Verify: `npm test -- src/notifications/store.test.ts`

## Validation Commands
- `npm test -- src/notifications/store.test.ts`
- `npm run typecheck`

## Acceptance Criteria
- Watched market resolution creates one in-app notification.
- Typecheck passes.
