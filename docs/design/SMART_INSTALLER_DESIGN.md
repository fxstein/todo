# Smart Installer Design

## Overview

A smart installation script that detects the user's environment and installs the optimal version (bash or zsh) automatically, while maintaining the simple one-liner installation approach.

## Installation Methods

### Method 1: Smart Installer (Recommended)

**One-liner command:**
```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

**What it does:**
1. Detects your operating system (macOS, Linux, Windows/WSL)
2. Checks for zsh and bash availability and versions
3. Installs the best version for your system
4. Provides clear feedback about what was installed and why

**Example output on macOS:**
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

**Example output on Linux with bash 5:**
```
todo.ai Smart Installer
========================

🔍 Detected: Linux
📦 Installing: bash version
   Reason: bash 5 detected (requires 4+)

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

**Example output on old macOS (bash 3.2, no zsh):**
```
todo.ai Smart Installer
========================

🔍 Detected: macOS
✗ Error: No compatible shell found

todo.ai requires either:
  • zsh (recommended for macOS)
  • bash 4.0+ (macOS ships with bash 3.2)

Install zsh: Already available on macOS 10.15+
Or upgrade bash: brew install bash
```

### Method 2: Direct Download (Manual Choice)

If you prefer to choose the version manually:

**Zsh version:**
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**Bash version (requires bash 4+):**
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.bash && chmod +x todo.ai
```

## Updated README Sections

### AI Agent Installation Section

Replace current section with:

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

### Manual Installation Section

Replace current section with:

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

**Note:** macOS ships with bash 3.2 which is not compatible with the bash version. Use zsh version on macOS or upgrade bash via homebrew.

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

## Decision Logic

The smart installer uses this decision tree:

```
┌─────────────────┐
│ Detect OS       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│macOS │  │Linux/ │
│      │  │Unix   │
└───┬──┘  └──┬────┘
    │        │
    │        │
    ▼        ▼
┌───────────────────────────┐
│Has zsh?                   │
│                           │
│macOS: Yes → Install zsh   │
│Linux: Check bash first    │
└───┬───────────────────┬───┘
    │                   │
    │ Yes (macOS)       │ No
    │                   │
    ▼                   ▼
┌────────┐         ┌──────────────┐
│Install │         │Check bash    │
│zsh     │         │version       │
│version │         └───┬──────────┘
└────────┘             │
                       │
                  ┌────┴─────┐
                  │          │
              ┌───▼───┐  ┌───▼────┐
              │Bash 4+│  │Bash <4 │
              └───┬───┘  └───┬────┘
                  │          │
                  ▼          ▼
              ┌────────┐ ┌───────────┐
              │Install │ │Has zsh?   │
              │bash    │ └─┬─────┬───┘
              │version │   │     │
              └────────┘   │Yes  │No
                           ▼     ▼
                       ┌────┐ ┌──────┐
                       │zsh │ │Error │
                       └────┘ └──────┘
```

**Priority order:**
1. **macOS:** zsh (default) → bash 4+ → error
2. **Linux/Unix:** bash 4+ (common) → zsh (fallback) → error

## Technical Details

### Script Features

1. **POSIX-compliant:** Uses `#!/bin/sh` for maximum compatibility
2. **No prompts:** Fully automated, zero interaction
3. **Color output:** Uses colors when terminal supports it
4. **Error handling:** Clear error messages with installation instructions
5. **Fallback:** Works with both `curl` and `wget`
6. **Version detection:** Automatically checks bash version
7. **Feedback:** Shows what's being installed and why

### Why This Approach?

#### Maintains Simplicity
- Still a one-liner command
- No user input required
- Works perfectly for AI agents

#### Improves Compatibility
- Automatically chooses the right version
- Clear error messages when requirements not met
- No "it doesn't work" surprises

#### Better User Experience
- Users don't need to know about bash/zsh differences
- Automatic detection removes decision burden
- Clear feedback about what was installed

#### Keeps Manual Control
- Advanced users can still download specific versions
- Direct URLs still work for specific use cases
- Doesn't force the smart installer

### Alternative: Inline Detection

For environments where piping to `sh` is not preferred, here's a one-liner with inline detection:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh)"
```

Or even more compact (but less readable):

```bash
curl -fsSL https://git.io/todo-ai-install | sh
```

(Requires setting up a git.io short URL or similar)

## Testing Scenarios

### Scenario 1: Modern macOS (10.15+)
- **System:** macOS 12+, zsh available, bash 3.2
- **Detection:** Detects macOS, finds zsh
- **Action:** Installs zsh version
- **Result:** ✅ Works immediately

### Scenario 2: Linux with bash 5
- **System:** Ubuntu 22.04, bash 5.1, no zsh
- **Detection:** Detects Linux, bash 5
- **Action:** Installs bash version
- **Result:** ✅ Works immediately

### Scenario 3: Linux with bash 4
- **System:** Ubuntu 18.04, bash 4.4, no zsh
- **Detection:** Detects Linux, bash 4
- **Action:** Installs bash version
- **Result:** ✅ Works immediately

### Scenario 4: Old macOS without zsh
- **System:** macOS 10.13, no zsh, bash 3.2
- **Detection:** Detects macOS, no zsh, bash too old
- **Action:** Shows error with clear instructions
- **Result:** ℹ️ User installs zsh or upgrades bash

### Scenario 5: WSL Ubuntu
- **System:** Windows 11 WSL2, Ubuntu 22.04, bash 5
- **Detection:** Detects Linux, bash 5
- **Action:** Installs bash version
- **Result:** ✅ Works immediately

### Scenario 6: Git Bash on Windows
- **System:** Windows with Git Bash, bash 4.4
- **Detection:** Detects Windows, bash 4
- **Action:** Installs bash version
- **Result:** ✅ Works immediately

### Scenario 7: Server with only zsh
- **System:** Linux server, zsh only, no bash
- **Detection:** Detects Linux, no bash 4+, has zsh
- **Action:** Installs zsh version
- **Result:** ✅ Works immediately

## Migration Path

### Phase 1: Add bash version and smart installer
1. ✅ Create `todo.bash` (completed)
2. ✅ Test bash version thoroughly (completed)
3. ✅ Create `install.sh` smart installer (completed)
4. Test installer on multiple platforms
5. Add installer to repository

### Phase 2: Update documentation
1. Update README.md with new installation methods
2. Keep direct download links for manual choice
3. Update AI agent prompt with new installer
4. Add "Which version?" section to docs

### Phase 3: Monitor and adjust
1. Gather user feedback on installation experience
2. Track which versions are being installed (via GitHub download stats)
3. Adjust decision logic if needed
4. Consider analytics to understand user environment distribution

## Future Enhancements

### Short URL
Create a memorable short URL:
```bash
curl -fsSL https://todo.ai/install | sh
```

Or:
```bash
curl -fsSL https://get.todo.ai | sh
```

### Version Selection
Allow users to override auto-detection:
```bash
curl -fsSL https://get.todo.ai | sh -s -- --bash
curl -fsSL https://get.todo.ai | sh -s -- --zsh
```

### Specific Version
Allow installing specific versions:
```bash
curl -fsSL https://get.todo.ai | sh -s -- --version 2.3.1
```

### Update Detection
Check if already installed and offer to update:
```bash
curl -fsSL https://get.todo.ai | sh
# Detected existing installation (v2.3.0)
# Latest version: v2.3.1
# Update? (Y/n)
```

But this adds prompts, which goes against the zero-interaction design.

### Analytics (Optional, Privacy-Conscious)
Add optional anonymous analytics to understand:
- Which OS distributions are using todo.ai
- Which shell versions are most common
- Installation success rate

Could use a simple counter API that only logs OS/shell version (no user identification):
```bash
# Optional, only if user explicitly opts in
curl -X POST https://api.todo.ai/install/log -d "os=linux&shell=bash&version=5.1"
```

## Conclusion

The smart installer:
- ✅ Maintains the simple one-liner installation
- ✅ Works perfectly for AI agents (no prompts)
- ✅ Improves user experience (automatic detection)
- ✅ Provides clear feedback and errors
- ✅ Keeps manual control for advanced users
- ✅ Follows the zero-interaction design philosophy

It's a natural evolution that improves compatibility without sacrificing simplicity.

