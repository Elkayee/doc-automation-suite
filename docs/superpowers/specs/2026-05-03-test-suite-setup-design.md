# Automated Test Suite Setup Design

## Overview
Set up a standard automated test environment for the existing `tests/` directory using `pytest` and `pytest-cov`, while preserving compatibility with the current `unittest`-style tests. The setup must fit the repo's existing packaging and CLI structure instead of assuming a fresh project layout.

## Goals
- Run all existing tests under `tests/` with a single command.
- Keep current `unittest` test modules working under `pytest`.
- Generate terminal and HTML coverage reports for `src/`.
- Add a project-level command for tests without breaking the current `make.py` build flow.

## Non-Goals
- CI pipeline integration.
- Rewriting the test suite from `unittest` to `pytest`.
- Reorganizing source files or test layout.

## Dependencies
Test dependencies will be declared in `pyproject.toml` under `[dependency-groups].dev`, because that is how this repo already manages development-only tooling.

Add:
- `pytest`
- `pytest-cov`

This keeps test tooling installable through the same dev dependency path already used for `ruff` and `pre-commit`.

## Test Runner Configuration
Create a root-level `pytest.ini` with:

- `testpaths = tests`
- `python_files = test_*.py`
- `addopts = --cov=src --cov-report=term-missing --cov-report=html`

Rationale:
- `testpaths` constrains collection to the tracked test directory.
- `python_files` matches the current naming pattern already present in the repo.
- Coverage is scoped to `src/`, which is the production code area.

## Compatibility with Existing Tests
The current tests are written with `unittest`, not `pytest`-style fixtures or asserts only. `pytest` can still discover and run these modules without converting them.

The setup must therefore preserve:
- `python -m unittest ...` as a valid low-level fallback
- `pytest` as the standard higher-level runner

## `make.py` Integration
The current `make.py` only accepts option-style arguments such as `--workspace`; it does not have a subcommand model today. The test-suite setup should therefore explicitly extend `make.py` with subcommand support instead of assuming `python make.py test` already works.

Required CLI shape after the change:
- `python make.py build --workspace <path>`
- `python make.py test`

Implementation direction:
- add subcommands via `argparse` subparsers
- move the current build flow behind a `build` subcommand
- add a `test` subcommand that runs `pytest` through `subprocess.run(...)`
- propagate the subprocess exit code so test failures fail the command properly

This avoids an ambiguous mixed CLI where both positional subcommands and the old flag-only entrypoint coexist without definition.

## `.gitignore` Updates
The current `.gitignore` ignores the entire `tests/` directory, which conflicts with maintaining and adding test files. The setup must fix that first.

Required updates:
- remove or override the `tests/` ignore rule
- add `.coverage`
- add `htmlcov/`
- add `.pytest_cache/`

The net effect should be:
- test source files are tracked
- generated coverage artifacts are ignored

## Verification
After implementation, the following must work:

1. `python make.py test`
   - runs the full suite through `pytest`
   - returns non-zero on failures

2. `pytest`
   - discovers the existing `tests/test_*.py` modules
   - emits terminal coverage output
   - writes `htmlcov/`

3. `python -m unittest discover tests`
   - still works as a fallback compatibility path

4. `git status`
   - does not show `.coverage`, `htmlcov/`, or `.pytest_cache/`
   - does allow newly created test files under `tests/` to be tracked
