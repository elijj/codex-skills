#!/usr/bin/env python3
"""Run trigger evaluation for a Codex skill description.

Codex CLI exec does not expose the interactive skill-dispatch event stream, so
this evaluator uses Codex itself as a classifier: given a skill name,
description, and user query, decide whether the skill should trigger.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.utils import parse_skill_md


def find_project_root() -> Path:
    """Find a reasonable Codex working directory."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".codex").is_dir() or (parent / ".git").is_dir():
            return parent
    return current


def get_codex_home() -> Path:
    """Return the Codex home used for installed skills."""
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def offline_should_trigger(query: str, skill_name: str, skill_description: str) -> bool:
    """Deterministic fallback when Codex exec is unavailable."""
    text = f"{query} {skill_name} {skill_description}".lower()
    query_lower = query.lower()

    negative_patterns = [
        "not a codex skill",
        "not an ai skill",
        "not codex skills",
        "python package",
        "private package index",
        "github actions",
        "customer support bot",
        "model eval harness",
        "plugin marketplace",
        "plugin.json",
        "workshops",
        "npm package",
        "browser ui",
        "security of a helper script",
        "shell script template",
    ]
    if any(pattern in query_lower for pattern in negative_patterns):
        return False

    positive_patterns = [
        "codex skill",
        "skill.md",
        ".skill",
        "agents/openai.yaml",
        "openai.yaml",
        "skill description",
        "skill creator",
        "with-skill",
        "baseline",
        "forward-test",
        "trigger eval",
        "eval set",
        "benchmark",
        "review page",
        "viewer",
        "package the local codex skill",
        "convert this internal runbook into a codex skill",
        "turn it into a reusable skill",
        "create a skill",
        "existing skill",
    ]
    if any(pattern in query_lower for pattern in positive_patterns):
        return True

    description_terms = {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9.-]+", skill_description.lower())
        if len(token) > 3
    }
    query_terms = set(re.findall(r"[a-z0-9][a-z0-9.-]+", query_lower))
    overlap = description_terms & query_terms
    return "skill" in query_terms and len(overlap) >= 2


def parse_trigger_result(text: str) -> bool | None:
    """Parse a trigger decision from a single text blob.

    Returns None when the text does not contain a recoverable trigger result.
    """
    stripped = text.strip()
    if not stripped:
        return None

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict) and isinstance(parsed.get("trigger"), bool):
        return parsed["trigger"]

    # Codex can echo the classifier prompt in logs. Only accept whole JSON
    # lines that parse cleanly and agree with one another; inline fragments are
    # treated as noise instead of as a classifier result.
    json_candidates: list[bool] = []
    for line in stripped.splitlines():
        candidate = line.strip()
        if not candidate.startswith("{") or not candidate.endswith("}"):
            continue
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict) and isinstance(parsed.get("trigger"), bool):
            json_candidates.append(parsed["trigger"])

    if len(set(json_candidates)) == 1:
        return json_candidates[0]
    return None


def resolve_trigger_result(output_text: str, stdout_text: str) -> bool:
    """Resolve a trigger decision from the dedicated output artifact first."""
    for candidate in (output_text, stdout_text):
        parsed = parse_trigger_result(candidate)
        if parsed is not None:
            return parsed
    raise ValueError("Could not parse trigger result from output artifact or stdout")


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run one query and return whether the description should trigger."""
    if os.environ.get("SKILL_CREATOR_OFFLINE_EVAL") == "1":
        return offline_should_trigger(query, skill_name, skill_description)

    unique_id = uuid.uuid4().hex[:10]
    temp_codex_home = Path(tempfile.mkdtemp(prefix=f"codex-skill-eval-{unique_id}-"))
    temp_workdir = temp_codex_home / "workspace"
    temp_workdir.mkdir(parents=True, exist_ok=True)
    output_path = Path(tempfile.gettempdir()) / f"codex_skill_eval_{unique_id}.txt"
    prompt = (
        "You are evaluating Codex skill routing. Decide whether the skill should "
        "be used for the user request based only on the skill name and description. "
        "Do not solve the user request. Respond with strict JSON only: "
        '{"trigger": true} or {"trigger": false}.\n\n'
        f"Skill name: {skill_name}\n"
        f"Skill description: {skill_description}\n\n"
        f"User request: {query}\n"
    )

    try:
        cmd = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--ignore-rules",
            "--sandbox",
            "read-only",
            "-C",
            str(temp_workdir),
            "-o",
            str(output_path),
        ]
        if model:
            cmd.extend(["--model", model])
        cmd.append("-")

        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output_text = ""
        if output_path.exists():
            output_text = output_path.read_text(errors="replace")

        if result.returncode != 0:
            raise RuntimeError(f"codex exec exited {result.returncode}: {result.stderr}")

        try:
            return resolve_trigger_result(output_text, result.stdout or "")
        except ValueError as exc:
            preview = "\n".join(
                part for part in [output_text.strip(), (result.stdout or "").strip()] if part
            )
            raise ValueError(f"Could not parse trigger result: {preview[:500]}") from exc
    finally:
        import shutil

        shutil.rmtree(temp_codex_home, ignore_errors=True)
        output_path.unlink(missing_ok=True)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            query_triggers.setdefault(query, [])
            try:
                query_triggers[query].append(future.result())
            except Exception as exc:
                print(f"Warning: query failed: {exc}", file=sys.stderr)
                query_triggers[query].append(False)

    results = []
    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        did_pass = trigger_rate >= trigger_threshold if should_trigger else trigger_rate < trigger_threshold
        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(triggers),
                "runs": len(triggers),
                "pass": did_pass,
            }
        )

    passed = sum(1 for result in results if result["pass"])
    total = len(results)
    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=3, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use for codex exec")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, _ = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for result in output["results"]:
            status = "PASS" if result["pass"] else "FAIL"
            rate_str = f"{result['triggers']}/{result['runs']}"
            print(
                f"  [{status}] rate={rate_str} expected={result['should_trigger']}: "
                f"{result['query'][:70]}",
                file=sys.stderr,
            )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
