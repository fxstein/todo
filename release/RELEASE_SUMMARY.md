# Release Summary

This release fixes a critical bug in the coordination setup process that was automatically switching users to enhanced mode without consent.

The main fix resolves issue #27 where running `setup-coordination github-issues` or `setup-coordination counterapi` would automatically switch from single-user mode to enhanced mode when creating a new configuration file. This violated the principle that coordination should be configurable independently of the numbering mode. The fix ensures that when a new config file is created during coordination setup, it preserves the current numbering mode (which defaults to single-user) instead of forcing enhanced mode.

This improvement means users can now configure coordination services (GitHub Issues or CounterAPI) in any numbering mode without being forced into enhanced mode. Coordination and numbering mode are now truly independent features, giving users more flexibility in how they configure todo.ai for their workflow.

**Key improvements:**
- Fixed coordination setup to preserve current numbering mode
- Coordination can now be configured independently of numbering mode
- Users can set up coordination in single-user mode without mode switch
