This beta release focuses on making the release pipeline reliable and repeatable.
We fixed the tag-based release gating so the publish jobs execute on tag pushes,
which unblocks PyPI publishing and GitHub release creation for beta builds.

Documentation for the Python v3 installation and migration flow was also refined
to align with the `ai-todo` package name and uv-first guidance. Together these
changes ensure the beta release process and user onboarding steps are consistent.
