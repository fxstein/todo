This release reorganizes all release-related files into a dedicated `release/` directory and updates the release log to use a proper log file format matching the todo.ai log architecture.

The most significant improvement is the complete reorganization of release infrastructure ([b5b1a8f](https://github.com/fxstein/todo.ai/commit/b5b1a8f...)). All release-related files (`release.sh`, `RELEASE_LOG.log`, `RELEASE_PROCESS.md`, `RELEASE_NUMBERING_ANALYSIS.md`) are now organized in a single `release/` directory for better project structure. This makes it easier to find and manage all release-related files in one place.

Additionally, the release log has been converted from a Markdown file to a proper log file format ([1c470a1](https://github.com/fxstein/todo.ai/commit/1c470a1...)), matching the architecture of the todo.ai log file. The log now uses a pipe-delimited format (`TIMESTAMP | USER | STEP | MESSAGE`) with newest entries at the top, providing a consistent logging experience across the project and making it easier to parse and analyze release operations.

