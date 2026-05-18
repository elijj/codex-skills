#!/usr/bin/env python3
"""Run goal-grader evals and write skill-creator-style artifacts."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import time
from pathlib import Path

from grade_goal import grade_goal, to_markdown


def slug(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "eval"


def check_assertion(assertion: str, result: dict[str, object], markdown: str) -> tuple[bool, str]:
    score = int(result["score"])
    grade = str(result["grade"])
    lower = markdown.lower()
    assertion_lower = assertion.lower()

    if "letter grade and numeric score" in assertion_lower:
        passed = bool(re.search(r"Grade: [A-F] \(\d+/100\)", markdown))
        return passed, f"grade={grade}, score={score}"
    if "score is at least 85" in assertion_lower:
        return score >= 85, f"score={score}"
    if "score is below 65" in assertion_lower:
        return score < 65, f"score={score}"
    if "score is below 80" in assertion_lower:
        return score < 80, f"score={score}"
    if "score is below 50" in assertion_lower:
        return score < 50, f"score={score}"
    if "scorecard" in assertion_lower:
        passed = "scorecard:" in lower and "| category | score | feedback |" in lower
        return passed, "scorecard table present" if passed else "scorecard table missing"
    if "improved /goal rewrite" in assertion_lower:
        passed = "improved /goal:" in lower and "/goal " in lower
        return passed, "rewrite present" if passed else "rewrite missing"
    if "does not invent security blockers" in assertion_lower:
        blockers = result["blockers"]
        return blockers == [], f"blockers={blockers}"
    if "missing verifiable end state" in assertion_lower:
        passed = "verifiable end state" in lower or "done with concrete" in lower
        return passed, "end-state feedback present" if passed else "end-state feedback missing"
    if "missing validation" in assertion_lower:
        passed = "validation" in lower or "command" in lower or "eval" in lower
        return passed, "validation feedback present" if passed else "validation feedback missing"
    if "external social actions" in assertion_lower or "x automation" in assertion_lower:
        passed = "post" in lower and "follow" in lower and "approval" in lower
        return passed, "approval-gated social actions mentioned" if passed else "social approval gate missing"
    if "splitting into a first goal" in assertion_lower:
        passed = "split" in lower or "follow-up" in lower or "first goal" in lower
        return passed, "split/follow-up guidance present" if passed else "split guidance missing"
    if "password or credential" in assertion_lower:
        passed = "credential" in lower or "password" in lower
        return passed, "credential blocker present" if passed else "credential blocker missing"
    if "dms or private data" in assertion_lower:
        passed = "private data" in lower or "dm" in lower
        return passed, "private-data blocker present" if passed else "private-data blocker missing"
    if "forbids posting" in assertion_lower:
        passed = "do not" in lower and "post" in lower and "like" in lower and "follow" in lower and "approval" in lower
        return passed, "external-write prohibition present" if passed else "external-write prohibition missing"
    return False, f"No programmatic checker for assertion: {assertion}"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--iteration", required=True)
    args = parser.parse_args()

    evals = json.loads(args.evals.read_text(encoding="utf-8"))
    iteration_dir = args.workspace / f"iteration-{args.iteration}"
    iteration_dir.mkdir(parents=True, exist_ok=True)

    benchmark_rows: list[dict[str, object]] = []
    pass_rates: list[float] = []

    for item in evals["evals"]:
        eval_name = item.get("name") or f"eval-{item['id']}"
        run_dir = iteration_dir / f"eval-{item['id']}-{slug(eval_name)}" / "with_skill"
        output_dir = run_dir / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        start = time.perf_counter()
        result = grade_goal(item["prompt"])
        markdown = to_markdown(result)
        duration = time.perf_counter() - start

        (output_dir / "result.md").write_text(markdown, encoding="utf-8")
        write_json(output_dir / "result.json", result)
        write_json(
            run_dir.parent / "eval_metadata.json",
            {
                "eval_id": item["id"],
                "eval_name": eval_name,
                "prompt": item["prompt"],
                "assertions": item.get("assertions", []),
            },
        )
        write_json(
            run_dir / "timing.json",
            {
                "total_tokens": 0,
                "duration_ms": round(duration * 1000, 3),
                "total_duration_seconds": round(duration, 3),
            },
        )

        expectations = []
        for assertion in item.get("assertions", []):
            passed, evidence = check_assertion(assertion, result, markdown)
            expectations.append({"text": assertion, "passed": passed, "evidence": evidence})
        passed_count = sum(1 for expectation in expectations if expectation["passed"])
        total = len(expectations)
        pass_rate = passed_count / total if total else 0.0
        pass_rates.append(pass_rate)
        grading = {
            "expectations": expectations,
            "summary": {
                "passed": passed_count,
                "failed": total - passed_count,
                "total": total,
                "pass_rate": round(pass_rate, 3),
            },
            "timing": {
                "total_duration_seconds": round(duration, 3),
            },
        }
        write_json(run_dir / "grading.json", grading)
        benchmark_rows.append(
            {
                "eval_id": item["id"],
                "eval_name": eval_name,
                "configuration": "with_skill",
                "pass_rate": round(pass_rate, 3),
                "score": result["score"],
                "grade": result["grade"],
                "duration_seconds": round(duration, 3),
            }
        )

    mean_pass_rate = statistics.mean(pass_rates) if pass_rates else 0.0
    benchmark = {
        "skill_name": evals["skill_name"],
        "iteration": args.iteration,
        "summary": {
            "mean_pass_rate": round(mean_pass_rate, 3),
            "eval_count": len(evals["evals"]),
        },
        "runs": benchmark_rows,
    }
    write_json(iteration_dir / "benchmark.json", benchmark)
    lines = [
        f"# goal-grader iteration {args.iteration} benchmark",
        "",
        f"- Mean pass rate: {mean_pass_rate:.3f}",
        f"- Eval count: {len(evals['evals'])}",
        "",
        "| Eval | Grade | Score | Pass Rate |",
        "| --- | --- | ---: | ---: |",
    ]
    for row in benchmark_rows:
        lines.append(f"| {row['eval_name']} | {row['grade']} | {row['score']} | {row['pass_rate']} |")
    (iteration_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(benchmark["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

