# Research: Existing Solutions for Multi-User Task Numbering Conflicts

## Overview

This document researches how other task management tools handle multi-user numbering conflicts and sequential ID assignment in collaborative environments.

## Research Scope

- GitHub Issues
- JIRA
- Linear
- Asana
- Trello
- GitLab Issues
- TaskWarrior (file-based system)
- Other distributed/version-controlled task management systems

---

## GitHub Issues

### Approach
- **Sequential numbering per repository**
- Numbers assigned by GitHub's central server atomically
- No conflicts possible (server assigns numbers sequentially)

### Implementation Details
- Issue numbers are assigned sequentially when issues are created
- GitHub's backend ensures atomic assignment (one number per issue, no gaps)
- Multiple users can create issues simultaneously without conflicts
- Issue numbers are unique across the entire repository
- No user-side numbering logic required (server handles it)

### Strengths
- ✅ Zero conflicts possible (server-side assignment)
- ✅ Simple sequential numbering (`#1`, `#2`, `#3`)
- ✅ No merge conflicts in numbering
- ✅ Works perfectly for multi-user scenarios
- ✅ Familiar pattern for users

### Limitations
- ❌ Requires server-side infrastructure (not applicable to file-based systems)
- ❌ Cannot work offline
- ❌ Requires network connectivity for assignment

### Applicability to todo.ai
- **Not directly applicable**: todo.ai is a file-based system without a central server
- **Key insight**: The concept of atomic assignment is critical
- **Potential approach**: Could be simulated with Git as a coordination mechanism

---

## JIRA

### Approach
- **Project Key + Sequential ID** (e.g., `PROJ-123`)
- Project prefix provides namespace isolation
- Sequential numbering within project
- Server-side assignment ensures uniqueness

### Implementation Details
- Format: `<PROJECT_KEY>-<SEQUENTIAL_ID>`
- Example: `PROJ-123`, `DEV-456`, `BUG-789`
- Project key acts as a namespace
- Sequential IDs assigned by JIRA server (atomic)
- Multiple projects can have same sequential IDs without conflict
- Users can create issues in parallel without conflicts

### Strengths
- ✅ Namespace isolation prevents conflicts across projects
- ✅ Human-readable task references
- ✅ Clear project ownership and context
- ✅ Scales to many projects
- ✅ Sequential numbering preserved within namespace

### Limitations
- ❌ Requires project key management
- ❌ Still needs server-side assignment for sequential IDs
- ❌ More complex than pure sequential numbering

### Applicability to todo.ai
- **Partially applicable**: Namespace/prefix concept could work
- **Potential implementation**: Branch names or user prefixes could act as namespaces
- **Format example**: `feature-auth-1`, `feature-api-1`, `main-50`
- Sequential numbering still needs coordination within namespace

---

## Linear

### Approach
- **Team prefix + Sequential ID** (e.g., `ENG-123`)
- Similar to JIRA's project key approach
- Sequential numbering within team namespace
- Server-side assignment

### Implementation Details
- Format: `<TEAM_PREFIX>-<SEQUENTIAL_ID>`
- Example: `ENG-123`, `DESIGN-45`, `QA-67`
- Team prefix provides isolation
- Sequential IDs assigned by Linear's backend (atomic)
- Multiple teams can have overlapping sequential IDs
- Parallel issue creation without conflicts

### Strengths
- ✅ Team-based namespace isolation
- ✅ Clear ownership and context
- ✅ Human-readable references
- ✅ Prevents cross-team conflicts
- ✅ Sequential numbering within team

### Limitations
- ❌ Requires team/prefix configuration
- ❌ Server-side assignment needed
- ❌ More complex than simple sequential

### Applicability to todo.ai
- **Partially applicable**: Prefix concept is useful
- **Potential implementation**:
  - Branch names as prefixes: `feature-auth-1`, `feature-api-1`
  - User names as prefixes: `alice-1`, `bob-2`
  - Project sections as prefixes: `backend-1`, `frontend-1`
- **Note**: Sequential numbering still needs coordination within namespace

---

## Asana

### Approach
- **Project-based with optional numbering**
- Tasks have unique global IDs (not user-visible)
- Optional sequential numbering per project
- Server-side assignment

### Implementation Details
- Internal IDs are UUIDs or globally unique identifiers
- User-visible numbering is optional and project-scoped
- Sequential numbering is a display feature, not core identity
- No conflicts possible due to global unique IDs
- Display numbering can have gaps without issues

### Strengths
- ✅ Zero conflicts (unique global IDs)
- ✅ User-visible numbering is optional (can be sequential)
- ✅ Clean separation between identity and display
- ✅ Flexible numbering schemes

### Limitations
- ❌ Requires server-side infrastructure
- ❌ UUIDs are less human-friendly than sequential numbers
- ❌ Sequential numbering is not core identity

### Applicability to todo.ai
- **Conceptually applicable**: UUID approach could work
- **Potential approach**: UUIDs for internal identity, sequential numbers for display
- **Trade-off**: UUIDs are less human-friendly than simple sequential numbers
- **Implementation**: Internal UUID, display as `#50` (sequential)

---

## Trello

### Approach
- **Card IDs are UUIDs**
- No sequential numbering
- Unique identifiers assigned by server
- Human-visible numbering is optional and board-scoped

### Implementation Details
- Card IDs: long alphanumeric strings (UUIDs)
- No sequential numbering at all
- Short card IDs for URLs (e.g., `abc123`)
- These are unique but not sequential
- No numbering conflicts possible

### Strengths
- ✅ Zero conflicts (UUIDs are globally unique)
- ✅ No numbering coordination needed
- ✅ Works perfectly for distributed systems
- ✅ Offline-friendly

### Limitations
- ❌ UUIDs are not human-friendly (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- ❌ Cannot reference tasks with simple numbers
- ❌ Lose sequential numbering benefits (ordering, human readability)

### Applicability to todo.ai
- **Partially applicable**: UUID concept, but loses sequential benefits
- **Potential approach**: Use UUIDs for conflict-free identity, sequential for display
- **Trade-off**: Breaks existing workflow that relies on simple sequential numbers

---

## GitLab Issues

### Approach
- **Sequential numbering per project** (like GitHub)
- Server-side atomic assignment
- Issue numbers are sequential within project scope
- No conflicts possible (server assigns)

### Implementation Details
- Similar to GitHub Issues
- Sequential numbering: `#1`, `#2`, `#3`, etc.
- Server-side assignment ensures uniqueness
- Multiple users can create issues simultaneously
- Numbers assigned atomically

### Strengths
- ✅ Simple sequential numbering
- ✅ Zero conflicts
- ✅ Familiar pattern for users
- ✅ Works perfectly for collaboration

### Limitations
- ❌ Requires server-side infrastructure
- ❌ Not applicable to file-based systems without server

### Applicability to todo.ai
- **Conceptually applicable**: Sequential numbering is good
- **Key insight**: Need to simulate server-side atomic assignment
- **Potential approach**: Use Git commits as atomic assignment mechanism

---

## TaskWarrior (File-Based System)

### Approach
- **UUID-based task IDs**
- No sequential numbering
- Tasks identified by UUIDs
- Human-readable aliases are optional

### Implementation Details
- Tasks have UUIDs as core identity (e.g., `abc123-def456-...`)
- UUIDs stored in task files
- No sequential numbering
- No conflicts possible (UUIDs are unique)
- Works offline and distributed

### Strengths
- ✅ Zero conflicts
- ✅ Works perfectly offline
- ✅ Distributed-friendly
- ✅ No coordination needed

### Limitations
- ❌ UUIDs are not human-friendly
- ❌ Cannot reference tasks with simple numbers
- ❌ Loses sequential numbering benefits (ordering, human readability)

### Applicability to todo.ai
- **Partially applicable**: UUID approach could work
- **Trade-off**: todo.ai's strength is sequential numbering
- **Impact**: UUIDs would break existing workflow and human-friendly references

---

## Git-Based Coordination Approaches

### Git Commit as Atomic Assignment

### Approach
- **Use Git commits as coordination mechanism**
- Pull before assigning new task numbers
- Take MAX(local, remote) + 1
- Commit immediately after assignment

### Implementation Details
- Before assigning task number: `git pull`
- Compare local and remote highest task numbers
- Use MAX(local, remote) + 1 as next task number
- Commit assignment immediately
- This simulates atomic assignment via Git

### Strengths
- ✅ Works with file-based systems
- ✅ Uses existing Git workflow
- ✅ Simulates server-side atomic assignment
- ✅ Preserves sequential numbering
- ✅ Minimal conflicts

### Limitations
- ❌ Requires Git to be available
- ❌ Requires network access for pull
- ❌ Small window for conflicts (between pull and commit)

### Applicability to todo.ai
- **Highly applicable**: Uses existing Git infrastructure
- **Implementation**: Add `git pull` before task assignment
- **Conflicts**: Rare, but can be resolved with MAX logic

---

## Conventional Commit Message Format

### Approach
- **No task numbering in tool itself**
- Tasks referenced by commit messages
- External task tracking systems

### Implementation Details
- Tasks tracked in external systems (GitHub Issues, JIRA)
- Commit messages reference external task IDs
- No local task numbering conflicts
- Git handles merge conflicts naturally

### Strengths
- ✅ Uses existing Git workflow
- ✅ No numbering conflicts in local files
- ✅ Integrates with external tools

### Limitations
- ❌ Requires external task tracking system
- ❌ Not a self-contained solution
- ❌ Loses local task management benefits

### Applicability to todo.ai
- **Not applicable**: todo.ai needs local task numbering
- **Note**: But could integrate with external systems as enhancement

---

## Summary of Findings

### Common Patterns

1. **Server-Side Assignment** (GitHub, JIRA, Linear, Asana, GitLab)
   - **Pattern**: All use server-side assignment
   - **Result**: Zero conflicts possible
   - **Key Insight**: Atomic assignment is critical
   - **Applicability**: Can be simulated with Git as coordination layer

2. **UUID-Based Systems** (Trello, TaskWarrior)
   - **Pattern**: Use UUIDs instead of sequential numbers
   - **Result**: Zero conflicts (UUIDs are unique)
   - **Key Insight**: Unique IDs don't need coordination
   - **Applicability**: Loses human-friendly sequential numbering

3. **Namespace/Prefix Approaches** (JIRA, Linear)
   - **Pattern**: Prefix + Sequential ID
   - **Result**: Conflicts only within same namespace
   - **Key Insight**: Namespace isolation reduces conflict scope
   - **Applicability**: Could work with branch/user prefixes

4. **Git-Based Coordination**
   - **Pattern**: Use Git as coordination mechanism
   - **Result**: Git handles merge conflicts
   - **Key Insight**: Git can provide atomic-like assignment
   - **Applicability**: High - todo.ai already uses Git

---

## Key Insights for todo.ai

1. **Server-side assignment eliminates conflicts**: But requires server infrastructure
2. **UUIDs eliminate conflicts**: But lose sequential numbering benefits
3. **Namespaces reduce conflict scope**: Branch/user prefixes could work
4. **Git can simulate atomic assignment**: Using Git commits as coordination
5. **Sequential numbering is valuable**: Should be preserved if possible
6. **Merge-time resolution is acceptable**: Common pattern in file-based systems

---

## Recommended Approaches for todo.ai

### Option 1: Git-Based Atomic Assignment ⭐ (Recommended)
**Simulate server-side assignment using Git**

- **Mechanism**: Use Git as coordination layer
- **Process**:
  1. Pull latest changes before assigning task number
  2. Take MAX(local, remote) + 1 as next number
  3. Assign task with this number
  4. Commit immediately
- **Result**: Minimal conflicts, preserves sequential numbering
- **Trade-offs**: Requires Git, small window for conflicts

### Option 2: Namespace/Prefix Approach
**Use branch/user prefixes for isolation**

- **Mechanism**: Branch/user name as prefix
- **Format**: `feature-auth-1`, `feature-api-1`, `main-50`
- **Process**: Sequential numbering within namespace
- **Result**: Conflicts only within same namespace
- **Trade-offs**: More complex, less simple sequential

### Option 3: UUID + Sequential Display
**UUID for identity, sequential for display**

- **Mechanism**: Internal UUID, display sequential number
- **Format**: Internal: `abc123-def456`, Display: `#50`
- **Process**: Sequential numbers are display-only
- **Result**: No conflicts, maintains sequential appearance
- **Trade-offs**: More complex, UUIDs less human-friendly

### Option 4: Merge-Time Conflict Resolution
**Accept conflicts, resolve at merge time**

- **Mechanism**: Allow conflicts, auto-resolve at merge
- **Process**: Renumber conflicting tasks automatically
- **Result**: Simple, accepts conflicts as normal
- **Trade-offs**: Conflicts happen, require resolution

---

## Conclusion

Most professional task management tools use server-side assignment to prevent conflicts. For file-based systems like todo.ai, the most applicable approaches are:

1. **Git-based coordination** (simulating atomic assignment) ⭐ **Most recommended**
2. **Namespace/prefix isolation** (reducing conflict scope)
3. **Merge-time conflict resolution** (accepting conflicts and resolving)

The research suggests that **Git can serve as a coordination mechanism** to simulate server-side atomic assignment, which would be the most compatible with todo.ai's current design while maintaining sequential numbering and minimal changes to existing workflow.
