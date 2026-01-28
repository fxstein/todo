# Contributing to ai-todo

Thank you for contributing. This document covers our Linear-driven development workflow and branch conventions.

## Linear & Development Workflow

We use a **headless** workflow: **Linear** is the source of truth for work; **GitHub** and **Cursor** execute it. See [docs/linear_integration_design.md](docs/linear_integration_design.md) for the full design.

### 1 Team = 1 Repo

- Each **Linear team** maps to **one GitHub repository**.
- For this repo: Linear team **ai-todo** → repository **fxstein/ai-todo**.
- Issue identifiers use the team key: **AIT-**&lt;number&gt; (e.g. AIT-12, AIT-266).
- One Linear issue → one branch → one PR. The branch name must include the issue identifier so Linear can auto-link.

### Branch naming (strict)

Branches **must** follow this format so Linear can auto-link PRs and commits:

```text
<your-username>/AIT-<id>-<description>
```

- **&lt;your-username&gt;:** Your GitHub/Linear username (lowercase). Example: `yourname`, `jdoe`.
- **&lt;id&gt;:** Linear issue ID number (e.g. `12`, `266`). **Required.**
- **&lt;description&gt;:** Short kebab-case description. Example: `fix-login`, `add-linear-check`.

**Examples:**

- `yourname/AIT-12-fix-login`
- `jdoe/AIT-266-linear-integration`

PRs opened from branches that do **not** match this format will fail the **Linear PR Check** workflow with:

> Branch must follow format username/AIT-123-description.

### Using the Cursor rule (automatic)

The Cursor rule **`.cursor/rules/linear-ai-todo-integration.mdc`** automates kickoff and branching:

1. Say **"Start work"** or **"Pick task"** in Cursor.
2. The agent will list your Linear issues (assigned to you), ask you to pick one, then:
   - Create a branch using Linear’s `gitBranchName` when present, or
   - Construct a branch name in the format above from the issue identifier and title.
3. After creating the branch, the agent will offer to set the Linear issue state to **In Progress**.

Using this rule ensures branch names always match the required format and stay linked to Linear.

### Manual workflow

If you are not using Cursor:

1. Pick an issue in Linear (team ai-todo).
2. Create a branch locally: `git checkout -b <your-username>/AIT-<id>-<description>`.
   - Replace `<your-username>` with your GitHub/Linear username (lowercase).
   - Example: `git checkout -b jdoe/AIT-12-fix-login`.
3. Open a PR from that branch to `main`. The branch name will be checked by the Linear PR Check workflow.

---

For other contribution guidelines (code style, tests, release process), see the main [README](README.md) and [docs/](docs/).
