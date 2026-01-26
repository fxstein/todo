import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run_shell(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)


def run_python(args, cwd=None):
    # Ensure PYTHONPATH includes repo root
    env = os.environ.copy()
    repo_root = str(Path.cwd())
    env["PYTHONPATH"] = repo_root

    cmd = [sys.executable, "-m", "ai_todo.cli.main", "--todo-file", "TODO.md"] + args
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def strip_ansi(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def main():
    test_dir = Path("validation_test_dir")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()

    repo_root = Path.cwd()
    todo_sh = repo_root / "legacy" / "todo.ai"

    print(f"Testing in {test_dir}")

    print("Step 1: Init with Shell")
    # Init requires interaction? No, `todo.ai init` is usually auto or has flags?
    # `todo.ai init` prompts.
    # But `todo.ai add` creates file if missing?
    # Let's try `add` directly.

    # Create empty TODO.md with correct structure manually to avoid init prompts
    (test_dir / "TODO.md").write_text(
        "# todo.ai ToDo List\n\n## Tasks\n\n------------------\n**Maintenance:** Use `todo.ai` script only\n",
        encoding="utf-8",
    )
    (test_dir / ".ai-todo").mkdir()
    (test_dir / ".ai-todo" / "config.yaml").write_text("mode: single-user\n", encoding="utf-8")

    print("Step 2: Add task with Python")
    res = run_python(["add", "Python Task"], cwd=test_dir)
    print("Python Output:", res.stdout.strip())
    if res.returncode != 0:
        print("Error:", res.stderr)

    print("Step 3: Add task with Shell")
    res = run_shell(f"{todo_sh} add 'Shell Task'", cwd=test_dir)
    print("Shell Output:", res.stdout.strip())
    if res.returncode != 0:
        print("Error:", res.stderr)

    print("Step 4: Compare List Output")
    py_list = run_python(["list"], cwd=test_dir).stdout
    sh_list = run_shell(f"{todo_sh} list", cwd=test_dir).stdout

    # Normalize
    py_norm = strip_ansi(py_list).strip()
    sh_norm = strip_ansi(sh_list).strip()

    # The shell script might output "Mode: ..." and tasks.
    # Let's compare lines.

    py_lines = [line.strip() for line in py_norm.splitlines() if line.strip()]
    sh_lines = [line.strip() for line in sh_norm.splitlines() if line.strip()]

    match = True
    if len(py_lines) != len(sh_lines):
        match = False
    else:
        for p, s in zip(py_lines, sh_lines, strict=False):
            if p != s:
                match = False
                break

    if match:
        print("\n✅ MATCH: Output is identical!")
    else:
        print("\n❌ MISMATCH: Output differs!")
        print("Python:")
        print("\n".join(py_lines))
        print("Shell:")
        print("\n".join(sh_lines))

    # Cleanup
    shutil.rmtree(test_dir)


if __name__ == "__main__":
    main()
