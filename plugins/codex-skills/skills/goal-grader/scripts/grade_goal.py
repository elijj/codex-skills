#!/usr/bin/env python3
"""Heuristic baseline grader for Codex /goal prompts."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Category:
    name: str
    cues: tuple[str, ...]
    weak_feedback: str
    strong_feedback: str


CATEGORIES = (
    Category(
        "Objective clarity",
        ("complete", "implement", "fix", "build", "create", "refactor", "diagnose", "optimize", "migrate", "write"),
        "Use one concrete verb and name the target repo, feature, or system.",
        "Objective uses concrete execution language.",
    ),
    Category(
        "Verifiable end state",
        ("done when", "acceptance", "pass", "passes", "green", "metric", "threshold", "report", "pr", "commit", "created"),
        "Add an observable done condition such as tests passing, a metric target, or a written artifact.",
        "Goal includes observable completion signals.",
    ),
    Category(
        "Scope boundaries",
        ("do not", "without", "only", "exclude", "out of scope", "avoid", "preserve", "leave unchanged"),
        "State boundaries and what not to change.",
        "Goal includes scope limits.",
    ),
    Category(
        "Deliverables",
        ("file", "files", "report", "plan", "summary", "commit", "pull request", "pr", "issue", "artifact", "config"),
        "Name expected artifacts or final outputs.",
        "Deliverables are named.",
    ),
    Category(
        "Validation loop",
        ("test", "typecheck", "lint", "build", "eval", "benchmark", "verify", "validate", "run"),
        "Name validation commands or checks to run after meaningful changes.",
        "Validation path is present.",
    ),
    Category(
        "Context and dependencies",
        ("repo", "path", "read", "docs", "issue", "ticket", "env", "credential", "input", "dataset", "branch"),
        "Point to required repo paths, docs, issues, inputs, or environment assumptions.",
        "Context and dependencies are discoverable.",
    ),
    Category(
        "Checkpoints",
        ("checkpoint", "phase", "progress", "after each", "log", "status", "iteration", "continue"),
        "Request progress checkpoints for long-running work.",
        "Checkpoint cadence is specified.",
    ),
    Category(
        "Stop and block rules",
        ("pause", "ask", "stop", "blocked", "escalate", "approval", "complete only", "external state"),
        "Define when to pause, ask, stop, or mark blocked.",
        "Stop/block behavior is explicit.",
    ),
    Category(
        "Safety and permissions",
        (
            "approval",
            "ask before",
            "pause before",
            "confirm before",
            "do not post",
            "do not deploy",
            "do not delete",
            "do not expose",
            "redact",
            "secrets",
            "credentials",
            "user data",
        ),
        "Add approval gates for secrets, destructive actions, deployments, external writes, and spend.",
        "Safety/permission language is present.",
    ),
    Category(
        "Autonomy fit",
        ("goal", "iterate", "until", "complete", "done when", "budget", "checkpoint", "validation"),
        "Make the task large enough for autonomous continuation but bounded by a clear finish line.",
        "Goal appears suitable for autonomous continuation.",
    ),
)


RISK_PATTERNS = (
    (
        r"(\b(delete|drop|truncate|wipe|reset|remove)\b.{0,50}\b(production|prod|user|users|customer|data|database|db|table|account|secret|credential|file|bucket)\b)|(\b(production|prod|user|users|customer|data|database|db|table|account|secret|credential|file|bucket)\b.{0,50}\b(delete|drop|truncate|wipe|reset|remove)\b)",
        "Destructive action needs explicit boundary and approval gate.",
    ),
    (r"\bdeploy|release|publish|post|message|email|tweet\b", "External side effect needs explicit approval gate."),
    (r"\bsecret|token|password|credential|api key\b", "Credential handling needs secrecy rules."),
    (r"\bpayment|purchase|buy|invoice|billing\b", "Spend or billing action needs explicit approval gate."),
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def cue_hit(text_lower: str, cue: str) -> bool:
    cue_lower = cue.lower()
    if re.fullmatch(r"[a-z0-9]+", cue_lower):
        return re.search(rf"\b{re.escape(cue_lower)}\b", text_lower) is not None
    return cue_lower in text_lower


def score_category(text_lower: str, category: Category) -> tuple[int, str]:
    hits = sum(1 for cue in category.cues if cue_hit(text_lower, cue))
    if hits >= 3:
        return 9, category.strong_feedback
    if hits == 2:
        return 8, category.strong_feedback
    if hits == 1:
        return 8, category.strong_feedback
    return 3, category.weak_feedback


def detect_blockers(text: str) -> list[str]:
    text_lower = text.lower()
    blockers: list[str] = []
    has_approval = any(term in text_lower for term in ("approval", "ask before", "pause before", "confirm before"))
    for pattern, message in RISK_PATTERNS:
        if re.search(pattern, text_lower) and not has_approval:
            blockers.append(message)
    if not any(term in text_lower for term in ("done when", "complete when", "acceptance", "pass", "passes", "threshold", "report")):
        blockers.append("No measurable done condition.")
    if len(text.split()) < 12:
        blockers.append("Goal too short to carry autonomous context.")
    return blockers


def grade(text: str) -> dict[str, object]:
    cleaned = normalize(text)
    text_lower = cleaned.lower()
    scorecard = []
    for category in CATEGORIES:
        score, feedback = score_category(text_lower, category)
        scorecard.append({"category": category.name, "score": score, "feedback": feedback})

    blockers = detect_blockers(cleaned)
    raw_score = round(sum(item["score"] for item in scorecard) / len(scorecard) * 10)
    penalty = min(20, 5 * len(blockers))
    score = max(0, raw_score - penalty)
    band = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 65 else "D" if score >= 50 else "F"

    fixes = [item["feedback"] for item in scorecard if item["score"] < 8][:3]
    if len(fixes) < 3:
        fixes.extend(blockers[: 3 - len(fixes)])

    return {
        "grade": band,
        "score": score,
        "blockers": blockers or ["None"],
        "scorecard": scorecard,
        "highest_impact_fixes": fixes or ["No high-impact fixes detected by baseline script."],
        "optimized_goal_template": make_rewrite_template(cleaned),
    }


def make_rewrite_template(text: str) -> str:
    body = text
    if body.lower().startswith("/goal"):
        body = body[5:].strip()
    return (
        "/goal Complete [specific objective] in [repo/path/system] without changing [boundaries]. "
        "First read [required context]. Work in checkpoints, keep a short progress log, and after each checkpoint "
        "run [validation]. Done when [verifiable end state]. Pause and ask before [risky action]. "
        f"Original intent: {body}"
    )


def to_markdown(result: dict[str, object]) -> str:
    lines = [f"Grade: {result['grade']} ({result['score']}/100)", "", "Blocking Issues:"]
    lines.extend(f"- {item}" for item in result["blockers"])
    lines.extend(["", "Scorecard:", "| Category | Score | Feedback |", "| --- | ---: | --- |"])
    for item in result["scorecard"]:
        lines.append(f"| {item['category']} | {item['score']} | {item['feedback']} |")
    lines.extend(["", "Highest-Impact Fixes:"])
    for index, fix in enumerate(result["highest_impact_fixes"], start=1):
        lines.append(f"{index}. {fix}")
    lines.extend(["", "Optimized /goal Template:", "```text", str(result["optimized_goal_template"]), "```"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade a Codex /goal prompt.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Goal prompt text.")
    source.add_argument("--file", type=Path, help="Path containing goal prompt text.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    args = parser.parse_args()

    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    result = grade(text)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(to_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
