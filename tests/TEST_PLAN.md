# todo.ai Test Strategy

## Purpose
- Establish a repeatable, automated test framework that validates every behaviour exposed by `todo.ai`
- Catch regressions quickly while supporting rapid iteration by AI agents and humans alike
- Provide guidance for contributors on how to extend coverage when new commands or options are introduced

## Scope Overview
- **System under test:** `todo.ai` zsh CLI (task lifecycle management, logging, formatting helpers)
- **Primary artifacts:** `TODO.md`, `.todo.ai/.todo.ai.serial`, `.todo.ai/.todo.ai.log`, backup archives
- **Out of scope (initially):** network connectivity to GitHub, integration with external scripts consuming TODO metadata

## Guiding Principles
- Prefer black-box validation through the CLI, but expose critical functions for white-box checks where isolation is valuable
- Tests must be deterministic, hermetic, and executable without network access
- Every test runs in a temporary workspace; never mutate the developer's real `TODO.md`
- Maintain compatibility with POSIX shells while leveraging zsh-specific features where unavoidable

## Test Architecture
- **Runner:** Adopt [ShellSpec](https://shellspec.info/) as the primary framework
  - Works with any POSIX shell, including zsh
  - Rich assertion language, hooks, and coverage reporting
  - Easy to invoke via `bundle exec shellspec` or `shellspec` binary from CI
- **Layout:**
  - `tests/spec/` → ShellSpec examples grouped by feature (`commands/`, `infrastructure/`, `formatting/`)
  - `tests/fixtures/` → canned `TODO.md` and `.todo.ai/*` seeds for scenario setup
  - `tests/helpers/` → reusable zsh helpers (e.g., sandbox creation, assertion extensions)
  - `tests/run.zsh` → convenience runner (wrapper around ShellSpec with environment preparation)
- **Shell isolation:** run each example within a disposable temp directory created by helper `create_sandbox`, exporting `TODO_FILE`, `TODO_SERIAL`, and `TODO_LOG` to point inside the sandbox

## Environment & Tooling Requirements
- Install `zsh` (already required by `todo.ai`)
- Install ShellSpec (per-project `bundle` or dedicated script that curls the binary release)
- Use `direnv`/`make` optional wrappers to simplify local execution (`make test`, `make test-watch`)
- Guarantee CI availability (GitHub Actions workflow `ci/tests.yml` running `shellspec` on Ubuntu latest with `zsh`)

## Test Fixture Strategy
- Provide baseline fixture representing a freshly initialized repo (`fixtures/empty_repo/`)
- Supply fixtures for complex states:
  - populated tasks with subtasks and metadata (notes, relationships, repository tags)
  - deleted section containing expiring tasks
  - log file populated with historical entries
  - serial file near integer rollover boundary
- Wrap fixture loading in helper `setup_fixture <name>` that copies contents into sandbox prior to test execution

## Coverage Matrix

| Area | Key behaviours | Notes |
| --- | --- | --- |
| Initialization | `init_todo_file`, `init_log_file`, `init_cursor_rules` create expected structure, idempotence | Validate header/footer, repo detection, last updated timestamp formatting |
| Serial management | `increment_serial`, `get_current_serial`, conflict resolution on missing files | Include concurrency simulation via rapid invocation loops |
| Command parsing | `show_usage`, invalid command routing, option validation errors | Ensure helpful diagnostics and non-zero exit codes |
| `add` | creation with/without tags, auto-increment, log entry | Cover whitespace trimming, quoting, collision handling |
| `add-subtask` | parent existence, two-level nesting, tag inheritance | Error when parent missing or invalid depth |
| `list` | default view, filtering flags (`--tag`, `--parents-only`, `--has-subtasks`, `--incomplete-only`) | Snapshot-based assertions on stdout |
| `complete` | single/bulk completion, `--with-subtasks`, range syntax | Validate Recently Completed section ordering |
| `undo` | reopen tasks across sections, handling for deleted tasks | Ensure metadata stays intact |
| `modify` | description updates, tag updates, no regression in formatting | Confirm serial numbers remain untouched |
| `delete` | soft delete semantics, expiry metadata, bulk deletions | Verify auto-purge hooks (needs time-freeze helper) |
| `archive` | completed vs incomplete flows, reason handling, status indicators | Ensure prompts are absent (AI friendly) |
| `relate` / `unrelate` | metadata persistence, validation of referenced IDs | Confirm comment block updates atomically |
| `note` | blockquote insertion, append, edit flows | Guard against breaking markdown indentation |
| `show` | aggregated display of task, subtasks, relationships, notes | Validate filtered output respects options |
| `restore` | recovery from Deleted and Recently Completed sections | Affirm constraints when ID not found |
| `--lint` / `--reformat` | detection of formatting errors, auto-fix operations | Compare before/after snapshots, ensure exit codes follow expectations |
| Backup & rollback | backup discovery, rollback safety nets | Use fixture with multiple backups |
| Update flow | simulate `update` command hitting mock remote | Stub network calls to avoid live traffic |
| Logging | entries written for every mutating command, ordering preserved | Diff log file after operations |
| Error handling | missing files, invalid IDs, permission issues | Confirm descriptive stderr messages |

## Cross-Cutting Concerns
- **Time-dependent behaviour:** provide shim to freeze time (e.g., export `TODO_AI_NOW="2025-01-01 00:00:00"` and patch `date` via function override) so assertions remain stable
- **Concurrency:** create stress scenario executing `todo.ai add` in parallel shells to verify serial integrity and log ordering
- **File permissions:** test read-only `TODO.md` and unwritable `.todo.ai` directories to ensure graceful failure messaging
- **Locale & encoding:** ensure ASCII output regardless of locale, validate behaviour when `$LANG` changes

## Automation Plan
- Add `tests/run.zsh` to orchestrate environment: installs ShellSpec if missing, exports required env vars, runs spec suite, emits junit report for CI integration
- Create `Makefile` targets: `make test`, `make test-unit`, `make test-integration`, `make test-watch`
- Configure GitHub Actions workflow:
  - checkout repository
  - install zsh + shellspec
  - execute `make test`
  - upload junit artifacts

## Future Enhancements
- Integrate coverage analysis via ShellSpec `--kcov` to measure function execution
- Add fuzz-style tests using [`shfuzz`](https://github.com/kward/shfuzz) to randomise command sequences
- Build performance benchmarks comparing command execution time before/after changes
- Generate golden master fixtures for high-risk commands (`list`, `show`) to detect formatting regressions

## Next Steps
- Implement `tests/helpers/sandbox.zsh` to manage isolated workspaces
- Port highest-risk commands (`add`, `complete`, `archive`, `delete`) into ShellSpec specs
- Expand suite iteratively alongside feature development, ensuring every regression bug gains a dedicated spec
