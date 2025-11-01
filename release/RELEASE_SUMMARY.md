This release fixes a critical update logic error that prevented new versions from properly executing their own update logic, migrations, and cursor rules updates.

**The Problem:**
When users ran the update command, the update process was executed from the old version's code. This meant that any new logic in the updated version (like new migrations, cursor rules updates, or other update-related code) never executed because the old version didn't have knowledge of those features.

**The Solution:**
The update process now follows a more reliable pattern: download the new version → execute the new version's code directly → then replace the old version. This ensures that migrations, cursor rules updates, and any other update logic in the new version execute with the new version's code, not the old version's code.

This fix ensures that users upgrading from any version to any newer version will reliably have all migrations run and all updates applied, regardless of what version they're upgrading from. The update process is now truly self-contained and future-proof.
