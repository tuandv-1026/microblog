# Feature Specification: Personal Blog Platform

**Feature Branch**: `001-personal-blog`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: User description: "Xây dựng nền tảng blog cá nhân với responsive mobile, render markdown, có trang Home/Category/About, layout 3 cột, đăng ký/đăng nhập, draft/publish, comment, emoji reactions, search theo title/author"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse and Read Blog Posts (Priority: P1)

A visitor arrives at the homepage and sees a 3-column layout with blog posts in the center showing previews, a menu for navigation, categories listed on the right (sorted by post count), and recent posts on the left. The visitor can click on any post to read the full content rendered from Markdown. The layout adapts seamlessly to mobile devices with a single-column view.

**Why this priority**: Core reading experience is the fundamental value proposition of a blog. Without this, the platform has no purpose.

**Independent Test**: Can be fully tested by creating sample posts with Markdown content and verifying homepage layout, post detail rendering, and responsive behavior on mobile viewports (375px-768px). Delivers immediate value as a read-only blog.

**Acceptance Scenarios**:

1. **Given** visitor is on homepage, **When** page loads, **Then** see 3-column layout: left (recent posts list), center (post previews with title, excerpt, author, date, stats), right (categories with post counts)
2. **Given** visitor is on homepage on mobile, **When** page loads, **Then** see single-column layout with stacked sections and touch-friendly navigation
3. **Given** visitor clicks a post preview, **When** post detail page loads, **Then** see full Markdown-rendered content with proper formatting (headings, lists, code blocks, links, emphasis)
4. **Given** visitor is viewing any page, **When** accessing navigation menu, **Then** can navigate to Home, Category pages, and About Me page
5. **Given** visitor views category list on sidebar, **When** categories are displayed, **Then** categories are ordered by post count (descending) by default

---

### User Story 2 - Filter and Sort Content (Priority: P1)

A visitor wants to find specific content by exploring categories, sorting posts by different criteria (creation time, likes, views), or searching by title or author name. The system provides intuitive filtering and search mechanisms accessible from the homepage and category pages.

**Why this priority**: Content discoverability is essential for any blog with more than a few posts. Without sorting/filtering, users cannot efficiently find what they need.

**Independent Test**: Can be tested by creating posts with various categories, timestamps, and engagement metrics, then verifying sort options, category filtering, and search functionality work correctly. Delivers value as an enhanced reading experience.

**Acceptance Scenarios**:

1. **Given** visitor is on homepage, **When** selecting sort option, **Then** posts reorder by selected criteria: creation time (newest/oldest), likes count, or views count
2. **Given** visitor clicks a category from sidebar, **When** category page loads, **Then** see only posts tagged with that category, maintaining the same layout structure
3. **Given** visitor enters text in search box, **When** submitting search, **Then** see posts matching the search term in either title or author name (case-insensitive)
4. **Given** visitor performs search with no results, **When** search completes, **Then** see friendly "No posts found" message with suggestion to try different terms
5. **Given** visitor is on mobile, **When** accessing sort and search controls, **Then** controls are touch-friendly and accessible via responsive menu

---

### User Story 3 - User Authentication (Priority: P2)

A new user wants to register an account to post blogs and interact with content. An existing user wants to log in to access their authoring dashboard. The system provides secure registration and login flows with proper validation.

**Why this priority**: Authentication is required for authoring and engagement features, but read-only browsing (P1) delivers value without it.

**Independent Test**: Can be tested by completing registration flow with various inputs (valid/invalid emails, weak passwords), verifying validation rules, and confirming login/logout functionality. Delivers value by enabling user identity management.

**Acceptance Scenarios**:

1. **Given** visitor clicks "Register" link, **When** registration form appears, **Then** see fields for email, username, password, and password confirmation
2. **Given** user submits registration with valid data, **When** form processes, **Then** account is created, user is logged in, and redirected to homepage or dashboard
3. **Given** user submits registration with invalid email or weak password, **When** validation runs, **Then** see inline error messages explaining requirements (email format, password min 8 chars)
4. **Given** registered user clicks "Login" link, **When** entering valid credentials, **Then** user is authenticated and sees personalized navigation (username, logout option, post creation link)
5. **Given** authenticated user clicks "Logout", **When** logout processes, **Then** session ends and user returns to public homepage view

---

### User Story 4 - Create and Publish Blog Posts (Priority: P2)

An authenticated user wants to write a blog post in Markdown using an enhanced editor with toolbar shortcuts, save it as a draft, preview the rendered output in split-view mode, assign or create categories, and publish it when ready. The system supports draft/publish workflow with clear state transitions.

**Why this priority**: Content creation is the author's primary workflow. Must come after authentication (P2 dependency) but before engagement features.

**Independent Test**: Can be tested by logging in, creating a post with Markdown content and categories, saving as draft, previewing rendered output, and publishing. Delivers value as a complete authoring experience.

**Acceptance Scenarios**:

1. **Given** authenticated user clicks "New Post" button, **When** editor page loads, **Then** see Markdown editor with toolbar (headings H1-H6, bold, italic, strikethrough, lists, links, images, tables, code, quotes), category management, and draft/publish actions
2. **Given** user types Markdown content, **When** selecting text and clicking toolbar buttons, **Then** Markdown syntax is inserted at cursor position or wraps selected text
3. **Given** user clicks "Split" view mode, **When** editor switches to split view, **Then** see side-by-side editor and live preview panels updating in real-time
4. **Given** user needs a new category, **When** typing category name in "Add Category" input and clicking "+ Add", **Then** category is created and automatically selected for current post
5. **Given** user clicks "Save as Draft", **When** draft saves, **Then** post is stored with draft status, visible only to author in their drafts list, not on public homepage
6. **Given** user has a draft post, **When** clicking "Publish", **Then** post status changes to published, appears on homepage timeline, and shows creation timestamp
7. **Given** user assigns categories during creation, **When** post is published, **Then** post appears in selected category pages and category counts update on sidebar
8. **Given** authenticated user views their own post, **When** post detail page loads, **Then** see "Edit" and "Delete" buttons accessible only to post author
9. **Given** user toggles between Edit/Split/Preview modes, **When** switching views, **Then** content persists and view changes without losing work

---

### User Story 5 - Comment and React with Emojis (Priority: P3)

An authenticated user wants to engage with blog posts by leaving comments and reacting with emojis (like 👍, love ❤️, haha 😄, wow 😮, sad 😢, angry 😠). Comments display the user's username automatically from their logged-in account. Emoji reactions are counters displayed with detailed breakdown near the post.

**Why this priority**: Engagement features enhance community but are not essential for core blog functionality (reading and writing). Can be deferred after authoring workflow is stable.

**Independent Test**: Can be tested by logging in, navigating to a published post, adding comments, clicking emoji reactions, and verifying counts update. Delivers value as social interaction layer.

**Acceptance Scenarios**:

1. **Given** authenticated user is viewing a published post, **When** scrolling to comments section, **Then** see existing comments (username from logged-in account, timestamp, text) and a comment input form
2. **Given** authenticated user enters comment text, **When** submitting comment, **Then** comment appears immediately below post content with user's name and timestamp
3. **Given** authenticated user clicks an emoji reaction button (like/love/haha/wow/sad/angry), **When** reaction registers, **Then** emoji counter increments and user's reaction is highlighted to prevent duplicate clicks
4. **Given** user has already reacted with an emoji, **When** clicking the same emoji again, **Then** reaction is removed and counter decrements (toggle behavior)
5. **Given** visitor is not logged in, **When** viewing post with comments and reactions, **Then** see existing comments and reaction counts but comment form shows "Login to comment" message
6. **Given** post has reactions, **When** viewing post card or post detail, **Then** see total reaction count and breakdown showing count per reaction type (e.g., "5 👍 3 ❤️ 2 😄")

---

### User Story 6 - About Me Page (Priority: P3)

A visitor wants to learn about the blog author by visiting a dedicated About Me page. The page displays author bio, profile information, and optionally a profile photo. Content is editable by the authenticated blog owner.

**Why this priority**: Static content page that adds personality but is not critical to core blog operations. Can be implemented last.

**Independent Test**: Can be tested by navigating to About Me page from menu, viewing static content, and (as admin) editing the bio via a simple form. Delivers value as author presentation.

**Acceptance Scenarios**:

1. **Given** visitor clicks "About Me" in navigation menu, **When** page loads, **Then** see author bio content rendered from Markdown, optional profile photo, and contact links
2. **Given** blog owner is authenticated, **When** viewing About Me page, **Then** see "Edit Bio" button that opens editor for updating content
3. **Given** blog owner edits bio content, **When** saving changes, **Then** updated content appears immediately on About Me page for all visitors

---

### Edge Cases

- What happens when user tries to publish a post without title or content? (Validation prevents submission with inline error messages)
- How does system handle Markdown syntax errors or malicious scripts in post content? (Markdown parser sanitizes output to prevent XSS; malformed Markdown renders as plaintext)
- What if user searches with special characters or SQL injection attempts? (Input is escaped/parameterized; search treats input as literal string)
- How are posts ordered when multiple posts have same like/view count? (Secondary sort by creation time descending as tiebreaker)
- What if category sidebar has 50+ categories? (Display top 10 by post count, with "Show More" link to full category page)
- Can users comment on draft posts? (No, comments are only enabled on published posts; draft URLs are author-only accessible)
- What happens when user clicks multiple emoji reactions simultaneously? (Only last click registers; UI disables buttons during processing to prevent race conditions)
- How does mobile layout handle very long post titles or category names? (Text truncates with ellipsis; full text appears on hover/long-press)

## Requirements *(mandatory)*

### Functional Requirements

**Homepage & Navigation**
- **FR-001**: System MUST display homepage with 3-column layout on desktop (≥1024px): left sidebar (recent posts list), center column (post previews), right sidebar (categories and stats)
- **FR-002**: System MUST adapt layout to single-column on mobile (<768px) with stacked sections: menu → post list → categories
- **FR-003**: System MUST provide navigation menu with links to Home, Category pages, and About Me page, accessible from all pages
- **FR-004**: Center column MUST display post previews containing: title, excerpt (first 150 chars of content), author name, creation date, view count, comment count, reaction count with breakdown by type, and formatted numbers (e.g., "1.2K views")
- **FR-005**: Right sidebar MUST display categories ordered by post count (descending) with post counts shown as badges

**Content Rendering**
- **FR-006**: System MUST store blog post content in raw Markdown format in database
- **FR-007**: System MUST render Markdown to HTML at display time supporting: headings (h1-h6), lists (ordered/unordered), links, emphasis (bold/italic), code blocks, and inline code
- **FR-008**: System MUST sanitize rendered HTML to prevent XSS attacks (strip script tags, dangerous attributes)
- **FR-009**: Post detail page MUST display full rendered Markdown content with responsive images (max-width: 100%)

**Sorting & Filtering**
- **FR-010**: Homepage MUST provide sort controls: creation time (newest first, oldest first), like count (descending), view count (descending)
- **FR-011**: Default sort order MUST be creation time descending (newest posts first)
- **FR-012**: Category pages MUST display only posts tagged with selected category, maintaining same layout as homepage
- **FR-013**: System MUST track view count for each post (increment on post detail page load every time, no session tracking)
- **FR-014**: System MUST track like count for each post (sum of like emoji reactions)
- **FR-015**: System MUST calculate and display comment count for each post (total number of comments)
- **FR-016**: System MUST calculate and display reaction count with breakdown by type (e.g., "5 👍 3 ❤️ 2 😄")

**Search**
- **FR-017**: System MUST provide search input field accessible from homepage header
- **FR-018**: Search MUST match query against post title AND author username (case-insensitive, partial match)
- **FR-019**: Search results page MUST display matching posts in same preview format as homepage
- **FR-020**: Search with no results MUST display "No posts found matching '[query]'" message

**User Authentication**
- **FR-021**: System MUST provide registration form with fields: email (unique), username (unique), password, password confirmation
- **FR-022**: System MUST validate email format (RFC 5322 compliant) and password strength (minimum 8 characters)
- **FR-023**: System MUST hash passwords using industry-standard algorithm (bcrypt or Argon2) before storage
- **FR-024**: System MUST provide login form with email and password fields
- **FR-025**: Authenticated users MUST see personalized navigation: username display, "New Post" link, "My Drafts" link, "Logout" button
- **FR-026**: System MUST maintain session state using secure cookies (HttpOnly, SameSite, HTTPS in production)

**Post Creation & Publishing**
- **FR-027**: Authenticated users MUST be able to create new posts via "New Post" form with fields: title, Markdown content, category selection (multi-select) or category creation
- **FR-028**: System MUST provide Markdown toolbar with buttons for: H1-H6 headings, bold, italic, strikethrough, bullet lists, numbered lists, task lists, horizontal rules, links, images, tables, inline code, code blocks, and quotes
- **FR-029**: System MUST support three view modes: Edit (editor only), Split (side-by-side editor and preview), Preview (preview only)
- **FR-030**: System MUST provide live preview of rendered Markdown that updates in real-time in Split view mode
- **FR-031**: System MUST allow users to create new categories directly from post editor with input field and "+ Add" button
- **FR-032**: Newly created categories MUST be automatically selected for the current post
- **FR-033**: System MUST support draft status: drafts visible only to author, not included in public homepage or search
- **FR-034**: System MUST provide "Save as Draft" and "Publish" actions in post editor
- **FR-035**: Published posts MUST display creation timestamp and author information
- **FR-036**: Post authors MUST be able to edit their own posts (title, content, categories) and delete their posts
- **FR-037**: System MUST validate post has title (non-empty) and content before allowing publish
- **FR-038**: Toolbar buttons MUST insert Markdown syntax at cursor position or wrap selected text

**Comments**
- **FR-039**: Authenticated users MUST be able to comment on published posts
- **FR-040**: Comments MUST automatically use the logged-in user's username (no manual name/email entry)
- **FR-041**: Comments table MUST store user_id as foreign key to users table
- **FR-042**: Comments MUST display: author username (from user account), timestamp, and comment text
- **FR-043**: Comments MUST be ordered chronologically (oldest first) below post content
- **FR-044**: Non-authenticated visitors MUST see existing comments but cannot submit new comments
- **FR-045**: Comment form MUST show "Login to comment" message for non-authenticated users

**Emoji Reactions**
- **FR-046**: System MUST support six emoji reactions per post: like 👍, love ❤️, haha 😄, wow 😮, sad 😢, angry 😠
- **FR-047**: Authenticated users MUST be able to toggle reactions (click to add, click again to remove)
- **FR-048**: Each user can only react once per emoji type per post (cannot like twice)
- **FR-049**: System MUST display reaction counts next to each emoji button
- **FR-050**: System MUST display reaction summary showing breakdown by type (e.g., "5 👍 3 ❤️ 2 😄") on post cards
- **FR-051**: Non-authenticated visitors MUST see reaction counts but cannot react (buttons disabled)

**About Me Page**
- **FR-052**: System MUST provide About Me page accessible via navigation menu
- **FR-053**: About Me page MUST display author bio content rendered from Markdown
- **FR-054**: Blog owner (first registered user or designated admin) MUST be able to edit About Me content via editor form
- **FR-055**: About Me page MAY include optional profile photo (uploaded image or external URL)

### Key Entities

- **User**: Represents registered account with email (unique), username (unique), hashed password, registration timestamp, and role (author/admin)
- **Post**: Represents blog post with title, content (Markdown text), author (User relationship), creation timestamp, status (draft/published), view count (increments on every view), comment_count (calculated), reaction_count (calculated), reaction_summary (breakdown by type), and categories (many-to-many relationship)
- **Category**: Represents content tag with name (unique) and slug (URL-friendly), related to Posts via many-to-many relationship, can be created by users during post creation
- **Comment**: Represents user comment with text, author (User relationship via user_id foreign key), post (Post relationship), and timestamp
- **Reaction**: Represents emoji reaction with type (like/love/haha/wow/sad/angry), user (User relationship), post (Post relationship), and timestamp (ensures one reaction per user per type per post)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Visitors can browse homepage and read full blog posts on both desktop and mobile devices without layout issues
- **SC-002**: Homepage loads and displays 20 posts with previews in under 2 seconds on 3G connection
- **SC-003**: Users can complete registration and publish their first blog post in under 5 minutes
- **SC-004**: Markdown content with 10+ formatting elements (headings, lists, code blocks) renders correctly without visual artifacts
- **SC-005**: Search returns accurate results for title and author queries in under 500ms for databases with 1000+ posts
- **SC-006**: Category filtering displays correct subset of posts with updated counts in under 1 second
- **SC-007**: Mobile users can navigate, read posts, and interact with touch-friendly controls (≥44px tap targets) without horizontal scrolling
- **SC-008**: Emoji reaction clicks register and update counters within 300ms with visual feedback
- **SC-009**: Comment submission appears immediately below post without page reload (AJAX or optimistic UI)
- **SC-010**: 95% of users successfully find specific content using search or category filters on first attempt

## Assumptions

- Single blog owner/admin model: first registered user or designated account has special privileges (edit About Me, moderate comments if moderation added later)
- Category assignment is optional: posts without categories still appear on homepage but not in category-filtered views
- Categories can be created by any authenticated user during post creation
- View count increments on every page view without session deduplication (simpler implementation, always increments)
- No comment moderation in v1: comments appear immediately (can be added as FR in future iteration if spam becomes issue)
- Comments automatically use logged-in user's username and email from their account (no manual entry)
- Profile photos are optional and can be external URLs (e.g., Gravatar) to avoid file upload complexity in v1
- Draft posts are not counted in category post counts shown on sidebar
- Sort and filter options do not persist across sessions (default to newest first on each visit)
- Search is simple text matching (no full-text search indexing or advanced query syntax in v1)
- Emoji reactions include 6 types: like, love, haha, wow, sad, angry (expanded from 4)
- React.StrictMode double-render is handled with AbortController to prevent duplicate API calls

## Out of Scope (Future Considerations)

- Comment moderation/approval workflow
- Post scheduling (publish at future date/time)
- Rich text WYSIWYG editor (Markdown-only in v1)
- Social media sharing buttons
- RSS/Atom feeds
- Email notifications for new comments
- User profile pages (beyond About Me for owner)
- Post tags separate from categories (categories are sufficient for v1)
- Advanced search (by date range, category, tags)
- Analytics dashboard (views over time, popular posts)
- Multi-user/multi-author blogs (single owner in v1)
- SEO optimizations (meta tags, sitemaps, structured data)

## Compliance & Security

- **Password Security**: MUST use bcrypt or Argon2 with appropriate work factor (cost 10+ for bcrypt)
- **XSS Prevention**: Markdown renderer MUST sanitize output using established library (e.g., DOMPurify, Bleach)
- **CSRF Protection**: All state-changing forms (login, register, post creation, comment submission) MUST include CSRF tokens
- **Input Validation**: All user inputs MUST be validated server-side (email format, password length, title/content non-empty)
- **SQL Injection Prevention**: All database queries MUST use parameterized queries or ORM with proper escaping
- **Session Management**: Sessions MUST expire after 7 days of inactivity; logout MUST invalidate session token

## Dependencies

- Markdown rendering library: Must support CommonMark or GitHub Flavored Markdown (GFM)
- HTML sanitization library: For XSS prevention in rendered Markdown
- CSS framework or responsive grid system: Bootstrap, Tailwind, or custom media queries for 3-column → 1-column responsive layout
- Authentication library: Password hashing and session management (bcrypt + secure session middleware)

## Constraints

- Mobile-first design: All features MUST be usable on 375px viewport (iPhone SE size)
- Performance: Homepage with 20 posts MUST load in under 2s on 3G connection
- Browser support: Modern browsers only (Chrome, Firefox, Safari, Edge - last 2 versions)
- Accessibility: Touch targets MUST be ≥44px on mobile, contrast ratios MUST meet WCAG AA standards
