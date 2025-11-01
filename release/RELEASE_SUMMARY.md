This release enhances the update process to automatically run migrations immediately after a successful update. Previously, users had to manually run the tool again after updating to ensure pending migrations were executed, which could lead to outdated installations if users forgot this step.

The enhancement automatically executes the updated script after installation, triggering all pending migrations that need to run for the new version. This ensures that migrations (such as the section order fix from version 1.3.5) are applied immediately without requiring additional user action. Migration messages are displayed during the update process, providing transparency about what changes are being applied to the user's installation.

This improvement makes the update process more seamless and ensures all installations remain in sync with the latest structural requirements, improving data consistency across all user installations.
