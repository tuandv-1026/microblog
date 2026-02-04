<!--
SYNC IMPACT REPORT
Version Change: N/A → 1.0.0 (Initial ratification)
Modified Principles: N/A (Initial creation)
Added Sections:
  - Core Principles (5 principles: Content-First, User-Centric UX, Moderation-Ready, Mobile-First, Markdown-Native)
  - Technical Standards
  - Development Workflow
Removed Sections: N/A
Templates Status:
  ✅ plan-template.md - Constitution Check section compatible
  ✅ spec-template.md - User Stories align with Content-First & User-Centric principles
  ✅ tasks-template.md - Task categorization supports all principles
Follow-up TODOs: None
-->

# Microblog CMS Constitution

## Core Principles

### I. Content-First Architecture
Every feature MUST serve the core content lifecycle: draft creation, tagging, publication, and reader engagement. The system architecture revolves around Posts as the central entity with clear state transitions (draft → published) and relationships (tags, comments).

**Rationale**: A microblog's value lies in seamless content creation and discovery. Architectural decisions must prioritize authoring efficiency and content accessibility over administrative complexity.

**Rules**:
- Post entity is the atomic unit; all features extend from it
- State transitions MUST be explicit and auditable (draft/published status with timestamps)
- Tags are first-class citizens, not afterthoughts (required for navigation)
- Content rendering (Markdown) MUST preserve author intent without data loss

### II. User-Centric UX (NON-NEGOTIABLE)
All user-facing features MUST be designed mobile-first and tested across responsive breakpoints. User interactions (reading, commenting, navigating) take precedence over administrative features.

**Rationale**: Modern web traffic is predominantly mobile. A microblog that fails on mobile devices fails entirely.

**Rules**:
- Mobile viewport (375px) is the primary design target
- Touch targets MUST be ≥44px (iOS/WCAG standard)
- Timeline and Tag pages MUST load and render completely on mobile
- Comment forms MUST be usable on mobile keyboards
- Responsive testing is mandatory before deployment

### III. Moderation-Ready
Comment moderation capabilities MUST be built into the system from day one. User-generated content requires review workflows before it pollutes the reader experience.

**Rationale**: Unmoderated comment sections destroy community trust and expose authors to liability. Prevention is cheaper than cleanup.

**Rules**:
- Comments default to pending approval (whitelist model)
- Authors MUST have approve/reject controls accessible from the post view
- Moderation actions (approve/delete) MUST be logged with timestamps
- Spam and abuse reporting mechanisms MUST be in place

### IV. Markdown-Native
All post content MUST be authored in Markdown and rendered to HTML only at display time. Storage format is Markdown; rendering is implementation detail.

**Rationale**: Markdown is portable, human-readable, and version-control friendly. Storing HTML locks content into presentation decisions and complicates editing.

**Rules**:
- Database stores raw Markdown text, not rendered HTML
- Markdown parser MUST support standard syntax (headings, lists, links, code blocks, emphasis)
- Rendering MUST sanitize output to prevent XSS (e.g., via DOMPurify or equivalent)
- Preview functionality during drafting is RECOMMENDED but not required for v1

### V. Simplicity Over Features
Start with the minimal viable feature set: write, tag, publish, read, comment, moderate. Do not add features (RSS feeds, search, analytics, etc.) until the core loop is proven stable.

**Rationale**: Feature creep kills launch velocity. A working microblog with five solid features beats a broken platform with twenty half-implemented ones.

**Rules**:
- New feature proposals MUST justify why the core loop is insufficient
- Every feature MUST have explicit acceptance criteria before implementation
- If a feature can be deferred to v2 without breaking the core experience, defer it
- Performance optimization comes AFTER functionality is validated

## Technical Standards

**Tech Stack Requirements**:
- Backend: Modern web framework with ORM support (e.g., Django, Rails, Laravel, Next.js API routes)
- Frontend: Component-based framework or vanilla JS with responsive CSS (Tailwind, Bootstrap, or custom)
- Database: Relational DB with transaction support (PostgreSQL, MySQL, or SQLite for prototyping)
- Markdown rendering: Established library (marked.js, markdown-it, or language equivalent)

**Security Baseline**:
- Authentication MUST protect author routes (create/edit posts, moderate comments)
- XSS prevention via Markdown sanitization and CSP headers
- CSRF protection on all state-changing operations (publish, approve, delete)
- Input validation on all user-submitted fields (post content, comments, tags)

**Performance Goals** (v1 targets):
- Timeline page load: <2s on 3G
- Markdown render time: <100ms for typical post (500-2000 words)
- Database queries: N+1 problem MUST be avoided (use eager loading for posts with tags/comments)

**Deployment**:
- Single-environment deployment acceptable for v1 (staging optional)
- Database migrations MUST be reversible
- Environment variables for secrets (DB credentials, session keys)

## Development Workflow

**Specification-First**:
- All features require a spec with user scenarios and acceptance criteria
- Specs MUST be approved before implementation begins
- Changes to scope during implementation require spec amendment

**Incremental Delivery**:
- Features MUST be delivered as independently testable user stories
- Priority 1 stories constitute the MVP and MUST be completed first
- Each story MUST be demonstrable to stakeholders upon completion

**Quality Gates**:
- Manual testing on mobile and desktop viewports REQUIRED
- Code review by at least one other developer (if team >1)
- Security review for auth and moderation logic

**Documentation**:
- README with setup instructions (dependencies, database setup, run commands)
- Inline comments for non-obvious logic (especially Markdown rendering and moderation workflows)
- Data model diagram or schema documentation in `/specs` directory

## Governance

This constitution supersedes any conflicting practices or conventions. All development work MUST be verifiable against these principles. When faced with implementation ambiguity, refer to this document for guidance.

**Amendment Process**:
- Proposed amendments MUST include rationale and impact analysis
- Version number MUST be incremented per semantic versioning (MAJOR for breaking changes to principles, MINOR for new principles/sections, PATCH for clarifications)
- Amendments take effect upon commit to this file
- All dependent templates and documentation MUST be updated within the same PR

**Compliance**:
- Feature specs and task lists MUST reference relevant principles
- Constitution violations flagged in code review MUST be resolved before merge
- Quarterly review to ensure principles remain aligned with project reality

**Version**: 1.0.0 | **Ratified**: 2026-02-04 | **Last Amended**: 2026-02-04
