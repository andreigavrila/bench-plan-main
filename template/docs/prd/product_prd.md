# Product Requirements Document

This PRD was assembled by merging earlier drafts and cross‑checking against the current codebase. Where sources diverged, this document favors the clearest rule set and notes open questions.

This document is intentionally **name-, platform-, and technology-agnostic**.

**Benchmark context:** This PRD is used as a rubric to evaluate autonomous build systems over time. A separate *Infrastructure & Execution Rider PRD* defines the current benchmark baseline (e.g., local vs hosted execution), identity injection for testing, and run isolation to prevent collisions.


---

## 1. Product Summary

**What it is**  
A personal TV + movie companion for collecting, organizing, rating, and discovering entertainment. Users build *their version* of each show (status, interest, tags, rating, notes/AI scoop), and the app uses that taste profile to power multiple discovery paths:
- Traditional search/browse.
- Conversational AI (“Ask”).
- “Alchemy” blending based on shared concepts.
- Per‑show “Explore Similar” via AI concepts.

**Why it exists**  
People don’t just want to watch shows—they want to remember what they loved, keep an intentional watchlist, and get smart, personalized discovery. The app makes a user’s taste visible and actionable.

**Primary value**  
1) A clean personal library that feels like a living map of what you watch and want to watch.  
2) Discovery that is grounded in that library rather than generic recommendations.

---

## 2. Goals & Success

**Primary goals**
- Enable users to build and maintain a meaningful personal collection of shows/movies.
- Make organization effortless through statuses, interest levels, and free‑form tags.
- Provide high‑quality, taste‑aware discovery through AI and Alchemy.
- Keep user data consistent and durable everywhere a show appears.

**Example success indicators**
- Weekly active additions to the collection.
- Repeat usage of status/tag/rating updates (maintenance).
- AI → collection conversion (saves after Ask/Alchemy/Explore Similar).
- Alchemy sessions completed and chained.
- Retention driven by “what should I watch next?” use cases.

---

## 3. Non‑Goals / Explicit Exclusions

- No requirement for offline mode beyond normal network failure handling.
- No requirement that data live only on device (cloud sync is allowed).
- No need to mimic any legacy panel/popup mechanics; keep UX direct.
- Search does not require complex pre‑loading or caching; live queries are fine.
- No requirement to expose every internal data field in UI.

---

## 4. Core Concepts & Objects

### 4.1 Show (Movie or TV)

A “Show” is the canonical entertainment item (movie or TV series). It has:
- **Public / community data:** title, year, posters/backdrops/logos, genres, runtime or seasons/episodes, language(s), overview/tagline, community score, popularity, trailers/images, cast/crew, streaming availability, budget/revenue (movies), similar/recommended shows.
- **User overlay (“My Data”):**
  - **My Status** (relationship to the show).
  - **My Interest** (priority level when status is Later).
  - **My Tags** (free‑form labels/lists).
  - **My Rating** (user score, including “unrated” state).
  - **AI Scoop** (optional personality‑driven description/review).

**Display rule:** Whenever a show appears anywhere (lists, search, recommendations, AI outputs), if the user has a saved version, display the user‑overlaid version (status/tags/rating/scoop). User edits always win over refreshed public data.

### 4.2 Status System (“My Status”)

Saved shows always have a status. Core statuses:
- **Active**: currently watching.
- **Later**: saved for later; paired with an interest level.
- **Wait**: paused / waiting for a season or the right moment.
- **Done**: completed.
- **Quit**: abandoned.
- **(Optional/hidden) Next**: an “up‑next” queue. Present in data model but not currently surfaced as a first‑class UI status.

**Important nuance:** “Interested” and “Excited” are *interest levels* for Later, but they surface as primary chips in the status UI. Selecting either sets:
- `My Status = Later`
- `My Interest = Interested` or `Excited`

Removing all status removes the show from the collection and clears all My Data.

### 4.3 Interest Levels (“My Interest”)

Interest only applies when status is Later:
- **Interested**: mild/normal priority.
- **Excited**: high priority / “next up.”

If status changes away from Later, interest becomes irrelevant (but may be retained for when the show returns to Later).

### 4.4 Tags (User Lists)

Tags are free‑form user labels:
- A show can have many tags.
- Tags implicitly form a personal tag library.
- Tags power filters and grouping across the app.

### 4.5 Filters (Ways to View the Collection)

Filters are sidebar/menu views over the collection:
- **Quick/default:** All Shows.
- **Tag filters:** one per tag, plus “No tags” if any tagless shows exist.
- **Data filters:** genre, decade, community score ranges.
- **Media‑type toggle:** All / Movies / TV (applies on top of any filter).

### 4.6 AI Chat Session (“Ask”)

Conversational discovery mode:
- User asks for recommendations or talks about taste in natural language.
- Session maintains short‑term context; older turns may be summarized to preserve feel while controlling token depth.
- AI can mention shows inline; these become selectable items and appear in a “mentioned shows” row.

### 4.7 Alchemy Session

Structured discovery by blending multiple shows into concepts:
1. User selects 2+ starting shows (library + global catalog).
2. AI extracts shared/combined “concept catalysts” (themes, vibes, ingredients).
3. User selects 1–8 concepts.
4. AI returns 6 recommended shows grounded to real catalog items with short reasons.
5. User can chain another round using results as new inputs.

### 4.8 Explore Similar (Per‑Show Concepts)

From any Show Detail:
1. User selects **Get Concepts** to extract concepts for that single show.
2. User selects concepts.
3. User selects **Explore Shows** to fetch AI recommendations tied to real show objects.

### 4.9 AI Scoop (“The Scoop”)

Optional AI‑generated personality description:
- Spoiler‑safe by default.
- Generated on demand from Show Detail.
- Cached for freshness (current behavior: 4 hours).  
- Persisted only if the show is already in the user’s collection.

### 4.10 Person (Cast/Crew)

Person profiles are reachable from any show’s cast/crew:
- Image gallery, bio.
- Filmography/credits grouped by year.
- Lightweight analytics charts (average project ratings, top genres, projects‑by‑year).
- Tapping a credit opens that show’s Detail.

---

## 5. Data Behaviors & Business Rules

These rules define implicit saves, defaults, merge behavior, and removal semantics.

### 5.1 Collection Membership

**Definition:** A show is “in collection” when it has an assigned status (equivalently, a stored Show with non‑nil `My Status`).

### 5.2 Saving Triggers

Any of these actions save a show to the collection:
- Setting any status.
- Choosing an interest chip (Interested/Excited).
- Rating an unsaved show.
- Adding at least one tag to an unsaved show.

### 5.3 Default Values When Saving

When a show is saved without explicit status:
- Default status: `Later`
- Default interest: `Interested`

Exception:
- First save via rating defaults status to `Done` (rating implies watched).

### 5.4 Removing from Collection

Trigger:
- User clears status (reselects active status and confirms removal).

Effects:
- Show is removed from storage.
- All My Data cleared: status, interest, tags, rating, and AI Scoop.
- A warning confirmation is shown (with an option to stop asking after repeated removals).

### 5.5 Re‑adding the Same Show

If the user encounters a show already saved:
- Preserve their latest status, interest, tags, rating, and AI Scoop.
- Refresh public metadata as available.
- Merge conflicts resolve by most recent update timestamp per field.

### 5.6 Timestamps

Every user field tracks last modification time:
- `myStatusUpdateDate`
- `myInterestUpdateDate`
- `myTagsUpdateDate`
- `myScoreUpdateDate`
- `aiScoopUpdateDate`

Uses:
- Sorting (recently updated shows first where applicable).
- Cloud conflict resolution (newer wins).
- AI cache freshness.

### 5.7 AI Data Persistence

| AI data | Persisted? | Freshness | Notes |
|---|---|---|---|
| AI Scoop | Yes (if in collection) | 4 hours | Regenerates after expiry on demand. |
| Alchemy results/reasons | No | Session only | Cleared when leaving Alchemy. |
| Ask chat history | No | Session only | Cleared when resetting/leaving Ask. |
| Mentioned shows strip | No | Session only | Derived from current chat context. |

### 5.8 AI Recommendations Map to Real Shows

When AI returns recommendations:
- AI outputs title + external ID (if available) + media type.
- System looks up the external catalog by external ID (if provided) and accepts the first result whose title matches case‑insensitively.
- If found, the recommendation becomes a real selectable Show and can carry the AI “reason” as transient text.
- If not found, the title may be shown non‑interactive or handed off to Search.

### 5.9 Tile Indicators

Show tiles display lightweight badges:
- **In‑collection indicator** when `My Status` exists.
- **User rating indicator** when `My Rating` exists.

### 5.10 Data Sync & Integrity

The app may support optional cross‑device sync for the user’s collection and preferences. When sync is enabled:
- The library and settings remain consistent across devices.
- Conflicts resolve per field using the most recent edit timestamp.
- Duplicate items are detected and merged transparently, without user disruption.

### 5.11 Data Continuity Across Versions

The app must preserve user libraries across updates, even when the underlying data model changes. On upgrade, any existing saved shows and “My Data” are automatically brought forward into the new model in a safe, transparent way, without requiring user intervention. Users should never lose their collection, ratings, tags, statuses, interest levels, or AI Scoop due to an update.

---

## 6. App Structure & Navigation

**Top‑level layout**
- **Filters/navigation panel:** All Shows, tag filters, data filters.
- **Main content area:** Home (filtered library), Detail, Find/Discover, Person, Settings.

**Global entry points**
- Persistent **Find/Discover** entry point from primary navigation.
- Persistent **Settings** entry point from primary navigation.

**Find/Discover hub modes**
- Search (external catalog)
- Ask (AI chat)
- Alchemy (concept blending)

Mode switching uses a clear mode switcher.

---

## 7. Major Features

### 7.1 Collection Home

**Purpose:** Display the user’s library organized by relationship/status.

**Behavior**
- Shows matching the selected filter(s) are displayed.
- Library is grouped into status sections:
  1. Active (prominent / larger tiles)
  2. Excited (Later + Excited)
  3. Interested (Later + Interested)
  4. Other statuses (collapsed group): Wait, Quit, Done, and any unclassified Later items without interest.
- Media‑type toggle at top: All / Movies / TV.
- Tiles show poster, title, and My Data badges.

**Empty states**
- No shows in collection: prompt to Search/Ask.
- Filter yields none: “No results found.”

### 7.2 Search (Find → Search)

**Purpose:** Find shows in the global catalog.

**Behavior**
- Text search by title/keywords.
- Results in a poster grid.
- In‑collection items are marked.
- Selecting a show opens Detail.
- Search can be auto‑opened on launch if user enabled “Search on Launch.”

### 7.3 Ask (Find → Ask)

**Purpose:** Discover via conversation.

**Behavior**
- Chat UI with user/assistant turns.
- Friendly, opinionated, spoiler‑safe tone; honest about mixed reception.
- AI may mention shows inline; mentioned shows appear in a horizontal strip.
- Tapping a mentioned show opens Detail (or hands off to Search if mapping fails).
- Welcome view shows 6 random starter prompts; user can refresh.
- Conversation context retained during the session; older turns summarized automatically after ~10 messages.

**Variants**
- **General Ask:** started from Find.
- **Ask About a Show:** launched from a Show Detail “Ask about …” button. Requirement: seed the conversation with show context (exact prefill behavior TBD; current app switches into Ask mode with a handoff show).

### 7.4 Alchemy (Find → Alchemy)

**Purpose:** Structured blending discovery.

**Flow**
1. Select 2+ starting shows.
2. Tap **Conceptualize Shows**.
3. Select concept catalysts (max 8).
4. Tap **ALCHEMIZE!**
5. Review recommendations and optionally choose **More Alchemy!** to chain.

**UX**
- Step clarity (cards/sections).
- Backtracking allowed (changing shows clears concepts/results).

### 7.5 Show Detail Page

**Purpose:** Single source of truth for a show with My Data + discovery.

**Major sections**
1. **Header media:** backdrops/posters/logos and videos when available.
2. **Core facts:** year, runtime or seasons/episodes, genres, languages.
3. **Community score + My Rating:** rating slider; rating an unsaved show auto‑saves as Done.
4. **My Status + Interest:** status chips; setting status saves; reselecting removes after confirmation.
5. **My Tags:** tag display + picker; adding a tag to unsaved show auto‑saves as Later + Interested.
6. **Overview.**
7. **AI Scoop (“The Scoop”).**
8. **Traditional recommendations:** strand of similar/recommended shows.
9. **Explore Similar:** Get Concepts → select → Explore Shows (AI recs).
10. **Streaming availability.**
11. **Cast & Crew:** horizontal strands → Person Detail.
12. **Seasons (TV only).**
13. **Budget vs Revenue (movies when available).**

### 7.6 Person Detail Page

**Purpose:** Explore talent behind shows.

**Behavior**
- Image gallery, name, bio.
- Analytics charts (ratings, genres, projects‑by‑year).
- Filmography grouped by year.
- Selecting a credit opens Show Detail.

### 7.7 Settings & Your Data

**App settings**
- Font size / readability.
- Search on launch.

**User**
- Username (synced across devices if enabled).

**AI**
- AI provider API key (benchmark mode: may be provided via environment variables; storing/syncing user-entered keys is optional and must never be committed to the repo) (synced across devices if enabled).
- AI model selection (synced across devices if enabled).

**Integrations**
- Content catalog provider API key (synced across devices if enabled).

**Your data**
- **Export / Backup:** “Export My Data” produces a `.zip` containing a JSON backup of all saved shows and My Data. Dates encoded ISO‑8601.  
- **Import / Restore:** desired but not currently implemented; see Open Questions.

---

## 8. Cross‑Cutting Rules & Principles

1. **User’s version takes precedence** everywhere.
2. **Discovery must be actionable:** every recommendation maps to a selectable real show.
3. **Taste‑aware AI:** Ask/Alchemy/Explore Similar use library + My Data + session context.
4. **Spoiler‑safe by default** unless user explicitly requests spoilers.
5. **Implicit behaviors feel natural:** auto‑save and defaults should not surprise.
6. **Your data is yours:** export/backup is first‑class.
7. **Identity is explicit (even in single‑user benchmarks):** every user‑owned record MUST be scoped to a `user_id` (or equivalent). In benchmark/dev mode, `user_id` may be injected via configuration or a dev-only selector (no full OAuth flow required).
8. **Runs/builds are isolated:** each build MUST choose (or be assigned) a stable `namespace_id` (or equivalent) used to partition all persisted data and to scope destructive tests to that build only.
9. **Backend is the source of truth:** clients may cache for performance, but correctness must not depend on local persistence. Clearing client storage must not lose user data. Offline-first behavior is not required.

---

## 9. Key User Journeys

1. **Build collection**
   - Find → Search → open show → set Interested/Excited/Active → optionally tag/rate.
2. **Rate‑to‑save**
   - Search → open show → adjust rating → auto‑saved as Done.
3. **Tag‑to‑save**
   - Search → open show → add tag → auto‑saved as Later + Interested.
4. **Maintain collection**
   - Home → browse by status → update My Data from Detail.
5. **Tag‑driven organization**
   - Add tags → sidebar gains tag filters → select tag filter → Home shows matching items by status.
6. **Ask discovery**
   - Find → Ask → ask for a vibe → select a recommendation → save.
7. **Explore Similar**
   - Detail → Get Concepts → select → Explore Shows → save one.
8. **Alchemy**
   - Find → Alchemy → pick 3 favorites → Conceptualize → select catalysts → Alchemize → chain another round.
9. **Talent deep‑dive**
   - Detail → select a person → Person Detail → select a credit → new Detail.
10. **Backup**
   - Settings → Export My Data → save zip to local or cloud storage.

---

## 10. Open Questions / Optional Extensions

- Should **Next** become a first‑class status in UI?
- Should users create **named custom lists** beyond tags (e.g., “Weekend Watchlist”)?
- Should generating **AI Scoop** on an unsaved show implicitly save it?
- Should clearing My Rating store an explicit **Unrated** state vs nil?
- Add **Import/Restore** from export zip (Settings mentions this but UI is missing).
- Support saving/sharing **Alchemy sessions** as reusable “blends.”
- Add explicit **myStatus filters** in sidebar (model supports it).

---

## 11. Out of Scope (for this PRD)

- Detailed caching/offline strategy beyond current freshness rules.
- Low‑level data schema and migration details.
- Vendor‑specific API integration specs (provider-specific details).
- UI animation/micro‑interaction prescriptions.
- Full social or community features.

---

## 12. Companion Documents

This functional PRD describes *what* the app does and *how* it works. The following companion documents capture the personality, tone, and craft decisions that define *why* the app feels the way it does:

### `where_is_the_heart_opus.md`
**Problem statement:** Analysis of what this functional PRD misses—the "soul" gap that would cause a rebuild to lose the app's heart.

### `ai_personality_opus.md`
**AI Personality & Prompt Design Guide:** Full verbatim prompts with annotations, the base personality, feature-specific variations, the 80 starter prompts, the emotional chameleon behavior, the honesty principle, and prompt evolution guidelines.

Key topics covered:
- The Scoop system prompt and response structure
- Ask personality (basic and extended prompts)
- All 80 conversation starter prompts
- Alchemy concept extraction and recommendation prompts
- The concept/vibe philosophy
- Red lines that should never be crossed in prompt changes

### `philosophy_opus.md`
**Product Philosophy & Emotional Design Guide:** The "why" behind design decisions, emotional targets for each feature, and what makes the app distinct.

Key topics covered:
- Core philosophy: "Your taste made visible and actionable"
- The 5 design principles (with reasoning)
- Emotional design targets for each feature
- The status system philosophy
- The concept/vibe philosophy (vibes over genres)
- UI tone and copy guidelines
- What this app is NOT

---

**Together, these three documents provide a complete blueprint—not just for rebuilding the app, but for rebuilding it with its heart intact.**
