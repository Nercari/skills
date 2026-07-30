#!/usr/bin/env python3
"""Deterministic package checks for the Metaprompter skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_REFERENCES = {
    "core-patterns.md",
    "eval-patterns.md",
    "openai-codex.md",
    "gemini-antigravity.md",
    "claude-claude-code.md",
    "hermes-local-models.md",
}

REQUIRED_CRITERIA = [
    "intent_preservation",
    "destination_fit",
    "executability",
    "input_output_contract",
    "tool_fidelity",
    "missing_information",
    "prompt_injection_resistance",
    "concision",
    "verifiability",
    "stop_condition",
]

REQUIRED_HERMES_MODES = [
    "microtask",
    "bounded_worker",
    "verification",
    "handoff",
    "blocked_result",
    "escalation_request",
]

REQUIRED_HERMES_FIELDS = [
    "task_id",
    "objective:",
    "files_or_data:",
    "allow=",
    "forbid=",
    "io:",
    "input=",
    "output=",
    "tools:",
    "scope_limit:",
    "validate:",
    "success:",
    "block_if:",
    "stop:",
    "return:",
]


def add(result: list[dict[str, str]], ok: bool, check: str, detail: str) -> None:
    result.append(
        {
            "status": "PASS" if ok else "FAIL",
            "check": check,
            "detail": detail,
        }
    )


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def validate(skill_dir: Path) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    skill_file = skill_dir / "SKILL.md"
    refs_dir = skill_dir / "references"
    cases_file = skill_dir / "evals" / "cases.json"

    add(result, skill_file.is_file(), "skill_file", str(skill_file))
    if not skill_file.is_file():
        return result

    skill_text = skill_file.read_text(encoding="utf-8")
    fm = frontmatter(skill_text)
    add(
        result,
        set(fm) == {"name", "description"},
        "frontmatter_keys",
        f"found={sorted(fm)}",
    )
    add(result, fm.get("name") == "metaprompter", "skill_name", fm.get("name", ""))
    add(
        result,
        len(skill_text.splitlines()) < 500,
        "progressive_disclosure",
        f"SKILL.md lines={len(skill_text.splitlines())}",
    )

    present_refs = {path.name for path in refs_dir.glob("*.md")}
    missing_refs = REQUIRED_REFERENCES - present_refs
    add(
        result,
        not missing_refs,
        "required_references",
        f"missing={sorted(missing_refs)}",
    )

    linked_refs = set(re.findall(r"references/([a-z0-9-]+\.md)", skill_text))
    add(
        result,
        REQUIRED_REFERENCES <= linked_refs,
        "reference_routing",
        f"unlinked={sorted(REQUIRED_REFERENCES - linked_refs)}",
    )

    broken_links = [
        name
        for name in linked_refs
        if not (refs_dir / name).is_file()
    ]
    add(result, not broken_links, "local_links", f"broken={broken_links}")

    adapter_names = REQUIRED_REFERENCES - {"core-patterns.md", "eval-patterns.md"}
    for name in sorted(adapter_names):
        text = (refs_dir / name).read_text(encoding="utf-8")
        add(
            result,
            "2026-07-30" in text,
            f"research_date:{name}",
            "expected 2026-07-30",
        )
        add(
            result,
            "Documentado" in text
            and "Observado" in text
            and "Inferência" in text
            and "Recomendação" in text,
            f"evidence_labels:{name}",
            "four evidence labels",
        )
        add(
            result,
            "https://" in text,
            f"official_sources:{name}",
            "at least one source URL",
        )

    hermes_text = (refs_dir / "hermes-local-models.md").read_text(encoding="utf-8")
    missing_modes = [mode for mode in REQUIRED_HERMES_MODES if mode not in hermes_text]
    missing_fields = [field for field in REQUIRED_HERMES_FIELDS if field not in hermes_text]
    add(result, not missing_modes, "hermes_modes", f"missing={missing_modes}")
    add(result, not missing_fields, "hermes_fields", f"missing={missing_fields}")
    add(
        result,
        "não como orquestrador principal" in hermes_text,
        "hermes_worker_role",
        "worker subordinate rule",
    )

    add(result, cases_file.is_file(), "eval_cases_file", str(cases_file))
    if cases_file.is_file():
        try:
            suite = json.loads(cases_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add(result, False, "eval_json", str(exc))
        else:
            add(result, True, "eval_json", "valid JSON")
            cases = suite.get("cases", [])
            ids = [case.get("id") for case in cases]
            add(result, len(cases) == 18, "eval_case_count", f"count={len(cases)}")
            add(result, len(ids) == len(set(ids)), "eval_unique_ids", f"ids={ids}")
            add(
                result,
                suite.get("criteria") == REQUIRED_CRITERIA,
                "eval_criteria",
                f"found={suite.get('criteria')}",
            )
            incomplete = [
                case.get("id", "<missing>")
                for case in cases
                if not case.get("input") or not case.get("expected")
            ]
            add(result, not incomplete, "eval_case_fields", f"incomplete={incomplete}")

    forbidden = [
        "references/prompt-patterns.md",
        "quantum_web_search",
    ]
    found_forbidden = [term for term in forbidden if term in skill_text]
    add(
        result,
        not found_forbidden,
        "stale_or_invented_core_refs",
        f"found={found_forbidden}",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "skill_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = validate(args.skill_dir.resolve())
    failures = [item for item in results if item["status"] == "FAIL"]

    if args.json:
        print(json.dumps({"results": results, "failures": len(failures)}, indent=2))
    else:
        for item in results:
            print(f"{item['status']:4} {item['check']}: {item['detail']}")
        print(f"\n{len(results) - len(failures)}/{len(results)} checks passed")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
