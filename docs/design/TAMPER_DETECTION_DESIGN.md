# Tamper Detection System Design

**Task:** #210.3
**Date:** 2026-01-25
**Status:** Draft

## 1. Overview

The Tamper Detection System aims to enforce the integrity of `TODO.md` by actively detecting and blocking unauthorized modifications. "Unauthorized" is defined as any change made outside the `todo-ai` ecosystem (CLI, MCP, Shell).

The system relies on a **Strict Checksum Verification** model:
1. Every valid operation updates a stored checksum.
2. Every read/write operation verifies the file against this checksum.
3. Any mismatch triggers a `TamperError`, blocking execution until resolved.

## 2. Core Components

### 2.1 Checksum File (`.todo.ai/checksum`)
A plain text file containing the SHA-256 hash of the normalized `TODO.md` content.
- **Location:** `.todo.ai/checksum`
- **Format:** `SHA256_HASH_STRING` (e.g., `a1b2c3d4...`)
- **Normalization:** Before hashing, `TODO.md` content is normalized (newlines converted to `\n`, encoding UTF-8) to ensure cross-platform consistency.

### 2.2 Shadow Copy (`.todo.ai/shadow/TODO.md`)
A hidden backup of the last known valid state of `TODO.md`.
- **Location:** `.todo.ai/shadow/TODO.md`
- **Purpose:** Enables diffing against the "last valid state" even if no Git commits exist.
- **Update Logic:** Updated atomically alongside the checksum whenever a valid `todo-ai` write occurs.

### 2.4 Tamper Event Archive (`.todo.ai/tamper/`)
A directory storing forensic copies of `TODO.md` whenever a tamper event is overridden.
- **Location:** `.todo.ai/tamper/YYYY-MM-DD_HH-MM-SS/`
- **Contents:**
  - `original.md`: The shadow copy (last known valid state) before the tamper event.
  - `forced.md`: The file content at the moment it was forced/accepted.
- **Trigger:** Created automatically when `todo-ai tamper accept` or `accept_tamper` is executed.

### 2.5 Log Enhancement (`.todo.ai/.todo.ai.log`)
The audit log will be expanded to track the *source* of edits and the *checksum* of the file after each operation.
- **New Columns:**
  - `INTERFACE`: `CLI`, `MCP`, `SHELL` (Legacy)
  - `CHECKSUM`: The first 8 chars of the new SHA-256 hash.
- **Format:** `TIMESTAMP | USER | INTERFACE | ACTION | TASK_ID | CHECKSUM | DESCRIPTION`

### 2.6 Configuration (`.todo.ai/config.yaml`)
A new security setting controls the strictness of tamper detection.

- **Setting:** `security.tamper_proof`
- **Type:** `boolean`
- **Default:** `false` (Passive Mode)
- **Behavior:**
  - `false` (Passive): Checksums are calculated and logged. Mismatches are logged but **do not block** execution.
  - `true` (Active): Checksum mismatches **block** execution (raise `TamperError`).

### 2.7 Tamper Mode State (`.todo.ai/tamper_mode`)
A file tracking the last known state of the `tamper_proof` setting to detect and log changes.
- **Location:** `.todo.ai/tamper_mode`
- **Content:** `true` or `false`
- **Update Logic:** Updated whenever `FileOps` detects a change in `config.yaml` vs this file. Logs `ACTION: SETTING_CHANGE` when updated.

## 3. Workflows

### 3.1 Verification Logic (The "Gatekeeper")
This logic runs *before* any command execution (in `FileOps.__init__` or `load()`).

1. **Read** `TODO.md` from disk.
2. **Calculate** SHA-256 hash of normalized content (`current_hash`).
3. **Read** stored hash from `.todo.ai/checksum` (`stored_hash`).
4. **Check Configuration:**
   - Read `tamper_proof` from config.
   - Compare with `.todo.ai/tamper_mode`. If changed, log `SETTING_CHANGE` and update state file.
5. **Compare Hashes:**
   - If `current_hash == stored_hash`: **Pass**.
   - If `stored_hash` is missing: **First Run / Reset**. (Warn user, create checksum, proceed).
   - If `current_hash != stored_hash`:
     - If `tamper_proof == true`: **FAIL**. Raise `TamperError`.
     - If `tamper_proof == false`: **WARN & LOG**. Log `ACTION: TAMPER_DETECTED` (Passive), update checksum to match current file (auto-accept), and proceed.

### 3.2 Write/Update Logic
This logic runs *after* a successful operation (in `FileOps.save()`).

1. **Write** new content to `TODO.md`.
2. **Calculate** new SHA-256 hash (`new_hash`).
3. **Write** `new_hash` to `.todo.ai/checksum`.
4. **Copy** `TODO.md` to `.todo.ai/shadow/TODO.md`.
5. **Log** the action with `INTERFACE` and `CHECKSUM`.

### 3.3 Tamper Handling (Recovery)
When `TamperError` is raised, the user/agent must explicitly "accept" the external changes to proceed.

#### CLI Recovery
When running a command (e.g., `todo-ai list`) and tampering is detected:
- **Default Behavior:** Error out with a message.
  ```text
  ⛔ TAMPER DETECTED: TODO.md has been modified externally.
  Expected hash: a1b2c3...
  Actual hash:   e5f6g7...

  Use 'todo-ai tamper diff' to see changes.
  Use 'todo-ai tamper accept' to accept external changes.
  ```

#### MCP Recovery
Agents encountering `TamperError` will receive a structured error message.
- **Error Message:** `TamperError: External modification detected. Use 'accept_tamper' tool to resolve.`
- **New Tool:** `accept_tamper(reason: str)`
  - Archives the event: Copies shadow and current file to `.todo.ai/tamper/<timestamp>/`.
  - Updates checksum and shadow copy to match current disk state.
  - Logs the event: `ACTION: FORCE_ACCEPT`, `DESCRIPTION: Accepted external changes: <reason>`.

### 3.4 No Global Force Option
**Decision:** We explicitly **REJECT** a global `--force` flag for standard commands.

- **Reasoning:**
  - Agents are prone to abusing `--force` to bypass errors instead of fixing root causes.
  - Tampering is a critical security/integrity event that requires a specific, deliberate resolution step.
  - Allowing `todo-ai add "foo" --force` would mask the fact that the file was corrupted.

- **Required Workflow:**
  - Users/Agents MUST run `todo-ai tamper accept` (CLI) or `accept_tamper` (MCP) first to resolve the state.
  - Only after the state is resolved (checksum matches) can normal commands proceed.

## 4. Component Behavior

### 4.1 Linter & Reformatter
- **Behavior:** These tools enforce structure. If they run on a tampered file:
  - They **MUST** fail verification first (just like any other command).
  - **Why?** If the linter auto-fixes a tampered file, it might "bless" a malicious edit (e.g., a deleted task) by re-hashing it.
  - **User Action:** User must run `todo-ai tamper accept` (which implicitly accepts the current state) OR manually revert the file.
  - **Refinement:** `todo-ai lint --fix` could theoretically accept changes, but it's safer to require explicit acceptance first.

### 4.2 Legacy Shell Script
- **Scope:** The shell script (`./todo.ai`) will **NOT** implement verification logic (too complex for bash).
- **Impact:** Shell script edits will cause `TamperError` in Python/MCP tools (because shell script won't update the checksum).
- **Mitigation:** Users migrating to Python/MCP should stop using the shell script. If they do use it, they will need to run `todo-ai tamper accept` once to resync.

## 5. Implementation Plan

### Phase 1: Core Logic (FileOps)
- [ ] Implement `calculate_checksum()` (SHA-256, normalized).
- [ ] Implement `verify_integrity()` in `FileOps`.
- [ ] Implement `update_integrity()` (write checksum + shadow copy).
- [ ] Update `FileOps.save()` to call `update_integrity()`.

### Phase 2: CLI Commands
- [ ] Create `todo-ai tamper` command group.
  - `diff`: Diff `TODO.md` vs `.todo.ai/shadow/TODO.md`.
  - `accept`: Archive event, update checksum/shadow to match current file.
- [ ] Ensure NO global `--force` flag is implemented.

### Phase 3: MCP Tools
- [ ] Create `accept_tamper` tool.
- [ ] Ensure all existing tools propagate `TamperError` clearly.

### Phase 4: Logging
- [ ] Update `Logger` class to include `INTERFACE` and `CHECKSUM` columns.
- [ ] Detect interface type (CLI vs MCP) via environment variable or entry point.

## 6. Security Considerations
- **Hash Collision:** SHA-256 is sufficient.
- **Race Conditions:** File locking is already handled by `FileOps`.
- **Shadow Copy Size:** `TODO.md` is text, usually small (<1MB). Storing one copy is negligible.
