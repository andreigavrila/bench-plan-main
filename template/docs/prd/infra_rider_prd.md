# Infrastructure & Execution Rider PRD (Benchmark Mode)

## 0. Purpose

This rider defines **how builds are expected to run, persist data, and remain isolated** when implementing the application described in `product_prd.md`.

It exists to:
- Reduce infrastructure friction (local + cloud build agents)
- Enable **repeatable benchmark runs**
- Prevent data collisions between runs/builds
- Preserve a clean migration path to future production hosting and authentication

This rider is intentionally scoped to **execution + data boundaries**, not product UX.

---

## 1. Non‑Goals

This rider does **not** prescribe:
- A permanent production backend (Supabase today does not mean Supabase forever)
- A permanent auth provider (Google OAuth is expected later but not required now)
- A fully offline-first architecture
- A specific UI framework beyond the benchmark baseline

---

## 2. Benchmark Baseline (Current Round)

For *this* benchmark round, builds MUST use:

- **Next.js (latest stable)** as the application runtime (UI + server boundary).
- **Supabase** as the persistence layer, accessed via official client libraries.

The Supabase instance may be **hosted** (preferred for cloud-agent runs) or **local** (optional for developer convenience). Builds MUST NOT assume Docker is available.

> If a future round swaps Supabase for another provider, the **behavioral requirements in this rider remain the same**.

---

## 3. Required Repo Deliverables

### 3.1 Environment variable interface
The repo MUST include:
- `.env.example` with all required variables (names + short comments)
- `.gitignore` that excludes `.env*` secrets (except `.env.example`)

The build MUST run by filling in environment variables, without editing source code.

**Credential handling rules**
- Secrets MUST NOT be committed to the repo.
- If using Supabase: browser/client code MUST use an **anon/public key**; any elevated key (e.g., service role) MUST be server-only.

### 3.2 One-command developer experience
The repo MUST include scripts (names flexible) that support:
- Start app
- Run tests
- Reset test data for a namespace/run

Examples (names are illustrative, not required):
- `npm run dev`
- `npm test`
- `npm run test:reset`

### 3.3 Database evolution artifacts
The repo MUST include a repeatable schema definition mechanism, such as:
- migrations, and optionally seed data / fixtures

The goal: a fresh database state can be created deterministically.

---

## 4. Identity & Isolation Model

### 4.1 Build/run namespace (required)
Each build MUST operate inside a **single stable namespace identifier** for its lifetime.

This identifier MAY be called `namespace_id`, `run_id`, `build_id`, etc.

The implementation MUST ensure:
- Two different namespaces do not read/write each other’s persisted data.
- Destructive testing operations are scoped to a namespace.

**Important:** The namespace is a *build isolation* primitive, not a user concept.

### 4.2 User identity (required)
Even if the benchmark is executed as “single user”:

- All user-owned persisted records MUST be associated with a `user_id` (or equivalent).
- The system MUST behave as if multiple users could exist (even if UI does not expose it yet).

`user_id` MUST be treated as an **opaque stable string** (or UUID).
Do not encode provider-specific meaning into it.

### 4.3 Relationship between namespace and user
Within a namespace, multiple users MAY exist.
At minimum, a single default user MAY exist.

When both are present, the effective partition is:
- `(namespace_id, user_id)`

---

## 5. Authentication Policy (Benchmark-Friendly)

### 5.1 Auth is not required to be “real” in benchmark mode
Benchmark builds MAY use a **development identity injection** mechanism (examples):
- `X-User-Id` header accepted by server routes in development/test
- a local dev-only “login as user” selector
- a fixed “default user” for the namespace in dev/test

This must be:
- clearly documented
- disabled or gated for production mode

### 5.2 Migration to real OAuth must be straightforward
The system MUST be designed so that replacing the dev identity mechanism with real OAuth later requires:
- configuration changes and auth wiring
- **not a schema redesign**

---

## 6. Data Ownership & Local Storage

### 6.1 Source of truth
Persisted user data MUST be stored server-side (i.e., in the configured persistence layer).
Clients MAY use caching for performance.

### 6.2 Cache is disposable
If a client uses local persistence/caching, it MUST be safe to:
- clear local storage
- reinstall the app

without losing user-owned data (within the namespace + backend).

---

## 7. Destructive Testing Rules

The system MUST support destructive testing without manual setup by:
- creating test data inside a namespace
- deleting/resetting test data inside that namespace

The system MUST NOT require global database teardown to reset tests.

---

## 8. “Cloud Agent” Compatibility

Docker MUST NOT be required to run the benchmark.

If Docker is used (e.g., for local Supabase), it MUST be optional and documented as such.

The primary supported path for cloud build agents is:
- connect to a provided hosted persistence instance
- use namespace isolation to avoid collisions
- run tests without privileged container access

---

## 9. Success Criteria

A build is compliant with this rider if:

- It provides `.env.example` and can be configured without code edits.
- It can run repeatedly without data collisions (namespace isolation).
- It associates all user-owned records with a `user_id`.
- It supports destructive test runs without global teardown.
- It can later adopt real OAuth without schema redesign.

