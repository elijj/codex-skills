# Plan: Fix Empty Row Import

## Summary
Fix CSV import crash on empty rows.

## Files to Change
| Path | Change | Reason |
| --- | --- | --- |
| `src/import/csv.ts` | Skip empty rows safely | Prevent crash |
| `src/import/csv.test.ts` | Add empty-row test | RED/GREEN evidence |

## Step-by-Step Tasks
### Task 1: Add reproducer
- Files: `src/import/csv.test.ts`
- Action: Add test for empty CSV row.
- Verify: `npm test -- src/import/csv.test.ts`

### Task 2: Fix parser
- Files: `src/import/csv.ts`
- Action: Skip empty rows without dropping valid rows.
- Verify: `npm test -- src/import/csv.test.ts`

## Validation Commands
- `npm test -- src/import/csv.test.ts`

## Acceptance Criteria
- Empty rows do not crash import.
- Existing valid rows still import.
