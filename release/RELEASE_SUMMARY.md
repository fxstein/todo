This release fixes two critical issues in the update process that prevented users from seeing proper migration feedback during updates.

**Fix 1: Migration Version Messages Now Display Correctly**
The update process was suppressing migration output, preventing users from seeing the helpful version range messages (e.g., "🔄 Running migrations: 1.5.0 → 1.5.5"). This has been fixed by allowing stderr messages to pass through while suppressing only stdout, ensuring migration status messages are visible during updates.

**Fix 2: New Version's Code Now Executes Properly During Update**
A critical bug was identified where the update process might not have been executing the new version's code correctly. The fix ensures that when updating, the newly downloaded version's script is explicitly executed using `/bin/zsh`, guaranteeing that the new version's migration logic and cursor rules updates run with the correct, up-to-date code rather than any cached or PATH-resolved version.

These fixes ensure that when users update todo.ai, they will:
- See clear migration progress messages showing version ranges
- Have confidence that the new version's code is actually executing
- Receive proper migration feedback during the update process

**Known Limitation:**
The enhanced migration version messages (e.g., "🔄 Running migrations: 1.5.0 → 1.5.6") are only visible when updating **from version 1.5.6 or later**. Users updating from version 1.5.0 or earlier will still see the legacy message format ("🔄 Running migrations...") during the update process itself, because those messages are printed by the older version's update function, which cannot be modified retroactively.

After successfully updating to version 1.5.6 or later, all subsequent updates will display the new enhanced migration version messages.
