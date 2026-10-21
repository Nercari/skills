# Review guide

## Hard stops
- Stop if a PR adds a secret or key to a skill or reference file.
- Stop on a push to main or a force-push. The HQ block in AGENTS.md forbids both.
- No other repo-specific rule is written in AGENTS.md. none known.

## Fragile files
- `metaprompter/scripts/validate_metaprompter.py`: it checks frontmatter, references, links and eval cases. A new reference file needs a link from `SKILL.md`.
- `metaprompter/evals/cases.json`: the validator reads it.
- `.claude/settings.json`, `.cursor/hooks/merge-gate.mjs`: the merge gate (commit b73b79b). Do not edit.

## Tests that must pass
- `python metaprompter/scripts/validate_metaprompter.py`: 29/29 checks passed (run).
- `python -m unittest tests.test_merge_gate -q`: OK (run).
