#!/usr/bin/env python3
"""Deterministic helper for grading Codex /goal prompts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Criterion:
    key: str
    label: str
    description: str
    positive: tuple[str, ...]
    negative: tuple[str, ...] = ()
    required_for_full: int = 2


CRITERIA = (
    Criterion(
        "objective_clarity",
        "Objective clarity",
        "One concrete objective with a specific target.",
        ("complete", "implement", "migrate", "fix", "create", "build", "configure", "run", "start", "audit", "measure", "optimize", "grade"),
        ("help me", "make it better", "do whatever", "until it's good", "everything"),
        1,
    ),
    Criterion(
        "verifiable_end_state",
        "Verifiable end state",
        "Defines done in terms of tests, files, metrics, or observable results.",
        ("done when", "until", "success", "acceptance", "passes", "pass", "verified", "score", "target", "all tests", "metrics"),
        ("until it's good", "when it feels", "whatever"),
        1,
    ),
    Criterion(
        "scope_boundaries",
        "Scope boundaries",
        "Names boundaries, non-goals, or files/systems not to touch.",
        ("without changing", "do not", "don't", "only", "avoid", "no unrelated", "in scope", "out of scope", "non-goal"),
        (),
        1,
    ),
    Criterion(
        "deliverables",
        "Deliverables",
        "Names concrete artifacts expected from the run.",
        ("file", "files", "report", "notes", "plan", "pr", "pull request", "commit", "dashboard", "config", "docs/", ".md", ".json", "artifact"),
        (),
        1,
    ),
    Criterion(
        "validation_loop",
        "Validation loop",
        "Defines commands, evals, checks, or measurement cadence.",
        ("test", "tests", "npm test", "pytest", "eval", "benchmark", "lint", "typecheck", "verify", "after each", "run ", "measure"),
        (),
        1,
    ),
    Criterion(
        "context_dependencies",
        "Context and dependencies",
        "Points to required inputs, docs, paths, repos, accounts, or setup assumptions.",
        ("read ", "docs/", "http://", "https://", "github.com", "repo", "path", "account", "oauth", "docker", "env", "credentials", "issue"),
        (),
        1,
    ),
    Criterion(
        "checkpoints",
        "Checkpoints",
        "Asks for phased work, progress logs, or checkpoint verification.",
        ("checkpoint", "phase", "milestone", "progress log", "after each", "daily", "weekly", "step"),
        (),
        1,
    ),
    Criterion(
        "stop_rules",
        "Stop/block rules",
        "Says when to pause, ask, stop, or escalate.",
        ("pause", "ask", "stop", "blocked", "approval", "before changing", "before posting", "explicit approval", "escalate"),
        (),
        1,
    ),
    Criterion(
        "safety_permissions",
        "Safety and permissions",
        "Protects secrets, destructive actions, external writes, auth, or private data.",
        ("secret", "token", "password", "credential", "oauth", "approval", "do not post", "do not delete", "do not deploy", "private", "dm", "auth"),
        ("password", "scrape my dms", "auto-like", "auto like", "auto-follow", "auto follow", "post tweets every hour", "do whatever"),
        1,
    ),
    Criterion(
        "autonomy_fit",
        "Autonomy fit",
        "Bigger than one prompt but smaller than an open-ended backlog.",
        ("goal", "complete", "done when", "checkpoint", "stop", "until", "target"),
        ("do whatever", "everything", "forever", "until my account grows", "and grow fast"),
        1,
    ),
)


BLOCKER_PATTERNS = (
    ("Credential risk", r"\b(password|cookies?|session token|2fa|two[- ]factor)\b"),
    ("Private data risk", r"\b(dm|dms|direct messages|private messages|scrape my dms)\b"),
    ("Unapproved social automation", r"\b(auto[- ]?(like|follow|dm|post)|post tweets every hour|follow 500)\b"),
    ("Unbounded autonomy", r"\b(do whatever|until it's good|until my account grows|forever)\b"),
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def contains_any(text: str, needles: Iterable[str]) -> int:
    lower = text.lower()
    return sum(1 for needle in needles if needle in lower)


def score_criterion(text: str, criterion: Criterion) -> tuple[int, str]:
    positive_hits = contains_any(text, criterion.positive)
    negative_hits = contains_any(text, criterion.negative)

    if negative_hits and positive_hits == 0:
        score = 0
    elif negative_hits:
        score = max(2, min(6, positive_hits * 2))
    elif positive_hits >= criterion.required_for_full + 1:
        score = 10
    elif positive_hits >= criterion.required_for_full:
        score = 8
    elif positive_hits == 1:
        score = 6
    else:
        score = 2

    if score >= 8:
        feedback = "Strong signal present."
    elif score >= 6:
        feedback = "Partly specified; tighten wording."
    elif score >= 3:
        feedback = "Weak or implicit; make it explicit."
    else:
        feedback = "Missing or unsafe."
    return score, feedback


def grade_for(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 65:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def find_blockers(text: str) -> list[str]:
    blockers: list[str] = []
    lower = text.lower()
    for label, pattern in BLOCKER_PATTERNS:
        if re.search(pattern, lower):
            blockers.append(label)
    return blockers


def high_impact_fixes(rows: list[dict[str, object]], blockers: list[str], text: str) -> list[str]:
    fixes: list[str] = []
    risky_blockers = [blocker for blocker in blockers if blocker != "Unbounded autonomy"]
    if risky_blockers:
        fixes.append("Add explicit approval gates and replace unsafe credential/private-data handling with official authenticated APIs.")
    elif "Unbounded autonomy" in blockers:
        fixes.append("Add a concrete stopping condition and split broad work into setup, measurement, and follow-up execution goals.")
    low_rows = [row for row in rows if int(row["score"]) < 7]
    for row in low_rows[:4]:
        label = str(row["label"])
        if label == "Verifiable end state":
            fixes.append("Define done with concrete tests, metrics, artifacts, or a clear acceptance threshold.")
        elif label == "Validation loop":
            fixes.append("Name the command, eval, check, or measurement loop Codex should run after each checkpoint.")
        elif label == "Scope boundaries":
            fixes.append("Add explicit scope boundaries and unrelated-change limits.")
        elif label == "Stop/block rules":
            fixes.append("Say when Codex must pause and ask before continuing.")
        elif label == "Autonomy fit":
            fixes.append("Split unrelated objectives into a first goal and follow-up goals.")
        else:
            fixes.append(f"Make `{label}` explicit in the goal.")
    if " and " in text.lower() and contains_any(text, ("do whatever", "grow fast", "everything")):
        fixes.append("Reduce the goal to one durable objective; move growth, posting, and follow-up agent work into separate goals.")
    deduped: list[str] = []
    for fix in fixes:
        if fix not in deduped:
            deduped.append(fix)
    return deduped[:5] or ["Goal is close. Add one sharper completion check if you want extra reliability."]


def improved_goal(original: str, blockers: list[str], rows: list[dict[str, object]]) -> str:
    stripped = re.sub(r"^/goal\s*", "", normalize(original), flags=re.IGNORECASE)
    lower = stripped.lower()
    if "x" in lower and ("oauth" in lower or "account" in lower or "post" in lower or "follow" in lower):
        return (
            "/goal Safely set up the X-account measurement workflow without performing social actions. "
            "First verify official API/OAuth access, required scopes, Docker prerequisites, and the relevant repo/docs. "
            "Create a local report with baseline metrics available through approved APIs, unresolved access gaps, and a proposed follow-up Hermes/X growth goal. "
            "Do not request passwords, scrape private data, post, like, follow, DM, or change account settings without explicit approval. "
            "Done when the report path is returned, all setup checks are documented, and any blocked API permissions are listed."
        )
    if any("Credential" in blocker or "Private data" in blocker or "social" in blocker.lower() for blocker in blockers):
        return (
            "/goal Replace the unsafe automation request with an approved, read-only measurement plan using official APIs. "
            "Document required OAuth scopes, data boundaries, and manual approval gates. "
            "Do not use passwords, cookies, private DMs, scraping, posting, liking, following, or messaging. "
            "Done when the safe plan, required credentials list, and manual approval checklist are written to a local report."
        )
    if len(stripped) < 80 or "make my app better" in lower:
        return (
            "/goal Complete one named improvement in [repo/path] without unrelated changes. "
            "First inspect [files/docs/issues]. Work in checkpoints, keep a short progress log, and after each checkpoint run [validation command]. "
            "Done when [specific tests/metrics/artifacts] prove the improvement works. Pause and ask if the next step requires product scope decisions."
        )
    return (
        "/goal "
        + stripped
        + " Work in checkpoints, keep a short progress log, validate after each checkpoint, and pause before risky or out-of-scope changes."
    )


def grade_goal(text: str) -> dict[str, object]:
    text = normalize(text)
    rows: list[dict[str, object]] = []
    for criterion in CRITERIA:
        score, feedback = score_criterion(text, criterion)
        rows.append(
            {
                "key": criterion.key,
                "label": criterion.label,
                "score": score,
                "feedback": feedback,
            }
        )

    blockers = find_blockers(text)
    raw_score = round(sum(int(row["score"]) for row in rows) * 10 / len(rows))
    penalty = 0
    if "Unapproved social automation" in blockers:
        penalty += 15
    if "Credential risk" in blockers:
        penalty += 12
    if "Private data risk" in blockers:
        penalty += 12
    if "Unbounded autonomy" in blockers:
        penalty += 8
    score = max(0, raw_score - penalty)
    if blockers and score > 49:
        score = min(score, 49)
    return {
        "grade": grade_for(score),
        "score": score,
        "raw_score": raw_score,
        "penalty": penalty,
        "blockers": blockers,
        "scorecard": rows,
        "fixes": high_impact_fixes(rows, blockers, text),
        "improved_goal": improved_goal(text, blockers, rows),
    }


def to_markdown(result: dict[str, object]) -> str:
    blockers = result["blockers"] or ["None"]
    lines = [
        f"Grade: {result['grade']} ({result['score']}/100)",
        "",
        "Blocking Issues:",
    ]
    lines.extend(f"- {blocker}" for blocker in blockers)
    lines.extend(
        [
            "",
            "Scorecard:",
            "| Category | Score | Feedback |",
            "| --- | ---: | --- |",
        ]
    )
    for row in result["scorecard"]:
        lines.append(f"| {row['label']} | {row['score']}/10 | {row['feedback']} |")
    lines.extend(["", "Highest-Impact Fixes:"])
    for index, fix in enumerate(result["fixes"], start=1):
        lines.append(f"{index}. {fix}")
    lines.extend(["", "Improved /goal:", "```text", str(result["improved_goal"]), "```", "", "Notes:"])
    if result["penalty"]:
        lines.append(f"- Safety/autonomy penalties applied: {result['penalty']} points.")
    lines.append("- Grade based on whether the goal can run as a durable, verifiable Codex execution contract.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade a Codex /goal prompt.")
    parser.add_argument("--text", help="Goal text. If omitted, stdin is used.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    if not normalize(text):
        print("No goal text provided.", file=sys.stderr)
        return 2
    result = grade_goal(text)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(to_markdown(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
