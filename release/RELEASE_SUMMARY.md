This beta release contains the revised fix for the critical CI/CD issue where release jobs were being skipped on tag pushes. After discovering that job output comparisons were unreliable in GitHub Actions conditionals, we switched to using direct GitHub context for tag detection.

The solution uses `startsWith(github.ref, 'refs/tags/v')` instead of comparing job outputs, which is the same proven approach that worked successfully in v3.0.0b7. This bypasses the job output propagation entirely and relies on GitHub's built-in context variables which are always available and dependable.

This release maintains all the comprehensive debug logging improvements added in v3.0.0b9, providing excellent diagnostic visibility at all critical workflow checkpoints. The changes job's is_tag output remains for debug purposes, while the actual conditional uses the more reliable direct context approach.
