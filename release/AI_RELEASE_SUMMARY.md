This beta fixes migrations writing .todo.ai data into the current working
directory when TODO_AI_ROOT or --root is used. Migrations now respect the
resolved root, keeping data and state consistent across nested workflows.

Users working inside subdirectories can safely set TODO_AI_ROOT without seeing
new .todo.ai folders created in the wrong place, which keeps repository hygiene
and tooling expectations aligned.
