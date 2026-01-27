# Security Best Practices

This guide covers security considerations when using ai-todo with Cursor AI.

## .cursorignore Protection

ai-todo uses `.cursorignore` to protect sensitive internal files from Cursor's AI features.

### Protected Directories

| Pattern | Purpose |
|---------|---------|
| `.ai-todo/state/` | Tamper detection state (checksums, shadow TODO.md) |
| `.todo.ai/state/` | Legacy state directory (backward compatibility) |
| `.ai-todo/backups/` | Task backups |
| `.todo.ai/backups/` | Legacy backups |

### What .cursorignore Protects Against

- **Tab completion** - Won't suggest content from ignored files
- **Inline edits** - AI won't reference ignored files
- **@ references** - Can't include ignored files in context

### Limitations

**Important:** `.cursorignore` does NOT provide complete protection:

| Limitation | Impact |
|------------|--------|
| **MCP/Tool Access** | MCP servers and terminal commands bypass .cursorignore |
| **Recently Viewed** | Files recently viewed may still appear in context |
| **Agent Mode** | Agent composer may access ignored directories |

**Note:** ai-todo's MCP server can access these files by design - this is necessary for tamper detection to function.

## Best Practices

1. **Don't store secrets in TODO.md** - Task descriptions are visible to AI agents
2. **Use environment variables** - Cursor ignores `.env` files by default
3. **Separate credentials** - Keep API keys in dedicated ignored files
4. **Understand limitations** - .cursorignore is defense-in-depth, not absolute protection

## Cursor Default Protections

Cursor automatically ignores these patterns (no configuration needed):

- `**/.env`, `**/.env.*` - Environment files
- `**/credentials.json`, `**/secrets.json` - Credential files
- `**/*.key`, `**/*.pem`, `**/id_rsa` - Private keys

## Related Documentation

- [Tamper Detection Guide](TAMPER_DETECTION.md) - Understanding file integrity protection
- [cursorignore Design](../cursorignore-design.md) - Technical design document
