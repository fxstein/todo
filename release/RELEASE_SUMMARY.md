This beta release addresses critical stability issues in the CI/CD pipeline that were causing release builds to fail silently. Specifically, it fixes a logic gap in the dependency validation that allowed the release process to skip essential steps when change detection failed.

It also includes a detailed failure analysis document describing the incident, its root cause, and the implemented safeguards to prevent recurrence.

Additionally, the release process has been improved to automatically detect and clean up orphan release tags from failed attempts, and to ensure release notes are generated from a clean state.
