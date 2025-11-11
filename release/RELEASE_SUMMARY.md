# Release Summary

This release introduces the smart installer with bash/zsh dual-version support and reorganizes documentation for better navigation.

## Smart Installer & Bash Version Support

The smart installer automatically detects your system (macOS, Linux, Windows/WSL) and shell environment (zsh, bash 4+) to install the optimal version. This eliminates compatibility issues and ensures todo.ai works everywhere out of the box.

**Key improvements:**
- **Zero-interaction installation** - One-liner that works on all platforms
- **Bash version support** - 8-21% faster, works on systems without zsh
- **Release-aware downloads** - Installs from stable releases, not development code
- **Automated bash conversion** - Bash version generated automatically during releases
- **Clear development workflow** - Develop in zsh, bash version created automatically

Technical details: The bash version requires only 7 syntax changes from zsh (array key iteration, shebang, local scope) and maintains 100% feature parity. Both versions are tested before each release.

## Documentation Reorganization

All documentation has been reorganized into logical categories for easier navigation:
- **guides/** - User-facing guides and tutorials (5 docs)
- **design/** - Technical design specifications (8 docs)
- **development/** - Contributor documentation (4 docs)
- **analysis/** - Research and analysis reports (7 docs)
- **archive/** - Historical and completed migrations (4 docs)

A comprehensive documentation index at `docs/README.md` makes it easy to find what you need.

## Benefits

- **Broader compatibility** - Works on more systems without requiring zsh installation
- **Better performance** - Bash version is consistently faster (8-21%)
- **Easier navigation** - Well-organized documentation structure
- **Maintained quality** - All cross-references updated, no broken links
