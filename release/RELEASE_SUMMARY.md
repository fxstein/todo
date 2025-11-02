# Release Summary

This release includes a significant simplification of the release numbering logic, making it easier to understand and maintain. The core change is that the system now uses a default-to-PATCH approach: commits are only explicitly checked for MAJOR (breaking changes) or MINOR (user-facing features), and everything else automatically defaults to PATCH. This eliminates the need for explicit PATCH prefix checks while maintaining the same classification accuracy.

The release also includes comprehensive documentation in the form of a new mapping document that clearly explains how commit prefixes, keywords, and file changes are classified. This document provides developers and AI agents with a clear reference for understanding release numbering decisions, complete with examples and a priority matrix.

These improvements make the release process more maintainable and transparent, ensuring that version bumps are correctly determined while reducing code complexity.
