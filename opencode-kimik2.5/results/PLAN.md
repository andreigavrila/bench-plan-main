# Implementation Plan: Personal TV + Movie Companion App

## Executive Summary

This document outlines the implementation plan for a personal TV and movie companion application. The app enables users to collect, organize, rate, and discover entertainment through a combination of manual curation and AI-powered discovery features.

**Core Stack:** Next.js (latest stable) + Supabase + TypeScript
**Architecture Pattern:** Fractal (Pages → Features → Sub-features)

---

## 1. Project Foundation

### 1.1 Repository Setup

**Files to Create:**
- `.env.example` - All required environment variables with comments
- `.gitignore` - Exclude `.env*` files (except `.env.example`)
- `package.json` - Dependencies and scripts
- `next.config.js` - Next.js configuration
- `tsconfig.json` - TypeScript configuration

**Required Environment Variables:**
```
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=           # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=      # Supabase anon/public key (browser-safe)
SUPABASE_SERVICE_ROLE_KEY=          # Service role key (server-only)

# AI Provider Configuration
AI_PROVIDER_API_KEY=                # OpenAI/Anthropic/etc API key
AI_MODEL=                           # Model identifier (e.g., gpt-4o)

# Content Catalog Provider
CATALOG_API_KEY=                    # TMDB or similar provider API key

# Benchmark/Development
NAMESPACE_ID=                       # Build/run isolation identifier
DEFAULT_USER_ID=                    # Dev-only user identity injection
```

**Scripts Required:**
- `npm run dev` - Start development server
- `npm run build` - Production build
- `npm test` - Run test suite
- `npm run test:reset` - Reset test data for namespace
- `npm run db:migrate` - Run database migrations
- `npm run db:seed` - Seed database with fixtures

### 1.2 Database Schema (Supabase)

**Migration Files:**

**001_create_shows_table.sql:**
```sql
create table shows (
  id uuid primary key default gen_random_uuid(),
  namespace_id text not null,
  user_id text not null,
  
  -- Identity
  external_id text,
  title text not null,
  show_type text not null check (show_type in ('movie', 'tv', 'person', 'unknown')),
  external_ids jsonb default '{}',
  
  -- Catalog meta
  overview text,
  genres text[] default '{}',
  tagline text,
  homepage text,
  original_language text,
  spoken_languages text[] default '{}',
  languages text[] default '{}',
  
  -- Images
  poster_url text,
  backdrop_url text,
  logo_url text,
  network_logos text[] default '{}',
  
  -- Ratings
  vote_average numeric,
  vote_count integer,
  popularity numeric,
  
  -- Dates
  last_air_date date,
  first_air_date date,
  release_date date,
  
  -- Movie-specific
  runtime integer,
  budget bigint,
  revenue bigint,
  
  -- TV-specific
  series_status text,
  number_of_episodes integer,
  number_of_seasons integer,
  episode_run_time integer[] default '{}',
  last_episode_run_time integer,
  
  -- User data ("My Data")
  my_tags text[] default '{}',
  my_tags_update_date timestamptz,
  my_score numeric,
  my_score_update_date timestamptz,
  my_status text check (my_status in ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_update_date timestamptz,
  my_interest text check (my_interest in ('excited', 'interested')),
  my_interest_update_date timestamptz,
  
  -- AI data
  ai_scoop text,
  ai_scoop_update_date timestamptz,
  
  -- Management
  details_update_date timestamptz,
  creation_date timestamptz default now(),
  is_test boolean default false,
  
  -- Provider data
  provider_data jsonb default '{}',
  
  -- Constraints
  constraint unique_user_show unique (namespace_id, user_id, external_id)
);

-- Indexes for performance
create index idx_shows_namespace_user on shows(namespace_id, user_id);
create index idx_shows_status on shows(namespace_id, user_id, my_status);
create index idx_shows_external on shows(external_id);
```

**002_create_settings_tables.sql:**
```sql
create table cloud_settings (
  id text primary key default 'globalSettings',
  namespace_id text not null,
  user_id text not null,
  user_name text not null,
  version numeric not null,
  catalog_api_key text,
  ai_api_key text,
  ai_model text not null,
  updated_at timestamptz default now(),
  
  constraint unique_user_settings unique (namespace_id, user_id)
);

create table app_metadata (
  namespace_id text primary key,
  data_model_version integer default 3,
  updated_at timestamptz default now()
);
```

**003_create_rls_policies.sql:**
```sql
-- Enable RLS
alter table shows enable row level security;
alter table cloud_settings enable row level security;

-- Shows: Users can only access their own namespace + user data
create policy shows_isolation_policy on shows
  for all
  using (namespace_id = current_setting('app.namespace_id', true)::text 
         and user_id = current_setting('app.user_id', true)::text);

-- Settings: Users can only access their own settings
create policy settings_isolation_policy on cloud_settings
  for all
  using (namespace_id = current_setting('app.namespace_id', true)::text 
         and user_id = current_setting('app.user_id', true)::text);
```

### 1.3 Project Structure

```
src/
├── config/
│   ├── constants.ts           # Global constants (statuses, interests, etc.)
│   ├── env.ts                 # Environment variable validation
│   └── theme.ts               # Design tokens
├── lib/
│   ├── supabase/
│   │   ├── client.ts          # Browser client
│   │   ├── server.ts          # Server-side client
│   │   └── admin.ts           # Service role client (server-only)
│   ├── ai/
│   │   ├── client.ts          # AI provider client
│   │   ├── prompts/
│   │   │   ├── scoop.ts       # The Scoop prompt
│   │   │   ├── ask.ts         # Ask chat prompts
│   │   │   ├── concepts.ts    # Concept extraction prompts
│   │   │   └── recommend.ts   # Recommendation prompts
│   │   └── parsers.ts         # Response parsers
│   └── catalog/
│       ├── client.ts          # Content catalog client (TMDB/etc)
│       ├── types.ts           # Catalog response types
│       └── mappers.ts         # Catalog → Show mappers
├── types/
│   └── index.ts               # Shared TypeScript types
├── utils/
│   ├── date.ts                # Date formatting utilities
│   ├── merge.ts               # Show merge logic
│   └── filters.ts             # Collection filtering logic
├── hooks/
│   ├── useAuth.ts             # Authentication/identity hook
│   ├── useNamespace.ts        # Namespace context hook
│   └── useSupabase.ts         # Supabase client hook
├── components/
│   ├── ui/                    # Shared UI primitives
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Chip/
│   │   ├── Input/
│   │   ├── Slider/
│   │   ├── Tile/
│   │   └── Modal/
│   └── shared/                # Shared feature components
│       ├── ShowTile/
│       ├── ShowGrid/
│       ├── StatusChips/
│       ├── RatingControl/
│       ├── TagPicker/
│       └── StreamProvider/
└── pages/
    ├── layout.tsx             # Root layout with providers
    ├── page.tsx               # Home/Collection page
    ├── globals.css
    ├── api/                   # API routes
    │   ├── ai/
    │   │   ├── scoop/route.ts
    │   │   ├── ask/route.ts
    │   │   ├── concepts/route.ts
    │   │   └── recommend/route.ts
    │   ├── catalog/
    │   │   ├── search/route.ts
    │   │   ├── details/route.ts
    │   │   └── person/route.ts
    │   └── export/route.ts
    ├── find/
    │   └── Find/
    │       ├── Find.tsx
    │       └── features/
    │           ├── SearchMode/
    │           ├── AskMode/
    │           └── AlchemyMode/
    ├── show/
    │   └── [id]/
    │       └── ShowDetail/
    │           ├── ShowDetail.tsx
    │           └── features/
    │               ├── HeaderMedia/
    │               ├── CoreFacts/
    │               ├── MyRelationship/
    │               ├── OverviewScoop/
    │               ├── AskAboutShow/
    │               ├── Recommendations/
    │               ├── ExploreSimilar/
    │               ├── StreamingProviders/
    │               ├── CastCrew/
    │               └── Seasons/
    ├── person/
    │   └── [id]/
    │       └── PersonDetail/
    │           ├── PersonDetail.tsx
    │           └── features/
    │               ├── ProfileHeader/
    │               ├── Filmography/
    │               └── Analytics/
    └── settings/
        └── Settings/
            ├── Settings.tsx
            └── features/
                ├── AppSettings/
                ├── UserSettings/
                ├── AISettings/
                └── DataManagement/
```

---

## 2. Shared Infrastructure

### 2.1 Types Definition

**src/types/index.ts:**
```typescript
export type ShowType = 'movie' | 'tv' | 'person' | 'unknown';

export type MyStatusType = 'active' | 'next' | 'later' | 'done' | 'quit' | 'wait';

export type MyInterestType = 'excited' | 'interested';

export type FilterType = 
  | 'all' 
  | 'genre' 
  | 'myStatus' 
  | 'communityScore' 
  | 'decade' 
  | 'myTag';

export interface Show {
  id: string;
  externalId?: string;
  title: string;
  showType: ShowType;
  externalIds?: Record<string, string>;
  
  // Catalog meta
  overview?: string;
  genres: string[];
  tagline?: string;
  homepage?: string;
  originalLanguage?: string;
  spokenLanguages: string[];
  languages: string[];
  
  // Images
  posterUrl?: string;
  backdropUrl?: string;
  logoUrl?: string;
  networkLogos: string[];
  
  // Ratings
  voteAverage?: number;
  voteCount?: number;
  popularity?: number;
  
  // Dates
  lastAirDate?: string;
  firstAirDate?: string;
  releaseDate?: string;
  
  // Movie-specific
  runtime?: number;
  budget?: number;
  revenue?: number;
  
  // TV-specific
  seriesStatus?: string;
  numberOfEpisodes?: number;
  numberOfSeasons?: number;
  episodeRunTime: number[];
  lastEpisodeRunTime?: number;
  
  // User data
  myTags: string[];
  myTagsUpdateDate?: string;
  myScore?: number;
  myScoreUpdateDate?: string;
  myStatus?: MyStatusType;
  myStatusUpdateDate?: string;
  myInterest?: MyInterestType;
  myInterestUpdateDate?: string;
  
  // AI data
  aiScoop?: string;
  aiScoopUpdateDate?: string;
  
  // Management
  detailsUpdateDate?: string;
  creationDate?: string;
  isTest: boolean;
  
  // Providers
  providerData?: ProviderData;
  
  // Transient (not persisted)
  cast?: CastMember[];
  crew?: CrewMember[];
  seasons?: Season[];
  videos?: Video[];
  recommendations?: ShowSummary[];
  similar?: ShowSummary[];
}

export interface ProviderData {
  countries: Record<string, {
    flatrate?: number[];
    rent?: number[];
    buy?: number[];
  }>;
}

export interface CastMember {
  id: string;
  name: string;
  character?: string;
  profileUrl?: string;
  order: number;
}

export interface CrewMember {
  id: string;
  name: string;
  job: string;
  department: string;
  profileUrl?: string;
}

export interface Season {
  seasonNumber: number;
  name: string;
  overview?: string;
  episodeCount: number;
  airDate?: string;
  posterUrl?: string;
}

export interface Video {
  key: string;
  name: string;
  site: string;
  type: string;
}

export interface ShowSummary {
  id: string;
  title: string;
  showType: ShowType;
  posterUrl?: string;
  releaseDate?: string;
}

export interface Person {
  id: string;
  name: string;
  biography?: string;
  profileUrl?: string;
  knownForDepartment?: string;
  birthday?: string;
  deathday?: string;
  placeOfBirth?: string;
  credits: PersonCredit[];
}

export interface PersonCredit {
  id: string;
  title: string;
  showType: ShowType;
  character?: string;
  job?: string;
  releaseDate?: string;
  posterUrl?: string;
}

export interface FilterConfiguration {
  type: FilterType;
  label: string;
  value: string;
}

export interface CloudSettings {
  id: string;
  userName: string;
  version: number;
  catalogApiKey?: string;
  aiApiKey?: string;
  aiModel: string;
}

export interface LocalSettings {
  autoSearch: boolean;
  fontSize: 'XS' | 'S' | 'M' | 'L' | 'XL' | 'XXL';
}

export interface Concept {
  id: string;
  label: string;
}

export interface AIRecommendation {
  externalId: string;
  title: string;
  mediaType: ShowType;
  reason: string;
}
```

### 2.2 Configuration Constants

**src/config/constants.ts:**
```typescript
// Status configuration
export const STATUS_CONFIG = {
  active: { label: 'Active', color: 'blue' },
  next: { label: 'Next', color: 'purple' },
  later: { label: 'Later', color: 'amber' },
  done: { label: 'Done', color: 'green' },
  quit: { label: 'Quit', color: 'red' },
  wait: { label: 'Wait', color: 'gray' },
} as const;

// Interest configuration
export const INTEREST_CONFIG = {
  excited: { label: 'Excited', color: 'rose' },
  interested: { label: 'Interested', color: 'amber' },
} as const;

// AI freshness timeouts (in milliseconds)
export const AI_FRESHNESS = {
  scoop: 4 * 60 * 60 * 1000, // 4 hours
} as const;

// Pagination defaults
export const PAGINATION = {
  searchResults: 20,
  collectionInitial: 50,
  recommendations: 10,
  castCrew: 20,
} as const;

// UI constants
export const UI = {
  maxConceptsSelectable: 8,
  exploreSimilarRecs: 5,
  alchemyRecs: 6,
  maxChatHistory: 10,
} as const;
```

### 2.3 Supabase Clients

**src/lib/supabase/client.ts:**
```typescript
import { createBrowserClient } from '@supabase/ssr';
import { Database } from './database.types';

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

**src/lib/supabase/server.ts:**
```typescript
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import { Database } from './database.types';

export function createClient() {
  const cookieStore = cookies();
  
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: '', ...options });
        },
      },
    }
  );
}
```

**src/lib/supabase/admin.ts:**
```typescript
import { createClient } from '@supabase/supabase-js';
import { Database } from './database.types';

// Server-only admin client for elevated operations
export const adminClient = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
);
```

### 2.4 Identity & Namespace Context

**src/hooks/useNamespace.ts:**
```typescript
'use client';

import { createContext, useContext, ReactNode } from 'react';

interface NamespaceContextValue {
  namespaceId: string;
  userId: string;
}

const NamespaceContext = createContext<NamespaceContextValue | null>(null);

export function NamespaceProvider({ 
  children, 
  namespaceId, 
  userId 
}: { 
  children: ReactNode; 
  namespaceId: string; 
  userId: string;
}) {
  return (
    <NamespaceContext.Provider value={{ namespaceId, userId }}>
      {children}
    </NamespaceContext.Provider>
  );
}

export function useNamespace() {
  const context = useContext(NamespaceContext);
  if (!context) {
    throw new Error('useNamespace must be used within NamespaceProvider');
  }
  return context;
}
```

---

## 3. Core Data Layer

### 3.1 Show Repository

**src/lib/shows/repository.ts:**
```typescript
import { SupabaseClient } from '@supabase/supabase-js';
import { Show, ShowType, MyStatusType, MyInterestType } from '@/types';

export class ShowRepository {
  constructor(
    private client: SupabaseClient,
    private namespaceId: string,
    private userId: string
  ) {}

  async getCollection(): Promise<Show[]> {
    const { data, error } = await this.client
      .from('shows')
      .select('*')
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId)
      .not('my_status', 'is', null)
      .order('my_status_update_date', { ascending: false });
    
    if (error) throw error;
    return data.map(this.mapFromDB);
  }

  async getByExternalId(externalId: string): Promise<Show | null> {
    const { data, error } = await this.client
      .from('shows')
      .select('*')
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId)
      .eq('external_id', externalId)
      .single();
    
    if (error && error.code !== 'PGRST116') throw error;
    return data ? this.mapFromDB(data) : null;
  }

  async saveShow(show: Show): Promise<Show> {
    const dbShow = this.mapToDB(show);
    
    const { data, error } = await this.client
      .from('shows')
      .upsert({
        ...dbShow,
        namespace_id: this.namespaceId,
        user_id: this.userId,
      })
      .select()
      .single();
    
    if (error) throw error;
    return this.mapFromDB(data);
  }

  async updateStatus(
    showId: string, 
    status: MyStatusType | null,
    interest?: MyInterestType
  ): Promise<void> {
    const updates: Record<string, unknown> = {
      my_status: status,
      my_status_update_date: new Date().toISOString(),
    };
    
    if (interest !== undefined) {
      updates.my_interest = interest;
      updates.my_interest_update_date = new Date().toISOString();
    }
    
    if (status === null) {
      // Clear all My Data when removing from collection
      updates.my_tags = [];
      updates.my_score = null;
      updates.my_interest = null;
      updates.ai_scoop = null;
    }
    
    const { error } = await this.client
      .from('shows')
      .update(updates)
      .eq('id', showId)
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId);
    
    if (error) throw error;
  }

  async updateTags(showId: string, tags: string[]): Promise<void> {
    const { error } = await this.client
      .from('shows')
      .update({
        my_tags: tags,
        my_tags_update_date: new Date().toISOString(),
      })
      .eq('id', showId)
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId);
    
    if (error) throw error;
  }

  async updateRating(showId: string, score: number | null): Promise<void> {
    const { error } = await this.client
      .from('shows')
      .update({
        my_score: score,
        my_score_update_date: new Date().toISOString(),
      })
      .eq('id', showId)
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId);
    
    if (error) throw error;
  }

  async updateScoop(showId: string, scoop: string): Promise<void> {
    const { error } = await this.client
      .from('shows')
      .update({
        ai_scoop: scoop,
        ai_scoop_update_date: new Date().toISOString(),
      })
      .eq('id', showId)
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId);
    
    if (error) throw error;
  }

  async deleteShow(showId: string): Promise<void> {
    const { error } = await this.client
      .from('shows')
      .delete()
      .eq('id', showId)
      .eq('namespace_id', this.namespaceId)
      .eq('user_id', this.userId);
    
    if (error) throw error;
  }

  private mapFromDB(dbRecord: Record<string, unknown>): Show {
    // Map database record to Show type
    return {
      id: dbRecord.id as string,
      externalId: dbRecord.external_id as string | undefined,
      title: dbRecord.title as string,
      showType: dbRecord.show_type as ShowType,
      // ... map all fields
    } as Show;
  }

  private mapToDB(show: Show): Record<string, unknown> {
    // Map Show type to database record
    return {
      external_id: show.externalId,
      title: show.title,
      show_type: show.showType,
      // ... map all fields
    };
  }
}
```

### 3.2 Show Merge Logic

**src/utils/merge.ts:**
```typescript
import { Show } from '@/types';

/**
 * Merge external catalog data into an existing show.
 * Non-user fields: prefer new non-empty values
 * User fields: resolve by timestamp
 */
export function mergeShows(stored: Show | null, fresh: Show): Show {
  if (!stored) {
    return {
      ...fresh,
      myTags: [],
      networkLogos: [],
      spokenLanguages: [],
      languages: [],
      genres: fresh.genres || [],
      episodeRunTime: fresh.episodeRunTime || [],
      isTest: false,
    };
  }

  const merged: Show = {
    ...stored,
    // Always refresh catalog fields
    title: fresh.title || stored.title,
    overview: fresh.overview || stored.overview,
    tagline: fresh.tagline || stored.tagline,
    posterUrl: fresh.posterUrl || stored.posterUrl,
    backdropUrl: fresh.backdropUrl || stored.backdropUrl,
    logoUrl: fresh.logoUrl || stored.logoUrl,
    voteAverage: fresh.voteAverage ?? stored.voteAverage,
    voteCount: fresh.voteCount ?? stored.voteCount,
    popularity: fresh.popularity ?? stored.popularity,
    genres: fresh.genres?.length ? fresh.genres : stored.genres,
    // ... merge other catalog fields
  };

  return merged;
}
```

---

## 4. Feature Implementation

### 4.1 Collection Home Page

**src/pages/page.tsx (Home/Collection):**
```typescript
import { ShowRepository } from '@/lib/shows/repository';
import { createClient } from '@/lib/supabase/server';
import { CollectionHome } from './CollectionHome/CollectionHome';

export default async function HomePage() {
  const supabase = createClient();
  const namespaceId = process.env.NAMESPACE_ID!;
  const userId = process.env.DEFAULT_USER_ID!;
  
  const repo = new ShowRepository(supabase, namespaceId, userId);
  const collection = await repo.getCollection();
  
  return (
    <NamespaceProvider namespaceId={namespaceId} userId={userId}>
      <CollectionHome initialCollection={collection} />
    </NamespaceProvider>
  );
}
```

**src/pages/CollectionHome/CollectionHome.tsx:**
```typescript
'use client';

import { useState, useMemo } from 'react';
import { Show, MyStatusType, MyInterestType } from '@/types';
import { ShowGrid } from '@/components/shared/ShowGrid';
import { FilterSidebar } from './features/FilterSidebar/FilterSidebar';
import { MediaTypeToggle } from './features/MediaTypeToggle/MediaTypeToggle';
import { useCollectionFilters } from './hooks/useCollectionFilters';

interface CollectionHomeProps {
  initialCollection: Show[];
}

export function CollectionHome({ initialCollection }: CollectionHomeProps) {
  const [mediaType, setMediaType] = useState<'all' | 'movie' | 'tv'>('all');
  const [activeFilter, setActiveFilter] = useState<string>('all');
  
  const { filteredShows, availableTags } = useCollectionFilters(
    initialCollection,
    mediaType,
    activeFilter
  );
  
  // Group shows by status sections
  const groupedShows = useMemo(() => {
    const active = filteredShows.filter(s => s.myStatus === 'active');
    const excited = filteredShows.filter(
      s => s.myStatus === 'later' && s.myInterest === 'excited'
    );
    const interested = filteredShows.filter(
      s => s.myStatus === 'later' && s.myInterest === 'interested'
    );
    const other = filteredShows.filter(
      s => ['wait', 'quit', 'done'].includes(s.myStatus || '') ||
            (s.myStatus === 'later' && !s.myInterest)
    );
    
    return { active, excited, interested, other };
  }, [filteredShows]);

  return (
    <div className="flex min-h-screen">
      <FilterSidebar
        activeFilter={activeFilter}
        onFilterChange={setActiveFilter}
        availableTags={availableTags}
      />
      
      <main className="flex-1 p-6">
        <MediaTypeToggle value={mediaType} onChange={setMediaType} />
        
        {filteredShows.length === 0 ? (
          <EmptyState />
        ) : (
          <>
            {groupedShows.active.length > 0 && (
              <StatusSection
                title="Active"
                shows={groupedShows.active}
                prominent
              />
            )}
            
            {groupedShows.excited.length > 0 && (
              <StatusSection
                title="Excited"
                shows={groupedShows.excited}
              />
            )}
            
            {groupedShows.interested.length > 0 && (
              <StatusSection
                title="Interested"
                shows={groupedShows.interested}
              />
            )}
            
            {groupedShows.other.length > 0 && (
              <StatusSection
                title="Other"
                shows={groupedShows.other}
                collapsible
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}

function StatusSection({ 
  title, 
  shows, 
  prominent = false,
  collapsible = false 
}: { 
  title: string; 
  shows: Show[]; 
  prominent?: boolean;
  collapsible?: boolean;
}) {
  return (
    <section className={`mb-8 ${prominent ? 'scale-105' : ''}`}>
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <ShowGrid shows={shows} size={prominent ? 'large' : 'medium'} />
    </section>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-96">
      <h3 className="text-xl font-medium mb-2">No shows in your collection</h3>
      <p className="text-gray-600 mb-4">
        Start building your collection by searching or asking for recommendations
      </p>
      <Button href="/find">Find Shows</Button>
    </div>
  );
}
```

### 4.2 Find/Discover Hub

**src/pages/find/page.tsx:**
```typescript
import { Find } from './Find/Find';

export default function FindPage() {
  return (
    <NamespaceProvider namespaceId={process.env.NAMESPACE_ID!} userId={process.env.DEFAULT_USER_ID!}>
      <Find />
    </NamespaceProvider>
  );
}
```

**src/pages/find/Find/Find.tsx:**
```typescript
'use client';

import { useState } from 'react';
import { SearchMode } from './features/SearchMode/SearchMode';
import { AskMode } from './features/AskMode/AskMode';
import { AlchemyMode } from './features/AlchemyMode/AlchemyMode';

type FindMode = 'search' | 'ask' | 'alchemy';

export function Find() {
  const [mode, setMode] = useState<FindMode>('search');

  return (
    <div className="min-h-screen p-6">
      <ModeSwitcher activeMode={mode} onModeChange={setMode} />
      
      {mode === 'search' && <SearchMode />}
      {mode === 'ask' && <AskMode />}
      {mode === 'alchemy' && <AlchemyMode />}
    </div>
  );
}

function ModeSwitcher({ 
  activeMode, 
  onModeChange 
}: { 
  activeMode: FindMode; 
  onModeChange: (mode: FindMode) => void;
}) {
  const modes: { id: FindMode; label: string }[] = [
    { id: 'search', label: 'Search' },
    { id: 'ask', label: 'Ask' },
    { id: 'alchemy', label: 'Alchemy' },
  ];

  return (
    <div className="flex gap-2 mb-6">
      {modes.map(mode => (
        <button
          key={mode.id}
          onClick={() => onModeChange(mode.id)}
          className={`px-4 py-2 rounded-lg ${
            activeMode === mode.id 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-100 hover:bg-gray-200'
          }`}
        >
          {mode.label}
        </button>
      ))}
    </div>
  );
}
```

### 4.3 Search Mode

**src/pages/find/Find/features/SearchMode/SearchMode.tsx:**
```typescript
'use client';

import { useState, useCallback } from 'react';
import { ShowSummary } from '@/types';
import { ShowGrid } from '@/components/shared/ShowGrid';
import { useSearch } from './hooks/useSearch';

export function SearchMode() {
  const [query, setQuery] = useState('');
  const { results, isLoading, error } = useSearch(query);

  return (
    <div>
      <SearchInput 
        value={query} 
        onChange={setQuery}
        placeholder="Search shows and movies..."
      />
      
      {isLoading && <LoadingState />}
      {error && <ErrorState message={error.message} />}
      
      {!isLoading && query && results.length === 0 && (
        <NoResultsState query={query} />
      )}
      
      {!isLoading && results.length > 0 && (
        <ShowGrid shows={results} />
      )}
    </div>
  );
}
```

### 4.4 Ask Mode (AI Chat)

**src/pages/find/Find/features/AskMode/AskMode.tsx:**
```typescript
'use client';

import { useState, useRef, useEffect } from 'react';
import { useAskSession } from './hooks/useAskSession';
import { MentionedShows } from './features/MentionedShows/MentionedShows';
import { ChatMessage } from '@/components/ui/ChatMessage';

export function AskMode() {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { 
    messages, 
    mentionedShows,
    isStreaming, 
    sendMessage,
    resetSession 
  } = useAskSession();

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isStreaming) return;
    await sendMessage(input);
    setInput('');
  };

  return (
    <div className="flex flex-col h-[calc(100vh-200px)]">
      {/* Starter Prompts */}
      {messages.length === 0 && <StarterPrompts onSelect={sendMessage} />}
      
      {/* Mentioned Shows */}
      {mentionedShows.length > 0 && (
        <MentionedShows shows={mentionedShows} />
      )}
      
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((msg, i) => (
          <ChatMessage
            key={i}
            role={msg.role}
            content={msg.content}
          />
        ))}
        {isStreaming && <StreamingIndicator />}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="border-t p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about shows, vibes, or recommendations..."
            className="flex-1 px-4 py-2 border rounded-lg"
          />
          <button 
            onClick={handleSend}
            disabled={isStreaming}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
          >
            Send
          </button>
        </div>
        <button 
          onClick={resetSession}
          className="mt-2 text-sm text-gray-500 hover:text-gray-700"
        >
          Reset conversation
        </button>
      </div>
    </div>
  );
}

function StarterPrompts({ onSelect }: { onSelect: (prompt: string) => void }) {
  const starters = [
    "What should I watch if I loved The Bear?",
    "Find me a cozy mystery series",
    "I need something upbeat and funny",
    "What's a hidden gem from the last 5 years?",
    "Recommend a show with great character development",
    "I want something intense but not violent",
  ];

  return (
    <div className="p-4">
      <h3 className="text-sm text-gray-500 mb-3">Try asking:</h3>
      <div className="flex flex-wrap gap-2">
        {starters.map((prompt, i) => (
          <button
            key={i}
            onClick={() => onSelect(prompt)}
            className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-full"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
```

### 4.5 Alchemy Mode

**src/pages/find/Find/features/AlchemyMode/AlchemyMode.tsx:**
```typescript
'use client';

import { useState } from 'react';
import { Show, Concept, AIRecommendation } from '@/types';
import { ShowSelector } from './features/ShowSelector/ShowSelector';
import { ConceptSelector } from './features/ConceptSelector/ConceptSelector';
import { Recommendations } from './features/Recommendations/Recommendations';

type AlchemyStep = 'select-shows' | 'select-concepts' | 'results';

export function AlchemyMode() {
  const [step, setStep] = useState<AlchemyStep>('select-shows');
  const [selectedShows, setSelectedShows] = useState<Show[]>([]);
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [selectedConcepts, setSelectedConcepts] = useState<string[]>([]);
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([]);

  const handleShowsSelected = async (shows: Show[]) => {
    setSelectedShows(shows);
    
    // Fetch concepts from AI
    const response = await fetch('/api/ai/concepts', {
      method: 'POST',
      body: JSON.stringify({ showIds: shows.map(s => s.externalId) }),
    });
    const data = await response.json();
    setConcepts(data.concepts);
    setStep('select-concepts');
  };

  const handleConceptualize = async () => {
    if (selectedConcepts.length === 0) return;
    
    const response = await fetch('/api/ai/recommend', {
      method: 'POST',
      body: JSON.stringify({
        conceptIds: selectedConcepts,
        sourceShowIds: selectedShows.map(s => s.externalId),
        count: 6,
      }),
    });
    const data = await response.json();
    setRecommendations(data.recommendations);
    setStep('results');
  };

  const handleChainAlchemy = () => {
    // Use recommendations as new inputs
    setSelectedShows([]);
    setSelectedConcepts([]);
    setRecommendations([]);
    setStep('select-shows');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <StepIndicator currentStep={step} />
      
      {step === 'select-shows' && (
        <ShowSelector
          selectedShows={selectedShows}
          onChange={setSelectedShows}
          onContinue={() => handleShowsSelected(selectedShows)}
          minShows={2}
        />
      )}
      
      {step === 'select-concepts' && (
        <ConceptSelector
          concepts={concepts}
          selectedIds={selectedConcepts}
          onChange={setSelectedConcepts}
          onBack={() => setStep('select-shows')}
          onContinue={handleConceptualize}
          maxSelection={8}
        />
      )}
      
      {step === 'results' && (
        <Recommendations
          recommendations={recommendations}
          selectedConcepts={concepts.filter(c => selectedConcepts.includes(c.id))}
          onChainAlchemy={handleChainAlchemy}
          onBack={() => setStep('select-concepts')}
        />
      )}
    </div>
  );
}

function StepIndicator({ currentStep }: { currentStep: AlchemyStep }) {
  const steps = [
    { id: 'select-shows', label: 'Select Shows' },
    { id: 'select-concepts', label: 'Choose Concepts' },
    { id: 'results', label: 'Discover' },
  ];
  
  const currentIndex = steps.findIndex(s => s.id === currentStep);

  return (
    <div className="flex items-center gap-4 mb-8">
      {steps.map((step, i) => (
        <div key={step.id} className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            i <= currentIndex ? 'bg-blue-600 text-white' : 'bg-gray-200'
          }`}>
            {i + 1}
          </div>
          <span className={i <= currentIndex ? 'text-blue-600' : 'text-gray-500'}>
            {step.label}
          </span>
          {i < steps.length - 1 && (
            <div className="w-8 h-px bg-gray-300 mx-2" />
          )}
        </div>
      ))}
    </div>
  );
}
```

### 4.6 Show Detail Page

**src/pages/show/[id]/page.tsx:**
```typescript
import { createClient } from '@/lib/supabase/server';
import { CatalogClient } from '@/lib/catalog/client';
import { ShowRepository } from '@/lib/shows/repository';
import { mergeShows } from '@/utils/merge';
import { ShowDetail } from './ShowDetail/ShowDetail';

interface Props {
  params: { id: string };
}

export default async function ShowDetailPage({ params }: Props) {
  const supabase = createClient();
  const namespaceId = process.env.NAMESPACE_ID!;
  const userId = process.env.DEFAULT_USER_ID!;
  
  const repo = new ShowRepository(supabase, namespaceId, userId);
  const catalog = new CatalogClient(process.env.CATALOG_API_KEY!);
  
  // Fetch from catalog
  const catalogShow = await catalog.getDetails(params.id);
  
  // Check for existing user data
  const storedShow = await repo.getByExternalId(params.id);
  
  // Merge
  const show = mergeShows(storedShow, catalogShow);
  
  return (
    <NamespaceProvider namespaceId={namespaceId} userId={userId}>
      <ShowDetail show={show} />
    </NamespaceProvider>
  );
}
```

**src/pages/show/[id]/ShowDetail/ShowDetail.tsx:**
```typescript
'use client';

import { Show } from '@/types';
import { HeaderMedia } from './features/HeaderMedia/HeaderMedia';
import { CoreFacts } from './features/CoreFacts/CoreFacts';
import { MyRelationship } from './features/MyRelationship/MyRelationship';
import { OverviewScoop } from './features/OverviewScoop/OverviewScoop';
import { Recommendations } from './features/Recommendations/Recommendations';
import { ExploreSimilar } from './features/ExploreSimilar/ExploreSimilar';
import { StreamingProviders } from './features/StreamingProviders/StreamingProviders';
import { CastCrew } from './features/CastCrew/CastCrew';
import { Seasons } from './features/Seasons/Seasons';
import { BudgetRevenue } from './features/BudgetRevenue/BudgetRevenue';

interface ShowDetailProps {
  show: Show;
}

export function ShowDetail({ show }: ShowDetailProps) {
  return (
    <div className="min-h-screen">
      {/* 1. Header Media */}
      <HeaderMedia
        backdropUrl={show.backdropUrl}
        posterUrl={show.posterUrl}
        logoUrl={show.logoUrl}
        videos={show.videos}
      />
      
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* 2. Core Facts + Community Score */}
        <CoreFacts
          year={show.releaseDate || show.firstAirDate}
          runtime={show.runtime}
          seasons={show.numberOfSeasons}
          voteAverage={show.voteAverage}
          voteCount={show.voteCount}
        />
        
        {/* 3. My Relationship Controls */}
        <MyRelationship show={show} />
        
        {/* 4. Overview + Scoop */}
        <OverviewScoop show={show} />
        
        {/* 5. Ask About This Show */}
        <AskAboutShow showId={show.externalId!} title={show.title} />
        
        {/* 6. Genres + Languages */}
        <GenresLanguages genres={show.genres} languages={show.spokenLanguages} />
        
        {/* 7. Traditional Recommendations */}
        {show.recommendations && (
          <Recommendations shows={show.recommendations} />
        )}
        
        {/* 8. Explore Similar */}
        <ExploreSimilar showId={show.externalId!} />
        
        {/* 9. Streaming Availability */}
        <StreamingProviders providers={show.providerData} />
        
        {/* 10. Cast & Crew */}
        {(show.cast || show.crew) && (
          <CastCrew cast={show.cast} crew={show.crew} />
        )}
        
        {/* 11. Seasons (TV only) */}
        {show.showType === 'tv' && show.seasons && (
          <Seasons seasons={show.seasons} />
        )}
        
        {/* 12. Budget/Revenue (Movies) */}
        {show.showType === 'movie' && (show.budget || show.revenue) && (
          <BudgetRevenue budget={show.budget} revenue={show.revenue} />
        )}
      </div>
    </div>
  );
}
```

**src/pages/show/[id]/ShowDetail/features/MyRelationship/MyRelationship.tsx:**
```typescript
'use client';

import { Show, MyStatusType, MyInterestType } from '@/types';
import { StatusChips } from '@/components/shared/StatusChips';
import { RatingControl } from '@/components/shared/RatingControl';
import { TagPicker } from '@/components/shared/TagPicker';
import { useShowMutations } from './hooks/useShowMutations';
import { useState } from 'react';

interface MyRelationshipProps {
  show: Show;
}

export function MyRelationship({ show }: MyRelationshipProps) {
  const { updateStatus, updateRating, updateTags, isPending } = useShowMutations(show.id);
  const [showRemovalConfirm, setShowRemovalConfirm] = useState(false);

  const handleStatusChange = async (status: MyStatusType | null) => {
    if (status === null && show.myStatus) {
      // Show confirmation before removal
      setShowRemovalConfirm(true);
      return;
    }
    
    await updateStatus({ 
      status, 
      interest: status === 'later' ? 'interested' : undefined 
    });
  };

  const handleInterestChange = async (interest: MyInterestType) => {
    await updateStatus({ 
      status: 'later', 
      interest 
    });
  };

  const handleRatingChange = async (rating: number | null) => {
    // Rating an unsaved show auto-saves as Done
    const isNewShow = !show.myStatus;
    await updateRating(rating, isNewShow);
  };

  const handleTagsChange = async (tags: string[]) => {
    // Adding tags to unsaved show auto-saves as Later + Interested
    const isNewShow = !show.myStatus && tags.length > 0;
    await updateTags(tags, isNewShow);
  };

  return (
    <section className="py-6 border-y">
      {/* Status Chips */}
      <div className="mb-4">
        <StatusChips
          currentStatus={show.myStatus}
          currentInterest={show.myInterest}
          onStatusChange={handleStatusChange}
          onInterestChange={handleInterestChange}
          disabled={isPending}
        />
      </div>
      
      {/* Rating */}
      <div className="mb-4">
        <RatingControl
          value={show.myScore}
          onChange={handleRatingChange}
          disabled={isPending}
        />
      </div>
      
      {/* Tags */}
      <TagPicker
        tags={show.myTags}
        onChange={handleTagsChange}
        disabled={isPending}
      />
      
      {/* Removal Confirmation Modal */}
      {showRemovalConfirm && (
        <RemovalConfirmationModal
          onConfirm={() => {
            updateStatus({ status: null });
            setShowRemovalConfirm(false);
          }}
          onCancel={() => setShowRemovalConfirm(false)}
        />
      )}
    </section>
  );
}
```

### 4.7 Person Detail Page

**src/pages/person/[id]/page.tsx:**
```typescript
import { CatalogClient } from '@/lib/catalog/client';
import { PersonDetail } from './PersonDetail/PersonDetail';

interface Props {
  params: { id: string };
}

export default async function PersonDetailPage({ params }: Props) {
  const catalog = new CatalogClient(process.env.CATALOG_API_KEY!);
  const person = await catalog.getPerson(params.id);
  
  return <PersonDetail person={person} />;
}
```

### 4.8 Settings Page

**src/pages/settings/page.tsx:**
```typescript
import { createClient } from '@/lib/supabase/server';
import { SettingsRepository } from '@/lib/settings/repository';
import { Settings } from './Settings/Settings';

export default async function SettingsPage() {
  const supabase = createClient();
  const namespaceId = process.env.NAMESPACE_ID!;
  const userId = process.env.DEFAULT_USER_ID!;
  
  const repo = new SettingsRepository(supabase, namespaceId, userId);
  const cloudSettings = await repo.getSettings();
  
  return (
    <NamespaceProvider namespaceId={namespaceId} userId={userId}>
      <Settings initialSettings={cloudSettings} />
    </NamespaceProvider>
  );
}
```

---

## 5. AI Integration

### 5.1 AI Client

**src/lib/ai/client.ts:**
```typescript
import OpenAI from 'openai';

export class AIClient {
  private client: OpenAI;
  private model: string;

  constructor(apiKey: string, model: string = 'gpt-4o') {
    this.client = new OpenAI({ apiKey });
    this.model = model;
  }

  async complete(options: {
    systemPrompt: string;
    messages: Array<{ role: 'user' | 'assistant'; content: string }>;
    temperature?: number;
    stream?: boolean;
  }): Promise<string> {
    const response = await this.client.chat.completions.create({
      model: this.model,
      messages: [
        { role: 'system', content: options.systemPrompt },
        ...options.messages,
      ],
      temperature: options.temperature ?? 0.7,
      stream: options.stream ?? false,
    });

    if (options.stream) {
      // Handle streaming
      return '';
    }

    return response.choices[0].message.content || '';
  }

  async *stream(options: {
    systemPrompt: string;
    messages: Array<{ role: 'user' | 'assistant'; content: string }>;
    temperature?: number;
  }): AsyncGenerator<string> {
    const stream = await this.client.chat.completions.create({
      model: this.model,
      messages: [
        { role: 'system', content: options.systemPrompt },
        ...options.messages,
      ],
      temperature: options.temperature ?? 0.7,
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        yield content;
      }
    }
  }
}
```

### 5.2 AI Prompts

**src/lib/ai/prompts/scoop.ts:**
```typescript
export const SCOOP_SYSTEM_PROMPT = `You are a fun, chatty TV/movie nerd friend writing a personality-driven "taste review" called "The Scoop." 

Your voice: warm, opinionated, spoiler-safe, specific. Like water-cooler gossip + critic brain + hype friend.

Write a mini blog post (150-350 words) with these sections:
1. Personal Take - your stance on the show
2. Stack-Up - honest comparison to reviews/critics
3. The Scoop (centerpiece) - vivid, emotional description of the experience
4. Fit/Warnings - who this is for (and not for)
5. Worth It? - gut check verdict

Rules:
- Spoiler-safe: focus on vibe, tone, structure, not plot
- Be specific: name the particular hook, not generic praise
- Honest about mixed reception
- Stay in TV/movie domain`;

export function buildScoopPrompt(show: {
  title: string;
  overview: string;
  genres: string[];
  year?: string;
  userLibrary?: string[];
}): string {
  return `Give me the scoop on: ${show.title} (${show.year || 'Unknown'})

Overview: ${show.overview}
Genres: ${show.genres.join(', ')}

Write The Scoop now.`;
}
```

**src/lib/ai/prompts/concepts.ts:**
```typescript
export const CONCEPTS_SYSTEM_PROMPT = `You are a concept extraction engine for TV shows and movies.

Generate 8 short concept "ingredients" that capture the core feeling, vibe, structure, and emotional DNA of the input show(s).

Output format:
- Bullet list only
- Each concept: 1-3 words
- Evocative and specific
- No plot details or spoilers
- Avoid generic concepts like "good characters" or "great story"

Concepts should draw from:
- Format/structure (procedural, serialized, episodic)
- Tone & vibe (quirky, fast-paced, cozy, tense)
- Emotional palette (optimism, togetherness, catharsis)
- Relationship dynamics (found family, rivals-to-friends)
- Craft cues (sharp writing, puzzle-box plotting)`;

export function buildConceptsPrompt(shows: Array<{
  title: string;
  overview: string;
  genres: string[];
}>): string {
  const showsText = shows.map((s, i) => `
Show ${i + 1}: ${s.title}
Overview: ${s.overview}
Genres: ${s.genres.join(', ')}
`).join('\n');

  return `Extract shared concepts from these shows:
${showsText}

Generate 8 concepts that capture what these shows have in common. Return as bullet list only.`;
}
```

### 5.3 AI API Routes

**src/pages/api/ai/scoop/route.ts:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { AIClient } from '@/lib/ai/client';
import { ShowRepository } from '@/lib/shows/repository';
import { createClient } from '@/lib/supabase/server';

export async function POST(request: NextRequest) {
  try {
    const { showId, forceRefresh = false } = await request.json();
    
    const namespaceId = process.env.NAMESPACE_ID!;
    const userId = process.env.DEFAULT_USER_ID!;
    
    const supabase = createClient();
    const repo = new ShowRepository(supabase, namespaceId, userId);
    const ai = new AIClient(process.env.AI_PROVIDER_API_KEY!, process.env.AI_MODEL);
    
    // Check for cached scoop
    const show = await repo.getByExternalId(showId);
    
    if (!forceRefresh && show?.aiScoop && show.aiScoopUpdateDate) {
      const cacheAge = Date.now() - new Date(show.aiScoopUpdateDate).getTime();
      const fourHours = 4 * 60 * 60 * 1000;
      
      if (cacheAge < fourHours) {
        return NextResponse.json({ scoop: show.aiScoop, cached: true });
      }
    }
    
    // Generate new scoop
    const { buildScoopPrompt, SCOOP_SYSTEM_PROMPT } = await import('@/lib/ai/prompts/scoop');
    const prompt = buildScoopPrompt(show);
    
    const scoop = await ai.complete({
      systemPrompt: SCOOP_SYSTEM_PROMPT,
      messages: [{ role: 'user', content: prompt }],
    });
    
    // Persist if show is in collection
    if (show?.myStatus) {
      await repo.updateScoop(show.id, scoop);
    }
    
    return NextResponse.json({ scoop, cached: false });
  } catch (error) {
    console.error('Scoop generation error:', error);
    return NextResponse.json(
      { error: 'Failed to generate scoop' },
      { status: 500 }
    );
  }
}
```

---

## 6. External Catalog Integration

### 6.1 Catalog Client

**src/lib/catalog/client.ts:**
```typescript
import { Show, Person, ShowSummary, CastMember, CrewMember, Season, Video } from '@/types';

export class CatalogClient {
  private apiKey: string;
  private baseUrl = 'https://api.themoviedb.org/3';

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  async search(query: string): Promise<ShowSummary[]> {
    const response = await fetch(
      `${this.baseUrl}/search/multi?api_key=${this.apiKey}&query=${encodeURIComponent(query)}`
    );
    const data = await response.json();
    return data.results
      .filter((r: Record<string, unknown>) => r.media_type === 'movie' || r.media_type === 'tv')
      .map(this.mapToShowSummary);
  }

  async getDetails(externalId: string): Promise<Show> {
    // Determine type from ID prefix or fetch both
    const [movieData, tvData] = await Promise.all([
      this.fetchMovie(externalId).catch(() => null),
      this.fetchTV(externalId).catch(() => null),
    ]);
    
    const data = movieData || tvData;
    if (!data) {
      throw new Error('Show not found');
    }
    
    return this.mapToShow(data);
  }

  async getPerson(personId: string): Promise<Person> {
    const response = await fetch(
      `${this.baseUrl}/person/${personId}?api_key=${this.apiKey}&append_to_response=combined_credits`
    );
    const data = await response.json();
    return this.mapToPerson(data);
  }

  private async fetchMovie(id: string): Promise<unknown> {
    const response = await fetch(
      `${this.baseUrl}/movie/${id}?api_key=${this.apiKey}&append_to_response=credits,videos,recommendations,watch/providers`
    );
    return response.json();
  }

  private async fetchTV(id: string): Promise<unknown> {
    const response = await fetch(
      `${this.baseUrl}/tv/${id}?api_key=${this.apiKey}&append_to_response=credits,videos,recommendations,watch/providers`
    );
    return response.json();
  }

  private mapToShow(data: Record<string, unknown>): Show {
    const isMovie = data.title !== undefined;
    
    return {
      id: data.id?.toString() || '',
      externalId: data.id?.toString(),
      title: (data.title || data.name) as string,
      showType: isMovie ? 'movie' : 'tv',
      overview: data.overview as string,
      genres: (data.genres as Array<{ name: string }>)?.map(g => g.name) || [],
      tagline: data.tagline as string,
      homepage: data.homepage as string,
      originalLanguage: data.original_language as string,
      spokenLanguages: (data.spoken_languages as Array<{ iso_639_1: string }>)?.map(l => l.iso_639_1) || [],
      languages: [],
      posterUrl: data.poster_path ? `https://image.tmdb.org/t/p/w500${data.poster_path}` : undefined,
      backdropUrl: data.backdrop_path ? `https://image.tmdb.org/t/p/original${data.backdrop_path}` : undefined,
      logoUrl: undefined, // Would need separate logo fetch
      networkLogos: [],
      voteAverage: data.vote_average as number,
      voteCount: data.vote_count as number,
      popularity: data.popularity as number,
      releaseDate: data.release_date as string,
      firstAirDate: data.first_air_date as string,
      lastAirDate: data.last_air_date as string,
      runtime: data.runtime as number,
      budget: data.budget as number,
      revenue: data.revenue as number,
      seriesStatus: data.status as string,
      numberOfEpisodes: data.number_of_episodes as number,
      numberOfSeasons: data.number_of_seasons as number,
      episodeRunTime: (data.episode_run_time as number[]) || [],
      myTags: [],
      networkLogos: [],
      spokenLanguages: [],
      languages: [],
      genres: [],
      episodeRunTime: [],
      isTest: false,
      cast: (data.credits?.cast as unknown[])?.map(this.mapToCastMember),
      crew: (data.credits?.crew as unknown[])?.map(this.mapToCrewMember),
      seasons: (data.seasons as unknown[])?.map(this.mapToSeason),
      videos: (data.videos?.results as unknown[])?.map(this.mapToVideo),
      recommendations: (data.recommendations?.results as unknown[])?.map(this.mapToShowSummary),
      similar: (data.similar?.results as unknown[])?.map(this.mapToShowSummary),
      providerData: this.mapProviders(data['watch/providers']),
    };
  }

  private mapToShowSummary(data: Record<string, unknown>): ShowSummary {
    return {
      id: data.id?.toString() || '',
      title: (data.title || data.name) as string,
      showType: data.media_type as 'movie' | 'tv',
      posterUrl: data.poster_path ? `https://image.tmdb.org/t/p/w200${data.poster_path}` : undefined,
      releaseDate: (data.release_date || data.first_air_date) as string,
    };
  }

  private mapProviders(data: Record<string, unknown>): ProviderData | undefined {
    if (!data?.results) return undefined;
    
    const providers: ProviderData = { countries: {} };
    
    for (const [country, countryData] of Object.entries(data.results)) {
      providers.countries[country] = {
        flatrate: (countryData as { flatrate?: Array<{ provider_id: number }> })?.flatrate?.map(p => p.provider_id),
        rent: (countryData as { rent?: Array<{ provider_id: number }> })?.rent?.map(p => p.provider_id),
        buy: (countryData as { buy?: Array<{ provider_id: number }> })?.buy?.map(p => p.provider_id),
      };
    }
    
    return providers;
  }

  // ... additional mapping methods
}
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

**Test file locations (adjacent to source):**
- `src/utils/merge.test.ts` - Show merge logic
- `src/lib/shows/repository.test.ts` - Repository methods
- `src/lib/ai/prompts/*.test.ts` - Prompt construction
- `src/hooks/*.test.ts` - Custom hooks

### 7.2 Integration Tests

**Test API routes:**
- `tests/api/ai/scoop.test.ts`
- `tests/api/ai/concepts.test.ts`
- `tests/api/catalog/search.test.ts`

### 7.3 E2E Tests

**Test user journeys:**
- Collection building flow
- Search and save flow
- Ask discovery flow
- Alchemy flow
- Settings and export flow

---

## 8. Implementation Phases

### Phase 1: Foundation (Week 1)
1. Project setup and dependencies
2. Database schema and migrations
3. Environment configuration
4. Supabase client setup
5. Type definitions

### Phase 2: Core Data Layer (Week 1-2)
1. Show repository implementation
2. Catalog client (TMDB integration)
3. Show merge logic
4. Basic API routes for shows

### Phase 3: Collection Home (Week 2)
1. Layout and navigation
2. Filter sidebar
3. Collection display with status grouping
4. Show tiles with indicators

### Phase 4: Search & Discovery (Week 2-3)
1. Search mode
2. Catalog integration
3. Show results display
4. Search on launch setting

### Phase 5: Show Detail (Week 3)
1. Detail page structure
2. Header media carousel
3. Core facts display
4. My Relationship controls (status, rating, tags)
5. Overview section

### Phase 6: AI Features - Scoop (Week 3-4)
1. AI client setup
2. Scoop generation endpoint
3. Scoop display and caching
4. Progressive streaming UI

### Phase 7: AI Features - Ask (Week 4)
1. Chat interface
2. Ask session management
3. Mentioned shows parsing
4. Conversation summarization

### Phase 8: AI Features - Alchemy & Explore Similar (Week 4-5)
1. Concept extraction
2. Concept selection UI
3. AI recommendations
4. Chaining support

### Phase 9: Person Detail (Week 5)
1. Person profile page
2. Filmography display
3. Analytics charts

### Phase 10: Settings & Polish (Week 5-6)
1. Settings page
2. Data export (JSON backup)
3. Font size preferences
4. Final testing and bug fixes

---

## 9. Key Implementation Notes

### 9.1 User Identity in Benchmark Mode
- Use `DEFAULT_USER_ID` environment variable for dev/test
- Store in request context for server components
- Include in all database queries via RLS

### 9.2 Namespace Isolation
- All persisted data must include `namespace_id`
- RLS policies enforce namespace + user isolation
- Test reset only clears data for the current namespace

### 9.3 AI Response Parsing
- Use strict structured output parsing
- Implement retry logic for parsing failures
- Fall back to unstructured display + search handoff

### 9.4 Data Freshness
- AI Scoop: 4-hour cache
- Catalog data: Refresh on each detail view (merge strategy)
- User data: Always current from database

### 9.5 Auto-Save Behaviors
- Rating unsaved show → Save as `Done`
- Adding tag to unsaved show → Save as `Later + Interested`
- Setting status → Save with default `Later + Interested` if not specified

### 9.6 Security Considerations
- Never commit API keys to repository
- Use server-only routes for elevated Supabase operations
- Validate all user inputs
- RLS policies enforce data isolation

---

## 10. Deliverables Checklist

- [ ] `.env.example` with all required variables
- [ ] `.gitignore` configured for secrets
- [ ] Database migrations in `supabase/migrations/`
- [ ] Type definitions in `src/types/`
- [ ] Repository layer for data access
- [ ] Catalog client for external API
- [ ] AI client and prompts
- [ ] All page components (Home, Find, Show Detail, Person Detail, Settings)
- [ ] Shared UI components
- [ ] API routes for AI and catalog
- [ ] Test suite with npm test
- [ ] Reset script for namespace isolation
- [ ] Data export functionality
