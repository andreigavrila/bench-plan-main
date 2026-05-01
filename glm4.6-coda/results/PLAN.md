# Implementation Plan: Personal TV/Movie Companion

## Executive Summary

This implementation plan covers building a personal TV and movie companion application with collection management, AI-powered discovery, and structured recommendation features. The app will use Next.js (latest stable) as the application runtime with Supabase for persistence, following the infrastructure requirements for namespace isolation and user scoping.

## 1. Architecture Overview

### 1.1 Technology Stack
- **Frontend**: Next.js (latest stable) with TypeScript
- **Backend**: Next.js API routes + Supabase
- **Database**: Supabase PostgreSQL
- **Authentication**: Development identity injection (with migration path to OAuth)
- **AI Integration**: Configurable AI provider (OpenAI, Anthropic, etc.)
- **External Catalog**: TMDB API (or similar) for show/movie data

### 1.2 System Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Next.js App   │────│  Supabase Backend │────│ External Catalog │
│  (Client + SSR) │    │  (PostgreSQL +   │    │    (TMDB API)    │
│                 │    │   Auth + RLS)    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌─────────┐            ┌─────────────┐         ┌─────────────┐
    │ AI API │            │ User Data   │         │ Media Data  │
    │ Provider│            │ (Namespaced)│         │ (Public)    │
    └─────────┘            └─────────────┘         └─────────────┘
```

## 2. Data Model & Schema Design

### 2.1 Core Entities

#### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL,
  namespace_id TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(namespace_id, username)
);
```

#### Shows Table (Core Product Entity)
```sql
CREATE TABLE shows (
  id TEXT PRIMARY KEY, -- External catalog ID
  title TEXT NOT NULL,
  show_type TEXT NOT NULL CHECK (show_type IN ('movie', 'tv', 'person', 'unknown')),
  
  -- Catalog Metadata
  overview TEXT,
  genres TEXT[],
  tagline TEXT,
  homepage TEXT,
  original_language TEXT,
  spoken_languages TEXT[],
  languages TEXT[],
  
  -- Images
  poster_url TEXT,
  backdrop_url TEXT,
  logo_url TEXT,
  network_logos TEXT[],
  
  -- Ratings & Popularity
  vote_average REAL,
  vote_count INTEGER,
  popularity REAL,
  
  -- Dates
  last_air_date TIMESTAMP,
  first_air_date TIMESTAMP,
  release_date TIMESTAMP,
  
  -- Movie-specific
  runtime INTEGER,
  budget BIGINT,
  revenue BIGINT,
  
  -- TV-specific
  series_status TEXT,
  number_of_episodes INTEGER,
  number_of_seasons INTEGER,
  episode_run_time INTEGER[],
  last_episode_run_time INTEGER,
  
  -- User Data (My Data)
  my_tags TEXT[],
  my_tags_update_date TIMESTAMP,
  my_score REAL,
  my_score_update_date TIMESTAMP,
  my_status TEXT CHECK (my_status IN ('active', 'next', 'later', 'done', 'quit', 'wait')),
  my_status_update_date TIMESTAMP,
  my_interest TEXT CHECK (my_interest IN ('excited', 'interested')),
  my_interest_update_date TIMESTAMP,
  
  -- AI Data
  ai_scoop TEXT,
  ai_scoop_update_date TIMESTAMP,
  
  -- Management
  details_update_date TIMESTAMP,
  creation_date TIMESTAMP,
  is_test BOOLEAN DEFAULT FALSE,
  
  -- External IDs
  external_ids JSONB,
  provider_data JSONB,
  
  -- Namespace & User Scoping
  user_id UUID REFERENCES users(id),
  namespace_id TEXT NOT NULL,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### User Settings Tables
```sql
-- Cloud Settings (synced)
CREATE TABLE cloud_settings (
  id TEXT PRIMARY KEY DEFAULT 'globalSettings',
  username TEXT NOT NULL,
  version BIGINT NOT NULL,
  catalog_api_key TEXT,
  ai_api_key TEXT,
  ai_model TEXT,
  user_id UUID REFERENCES users(id),
  namespace_id TEXT NOT NULL,
  
  UNIQUE(user_id, namespace_id)
);

-- Local Settings
CREATE TABLE local_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  auto_search BOOLEAN DEFAULT FALSE,
  font_size TEXT CHECK (font_size IN ('XS', 'S', 'M', 'L', 'XL', 'XXL')),
  user_id UUID REFERENCES users(id),
  namespace_id TEXT NOT NULL,
  
  UNIQUE(user_id, namespace_id)
);
```

### 2.2 Indexes & Performance
```sql
-- Perf indexes for collection queries
CREATE INDEX idx_shows_user_namespace ON shows(user_id, namespace_id);
CREATE INDEX idx_shows_my_status ON shows(my_status) WHERE my_status IS NOT NULL;
CREATE INDEX idx_shows_my_tags ON shows USING GIN(my_tags);
CREATE INDEX idx_shows_show_type ON shows(show_type);

-- Search indexes
CREATE INDEX idx_shows_title_gin ON shows USING gin(to_tsvector('english', title));
CREATE INDEX idx_shows_overview_gin ON shows USING gin(to_tsvector('english', overview));
```

### 2.3 Row Level Security (RLS)
```sql
-- Enable RLS
ALTER TABLE shows ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE cloud_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE local_settings ENABLE ROW LEVEL SECURITY;

-- Shows RLS Policies
CREATE POLICY "Users can access their own shows in their namespace" 
ON shows FOR ALL USING (
  namespace_id = current_setting('app.current_namespace', true) AND
  user_id = current_setting('app.current_user_id', true)::uuid
);

-- Users RLS Policies
CREATE POLICY "Users can access themselves in their namespace"
ON users FOR ALL USING (
  namespace_id = current_setting('app.current_namespace', true)
);
```

## 3. API Design

### 3.1 Authentication & Context Middleware
```typescript
// middleware.ts or API middleware
export async function middleware(req: NextRequest) {
  const namespaceId = req.headers.get('x-namespace-id') || process.env.DEFAULT_NAMESPACE;
  const userId = req.headers.get('x-user-id') || getDefaultUserForNamespace(namespaceId);
  
  // Set context for RLS policies
  supabase.rpc('set_session_context', {
    namespace_id: namespaceId,
    user_id: userId
  });
}
```

### 3.2 Core API Endpoints

#### Collection Management
```typescript
// GET /api/shows - Get user's collection with filters
// POST /api/shows - Save show to collection
// PUT /api/shows/[id] - Update show (status, tags, rating)
// DELETE /api/shows/[id] - Remove from collection
```

#### Search & Discovery
```typescript
// GET /api/search?q=... - Search external catalog
// GET /api/recommendations/traditional/[id] - Similar shows
// POST /api/ai/ask - AI chat discovery
// POST /api/ai/concepts - Generate concepts for shows
// POST /api/ai/recommendations - Get concept-based recommendations
// POST /api/ai/scoop - Generate AI scoop for show
```

#### Data Management
```typescript
// GET /api/export - Export user data
// POST /api/import - Import user data
// GET /api/settings - Get user settings
// PUT /api/settings - Update user settings
```

### 3.3 External Catalog Integration
```typescript
// TMDB Service
class TMDBService {
  async searchShows(query: string): Promise<Show[]>
  async getShowDetails(id: string): Promise<Show>
  async getSimilarShows(id: string): Promise<Show[]>
  async getCastCrew(id: string): Promise<CastCrew[]>
  async getProviders(id: string, region: string): Promise<ProviderData>
}
```

## 4. Frontend Architecture

### 4.1 Page Structure & Routing
```
/                               # Home - Collection view (filtered)
/find/search                    # Search external catalog
/find/ask                       # AI chat discovery
/find/alchemy                   # Concept blending discovery
/show/[id]                      # Show detail page
/person/[id]                    # Person detail page
/settings                        # Settings & data management
```

### 4.2 Component Hierarchy
```
AppLayout
├── NavigationPanel (filters/sidebar)
├── MainContent
│   ├── HomePage
│   │   ├── FilterToggleBar
│   │   ├── StatusSections
│   │   └── ShowGrid
│   ├── SearchPage
│   │   ├── SearchInput
│   │   └── ResultsGrid
│   ├── AskPage
│   │   ├── ChatInterface
│   │   ├── MentionedShowsStrip
│   │   └── StarterPrompts
│   ├── AlchemyPage
│   │   ├── ShowSelector
│   │   ├── ConceptPicker
│   │   └── ResultsDisplay
│   ├── ShowDetailPage
│   │   ├── MediaCarousel
│   │   ├── MyDataControls
│   │   ├── Overview & Scoop
│   │   ├── Recommendations
│   │   ├── ExploreSimilar
│   │   └── CastCrew
│   └── PersonDetailPage
└── SettingsPage
```

### 4.3 State Management
- **Server State**: React Query (SWR alternative) for API calls
- **Client State**: React Context for current user/namespace, UI preferences
- **Form State**: React Hook Form for settings and data entry
- **Local Caching**: IndexedDB for offline-friendly cache of show data

## 5. AI Integration

### 5.1 AI Service Architecture
```typescript
interface AIService {
  // CoreAI surfaces
  generateAskResponse(context: AskContext): Promise<AskResponse>
  generateConcepts(shows: Show[]): Promise<string[]>
  generateRecommendations(concepts: string[], context: RecommendationContext): Promise<Recommendation[]>
  generateScoop(show: Show): Promise<ScoopResponse>
  
  // Personality management
  setPersona(persona: AIPersona): void
  getPromptForSurface(surface: AISurface): string
}
```

### 5.2 Prompt Management System
```typescript
// Prompt templates with personality injection
const promptTemplates = {
  ask: {
    base: "You are a fun, chatty TV/movie nerd friend...",
    withContext: "...User's library: {userLibrary}...",
    withShow: "...About this show: {showContext}..."
  },
  concepts: {
    single: "Extract 1-3 word concept ingredients from this show...",
    multi: "Extract shared concepts across these shows..."
  },
  scoop: {
    base: "Write a mini blog-post of taste review...",
    structure: "Personal take, honest stack-up, the Scoop centerpiece, fit/warnings, verdict..."
  }
};
```

### 5.3 AI Configuration
```typescript
// Configurable AI providers
interface AIProvider {
  name: string
  apiKey: string
  model: string
  maxTokens: number
  temperature: number
}

// Environment variables
NEXT_PUBLIC_AI_PROVIDER=openai
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## 6. Discovery Features Implementation

### 6.1 Ask (Chat) Implementation
```typescript
// Chat session management
class ChatService {
  private messages: Message[] = []
  private contextSummary: string = ""
  
  async sendMessage(userMessage: string): Promise<ChatResponse> {
    // Build context with user library, recent conversation
    const context = this.buildContext()
    
    // Call AI service
    const response = await aiService.generateAskResponse({
      message: userMessage,
      context: context,
      library: await this.getUserLibrary()
    })
    
    // Parse mentioned shows for UI strip
    const mentionedShows = this.parseMentionedShows(response.structuredOutput)
    
    // Update message history and summarize if needed
    this.updateHistory(userMessage, response)
    
    return {
      text: response.commentary,
      mentionedShows,
      suggestions: response.suggestions
    }
  }
}
```

### 6.2 Alchemy (Concept Blending) Implementation
```typescript
class AlchemyService {
  async generateConcepts(shows: Show[]): Promise<Concept[]> {
    if (shows.length < 2) throw new Error("Need at least 2 shows")
    
    return await aiService.generateConcepts(shows)
  }
  
  async getRecommendations(concepts: string[], library: Show[]): Promise<Recommendation[]> {
    return await aiService.generateRecommendations({
      concepts,
      userLibrary: library,
      limit: 6
    })
  }
}
```

### 6.3 Explore Similar Implementation
```typescript
class ExploreSimilarService {
  async getConcepts(show: Show): Promise<Concept[]> {
    return await aiService.generateConcepts([show])
  }
  
  async getRecommendations(concepts: string[], baseShow: Show): Promise<Recommendation[]> {
    return await aiService.generateRecommendations({
      concepts,
      baseShow,
      limit: 5
    })
  }
}
```

## 7. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
1. **Project Setup**
   - Initialize Next.js app with TypeScript
   - Set up Supabase client and schemas
   - Configure environment variables
   - Set up middleware for namespace/user context

2. **Core Data Layer**
   - Implement database schemas and migration scripts
   - Set up RLS policies
   - Create base API endpoints for CRUD operations
   - Implement TMDB service integration

3. **Authentication & Context**
   - Implement development identity injection
   - Set up namespace isolation
   - Create user management utilities

### Phase 2: Core Features (Weeks 3-4)
1. **Collection Management**
   - Show detail page with My Data controls
   - Status, interest, tags, rating functionality
   - Collection home with filtering
   - Save/remove functionality with confirmations

2. **Search & Browse**
   - Search page with TMDB integration
   - Results grid with collection indicators
   - Basic filtering by genre, decade, media type

3. **UI Foundation**
   - Component library for common elements
   - Responsive design
   - Loading states and error handling

### Phase 3: AI Discovery (Weeks 5-6)
1. **AI Service Setup**
   - AI service architecture
   - Prompt templates and personality system
   - Provider configuration and fallbacks

2. **Ask Implementation**
   - Chat interface with message history
   - Mentioned shows parsing and display
   - Starter prompts and context management
   - "Ask about this show" integration

3. **Concept System**
   - Concept generation for single/multiple shows
   - Concept selection UI
   - Real catalog mapping for recommendations

### Phase 4: Advanced Discovery (Weeks 7-8)
1. **Alchemy Implementation**
   - Multi-show concept blending
   - Step-by-step wizard UI
   - Results display and chaining

2. **Explore Similar**
   - Single-show concept extraction
   - Similar recommendations with concept reasoning
   - Integration into show detail page

3. **AI Scoop**
   - Scoop generation on detail pages
   - Caching with 4-hour freshness
   - Progressive loading

### Phase 5: Polish & Optimization (Weeks 9-10)
1. **Performance Optimization**
   - Image optimization and CDN setup
   - Query optimization and database indexing
   - Client-side caching strategies

2. **User Experience Polish**
   - Micro-interactions and animations
   - Empty states and onboarding
   - Accessibility improvements

3. **Settings & Data Management**
   - Settings page implementation
   - Data export/import functionality
   - User preferences and cloud sync

### Phase 6: Testing & Deployment (Weeks 11-12)
1. **Testing Coverage**
   - Unit tests for core business logic
   - Integration tests for API endpoints
   - E2E tests for critical user journeys
   - Load testing for AI endpoints

2. **Production Readiness**
   - Environment configuration for production
   - Monitoring and error tracking setup
   - Backup and disaster recovery procedures

3. **Documentation & Handoff**
   - API documentation
   - Deployment guides
   - Maintenance procedures

## 8. Key Technical Decisions & Rationale

### 8.1 Data Architecture
- **Decision**: Use Supabase for production-ready PostgreSQL with built-in auth and RLS
- **Rationale**: Reduces infrastructure complexity while providing reliability and scalability
- **Trade-offs**: Vendor lock-in, but migration path is straightforward

### 8.2 AI Integration Strategy
- **Decision**: Provider-agnostic AI service with configurable prompts
- **Rationale**: Flexibility to switch providers and optimize for cost/performance
- **Trade-offs**: Slightly more complex abstraction layer

### 8.3 Frontend Framework
- **Decision**: Next.js with TypeScript
- **Rationale**: Required by infrastructure rider, excellent developer experience, built-in optimization
- **Trade-offs**: Framework-specific patterns, but industry standard

### 8.4 State Management
- **Decision**: React Query for server state, React Context for client state
- **Rationale**: Separates concerns effectively, reduces boilerplate, excellent caching
- **Trade-offs**: Learning curve for React Query patterns

## 9. Risk Assessment & Mitigation

### 9.1 Technical Risks
- **AI API rate limits**: Implement caching and retry logic
- **External catalog downtime**: Cache popular shows locally
- **Database performance**: Optimize queries and indexes early
- **Authentication complexity**: Keep development identity simple initially

### 9.2 Product Risks
- **AI quality consistency**: Implement prompt testing and golden set validation
- **User adoption**: Focus on core collection management first
- **Performance perception**: Optimize loading states and progressive enhancement

### 9.3 Infrastructure Risks
- **Namespace isolation errors**: Comprehensive testing of multi-tenant scenarios
- **Data loss**: Regular backups and point-in-time recovery
- **Cost overruns**: Monitor API usage and implement cost controls

## 10. Success Metrics

### 10.1 Technical Metrics
- API response time < 200ms for cached operations
- Database query optimization: >95% of queries under 100ms
- Zero data loss incidents
- 99.9% uptime for core features

### 10.2 Product Metrics
- Collection creation rate: >80% of new users save 3+ shows in first week
- Discovery engagement: >50% of users try Ask or Alchemy features
- Retention: >60% of users return within 7 days

### 10.3 Quality Metrics
- AI prompt success rate: >85% of responses pass quality bar
- External catalog mapping: >95% of AI recommendations resolve to real shows
- User satisfaction: Qualitative feedback on AI personality and usefulness

---

This implementation plan provides a comprehensive roadmap for building the personal TV/movie companion application while adhering to all infrastructure requirements and maintaining the product's core vision of making "taste visible and actionable."