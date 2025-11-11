# README Preview with Smart Installer

This shows how the README.md sections would change with the smart installer.

## Current Installation Section (Lines 5-16)

```markdown
## AI Agent Installation: Copy-paste this to your agent:

```
Adopt todo.ai for task tracking. Install using:
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai

Then create a task "Implement user authentication" with subtasks:
- Design database schema
- Create API endpoints  
- Add frontend components
- Write tests
```
```

## Proposed New Installation Section

```markdown
## AI Agent Installation: Copy-paste this to your agent:

```
Adopt todo.ai for task tracking. Install using:
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh

Then create a task "Implement user authentication" with subtasks:
- Design database schema
- Create API endpoints  
- Add frontend components
- Write tests
```
```

**What changed:**
- Uses smart installer instead of direct download
- Installer automatically detects environment and installs optimal version
- Still one-liner, still zero interaction
- Better compatibility across platforms

## Current Manual Installation Section (Lines 128-136)

```markdown
## Manual Installation

```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**To update:** Re-run the curl command, or use `./todo.ai update`

**To uninstall:** Run `./todo.ai uninstall` (removes script only) or `./todo.ai uninstall --all` (removes script, data, and rules)
```

## Proposed New Manual Installation Section

```markdown
## Installation

### Smart Installer (Recommended)

Automatically detects your system and installs the best version:

```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

The installer will:
- ✅ Detect your OS (macOS, Linux, Windows/WSL)
- ✅ Check shell availability (zsh, bash 4+)
- ✅ Install the optimal version for your system
- ✅ Provide clear feedback about the installation

**Example output:**
```
todo.ai Smart Installer
========================

🔍 Detected: macOS
📦 Installing: zsh version
   Reason: zsh is default on modern macOS

⬇️  Downloading from GitHub...
✓ Downloaded successfully
✓ Made executable

✅ Installation complete!

Get started:
  ./todo.ai --help     Show all commands
  ./todo.ai add "Fix bug" '#bug'     Create a task

📚 Repository: https://github.com/fxstein/todo.ai

todo.ai version 2.3.1
Repository: https://github.com/fxstein/todo.ai
Update: ./todo.ai update
```

### Manual Installation

If you prefer to choose the version manually:

**Zsh version** (recommended for macOS):
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**Bash version** (recommended for Linux, requires bash 4+):
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.bash && chmod +x todo.ai
```

**Requirements:**
- Zsh version: zsh (any version)
- Bash version: bash 4.0+

> **Note:** macOS ships with bash 3.2 which is not compatible with the bash version. The smart installer will automatically choose zsh on macOS, or you can upgrade bash via homebrew (`brew install bash`).

### Update

```bash
./todo.ai update
```

### Uninstall

```bash
./todo.ai uninstall              # Remove script only
./todo.ai uninstall --all        # Remove script, data, and rules
```
```

## Side-by-Side Comparison

### Before (Current)

| Aspect | Current Approach |
|--------|------------------|
| Installation | One-liner direct download |
| Compatibility | User must know which version they need |
| Platform detection | None - downloads zsh version always |
| Error handling | User discovers incompatibility after install |
| User experience | Simple but potentially broken |

**Installation command:**
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**Problems:**
- Downloads zsh version even on systems without zsh
- No indication of what's being installed
- Silent failure if zsh not available
- User must troubleshoot compatibility issues

### After (With Smart Installer)

| Aspect | Smart Installer Approach |
|--------|--------------------------|
| Installation | One-liner smart installer |
| Compatibility | Automatic detection and optimal choice |
| Platform detection | Detects OS and shell versions |
| Error handling | Clear error messages with solutions |
| User experience | Simple AND reliable |

**Installation command:**
```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

**Benefits:**
- ✅ Automatically detects and installs optimal version
- ✅ Shows what's being installed and why
- ✅ Clear error messages if requirements not met
- ✅ Works reliably across platforms
- ✅ Still one-liner, still zero interaction
- ✅ Better for AI agents (works everywhere)

## For AI Agents

The smart installer is **perfect for AI agents** because:

1. **Still one-liner:** No additional complexity
2. **Zero interaction:** No prompts, fully automated
3. **Better reliability:** Works on more systems out of the box
4. **Clear feedback:** Agent can see what was installed
5. **Error messages:** Clear instructions if installation fails

**Current AI agent prompt:**
```
Adopt todo.ai for task tracking. Install using:
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**New AI agent prompt:**
```
Adopt todo.ai for task tracking. Install using:
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

**Agent can parse installer output:**
```
🔍 Detected: Linux
📦 Installing: bash version
   Reason: bash 5 detected (requires 4+)
✅ Installation complete!
```

This gives agents context about:
- What environment they're running in
- Which version was installed
- Whether installation succeeded

## Migration Strategy

### Phase 1: Add Smart Installer (Non-Breaking)
1. Add `install.sh` to repository
2. Add `todo.bash` to repository
3. Keep existing direct download links working
4. Update README with both options
5. Recommend smart installer as primary method

### Phase 2: Update Documentation (Gradual)
1. Update AI agent prompt in README to use smart installer
2. Keep direct download method documented as "Manual Installation"
3. Add troubleshooting section referencing installer output
4. Update GETTING_STARTED.md with smart installer examples

### Phase 3: Monitor & Iterate (Optional)
1. Gather feedback from users
2. Improve error messages based on actual usage
3. Add analytics (opt-in) to understand platform distribution
4. Adjust detection logic if needed

## Conclusion

The smart installer maintains the **simplicity and zero-interaction philosophy** of todo.ai while adding **intelligence and reliability**. It's still a one-liner, still works perfectly for AI agents, but now it works reliably across all platforms.

**Key advantages:**
- 🎯 **Same simplicity:** Still one-liner, still zero interaction
- 🚀 **Better reliability:** Works on more systems automatically
- 📊 **Clear feedback:** Shows what's being installed and why
- 🛠️ **Better errors:** Clear instructions when requirements not met
- 🤖 **AI-agent friendly:** Works everywhere, parseable output
- 🔧 **Maintains control:** Direct download still available for manual choice

The smart installer is a **natural evolution** that improves the installation experience without sacrificing the core philosophy of simplicity.

