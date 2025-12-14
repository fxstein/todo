# Installation

## Smart Installer (Recommended)

One-liner that auto-detects your system and installs the optimal version:

```bash
curl -fsSL https://raw.githubusercontent.com/fxstein/todo.ai/main/install.sh | sh
```

**What it does:**
1. Detects your OS (macOS, Linux, Windows/WSL)
2. Checks shell availability (zsh, bash 4+)
3. Fetches latest release from GitHub
4. Installs the optimal version for your system
5. Zero interaction required

**Example output:**
```
todo.ai Smart Installer
========================

🔍 Detected: macOS
📦 Installing: zsh version (todo.ai)
   Reason: zsh is default on modern macOS

🔍 Checking for latest release...
✓ Latest release: v2.3.1
📥 Downloading from release...
✓ Downloaded successfully
✓ Made executable

✅ Installation complete!
```

## Manual Installation

If you prefer to choose the version manually:

**Zsh version** (recommended for macOS):
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.ai && chmod +x todo.ai
```

**Bash version** (recommended for Linux, requires bash 4+):
```bash
curl -o todo.ai https://raw.githubusercontent.com/fxstein/todo.ai/main/todo.bash && chmod +x todo.ai
```

## Requirements

| Version | Shell | Availability |
|---------|-------|--------------|
| Zsh     | zsh (any version) | Default on macOS 10.15+ |
| Bash    | bash 4.0+ | Default on most Linux |

**Note:** macOS ships with bash 3.2 which doesn't support the bash version. Use zsh or upgrade bash via homebrew: `brew install bash`

## Troubleshooting

**Error: No compatible shell found**
- macOS: zsh is pre-installed on 10.15+ (`/bin/zsh`)
- Linux: `sudo apt install zsh` or `sudo yum install zsh`
- Or upgrade bash: requires 4.0+ for associative arrays

**Error: Download failed**
- Check internet connection
- Verify GitHub is accessible
- Try wget instead: `wget -O todo.ai <url> && chmod +x todo.ai`

**Error: Permission denied**
- Add executable permission: `chmod +x todo.ai`
- Or run via shell: `zsh todo.ai list` or `bash todo.bash list`

## Technical Details

See [BASH_VS_ZSH_ANALYSIS.md](../analysis/BASH_VS_ZSH_ANALYSIS.md) for:
- Performance comparison (bash 8-21% faster)
- Compatibility analysis
- Conversion details (only 7 changes needed)
- Detailed recommendations
