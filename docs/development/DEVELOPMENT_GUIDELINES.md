# Development Guidelines

## Zsh-First Development Workflow

### Critical Rules

1. **Always develop in `todo.ai` (zsh version)** ✅
   - This is the primary development file
   - All changes, features, and fixes go here
   - Version controlled and tested

2. **NEVER manually edit `todo.bash`** ❌
   - It's auto-generated during releases
   - Manual edits will be overwritten
   - Treated as build artifact

3. **Bash conversion is automated** 🤖
   - Happens during `./release/release.sh --prepare`
   - 7 automatic transformations applied
   - Both versions tested before release

4. **If todo.bash needs changes, modify todo.ai** 🔄
   - Make the change in the zsh version
   - Release script will convert it
   - Ensures consistency

### Development Workflow

```bash
# 1. Make changes to todo.ai (zsh version)
vim todo.ai

# 2. Test locally
./todo.ai list

# 3. Commit (todo.bash not in git until release)
git add todo.ai
git commit -m "feat: add new feature"

# 4. Release process handles bash conversion
./release/release.sh --prepare
# → Creates todo.bash automatically
# → Tests both versions
# → Shows diff summary
```

### File Status

| File | Status | Editable | Version Controlled |
|------|--------|----------|-------------------|
| `todo.ai` | Primary source | ✅ Yes | ✅ Yes |
| `todo.bash` | Generated | ❌ No | ⚠️ Only in releases |
| `install.sh` | Source | ✅ Yes | ✅ Yes |

### Release Process

1. **Prepare:** `./release/release.sh --prepare --summary release/RELEASE_SUMMARY.md`
   - Converts `todo.ai` → `todo.bash`
   - Tests both versions
   - Shows what will be released

2. **Execute:** `./release/release.sh --execute`
   - Creates GitHub release
   - Uploads `todo.ai` (zsh)
   - Uploads `todo.bash` (bash)
   - Uploads `install.sh`

### Why This Approach?

- ✅ **Single source of truth:** All development in one file
- ✅ **No confusion:** Clear which file to edit
- ✅ **Automated:** No manual conversion errors
- ✅ **Tested:** Both versions validated before release
- ✅ **Enforced:** Cursor rule prevents bash editing

### See Also

- `.cursor/rules/zsh-first-development.mdc` - Cursor rule enforcing this workflow
- `docs/analysis/BASH_VS_ZSH_ANALYSIS.md` - Why we support both versions
- `release/release.sh` - Automated conversion logic

