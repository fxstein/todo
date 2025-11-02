# Release Summary

This release fixes a critical bug in the bug reporting feature where bug reports were being created in the customer's repository instead of the todo.ai repository. This fix ensures that when users report bugs about todo.ai, the issues are correctly created in the todo.ai repository at https://github.com/fxstein/todo.ai/issues, regardless of where the tool is installed.

The release also includes documentation improvements with the addition of a comprehensive multi-user/multi-branch conflict analysis document. This document identifies and analyzes eight different conflict scenarios that can occur when using todo.ai in collaborative environments, providing a foundation for future multi-user support features.

These improvements ensure that bug reports reach the correct destination and lay the groundwork for understanding and addressing task numbering conflicts in multi-user scenarios.
