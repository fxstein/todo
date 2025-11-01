This release enhances the migration system with improved visibility into version updates. When migrations run, users now see exactly which version numbers are being updated, making it easier to track their migration progress.

**Enhancement:**
The migration output has been updated to display version ranges instead of a generic "Running migrations..." message. When migrations execute, users will now see a clear message like "🔄 Running migrations: 1.3.5 → 1.5.4", showing the exact version range being migrated.

**How it works:**
The system determines the "from" version by finding the highest already-executed migration version. If no migrations have been executed yet, it uses the lowest pending migration version as an estimate. The "to" version is always the current version of todo.ai. This provides users with better visibility into which version numbers are being updated during the migration process.

This enhancement is particularly useful when upgrading from older versions, as users can now see exactly which migrations are running and what version range they're transitioning through.
