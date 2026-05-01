# Implementation Plan for Personal TV & Movie Companion App

This document outlines the implementation plan based on the PRD specifications.

## Architecture Overview
- Client-server architecture with Next.js frontend and Supabase backend
- Namespace isolation for build/run separation
- User-scoped data storage

## Data Models
- Show entity with public catalog data and user overlay (My Data)
- Supporting entities: CloudSettings, AppMetadata, LocalSettings, UIState
- Merge rules: non-my fields use selectFirstNonEmpty, my fields resolved by timestamp

## API Endpoints
- Supabase REST API with RLS for data access
- Custom AI endpoints for Scoop, concepts, recommendations, Ask
- Authentication via Supabase Auth

## Feature Implementation
1. Collection Management (status, interest, tags, rating, auto-save rules)
2. Discovery Features (Search, Ask, Alchemy, Explore Similar, AI Scoop)
3. Supporting Features (Person Detail, Settings, Data Export/Import)

## Technical Stack
- Frontend: Next.js (latest stable), TypeScript
- Backend: Supabase (PostgreSQL, Auth, Storage)
- External Services: TMDB (catalog), AI provider (OpenAI/Anthropic)
- Tooling: npm, ESLint, Prettier, Jest, React Testing Library

## Development Considerations
- Data synchronization and merge rules per storage-schema.md
- AI integration with structured outputs and fallback strategies
- Privacy & Security: RLS policies, anon key usage, secret management
- Performance: pagination, caching, image optimization
- Accessibility: semantic HTML, ARIA labels, responsive design

## Testing Strategy
- Unit tests for components and utilities
- Integration tests for Supabase interactions and API routes
- End-to-end tests for key user journeys (build collection, rate-to-save, Ask discovery, Alchemy, etc.)
- Destructive testing with namespace isolation

## Deployment & Infrastructure
- Development: npm run dev, npm test, npm run test:reset
- Benchmark compliance: .env.example, one-command experience, deterministic test data
- Production: environment-specific configs, CDN, monitoring, backups

## Open Questions & Future Extensions
- Next status as first-class UI status
- Named custom lists beyond tags
- Implicit save on AI Scoop generation
- Explicit Unrated state
- Import/Restore from export zip
- Alchemy session sharing
- Explicit myStatus filters in sidebar

This plan adheres to the Infrastructure Rider requirements for namespace isolation, user scoping, and benchmark compliance.