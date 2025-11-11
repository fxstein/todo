# GitHub API Analysis for Atomic Task Number Coordination

## Overview

This document analyzes GitHub's public APIs to identify options for atomic task number assignment and coordination in multi-user scenarios for `todo.ai`.

## Candidate APIs

### 1. GitHub Gists API

**URL:** `https://api.github.com/gists/{gist_id}`

**Endpoints:**
- `GET /gists/{gist_id}` - Retrieve gist content
- `PATCH /gists/{gist_id}` - Update gist content
- `POST /gists` - Create new gist

**Use Case:**
Store the current "next available task number" in a Gist file (e.g., `task_counter.txt`).

**Pros:**
- ✅ Simple file-based storage
- ✅ Version-controlled (history available)
- ✅ Can be private or public
- ✅ Accessible via GitHub CLI (`gh`)
- ✅ Works across all repositories (not tied to a specific repo)

**Cons:**
- ⚠️ **ETag/optimistic locking support unclear** - Need to verify if Gists API supports conditional requests
- ⚠️ **Rate limits:** 5,000 requests/hour (authenticated), 60 requests/hour (unauthenticated)
- ⚠️ **Concurrency handling:** May need retry logic for concurrent updates
- ⚠️ **Storage location:** Gists are separate from repository (may not be obvious to users)

**Implementation Example:**
```bash
# Get current number
current_num=$(gh api gists/GIST_ID --jq '.files.task_counter.txt.content' | tr -d '"' | head -n1)

# Increment and update
new_num=$((current_num + 1))
gh api -X PATCH gists/GIST_ID \
  --field "files[task_counter.txt][content]=$new_num"
```

**Atomicity:**
- ⚠️ **Not truly atomic** - Read-modify-write requires multiple API calls
- ⚠️ **Race conditions possible** - Two users can read same number, both increment
- ✅ **Can use retry logic** - Check if update succeeded, retry with new value on failure

---

### 2. GitHub Issues API ⭐ (BEST FOR FORKS)

**URL:** `https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}`

**Endpoints:**
- `GET /repos/{owner}/{repo}/issues/{issue_number}` - Retrieve issue
- `PATCH /repos/{owner}/{repo}/issues/{issue_number}` - Update issue (requires write access)
- `POST /repos/{owner}/{repo}/issues` - Create new issue
- `POST /repos/{owner}/{repo}/issues/{issue_number}/comments` - Comment on issue

**Use Case:**
Store the current "next available task number" in a dedicated Issue's body. **OR** use issue comments to append atomic updates.

**CRITICAL ADVANTAGE: Fork Contributors CAN Interact!**
- ✅ **Fork contributors CAN create/comment on upstream issues** - No write access needed!
- ✅ **Public repo access:** Only needs `public_repo` scope (not full write access)
- ✅ **Works for open source:** Fork contributors can participate in coordination
- ✅ **Read access sufficient:** Can create and comment on issues with just read access

**Pros:**
- ✅ **Fork-friendly:** Fork contributors can interact with upstream issues
- ✅ Repository-scoped (visible in repository)
- ✅ Accessible via GitHub CLI (`gh`)
- ✅ Integrates with repository workflow
- ✅ Can use labels, milestones for metadata
- ✅ **Lower permission requirement:** `public_repo` scope enough for public repos

**Cons:**
- ⚠️ **ETag/optimistic locking support unclear** - Need to verify conditional requests
- ⚠️ **Rate limits:** 5,000 requests/hour (authenticated)
- ⚠️ **Concurrency handling:** May need retry logic
- ⚠️ **Repository-specific** - Requires repository context
- ⚠️ **Issues are meant for bugs/features** - Using for coordination is unconventional
- ⚠️ **Cannot update existing issue** without write access (can only create/comment)

**Two Implementation Approaches:**

**Approach 1: Update Issue Body (Requires Write Access)**
```bash
# Get current number from issue body
current_num=$(gh api repos/:owner/:repo/issues/:issue_number --jq '.body' | grep -oP '\d+')

# Increment and update
new_num=$((current_num + 1))
gh api -X PATCH repos/:owner/:repo/issues/:issue_number \
  --field "body=Current next task number: $new_num"
```
- ⚠️ **Requires write access** - Only works for collaborators
- ⚠️ **Not suitable for forks** - Fork contributors cannot update

**Approach 2: Append Comments (Works for Forks!)**
```bash
# Get latest task number from issue comments
latest_comment=$(gh api repos/:owner/:repo/issues/:issue_number/comments --jq '.[0].body')

# Extract number from comment
current_num=$(echo "$latest_comment" | grep -oP '\d+')

# Increment and append as new comment
new_num=$((current_num + 1))
gh api -X POST repos/:owner/:repo/issues/:issue_number/comments \
  --field "body=Next task number: $new_num"
```
- ✅ **Works for fork contributors** - Can comment without write access
- ✅ **Atomic assignment possible** - Last comment wins
- ✅ **Works for open source** - Fork contributors can participate

**Atomicity:**
- ⚠️ **Not truly atomic** - Requires read-modify-write or read-comment
- ⚠️ **Race conditions possible** - Two users can read same number
- ✅ **Can use retry logic** - Check latest comment, retry if changed
- ✅ **Comment-based approach** - Last comment with highest number wins (simpler)

**This is the BEST option for fork-based workflows!**

---

### 3. Repository Contents API

**URL:** `https://api.github.com/repos/{owner}/{repo}/contents/{path}`

**Endpoints:**
- `GET /repos/{owner}/{repo}/contents/{path}` - Get file contents
- `PUT /repos/{owner}/{repo}/contents/{path}` - Create or update file

**Use Case:**
Store task number in a file within the repository (e.g., `.todo.ai/task_counter.txt`).

**Pros:**
- ✅ Repository-scoped (part of repository)
- ✅ Version-controlled via Git
- ✅ Accessible via GitHub CLI (`gh`)
- ✅ **Supports SHA-based updates** - Can use file SHA for optimistic locking!

**Cons:**
- ⚠️ **Requires repository context**
- ⚠️ **Rate limits:** 5,000 requests/hour (authenticated)
- ⚠️ **File must be committed** - Changes go through Git workflow

**SHA-Based Optimistic Locking:**
The Repository Contents API supports conditional updates using file SHA:
```bash
# Get file with SHA
file_info=$(gh api repos/:owner/:repo/contents/.todo.ai/task_counter.txt)
current_num=$(echo "$file_info" | jq -r '.content' | base64 -d)
file_sha=$(echo "$file_info" | jq -r '.sha')

# Increment and update with SHA (optimistic locking)
new_num=$((current_num + 1))
gh api -X PUT repos/:owner/:repo/contents/.todo.ai/task_counter.txt \
  --field "message=Increment task counter" \
  --field "content=$(echo -n "$new_num" | base64)" \
  --field "sha=$file_sha"
```

**Atomicity:**
- ✅ **Better atomicity** - SHA-based update prevents concurrent modifications
- ✅ **Optimistic locking** - Update fails if file changed (SHA mismatch)
- ✅ **Can retry on failure** - Fetch new SHA, retry update

**This is the most promising approach!**

---

### 4. GitHub Releases API

**URL:** `https://api.github.com/repos/{owner}/{repo}/releases`

**Endpoints:**
- `GET /repos/{owner}/{repo}/releases` - List releases
- `POST /repos/{owner}/{repo}/releases` - Create release
- `PATCH /repos/{owner}/{repo}/releases/{release_id}` - Update release

**Use Case:**
Use release version numbering as task numbers (not practical).

**Pros:**
- ✅ Version-controlled
- ✅ Repository-scoped

**Cons:**
- ❌ **Not suitable** - Releases are for software versions, not task coordination
- ❌ **Cannot atomically update** - Releases are immutable once published

---

### 5. GitHub Discussions API (Beta)

**URL:** `https://api.github.com/repos/{owner}/{repo}/discussions`

**Use Case:**
Store task number in a discussion post (not practical).

**Cons:**
- ❌ **Not suitable** - Discussions are for community conversations
- ❌ **Cannot atomically update** - Discussions are not designed for coordination

---

## Recommended Approach: Repository Contents API with SHA-Based Locking

**Why Repository Contents API is best:**

1. **SHA-Based Optimistic Locking:**
   - GitHub API returns file SHA with every GET request
   - PUT updates require the current SHA
   - If file changed, SHA mismatch causes update to fail
   - This provides optimistic locking for atomic updates

2. **Repository Integration:**
   - File is part of repository
   - Visible in repository structure
   - Version-controlled via Git
   - Changes show in Git history

3. **Implementation Pattern:**
   ```bash
   # Attempt atomic update with retry
   max_retries=5
   for attempt in $(seq 1 $max_retries); do
       # Get current state with SHA
       file_data=$(gh api repos/:owner/:repo/contents/.todo.ai/task_counter.txt)
       current_num=$(echo "$file_data" | jq -r '.content' | base64 -d)
       file_sha=$(echo "$file_data" | jq -r '.sha')
       
       # Increment
       new_num=$((current_num + 1))
       
       # Attempt update with SHA
       response=$(gh api -X PUT repos/:owner/:repo/contents/.todo.ai/task_counter.txt \
         --field "message=Increment task counter" \
         --field "content=$(echo -n "$new_num" | base64)" \
         --field "sha=$file_sha" 2>&1)
       
       # Check if update succeeded (no SHA mismatch)
       if echo "$response" | grep -q "sha"; then
           # Success - we got the new number atomically
           echo "$new_num"
           exit 0
       fi
       
       # SHA mismatch - file changed, retry
       sleep 0.1
   done
   
   # Failed after retries
   echo "ERROR: Could not update task counter after $max_retries attempts" >&2
   exit 1
   ```

4. **True Atomic Assignment:**
   - Each update attempt is atomic (single API call)
   - Optimistic locking prevents race conditions
   - Retry logic handles concurrent requests
   - Eventually succeeds when no other updates occur

**Authentication & Permissions Required:**

**Personal Access Tokens (Classic):**
- **Public repositories:** `public_repo` scope (grants read/write access to public repos)
- **Private repositories:** `repo` scope (grants full control over private repos)
- **Note:** `repo` scope is quite broad - grants full access to all repository contents, settings, and metadata

**Fine-Grained Personal Access Tokens:**
- **Contents** repository permission set to **"Read and write"**
- More granular control - can restrict to specific repositories
- Recommended for better security

**GitHub Apps:**
- **Contents** repository permission with **"Read and write"** access
- Required if using GitHub App authentication

**Security Considerations:**
- ⚠️ **Broad permissions:** `repo` scope grants full repository access (not just contents)
- ⚠️ **Token security:** Tokens must be stored securely (not in code, use environment variables)
- ⚠️ **Least privilege:** Fine-grained tokens are recommended for better security
- ⚠️ **Repository access:** User must have write access to the repository

**CRITICAL LIMITATION: Fork Access**

- ❌ **No write access to upstream:** Users working with forks **cannot** write to the upstream repository
- ❌ **Only fork write access:** Fork contributors can only write to their own fork
- ❌ **Breaks single source of truth:** Counter file in upstream cannot be updated by fork contributors
- ❌ **Collaborators only:** Only repository collaborators/maintainers can update upstream counter

**Impact:**
- ✅ **Works for collaborators:** Repository contributors/maintainers can use this approach
- ❌ **Does NOT work for forks:** Fork contributors cannot update upstream counter file
- ⚠️ **Limited applicability:** Only viable for repositories where all users are collaborators
- ⚠️ **Not suitable for open source:** Cannot work with public repositories where contributors use forks

**This is a major limitation for open-source or public repository scenarios where contributors use forks!**

**Limitations:**
- ❌ **CRITICAL: No fork write access** - Fork contributors cannot write to upstream repository
- ❌ **Collaborators only** - Only repository collaborators can update counter file
- ⚠️ **Requires repository context** - Must know repository owner/name
- ⚠️ **File must be committed** - Changes go through Git (can be automated)
- ⚠️ **Rate limits:** 5,000 requests/hour (authenticated)
- ⚠️ **Network required** - Cannot work offline
- ⚠️ **Authentication required** - GitHub tokens needed for all users
- ⚠️ **Not suitable for open source** - Public repos with fork-based contributions won't work

**Trade-offs:**
- ✅ **Provides true atomic assignment** - Much better than Git-based coordination
- ✅ **Optimistic locking** - Prevents race conditions
- ✅ **Repository integration** - File is visible in repository
- ⚠️ **Requires authentication** - GitHub tokens needed
- ⚠️ **Requires network** - Cannot work offline

---

## Comparison Table

| API | Atomic Assignment | Optimistic Locking | Repository Scope | Fork Support | Rate Limit |
|-----|------------------|-------------------|------------------|--------------|------------|
| **Issues (Comments)** | ⚠️ Partial | ❌ No (retry only) | ✅ Yes | ✅ **YES** | 5,000/hr |
| **Repository Contents** | ✅ Yes (with SHA) | ✅ Yes (SHA-based) | ✅ Yes | ❌ No | 5,000/hr |
| Gists | ⚠️ Partial | ❌ No (retry only) | ❌ No | ⚠️ Partial | 5,000/hr |
| Issues (Update) | ⚠️ Partial | ❌ No (retry only) | ✅ Yes | ❌ No | 5,000/hr |
| Git-based | ❌ No | ❌ No | ✅ Yes | ❌ No | N/A |

---

## Implementation Recommendation

### Option A: Repository Contents API (For Collaborators Only)

**Use Repository Contents API with SHA-based optimistic locking:**

1. **Store counter file:** `.todo.ai/task_counter.txt` in repository
2. **Atomic update pattern:**
   - GET file with SHA
   - Increment number
   - PUT update with SHA (optimistic lock)
   - Retry on SHA mismatch (concurrent update detected)
3. **Benefits:**
   - True atomic assignment
   - Optimistic locking prevents race conditions
   - Repository-integrated
4. **Limitations:**
   - ❌ **Does NOT work with forks** - Fork contributors cannot update upstream file
   - ✅ **Only for collaborators** - Users must have write access

### Option B: Issues API with Comments (For Forks!) ⭐ RECOMMENDED FOR OPEN SOURCE

**Use GitHub Issues API with comment-based coordination:**

1. **Create dedicated coordination issue:** e.g., "Task Number Coordination" in repository
2. **Atomic assignment pattern:**
   - GET latest comment from coordination issue
   - Extract current task number from comment
   - Increment number
   - POST new comment with incremented number
   - Retry if latest comment changed (concurrent update detected)
3. **Benefits:**
   - ✅ **Works with forks!** - Fork contributors can comment on upstream issues
   - ✅ **Lower permissions** - Only needs `public_repo` scope (not write access)
   - ✅ **Open source friendly** - Fork contributors can participate
   - ✅ **Repository-integrated** - Visible in repository issues
   - ✅ **Simple coordination** - Last comment with highest number wins
4. **Limitations:**
   - ⚠️ **Not truly atomic** - Race conditions possible (can retry)
   - ⚠️ **Comment-based** - Requires parsing comments for numbers
   - ⚠️ **Rate limits** - 5,000 requests/hour

**For fork-based workflows, Issues API with comments is the BEST option!**

---

## Security & Permissions Summary

**Required Permissions for Repository Contents API:**

| Authentication Method | Required Permission | Scope |
|----------------------|---------------------|-------|
| **Classic PAT (Public Repo)** | `public_repo` scope | Read/write to public repos |
| **Classic PAT (Private Repo)** | `repo` scope | Full access to private repos |
| **Fine-Grained PAT** | Contents: Read and write | Repository-specific |
| **GitHub App** | Contents: Read and write | App-specific |

**Security Best Practices:**
1. **Use fine-grained tokens** - More granular, repository-specific permissions
2. **Store tokens securely** - Environment variables, not in code
3. **Rotate tokens regularly** - Periodic token rotation for security
4. **Minimal permissions** - Only grant necessary permissions (Contents: Read/write)
5. **Repository access control** - Users must have write access to repository

**User Requirements:**
- ✅ Users need GitHub account
- ✅ Users need GitHub CLI (`gh`) installed and authenticated
- ✅ Users need write access to repository
- ✅ Users need appropriate token with Contents permissions

---

## Alternative: Free Cloud APIs & Storage Services

Beyond GitHub APIs, several free cloud APIs and storage services provide atomic counter coordination capabilities:

### 1. CounterAPI ⭐ (DEDICATED COUNTER SERVICE)

**URL:** `https://api.counterapi.dev/v1/`

**Service:** Dedicated counting/counter API service

**Pros:**
- ✅ **Designed for counting** - Purpose-built for counter use cases
- ✅ **Free tier** - Unlimited API access on free plan
- ✅ **REST API** - Simple HTTP requests
- ✅ **No authentication required** - Works without tokens (for basic usage)
- ✅ **Atomic operations** - Built-in atomic increment
- ✅ **Works from anywhere** - Not tied to GitHub or repositories

**Cons:**
- ⚠️ **Third-party dependency** - Relies on external service
- ⚠️ **Service availability** - Depends on CounterAPI being online
- ⚠️ **Not repository-integrated** - Counter is separate from repository

**Example Usage:**
```bash
# Get current value
current_num=$(curl -s "https://api.counterapi.dev/v1/NAMESPACE/COUNTER_NAME" | jq '.value')

# Increment atomically
new_num=$(curl -s -X POST "https://api.counterapi.dev/v1/NAMESPACE/COUNTER_NAME/up" | jq '.value')
```

**Feasibility:** Very promising - dedicated service for this exact use case!

---

### 2. Abacus (Free Counting API)

**URL:** `https://v2.jasoncameron.dev/abacus/api/`

**Service:** Free counting API with namespaces

**Pros:**
- ✅ **Free counting API** - Purpose-built for counters
- ✅ **Namespace support** - Can organize counters by namespace
- ✅ **REST API** - Simple HTTP requests
- ✅ **Optional expiration** - Counters can have expiration dates

**Cons:**
- ⚠️ **Third-party dependency** - Relies on external service
- ⚠️ **Service availability** - Depends on service being online
- ⚠️ **Not repository-integrated** - Counter is separate from repository

**Feasibility:** Good option - similar to CounterAPI

---

### 3. Firebase Firestore

**URL:** `https://firestore.googleapis.com/v1/`

**Service:** Google's NoSQL database with free tier

**Pros:**
- ✅ **Atomic transactions** - True atomic read-modify-write operations
- ✅ **Free tier** - Generous free quota (50K reads/day, 20K writes/day)
- ✅ **Google infrastructure** - Highly reliable and scalable
- ✅ **SDK support** - Official SDKs for many languages
- ✅ **Real-time sync** - Can listen to changes in real-time

**Cons:**
- ⚠️ **Requires Google account** - Users need Firebase project setup
- ⚠️ **Authentication needed** - Requires Firebase authentication
- ⚠️ **Not repository-integrated** - Counter is separate from repository
- ⚠️ **More complex setup** - Requires Firebase project configuration

**Example Usage:**
```javascript
// Using Firebase Admin SDK
const counterRef = db.collection('counters').doc('taskCounter');
const newValue = await db.runTransaction(async (transaction) => {
    const counter = await transaction.get(counterRef);
    const newCount = (counter.data()?.value || 0) + 1;
    transaction.update(counterRef, { value: newCount });
    return newCount;
});
```

**Feasibility:** Excellent atomic operations, but requires Firebase setup

---

### 4. Cloudflare Durable Objects

**URL:** Cloudflare Workers with Durable Objects

**Service:** Cloudflare's edge computing with transactional storage

**Pros:**
- ✅ **Atomic operations** - Strong consistency guarantees
- ✅ **Free tier** - Generous free quota
- ✅ **Global distribution** - Low latency worldwide
- ✅ **Transactional storage** - Built-in atomic operations

**Cons:**
- ⚠️ **Requires Cloudflare account** - Users need Cloudflare setup
- ⚠️ **More complex** - Requires Workers deployment
- ⚠️ **Not repository-integrated** - Counter is separate from repository
- ⚠️ **JavaScript/TypeScript** - Primarily for Workers platform

**Feasibility:** Good atomic operations, but requires Cloudflare platform

---

### 5. JSONBin.io

**URL:** `https://api.jsonbin.io/v3/`

**Service:** Free JSON storage API

**Pros:**
- ✅ **Free tier** - Free JSON storage
- ✅ **REST API** - Simple HTTP requests
- ✅ **JSON-based** - Easy to store counter data
- ✅ **Version history** - Tracks changes over time

**Cons:**
- ⚠️ **Not truly atomic** - Requires read-modify-write with retry
- ⚠️ **Rate limits** - Free tier has rate limits
- ⚠️ **Third-party dependency** - Relies on external service
- ⚠️ **Not repository-integrated** - Counter is separate from repository

**Feasibility:** Good for simple storage, but not atomic by default

---

### 6. Google Sheets API

**URL:** `https://sheets.googleapis.com/v4/`

**Service:** Google Sheets as database

**Pros:**
- ✅ **Free tier** - Google Sheets is free
- ✅ **Familiar interface** - Users can see/edit in spreadsheet
- ✅ **REST API** - Simple HTTP requests
- ✅ **Visible/auditable** - Changes visible in spreadsheet

**Cons:**
- ⚠️ **Not truly atomic** - Requires read-modify-write with retry
- ⚠️ **Requires OAuth** - Google authentication needed
- ⚠️ **Rate limits** - API has rate limits
- ⚠️ **Slower** - Not optimized for high-frequency updates

**Feasibility:** Usable but not ideal - not atomic by default

---

## Comparison: Free Cloud APIs vs GitHub APIs

| Service | Atomic Operations | Free Tier | Fork Support | Repository Integration | Setup Complexity |
|---------|------------------|-----------|--------------|------------------------|------------------|
| **CounterAPI** | ✅ Yes | ✅ Unlimited | ✅ Yes | ❌ No | ⭐ Very Easy |
| **Abacus** | ✅ Yes | ✅ Free | ✅ Yes | ❌ No | ⭐ Very Easy |
| **Firebase Firestore** | ✅ Yes | ✅ 50K reads/day | ✅ Yes | ❌ No | ⚠️ Medium |
| **Cloudflare Durable** | ✅ Yes | ✅ Free tier | ✅ Yes | ❌ No | ⚠️ Complex |
| **JSONBin.io** | ⚠️ Partial | ✅ Free | ✅ Yes | ❌ No | ⭐ Easy |
| **GitHub Issues (Comments)** | ⚠️ Partial | ✅ Free | ✅ Yes | ✅ Yes | ⭐ Easy |
| **GitHub Contents** | ✅ Yes | ✅ Free | ❌ No | ✅ Yes | ⭐ Easy |

---

## Recommendation: CounterAPI or Abacus for Simple Counter Use

**For a simple, dedicated counter service:**

1. **CounterAPI or Abacus** - Purpose-built for counters, very easy to use
   - ✅ Simple REST API
   - ✅ No authentication needed (basic usage)
   - ✅ Atomic operations built-in
   - ✅ Works for forks (no repository dependency)
   - ⚠️ Third-party dependency (service availability risk)

2. **Firebase Firestore** - For more robust needs
   - ✅ True atomic transactions
   - ✅ Free tier with generous limits
   - ✅ Google infrastructure (highly reliable)
   - ⚠️ Requires Firebase setup

3. **GitHub Issues API** - For repository integration
   - ✅ Repository-integrated
   - ✅ Works for forks
   - ✅ Visible in repository
   - ⚠️ Not truly atomic (can retry)

**Best Overall Option:**
- **CounterAPI or Abacus** - If you want simplest solution, dedicated counter service
- **GitHub Issues API** - If you want repository integration
- **Firebase Firestore** - If you need true atomic transactions and don't mind setup

---

## Next Steps

1. **Verify SHA-based locking** - Test with concurrent requests to confirm optimistic locking works
2. **Design counter file structure** - Format and location of task counter file
3. **Implement retry logic** - Handle SHA mismatches gracefully
4. **Design error handling** - Network failures, rate limits, authentication errors
5. **Design authentication flow** - Token validation, error messages for missing permissions
6. **Consider fallback** - What happens if API unavailable (offline mode)
7. **Security documentation** - Guide for users on setting up tokens and permissions
8. **Evaluate CounterAPI/Abacus** - Test dedicated counter services as alternative to GitHub APIs

