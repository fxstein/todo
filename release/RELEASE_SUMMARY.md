# Release Summary

This release enhances the cursor rules update system to ensure that AI agents always have the latest rules and that users are properly notified when rules are updated.

## Key Improvements

**Enhanced Cursor Rules Update System:**
- The `init_cursor_rules` function now intelligently detects and updates outdated sections, not just missing ones. This ensures that existing installations automatically get the latest rules (such as the critical bug reporting requirements) when they update `todo.ai`.
- When cursor rules are updated, comprehensive prompts are now displayed for both humans and AI agents, clearly explaining that rules only take effect in new chat sessions.
- The update process now includes automatic cursor rules updates, ensuring users always have the latest rules after updating `todo.ai`.

**Better User Experience:**
- Clear, actionable instructions are provided when cursor rules are updated, explaining the need to start a new chat session.
- AI agents are explicitly instructed to inform users about rule updates and request a new session.
- This prevents confusion when agents bypass required workflows (like using `./todo.ai report-bug` instead of directly creating GitHub issues).

**Usage:**

For AI Agents:
```
When cursor rules are updated, inform the user:
"Cursor rules have been updated. Please start a new chat session for the updated rules to take effect."
```

For Humans:
```
Start a new chat session in Cursor after updating todo.ai to ensure the latest rules are applied.
```

**Note:** This release ensures that the critical bug reporting requirements (requiring `./todo.ai report-bug` instead of direct `gh issue create`) are automatically updated in all installations, preventing agents from bypassing the bug reporting workflow.
