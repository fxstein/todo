# Release Summary: v3.0.0b17

This beta release focuses on **Windows compatibility**, **parity test improvements**, and **stability fixes** following the major Tamper Detection feature introduced in b16.

## Key Improvements

### Windows Compatibility Fix
All test files now explicitly specify UTF-8 encoding when reading files, resolving failures on Windows where the system default encoding (cp1252) couldn't decode emoji characters in TODO.md headers. This ensures consistent cross-platform behavior.

### Parity Test Robustness
The Python vs Shell parity tests have been significantly improved to focus on **functional equivalence** rather than cosmetic differences:
- Dates on completed tasks are now normalized (Python adds completion dates, Shell doesn't)
- Section header naming differences are ignored ("Archived Tasks" vs "Recently Completed")
- Header and footer content differences are filtered out

### File Structure Preservation
Fixed a regression where custom headers and footers in TODO.md files were being overwritten with standard templates. The system now correctly preserves existing file structure during read/write cycles.

## Summary of Changes
- **3 bug fixes** for test infrastructure and file operations
- **1 test improvement** for cross-platform compatibility
- Multiple housekeeping commits for task management

This release completes the stabilization work for the v3.0.0 release candidate.
