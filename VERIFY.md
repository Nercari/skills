# VERIFY

This file is the merge evidence for this repo. Generate the real steps with `create-verification-skill` and keep them current with `maintain-verification-skill`. Paste the real command output in the PR body. Update this file in the same PR when behavior changes.

## Commands

- (fill in: build, tests, and how to run the app like a user)

## Essential check

GREEN for a merge. Runs the metaprompter structure validator: frontmatter, references, links, eval cases. Offline.

```bash
python3 metaprompter/scripts/validate_metaprompter.py
python -m unittest tests.test_merge_gate -q
```
