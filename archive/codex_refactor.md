# Cookbook Refactor Plan

This roadmap keeps refactors incremental so changes land in small, reviewable slices.
It follows `/AGENTS.md` expectations: clear structure, mirrored tests, and light automation via
`Makefile` and scripts. The repo is empty today, so early steps focus on scaffolding and stack
decisions.

---

## 1. Preflight & Baseline

- **1.1 Choose stack and scaffolding**
  - Pick the primary stack (Node/TS or Python) and apply indentation and naming rules from AGENTS.
  - Add minimal scaffolding only (e.g. `package.json`, `requirements.txt`, `.gitignore`, base
    `Makefile` skeleton) without feature code.

- **1.2 Map current structure**
  - Sketch existing or planned directories: `src/`, `recipes/`, `tests/`, `scripts/`, `docs/`.
  - Identify ad hoc scripts that should migrate into `scripts/`.
  - Note runtimes and any external tools you expect to use.

- **1.3 Capture behavior and constraints**
  - List key user flows and CLIs (what works today or is expected to work first).
  - Note performance hotspots, flaky areas, or modules that are risky to touch.
  - Record external integrations (APIs, databases, CLIs).

- **1.4 Establish a measurement baseline**
  - Capture current test status, coverage (if available), and basic performance notes.
  - Decide which metrics matter most: test pass rate, startup time, key command latencies.

**Outcome:** A short inventory doc (e.g. `docs/current-state.md`) with structure, stack, and pain
points.

---

## 2. Directory Layout and Module Boundaries

Align the repo to the directory conventions in AGENTS.

- **2.1 Normalize top level layout**
  - Ensure presence of:
    - `src/` for primary modules and any CLI or services.
    - `recipes/` for runnable examples with small READMEs.
    - `tests/` mirroring `src/`.
    - `scripts/` for automation and validation helpers.
    - `docs/` for guides and design notes.
    - `ai_docs/archive/change-notes.md` for change logging.

- **2.2 Introduce clear module layers under `src/`**
  - Organize by concern:
    - `src/core/` for pure domain logic with minimal dependencies.
    - `src/adapters/` for I/O, network, database, filesystem integrations.
    - `src/cli/` for command line interface and entrypoints.
    - `src/config/` for configuration loading and env handling.
  - Move existing code into the closest layer with no behavior changes at this stage.

- **2.3 Establish file naming and exports**
  - Convert files to kebab case.
  - Keep each module focused on a single concern with a small, explicit public surface.

**Outcome:** A layout that matches the conventions and makes future changes predictable.

---

## 3. Tooling, Makefile, and Environment

Add or refine tooling to support safe refactors.

- **3.1 Create or standardize `Makefile`**
  - Add targets:
    - `make setup` to install dependencies (`npm install` or `pip install -r requirements.txt`).
    - `make dev` to run local dev server or watch mode (set host and port per stack).
    - `make lint` to run formatting and linting.
    - `make test` to run the suite; support `COVERAGE=1 make test` when coverage is set up.

- **3.2 Linting and formatting**
  - For JS/TS:
    - Configure Prettier and ESLint with 2 space indentation and 100 char max line length.
  - For Python:
    - Configure Black and Ruff with 4 space indentation and 100 char max line length.
  - Add lint scripts in `package.json` or equivalent and wire them to `make lint`.

- **3.3 Environment configuration**
  - Add `.env.example` documenting all required env vars.
  - Centralize config loading (e.g. `src/config/env.ts` or `src/config/env.py`) rather than
    scattering env access.

**Outcome:** A standard tooling surface that makes running, linting, and testing the project simple.

---

## 4. Testing Strategy and Coverage

Shape the test layout to mirror the code and support incremental refactors.

- **4.1 Mirror `src/` under `tests/`**
  - Use structure like:
    - `tests/core/test_<module>.py` or `tests/core/<module>.spec.ts`.
    - `tests/cli/...` for CLI entrypoints.
  - Add at least one integration path per feature.

- **4.2 Strengthen the safety net**
  - Identify critical behaviors and write integration tests for end to end flows.
  - Add fixture data under `tests/fixtures/` and avoid network calls and nondeterministic I/O.
  - Add regression tests that encode known bugs or edge cases.

- **4.3 Standardize test tooling**
  - Confirm use of `pytest` (Python) or `vitest/jest` (JS/TS) and document it.
  - Ensure `make test` invokes the standard runner and supports coverage flags.

**Outcome:** A test suite that mirrors `src/` and provides confidence for deeper refactors.

---

## 5. Core Refactors (Incremental)

Perform behavior preserving refactors in small, verifiable steps.

- **5.1 Extract pure core logic**
  - Move domain logic from CLI or framework glue into `src/core/` as pure functions or small
    classes.
  - Apply naming conventions: classes in PascalCase, functions and variables in camelCase,
    constants in SCREAMING_SNAKE_CASE.

- **5.2 Untangle I/O from logic**
  - Isolate filesystem, network, and env access into `src/adapters/`.
  - Replace direct calls from core modules with injected dependencies or adapter interfaces.

- **5.3 Simplify modules**
  - Split large, multi purpose modules into smaller ones with a single responsibility.
  - Remove dead code and unused parameters only when covered by tests or clearly unused.

- **5.4 Improve error handling and boundaries**
  - Introduce domain specific error types where helpful.
  - Normalize error surfaces so CLI and APIs map errors to messages and exit codes consistently.

**Outcome:** Smaller modules with clean boundaries and less coupling.

---

## 6. CLI, Recipes, and Documentation

Polish user facing surfaces to be consistent and discoverable.

- **6.1 CLI refactor**
  - Centralize CLI entrypoints under `src/cli/`.
  - Keep each command a thin layer over `src/core/` logic.
  - Normalize argument parsing, help output, and exit codes.

- **6.2 Recipes and examples**
  - Move example scripts and usage snippets into `recipes/`.
  - For each recipe add a minimal `README.md` describing purpose, prerequisites, and how to run it.
  - Keep recipes small and focused, favoring copy and paste ready patterns.

- **6.3 Docs alignment**
  - Update root `README.md` with quick start (setup, dev, test, lint), stack overview, and links to
    key docs and `recipes/`.
  - Add focused guides in `docs/` (e.g. architecture overview, contributing guidelines).

**Outcome:** A consistent CLI surface, curated examples, and documentation that matches the
structure.

---

## 7. Automation and Validation Scripts

Encapsulate repeatable tasks in scripts aligned with repo conventions.

- **7.1 Script consolidation**
  - Move any ad hoc shell or Python helpers into `scripts/`.
  - Keep scripts idempotent and safe to run multiple times.

- **7.2 Static output checks (for web or static content)**
  - Wire `scripts/codex-validate-html.sh` and `scripts/codex-link-check.sh` into `make lint` or a
    dedicated target such as `make check-docs` when applicable.

- **7.3 Continuous integration hooks (if or when CI is added)**
  - Define a minimal CI matrix: `make setup`, `make lint`, `make test`.
  - Optionally run coverage with `COVERAGE=1 make test` on main branches.

**Outcome:** Automated validation that guards refactors from regressions.

---

## 8. Change Management and Logging

Track refactor progress and communicate clearly.

- **8.1 Change log discipline**
  - Create or maintain `ai_docs/archive/change-notes.md`.
  - For each notable refactor add a dated entry summarizing what changed and how it was validated.

- **8.2 Commit and PR hygiene**
  - Use `type(scope): summary` commit messages (e.g. `refactor(core): extract recipe loader`).
  - Keep refactor PRs small and focused; avoid mixing large behavior changes with structural moves.

- **8.3 Non goals and guardrails**
  - Avoid cross site edits or infra changes unless explicitly required.
  - Do not change secrets or deploy to production until a formal process exists.

**Outcome:** A transparent history of refactors with clear validation notes and limited risk.

---

## 9. Execution Strategy

Apply the refactor plan safely and incrementally.

- **9.1 Phase ordering**
  1. Preflight and baseline (Section 1).
  2. Directory and module layout (Section 2).
  3. Tooling and Makefile (Section 3).
  4. Testing and coverage improvements (Section 4).
  5. Core refactors and decoupling (Section 5).
  6. CLI, recipes, docs polish (Section 6).
  7. Automation and scripts (Section 7).
  8. Change logging and follow ups (Section 8).

- **9.2 Working mode**
  - For each phase define small, reviewable slices (for example, move only `src/cli`).
  - Run lint and tests locally after each slice.
  - Update `ai_docs/archive/change-notes.md` with what changed and how it was validated.

- **9.3 Acceptance**
  - Use `codex/templates/change-request.md` and `codex/templates/acceptance.md` to structure
    proposals and acceptance criteria for larger refactors.

**Final Outcome:** A `cookbook` codebase with clear structure, strong tests, predictable tooling,
and documentation that makes future refactors cheaper and safer.
