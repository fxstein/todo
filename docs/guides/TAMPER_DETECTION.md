# Tamper Detection System

todo.ai includes a simple **Tamper Detection System** to ensure the integrity of your `TODO.md` file. This system protects your task data from accidental manual edits, unauthorized modifications, and corruption.

> **Note:** This system is **not cryptographic security** and is not designed to prevent malicious attacks. It is a simple integrity check to track and manage manual modifications to `TODO.md` that happen outside the tool's workflow.

**The system is optional and runs in logging-only mode by default.** It will detect and log external changes without blocking your workflow unless you explicitly enable strict mode.

## How It Works

The system maintains a cryptographic checksum (SHA-256) of your `TODO.md` file. Every time you use a valid `todo-ai` command (CLI or MCP), this checksum is updated.

If you (or an external tool) edit `TODO.md` manually:
1. The system detects that the file content does not match the stored checksum.
2. It compares the file modification time against the last known valid state.
3. It triggers a **Tamper Alert**.

## Security Modes

You can configure the strictness of the system in `.todo.ai/config.yaml`:

```yaml
security:
  tamper_proof: false  # Default (Passive Mode)
```

### Passive Mode (`false`) - Default
- **Behavior:** Detects tampering, logs a warning, but **automatically accepts** the changes.
- **Use Case:** Best for single-user environments where you occasionally make quick manual edits and want the system to just "catch up".
- **Log Entry:** `TAMPER_DETECTED` (with auto-accept).

### Active Mode (`true`) - Strict
- **Behavior:** Detects tampering and **blocks** all `todo-ai` commands until resolved.
- **Use Case:** Essential for multi-user environments, automated pipelines, or when using AI agents to prevent them from hallucinating edits.
- **Error Message:**
  ```text
  ⛔ TAMPER DETECTED: TODO.md has been modified externally.
  Expected hash: a1b2c3...
  Actual hash:   e5f6g7...
  ```

## Resolving Tamper Alerts

If you are in **Active Mode** and trigger a tamper alert, you must explicitly resolve it.

### 1. Review Changes
See exactly what changed between the last valid state and the current file:

```bash
todo-ai tamper diff
```

This shows a color-coded diff comparing the **Shadow Copy** (last known valid state) vs. the **Current File** (tampered).

### 2. Accept Changes
If the manual edits were intentional, you can accept them. This updates the checksum to match the current file and logs the event.

```bash
todo-ai tamper accept "Fixed typo manually"
```

**Note:** Accepting changes creates a forensic backup in `.todo.ai/tamper/<timestamp>/` containing both the original and forced versions.

### 3. Revert Changes (Manual)
If the changes were accidental, you can manually revert `TODO.md` using your editor or git:

```bash
git checkout TODO.md
```

## Forensic Auditing

The system maintains a comprehensive audit trail:

1. **Shared Log (`.todo.ai/.todo.ai.log`):** Tracks all valid operations.
2. **Audit Log (`.todo.ai/state/audit.log`):** Local-only log that persists even if you switch branches or revert git changes.
3. **Tamper Archive (`.todo.ai/tamper/`):** Stores snapshots of files involved in forced updates.

## Best Practices

- **Keep Active Mode ON** when working with AI Agents to prevent them from bypassing the toolset.
- **Use `todo-ai edit`** if you must edit manually; the system is aware of this command (future feature).
- **Check `todo-ai log`** to see who (or what) modified your tasks.
