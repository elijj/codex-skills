# Plan: Fix skill-creator trigger parser

## Summary
Fix the `skill-creator/scripts/run_eval.py` trigger-result parser so echoed prompt text or log noise cannot override the real classifier result. Add a regression test that proves the evaluator reads the actual model output instead of the full concatenated transcript.

## User Story
As a skill maintainer, I need trigger evaluations to reflect the model's real yes/no decision so description optimization does not drift or loop on parser artifacts.

## Problem -> Solution
`run_eval.py` currently concatenates the `-o` output artifact, `stdout`, and `stderr`, then scans the combined text for trigger markers. That makes the final decision vulnerable to echoed prompt text or later log lines that mention `{"trigger": ...}` after the real answer. The fix is to isolate result extraction so the dedicated output artifact is trusted first, with any fallback parsing constrained to model output only and never to unrelated diagnostics.

## Metadata
- Complexity: Medium
- Source input: code review finding from local diff
- Created: 2026-05-05

## Mandatory Reading
- `plugins/codex-skills/skills/skill-creator/scripts/run_eval.py`: current parsing flow and cleanup behavior.
- `plugins/codex-skills/skills/skill-creator/scripts/run_loop.py`: how `run_eval` feeds the optimize loop.
- `plugins/codex-skills/skills/skill-creator/scripts/improve_description.py`: related `codex exec` subprocess pattern.
- `plugins/codex-skills/skills/skill-creator/scripts/quick_validate.py`: existing validation style for skill-creator.
- `README.md`: repo-level validation and bundle guidance.

## External Documentation
- None required. This change uses the repo's existing Python and shell tooling.

## Patterns to Mirror
### NAMING_CONVENTION
Keep helper names close to the current script style: small, direct, function-level helpers in `run_eval.py`.

### ERROR_HANDLING
Preserve the existing `RuntimeError` / `ValueError` behavior and tempdir cleanup; make parser failures explicit instead of silently accepting ambiguous text.

### LOGGING_PATTERN
Keep diagnostic output on `stderr` and JSON results on the explicit output path, following the current script split.

### TEST_STRUCTURE
Use standard-library `unittest` with a focused regression test module under the `skill-creator/tests/` tree, since the repo does not currently define a Python test framework.

## Files to Change
| Path | Change | Reason |
| --- | --- | --- |
| `plugins/codex-skills/skills/skill-creator/scripts/run_eval.py` | Refactor trigger parsing so the real model output is authoritative and transcript noise cannot override it. | Fix the parser bug reported in review. |
| `plugins/codex-skills/skills/skill-creator/tests/test_run_eval.py` | Add regression coverage for echoed prompt/log noise and for the no-parse failure path. | Prevent the bug from returning. |
| `plugins/codex-skills/skills/skill-creator/tests/__init__.py` | Add only if needed for test discovery/imports. | Keep `unittest` discovery stable. |

## NOT Building
- Do not change the skill description text or trigger eval sets unless the parser fix exposes a genuine wording issue.
- Do not clean up the unrelated root-level nested worktree directories as part of this change.
- Do not rewrite the broader skill-creator loop or packaging logic.

## Step-by-Step Tasks
### Task 1: Isolate trigger extraction
- Files: `plugins/codex-skills/skills/skill-creator/scripts/run_eval.py`
- Action: Extract the trigger parse into a small helper that reads the dedicated output artifact first, then applies any fallback only to model output, not to echoed logs or `stderr`.
- Dependencies: none
- Verify: A synthetic transcript with a later echoed `{"trigger": false}` cannot override an earlier valid `{"trigger": true}` model response.

### Task 2: Add regression tests
- Files: `plugins/codex-skills/skills/skill-creator/tests/test_run_eval.py`
- Action: Mock the subprocess/output path so the test can feed the helper a valid result plus later diagnostic noise, and assert the parsed trigger stays correct; add a second case for a truly unparseable response.
- Dependencies: Task 1
- Verify: `python3 -m unittest discover -s plugins/codex-skills/skills/skill-creator/tests`

### Task 3: Run validation
- Files: none
- Action: Run the focused unit test, then the repo's skill validation script, then a syntax check on the touched Python file.
- Dependencies: Tasks 1-2
- Verify: `python3 -m py_compile plugins/codex-skills/skills/skill-creator/scripts/run_eval.py` and `bash scripts/validate-skills.sh`

## Testing Strategy
- Unit: parser regression tests around `run_eval.py`.
- Integration: none needed; the bug is confined to local parsing and subprocess result handling.
- E2E/manual: if the test harness is noisy, reproduce with a synthetic transcript before widening the fix.

## Validation Commands
- `python3 -m unittest discover -s plugins/codex-skills/skills/skill-creator/tests`
- `python3 -m py_compile plugins/codex-skills/skills/skill-creator/scripts/run_eval.py`
- `bash scripts/validate-skills.sh`

## Acceptance Criteria
- `run_eval.py` no longer lets echoed prompt text or later log lines override a valid trigger result.
- The parser still fails loudly when no valid trigger result can be recovered.
- Regression tests cover the false-positive parsing case and the failure path.
- Repo validation still passes after the change.

## Risks
- The Codex CLI output format may change again, so the parser should stay narrowly scoped to the explicit result artifact and explicit JSON-looking output.
- The current repo has no Python test runner config, so test discovery/import path setup may need one small support file.

## Notes
- The untracked nested worktree directories at the repo root are local workspace artifacts and are intentionally out of scope for this plan.
