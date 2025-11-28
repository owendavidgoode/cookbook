# Repository Guidelines

This file sets expectations for contributors to `cookbook`. The repo is empty today; use these norms when adding code so early choices stay consistent.

## References
- Shared process: `/AGENTS.md`
- Local README: `cookbook/README.md` (keep quick start and stack notes here)
- Templates: `codex/templates/agents-template-simple.md`, `codex/templates/change-request.md`, `codex/templates/acceptance.md`
- Scripts: `scripts/codex-scaffold-agents.sh` (doc scaffolding), `scripts/codex-validate-html.sh` and `scripts/codex-link-check.sh` for static output checks

## Project Structure & Module Organization
- `src/` for primary modules/CLI; keep one concern per folder.
- `recipes/` for runnable examples/snippets with brief READMEs.
- `tests/` mirrors `src/` (`tests/<area>/test_<module>.py` or `<module>.spec.ts`).
- `scripts/` for repeatable automation; keep idempotent.
- `ai_docs/archive/change-notes.md` logs changes (create if missing); `docs/` for longer form guides.

## Build, Test, and Development Commands
- Preferred make targets (add to `Makefile` if absent):
  - `make setup` installs deps (wraps `npm install` or `pip install -r requirements.txt`).
  - `make dev` starts the local server/watch mode at `http://localhost:4173` (adjust in README).
  - `make lint` runs format/lint (Prettier/ESLint for JS, Ruff/Black for Python).
  - `make test` runs the full suite; use `COVERAGE=1 make test` to enforce coverage when available.

## Coding Style & Naming Conventions
- Indent: 2 spaces for JS/TS/JSON/YAML; 4 for Python.
- Files kebab-case; classes PascalCase; functions/vars camelCase; constants SCREAMING_SNAKE_CASE.
- Keep lines ≤100 chars; prefer pure functions and small modules; document env vars in `.env.example`.

## Testing Guidelines
- Mirror each module with a test file; include at least one integration path per feature.
- Use the stack’s native runner (e.g., `pytest` or `vitest`) under `make test`.
- For fixtures, prefer local data under `tests/fixtures/` and avoid network calls.
- Add regression tests for fixed bugs before merging.

## Commit & Pull Request Guidelines
- Commits: `type(scope): summary` (e.g., `feat(recipes): add pesto example`), one logical change per commit.
- PRs: short description, linked issue/TODO line, test results, and screenshots/CLI output when user-facing.
- Keep PRs small; update `ai_docs/archive/change-notes.md` with date, change summary, and validation.

## Safety, Deploy, and Definition of Done
- Stop conditions: no cross-site edits, no destructive git resets, no infra/secret changes, and no production deploys without explicit approval.
- Deploy: none configured; treat outputs as local-only until a release process is documented in README.
- Done when lint/test pass, local run is clean, docs (README + this file) match behavior, and change-notes capture what changed and how it was validated.
