## Release 3.0.0b9

This beta release fixes the critical CI/CD issue where release jobs were being skipped on tag pushes, preventing any releases from being published since v3.0.0b8. The root cause was identified as a missing job-level conditional that was inadvertently removed, causing GitHub Actions to skip the validate-release and release jobs entirely.

The fix restores the explicit `if: needs.changes.outputs.is_tag == 'true'` condition to the validate-release job, eliminating the ambiguity that caused GitHub Actions to apply implicit skipping logic. Additionally, comprehensive debug logging has been added throughout the workflow to provide detailed diagnostics at all critical points, significantly improving our ability to quickly diagnose similar issues in the future.

This release includes extensive analysis documentation detailing the investigation process, root cause analysis, and output propagation verification. The debug logging additions provide verbose tag detection with condition evaluation, dependency status verification, output propagation tracking, and conditional evaluation display across five key workflow checkpoints.

---

### 🐛 Bug Fixes

- Restore job-level conditional to validate-release job (task#186.5) ([6331e5e](https://github.com/fxstein/todo.ai/commit/6331e5e71c9831c1b099847e19ded83c5f3738e0))

### 🔧 Other Changes

- chore: Add AI release summary for beta release ([5ec4585](https://github.com/fxstein/todo.ai/commit/5ec4585c3b702e4e118fc158f02410189d68b6d5))
- infra: Add comprehensive debug logging to CI/CD workflow (task#186.4) ([4b28631](https://github.com/fxstein/todo.ai/commit/4b286318d35486931c0eea6c23792fdf34493cdc))
- docs: Complete output propagation analysis for CI/CD issue (task#186.2, task#186.3) ([4b34a54](https://github.com/fxstein/todo.ai/commit/4b34a541ac4ef719debda11c4b1c2c73a8097916))
- docs: Document diagnostic findings for CI/CD release job skipping (task#186.1) ([4d643af](https://github.com/fxstein/todo.ai/commit/4d643afc0abca682c4406e00ffb483671269cddb))
- docs: Document CI/CD release job skipping issue and create investigation tasks (task#186) ([f713dbb](https://github.com/fxstein/todo.ai/commit/f713dbbf4a5f9f9f2d31659aaca917723e241046))

## Previous Beta Release Notes

## Release 3.0.0b8

This beta release focuses on hardening the CI/CD pipeline and improving the user experience for task notes. Key improvements include fixes for silent CI/CD failures, optimized workflow triggers for documentation-only changes, and enhanced release process reliability with orphan tag cleanup.

User-facing changes include the removal of confirmation prompts for `update-note` and `delete-note` commands to streamline workflow, and a fix for preserving checkbox states when modifying tasks.

---

### ✨ Features

- remove update-note confirmation prompt (task#185) ([b95f09e](https://github.com/fxstein/todo.ai/commit/b95f09e7df15ccd0cadfe9d48ed4fa6848d35dce))
- remove delete-note confirmation prompt (task#184) ([8e14e4c](https://github.com/fxstein/todo.ai/commit/8e14e4c02ab24966ccdfe89f8c85fefc23ec2708))

### 🐛 Bug Fixes

- preserve checkbox state on task modify ([a157e41](https://github.com/fxstein/todo.ai/commit/a157e41059234a13163af03db7b67c344f60bcba))
- derive code changes from file list ([c75f25d](https://github.com/fxstein/todo.ai/commit/c75f25de86ce993e23ac9b8a0ea5b33721978c0a))
- restore simple md/log change filters ([f1deaa1](https://github.com/fxstein/todo.ai/commit/f1deaa1054ae17ee2825d6dc90d13b0b7234a475))
- tighten CI change filters for docs/logs ([e5dc9c8](https://github.com/fxstein/todo.ai/commit/e5dc9c87bd2c9c118c1721cb508954692e34e754))
- use repo-root for workflow file checks ([a2cc4d5](https://github.com/fxstein/todo.ai/commit/a2cc4d51cf8f56e6968e2bfe5f1fba1930532e83))

### 🔧 Other Changes

- chore: Update release summary for beta release ([c81a98d](https://github.com/fxstein/todo.ai/commit/c81a98da50dc8f125eac451535a41b486a3a30d8))
- chore: Update release summary for beta release ([24abc5d](https://github.com/fxstein/todo.ai/commit/24abc5d1a825b61404a0d8e0b785d98023279c75))
- chore: Auto-commit changes before release ([7066836](https://github.com/fxstein/todo.ai/commit/70668361950ba7793d74ce15cdfe90e261aa6e9a))
- chore: Update release summary for beta release ([5804ce4](https://github.com/fxstein/todo.ai/commit/5804ce43d3fc0e111512e9e2f59f31e78e8661ef))
- docs: Add analysis of CI/CD silent failure incident ([08f1b3e](https://github.com/fxstein/todo.ai/commit/08f1b3ef786d1f7ec0d9860cc7d626bcc527f263))
- infra: Fix CI/CD pipeline silent failure on changes job error ([86109bb](https://github.com/fxstein/todo.ai/commit/86109bb61516ef4bd088f63bb64203f72d56b6fe))
- chore: Bump version to 3.0.0b11 ([6258729](https://github.com/fxstein/todo.ai/commit/62587290add1be8e3b5e25db11db630932d8608e))
- chore: add AI release summary ([0a95e10](https://github.com/fxstein/todo.ai/commit/0a95e105050f1d47c008461e43c6db0d377f7b35))
- infra: avoid skipping validate-release on tag runs ([dd9a222](https://github.com/fxstein/todo.ai/commit/dd9a2229c10136bdec635044bffdd7d8baa4096c))
- chore: Bump version to 3.0.0b10 ([0b2d209](https://github.com/fxstein/todo.ai/commit/0b2d209231c74d8a7f30eee976a7ad248e5718b1))
- chore: add AI release summary ([cd73f1d](https://github.com/fxstein/todo.ai/commit/cd73f1d3d192b1e6a9db12b131ba60dcd5b0f0c0))
- infra: derive tag context for release jobs ([f124f2d](https://github.com/fxstein/todo.ai/commit/f124f2d38793ac815830d3315360d9d174f65b52))
- chore: Bump version to 3.0.0b9 ([d027893](https://github.com/fxstein/todo.ai/commit/d02789308492d40e8956367e630520944d52971f))
- chore: add AI release summary ([0397926](https://github.com/fxstein/todo.ai/commit/03979263cd56e02f17a09ba160ba954ce1a83a45))
- infra: run release jobs on tag refs reliably ([246436b](https://github.com/fxstein/todo.ai/commit/246436bfd6eda0d97097d1873a9403a7e06609d6))
- chore: Bump version to 3.0.0b8 ([e6f1441](https://github.com/fxstein/todo.ai/commit/e6f144142e40096f2d4b790b1267749f5fbd2fb1))
- chore: add AI release summary ([4033725](https://github.com/fxstein/todo.ai/commit/4033725bd2038826f7ab11b94d9e016e88661743))
- chore: Bump version to 3.0.0b8 ([ee58d8d](https://github.com/fxstein/todo.ai/commit/ee58d8d3791fc56236bc7ccfebf8b65902364b9f))
- chore: add AI release summary ([e43b2d2](https://github.com/fxstein/todo.ai/commit/e43b2d2c71c040d6bb5703056fd0264bfba9c344))
- infra: run release jobs on tag refs ([3a761a5](https://github.com/fxstein/todo.ai/commit/3a761a5817912ef63794b3e0b0e0c106c2cbfe8b))
- docs: update v3 install and migration guide ([0be3dc6](https://github.com/fxstein/todo.ai/commit/0be3dc6d7f328c7456e9611b4909889a26c7300c))
- internal: complete task#163.44 ([f0f972c](https://github.com/fxstein/todo.ai/commit/f0f972c00ac6832aaeaed1b55471d26f8a53e3d4))
- internal: complete task#172.1 and task#172.2 ([5e37683](https://github.com/fxstein/todo.ai/commit/5e37683fec2980a432f0aad8969726d581356890))
- internal: complete task#172.3 and task#172.4 ([98be4aa](https://github.com/fxstein/todo.ai/commit/98be4aafc3b4c88bfb6b887f7c9a9b438cbf69b4))
- chore: Bump version to 3.0.0b8 ([9688cc1](https://github.com/fxstein/todo.ai/commit/9688cc1418aa99acf62904ed06325131496c90d6))
- chore: add AI release summary ([1074656](https://github.com/fxstein/todo.ai/commit/1074656900892d87201c0c10c646bd44ea1fdc71))
- internal: archive task#183 and task#185 ([5b6994d](https://github.com/fxstein/todo.ai/commit/5b6994d89d134d51968e55e3c2d535121466f4e1))
- internal: complete task#183 CI/CD optimization ([a52e326](https://github.com/fxstein/todo.ai/commit/a52e3267a3ff24c9b636cd1222ec9c566a9fd23e))
- internal: complete task#185 update-note prompt ([0282abb](https://github.com/fxstein/todo.ai/commit/0282abb630a958bb2cf010832d7a1c14edadc91e))
- internal: complete task#184 delete-note prompt ([6e7adf4](https://github.com/fxstein/todo.ai/commit/6e7adf4b784c2bb5c80548b460c35dcbe36219cf))
- internal: remove task#183 test note ([db6275d](https://github.com/fxstein/todo.ai/commit/db6275d1b73a0be50321ebbf87bb77922a006de5))
- internal: add task#184 for note deletion prompt ([fb714b9](https://github.com/fxstein/todo.ai/commit/fb714b9b83ab3c4d5c1b532251869424a050143b))
- internal: add tests note for task#183 ([ac02a90](https://github.com/fxstein/todo.ai/commit/ac02a904ec21f4f997a8737e4ec29615595f6c9b))
- internal: complete task#183.3 CI/CD workflow changes ([f3189ec](https://github.com/fxstein/todo.ai/commit/f3189ec104f102aa7f5d436503d73d1f9f79997a))
- infra: add logs-quality gate to CI/CD ([269528f](https://github.com/fxstein/todo.ai/commit/269528fc893793337bc71c7d36d8a94f666e10c9))
- infra: split docs and code checks in CI/CD ([622223f](https://github.com/fxstein/todo.ai/commit/622223ff175d30cfdeac51d7d9aab1d4c06e023a))
- infra: gate CI for docs/log-only changes (task#183.3, task#183.4) ([825ce0a](https://github.com/fxstein/todo.ai/commit/825ce0a075fb7ce1cce33de55adf2856fa2625c0))
- internal: complete task#183.2 CI/CD design ([5a848b9](https://github.com/fxstein/todo.ai/commit/5a848b9271bcae73bdd0d8c725c571292305a989))
- docs: add CI/CD optimization design (task#183.2) ([9a5045b](https://github.com/fxstein/todo.ai/commit/9a5045b5cc5eaa4589b4e6406d4d9a39e4355e75))
- internal: complete task#183.1 CI/CD analysis ([8639a30](https://github.com/fxstein/todo.ai/commit/8639a30dc141c603ca10b73174100e6d32ff3489))
- docs: add CI/CD optimization analysis for b6/b7 ([7f55114](https://github.com/fxstein/todo.ai/commit/7f551146a6a1154a82394404504240ca971857b2))
- infra: add task#183 CI/CD optimization plan ([bd46e09](https://github.com/fxstein/todo.ai/commit/bd46e09f158013bd929ba2b38faf9a2b87708375))
- internal: archive task#181 (release stabilization) ([e1bdd62](https://github.com/fxstein/todo.ai/commit/e1bdd626d1f6adf5dcd45b764629c5d7c1056d8e))
- internal: complete task#182 and subtasks ([9ad199f](https://github.com/fxstein/todo.ai/commit/9ad199f1ffc5157d74c7cfadcaf93199201dbbde))

## Previous Beta Release Notes

## Release 3.0.0b7

This beta fixes migrations writing .todo.ai data into the current working
directory when TODO_AI_ROOT or --root is used. Migrations now respect the
resolved root, keeping data and state consistent across nested workflows.

Users working inside subdirectories can safely set TODO_AI_ROOT without seeing
new .todo.ai folders created in the wrong place, which keeps repository hygiene
and tooling expectations aligned.

---

### 🐛 Bug Fixes

- scope migrations to resolved root (task#182.17) ([e8e438c](https://github.com/fxstein/todo.ai/commit/e8e438c39ab2ac886c0bca97725cd7dd9a1ee98c))

### 🔧 Other Changes

- chore: update AI release summary ([f4e914b](https://github.com/fxstein/todo.ai/commit/f4e914bb63364dc2f783db7d67d7a168dcf67424))

## Previous Beta Release Notes

## Release 3.0.0b6

This beta improves repository root detection for submodule layouts by correctly
handling gitdir pointer files. Running `show-root` from inside a submodule now
resolves to the superproject root instead of the nested module directory.

The update ensures consistent scoping for Cursor rules and todo.ai data when
working in projects that use submodules, reducing accidental initialization in
the wrong directory.

---

### 🐛 Bug Fixes

- handle submodule gitdir files for root resolution (task#182.10) ([3f6bf8b](https://github.com/fxstein/todo.ai/commit/3f6bf8bd1a5b97f35efca812f2f80d847171d0cd))

### 🔧 Other Changes

- chore: update AI release summary ([fc3e17a](https://github.com/fxstein/todo.ai/commit/fc3e17a6a160086d06a097cb628da7a11e7c147d))

## Previous Beta Release Notes

## Release 3.0.0b5

This beta fixes repository root resolution when running inside submodules, so
`show-root` now reliably points to the superproject instead of the nested
submodule directory. The shell and Python CLIs both detect submodule gitdir
paths and resolve back to the correct top-level repo for consistent behavior.

The update tightens submodule path detection to avoid false matches, making the
root logic more robust across complex workspaces. This ensures Cursor rules and
todo.ai data stay scoped to the intended repository even when working deep in
submodule trees.

---

### 🐛 Bug Fixes

- tighten submodule gitdir marker (task#182.10) ([186a87e](https://github.com/fxstein/todo.ai/commit/186a87e245fd1ef0f214b0e63cf6b95fb4581858))
- resolve root to superproject from submodules (task#182.10) ([79acd78](https://github.com/fxstein/todo.ai/commit/79acd7812f8992b30da8b0b5920e3b58ee532136))

### 🔧 Other Changes

- chore: update AI release summary ([9ae1e51](https://github.com/fxstein/todo.ai/commit/9ae1e5136299111b9a9e2ee7be98efc08c12eaa2))
- internal: update task#182 release subtasks ([2848728](https://github.com/fxstein/todo.ai/commit/28487285ed51e45627fe0b8b28748ff1cf15c7a6))
- internal: archive tasks task#179 and task#180 ([0605084](https://github.com/fxstein/todo.ai/commit/0605084dde8cc6578ce94ba162b1843e8b8a2bf8))

## Previous Beta Release Notes

## Release 3.0.0b4

This beta hardens repo-scoped usage by pinning todo.ai to the repository (or
super-repo) root by default, preventing accidental initialization in the wrong
directory. It also adds a `show-root` command with `--root` and `TODO_AI_ROOT`
overrides, plus parity tests to verify the behavior across the shell and Python
interfaces.

Release tooling is more reliable with a clarified AI summary pipeline, a
finalized `--set-version` workflow, and CI gating that focuses on the latest
commit to avoid false failures. Documentation updates cover the pinned-root
feature, usage patterns, and the overall design so users and contributors have
clear guidance.

---

### ✨ Features

- add show-root parity tests (task#182.5, task#182.6) ([429af92](https://github.com/fxstein/todo.ai/commit/429af92c94203bf036799bf655ca1379e6ec416a))
- add pinned root resolution (task#182.4) ([42733df](https://github.com/fxstein/todo.ai/commit/42733df68c7ad6c48e7a115b79273f775ceeeef5))
- add task#182 for pinned directory design ([c845a42](https://github.com/fxstein/todo.ai/commit/c845a42a2a348eb17aa71970ae0a51d70946aba9))

### 🐛 Bug Fixes

- skip show-root shell test on Windows ([2cbcc0e](https://github.com/fxstein/todo.ai/commit/2cbcc0e765b641651d74d7fb2682e0276325c97a))

### 🔧 Other Changes

- docs: add AI release summary ([8d9e63f](https://github.com/fxstein/todo.ai/commit/8d9e63f7879cd1d101d232c570e08b2b6f60d08a))
- docs: shorten release agent rules ([2656ba6](https://github.com/fxstein/todo.ai/commit/2656ba650e9a7c0ae594e23f76f987bde6b8047c))
- chore: add AI release summary ([d78b30e](https://github.com/fxstein/todo.ai/commit/d78b30e7a57ef0091710028e02380fa39ee7fc6e))
- infra: scope CI gate to HEAD commit ([89c6ec4](https://github.com/fxstein/todo.ai/commit/89c6ec413176352af519e44b67a1073f11841ef1))
- infra: check latest CI run only ([1924a58](https://github.com/fxstein/todo.ai/commit/1924a58691bf5951ead2f7bc81731310a0aa9b07))
- docs: document pinned root usage (task#182.7) ([59b67ab](https://github.com/fxstein/todo.ai/commit/59b67ab29e569aa0dde4c72ec6eced24308dfa8f))
- docs: update pinned root task tracking (task#182) ([c292b40](https://github.com/fxstein/todo.ai/commit/c292b4017677fe8425f45ea6e635fedf5e3f4e3c))
- docs: finalize pinned root design (task#182.3) ([6aacf1e](https://github.com/fxstein/todo.ai/commit/6aacf1e9126f3c8d846891802f5e5df161d9f151))
- docs: analyze pinned directory options (task#182) ([40d1eaf](https://github.com/fxstein/todo.ai/commit/40d1eaf40959b26d05613bea15ff27dff13c81e0))

## Previous Beta Release Notes

## Release 3.0.0b3

This beta focuses on reliability for hierarchical task management in the new
Python-based todo.ai. Subtasks now insert directly under their intended parent
task (or the parent’s last subtask), preventing the mis-grouping that previously
collapsed all subtasks under a single task.

Alongside the fix, the release includes routine maintenance and task cleanup to
keep the repository and workflows tidy. The core user-facing change is the
correct subtask placement behavior, which restores confidence in multi-parent
task trees.

---

### 🐛 Bug Fixes

- Place subtasks under correct parent (task#178, #40) ([9e1d668](https://github.com/fxstein/todo.ai/commit/9e1d668edc958818951bde86011e9f2469109efd))

### 🔧 Other Changes

- docs: refresh release summary (task#179) ([7eece50](https://github.com/fxstein/todo.ai/commit/7eece500ddc61fbdedca8c63df6ab7b8874353b5))
- chore: add AI release summary ([d5208d4](https://github.com/fxstein/todo.ai/commit/d5208d420489125a686a17f1e963c8bec5b54dce))
- chore: Archive completed tasks 173-178 (task#178) ([f68320c](https://github.com/fxstein/todo.ai/commit/f68320c606dad5391510440a0b60857df92799f1))
