#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$ROOT_DIR/plugins/codex-skills/skills"
VALIDATOR="$SKILLS_DIR/skill-creator/scripts/quick_validate.py"

converted_skills=(
  harness-skill-porting
  karpathy-guidelines
  refactor-cleaner
  warp-worktree-fix
  implementation-planning
  tdd-workflow
  build-fix
  code-review
  prp-plan
  prp-implement
  prp-pr
  prp-commit
  e2e-testing
  cost-aware-llm-pipeline
)

echo "== Skill structure =="
for skill_dir in "$SKILLS_DIR"/*; do
  [[ -d "$skill_dir" ]] || continue
  python3 "$VALIDATOR" "$skill_dir"
done

echo "== Eval JSON =="
while IFS= read -r -d '' json_file; do
  python3 -m json.tool "$json_file" >/dev/null
done < <(find "$SKILLS_DIR" -path '*/evals/*.json' -type f -print0)

echo "== Converted skill release checks =="
for skill in "${converted_skills[@]}"; do
  skill_dir="$SKILLS_DIR/$skill"
  [[ -f "$skill_dir/references/source-parity.md" ]] || {
    echo "Missing $skill/references/source-parity.md" >&2
    exit 1
  }
  [[ -f "$skill_dir/evals/evals.json" ]] || {
    echo "Missing $skill/evals/evals.json" >&2
    exit 1
  }
  [[ -f "$skill_dir/evals/trigger_eval_$skill.json" ]] || {
    echo "Missing $skill/evals/trigger_eval_$skill.json" >&2
    exit 1
  }
  python3 - "$skill" "$skill_dir/evals/evals.json" "$skill_dir/evals/trigger_eval_$skill.json" <<'PY'
import json
import sys

skill, task_eval_path, trigger_eval_path = sys.argv[1:4]
task_evals = json.load(open(task_eval_path))
trigger_evals = json.load(open(trigger_eval_path))

missing_assertions = [
    item.get("id")
    for item in task_evals.get("evals", [])
    if not item.get("assertions")
]
if missing_assertions:
    raise SystemExit(f"{skill}: task evals missing assertions: {missing_assertions}")

if len(trigger_evals) != 20:
    raise SystemExit(f"{skill}: expected 20 trigger evals, found {len(trigger_evals)}")

positive = sum(1 for item in trigger_evals if item.get("should_trigger") is True)
negative = sum(1 for item in trigger_evals if item.get("should_trigger") is False)
if positive != 10 or negative != 10:
    raise SystemExit(f"{skill}: expected 10 positive and 10 negative trigger evals, found {positive}/{negative}")

for index, item in enumerate(trigger_evals):
    if not isinstance(item.get("query"), str) or not item["query"].strip():
        raise SystemExit(f"{skill}: trigger eval {index} is missing a non-empty query")
    if not isinstance(item.get("should_trigger"), bool):
        raise SystemExit(f"{skill}: trigger eval {index} is missing boolean should_trigger")
PY
done

echo "All skill validation checks passed."
