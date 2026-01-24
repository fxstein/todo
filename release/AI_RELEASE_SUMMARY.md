This beta release fixes the release pipeline so tag-triggered jobs reliably run,
including validation and publish steps. It should allow the beta to publish to
PyPI and generate the GitHub release without manual intervention.

We also include the recent workflow gating adjustments and release tooling
improvements that make retries safe and transparent. This keeps the beta
process stable while we validate the end-to-end release flow.
