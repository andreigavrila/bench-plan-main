# Persistent data schema (technical reference)

This folder contains a technical reference for persistence rules and data shapes.

Important:
- The accompanying `storage-schema.ts` file is a **clear schema representation**, not a requirement to implement the product in TypeScript.
- This document may reference a current implementation’s field names and storage patterns, but a rebuild may use any technologies as long as it preserves the product behaviors and merge rules described here.

## Stored entities (conceptual)

### `Show` (movie or TV series)

**Purpose:** local representation of a catalog item plus user + AI annotations.

**Stored fields (non‑transient):**

- Identity
  - `id` *(String, required)*: primary key; stable identifier.
  - `title` *(String, required)*: display title.
  - `showType` *(ShowType, required)*: `"movie" | "tv" | "person" | "unknown"`.
  - `externalIds` *(Object?)*: optional external identifiers for catalog resolution (implementation-defined).
- Catalog meta
  - `overview` *(String?)*.
  - `genres` *([String], default `[]`)*: genre names (not IDs).
  - `tagline` *(String?)*.
  - `homepage` *(String?)*.
  - `originalLanguage` *(String?)*: catalog original language code.
  - `spokenLanguages` *([String], default `[]`)*: ISO 639‑1 codes.
  - `languages` *([String], default `[]`)*: catalog language codes.
- Images
  - `posterUrlString` *(String?)*: full poster URL.
  - `backdropUrlString` *(String?)*: full backdrop URL.
  - `logoUrlString` *(String?)*: full logo URL (best‑rated, prefer English).
  - `networkLogos` *([String], default `[]`)*: reserved; not currently populated.
- Ratings / popularity
  - `voteAverage` *(Double?)*, `voteCount` *(Int?)*, `popularity` *(Double?)*.
- Dates
  - `lastAirDate` *(Date?)*, `firstAirDate` *(Date?)*, `releaseDate` *(Date?)*.
- Movie‑specific
  - `runtime` *(Int?)*, `budget` *(Int?)*, `revenue` *(Int?)*.
- TV‑specific
  - `seriesStatus` *(String?)*: series availability/status string (catalog-defined).
  - `numberOfEpisodes` *(Int?)*, `numberOfSeasons` *(Int?)*.
  - `episodeRunTime` *([Int], default `[]`)*.
  - `lastEpisodeRunTime` *(Int?)*: reserved; not currently populated.
- User data (“my*”)
  - `myTags` *([String])* and `myTagsUpdateDate` *(Date?)*.
  - `myScore` *(Double?)* and `myScoreUpdateDate` *(Date?)*.
  - `myStatus` *(MyStatusType?)* and `myStatusUpdateDate` *(Date?)*.
  - `myInterest` *(MyInterestType?)* and `myInterestUpdateDate` *(Date?)*.
- AI data
  - `aiScoop` *(String?)* and `aiScoopUpdateDate` *(Date?)*.
- Management
  - `detailsUpdateDate` *(Date?)*: refreshed whenever external catalog details merged.
  - `creationDate` *(Date?)*: set when first created locally.
  - `isTest` *(Bool, default false)*.
- Providers
  - `providerData` *(ProviderData?)* stored as an opaque blob (implementation-defined).

**Not stored (transient):**
`cast`, `crew`, `seasons`, `images*`, `videos`, `recommendations`, `similar`, `lastEpisodeToAir`, `aiDescription`, `showTileState`, `isSelected`. These are fetched/mapped for UI but intentionally re‑pullable.

### `ProviderData` (embedded in `Show`)

This structure stores provider IDs by region. Exact storage mechanism is implementation-defined.

```
ProviderData {
  countries: {
    [countryCode: string]: {
      flatrate?: number[],
      rent?: number[],
      buy?: number[]
    }
  }
}
```

Stores only provider **IDs**, not full provider objects.

### `CloudSettings` (optional synced settings)

**Purpose:** app‑wide settings that may be synced across devices.

Fields:
- `id` *(String, default `"globalSettings"`)*.
- `userName` *(String)* random name on first launch.
- `version` *(Double)* epoch seconds; used for conflict resolution.
- `catalogApiKey` *(String?)*, `aiApiKey` *(String?)*.
- `aiModel` *(String)* model key/name.

### `AppMetadata`

**Purpose:** tracks data model version for migrations.

- `dataModelVersion` *(Int, default 3)*.

## Other persistent storage (key-value settings)

### Local settings

Stored keys:
- `autoSearch` *(Bool)*: whether Search opens automatically on launch (default is product-defined).
- `fontSize` *(String)*: one of `"XS" | "S" | "M" | "L" | "XL" | "XXL"`.

### UI state

Stored keys:
- `hideStatusRemovalConfirmation` *(Bool)*: if true, suppress “remove status” confirmation.
- `statusRemovalCountKey` *(Int)*: count of confirmations shown.
- `lastSelectedFilter` *(FilterConfiguration?)* encoded as JSON:
  - `{ type: "all" | "genre" | "myStatus" | "communityScore" | "decade" | "myTag", label: string, value: string }`.

## External catalog → Show mapping strategy

**High‑level flow:**
1. Decode external catalog payload into a fresh `Show`.
2. If a stored show with the same `id` exists, merge the new catalog show into it using the merge rules below.
3. Persist the merged stored show.

### Field mapping rules (conceptual)

- **IDs**
  - External catalog `id` → `Show.id`.
  - External IDs (if present) → `Show.externalIds` (or equivalent).
- **Title**
  - Prefer catalog title (movies) or series name (TV).
  - If neither exists, decoding fails.
- **Show type**
  - Catalog media type → `showType` / `mediaType`.
  - Else infer: if `name` exists → `.tv`, if `title` exists → `.movie`, else `.unknown` (reject).
- **Overview**
  - Catalog overview → `overview`.
- **Genres**
  - Map catalog genre identifiers to genre display names.
  - Stored as `[String]` of names.
- **Dates**
  - Parse dates using multiple accepted formats.
- **Ratings**
  - Store community score metrics and popularity directly (if provided).
- **Movie fields**
  - Store runtime/budget/revenue directly (if provided).
- **TV fields**
  - Store series status (if provided).
  - Store episode/season counts (if provided).
- **Images**
  - Map image references/paths to renderable URLs (or equivalent).
  - If multiple logos exist, choose a single “best” logo deterministically (rule is implementation-defined).
- **Spoken languages**
  - Store spoken language codes (if provided).
- **Providers**
  - Store provider availability by region (IDs only; provider metadata can be fetched separately).
- **Transient fetches**
  - `credits`, `seasons`, `videos`, `recommendations`, `similar`, `images.*` are decoded and attached to transient properties for UI but are not persisted.

### Merge / overwrite policy (important)

When external catalog data is merged into an existing stored show:

- **Non‑my fields** use `selectFirstNonEmpty(newValue, oldValue)`:
  - Never overwrite a non‑empty stored string/array with an empty string/empty array.
  - Never overwrite a non‑nil stored value with `nil`.
- **My fields** (`myTags`, `myScore`, `myStatus`, `myInterest`) resolve by timestamp:
  - If both sides have update dates, keep the newer.
  - If only one side has an update date, keep that side.
  - This preserves user edits across sync merges and catalog refreshes.
- `detailsUpdateDate` should be set to “now” after merge.
- `creationDate` is set only on first creation; catalog refreshes do not change it.
