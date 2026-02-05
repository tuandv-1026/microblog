# Testing Guide for Microblog Platform

## Overview

This document provides comprehensive testing procedures for the Microblog platform, covering unit tests, integration tests, manual testing, and end-to-end testing.

---

## 🧪 Automated Testing

### Backend Unit Tests

**Location:** `backend/tests/unit/`

**Run all unit tests:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pytest tests/unit/ -v
```

**Unit test categories:**

1. **Service Tests** (`test_auth_service.py`, `test_markdown_service.py`)
   - Password hashing and verification
   - Markdown rendering and sanitization
   - Excerpt generation
   - View counter session tracking

2. **Use Case Tests** (`test_auth_usecase.py`)
   - User registration logic
   - Login validation
   - Post creation workflow
   - Draft/publish transitions

3. **Repository Tests** (if implemented)
   - Database query logic
   - Filtering and sorting
   - Relationship loading

**Expected Coverage:** ≥80%

### Backend Integration Tests

**Location:** `backend/tests/integration/`

**Run all integration tests:**
```bash
pytest tests/integration/ -v
```

**Integration test categories:**

1. **Authentication Router** (`test_auth_router.py`)
   - POST /api/auth/register
   - POST /api/auth/login
   - POST /api/auth/logout
   - GET /api/auth/me

2. **Posts Router** (`test_posts_router.py`)
   - GET /api/posts (list with filters)
   - GET /api/posts/{slug} (single post + view counter)
   - POST /api/posts (create)
   - PUT /api/posts/{id} (update)
   - DELETE /api/posts/{id} (delete)

3. **Comments & Reactions** (`test_comments_router.py`, `test_reactions_router.py`)
   - Comment CRUD operations
   - Reaction toggle logic
   - Reaction summaries

4. **Search & Categories** (`test_search_router.py`, `test_categories_router.py`)
   - Full-text search
   - Category listing with post counts

**Test Database:** Uses in-memory SQLite or test MySQL instance

### Frontend Tests (Future)

**To be implemented:**
- Component unit tests with Jest + React Testing Library
- API integration mocking with MSW (Mock Service Worker)
- Accessibility tests with jest-axe
- Visual regression tests with Percy or Chromatic

---

## 🖱️ Manual Testing

### Test Environment Setup

1. **Start application:**
   ```bash
   docker-compose up -d
   docker-compose exec backend alembic upgrade head
   docker-compose exec backend python scripts/seed_data.py
   ```

2. **Access application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

3. **Test accounts:**
   - Admin: `admin` / `admin123`
   - Author1: `author1` / `password1`
   - Author2: `author2` / `password2`

---

## ✅ Manual Test Cases

### TC001: Guest User - Browse Posts

**Preconditions:** No login required

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to http://localhost:3000 | Homepage loads with 3-column layout |
| 2 | Observe homepage | See recent posts (left), post list (center), categories (right) |
| 3 | Click on a post title | Navigate to full post page |
| 4 | Scroll to see Markdown content | Content renders properly with formatting |
| 5 | Check view counter | View count increases by 1 (first view) |
| 6 | Refresh page | View count stays same (session tracking works) |

**Status:** ✅ Pass / ❌ Fail

---

### TC002: Guest User - Filter by Category

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | On homepage, click "Technology" in sidebar | Navigate to /category/technology |
| 2 | Observe post list | Only posts with "Technology" category shown |
| 3 | Check sidebar | Categories still visible |
| 4 | Click another category | Filter updates to new category |

**Status:** ✅ Pass / ❌ Fail

---

### TC003: Guest User - Search Posts

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Enter "tutorial" in search bar | Search input accepts text |
| 2 | Press Enter or click search button | Navigate to /search?q=tutorial |
| 3 | Observe results | Posts matching "tutorial" displayed |
| 4 | Check result count | "X results for 'tutorial'" shown |
| 5 | Try empty search | No navigation or error message |

**Status:** ✅ Pass / ❌ Fail

---

### TC004: Guest User - Sort Posts

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | On homepage, click sort dropdown | Options: Newest, Oldest, Most Likes, Most Views |
| 2 | Select "Oldest" | Posts reorder by oldest first |
| 3 | Select "Most Views" | Posts reorder by view count descending |
| 4 | Navigate to another page and back | Sort preference maintained |

**Status:** ✅ Pass / ❌ Fail

---

### TC005: User Registration

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Register" in header | Navigate to /register |
| 2 | Fill email: test@example.com | Input accepts email |
| 3 | Fill username: testuser | Input accepts text |
| 4 | Fill password: testpass123 | Password masked |
| 5 | Fill confirm password: testpass123 | Password masked |
| 6 | Click "Register" | Success message, navigate to /login |

**Status:** ✅ Pass / ❌ Fail

---

### TC006: User Login

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Login" in header | Navigate to /login |
| 2 | Enter email: admin@example.com | Input accepts email |
| 3 | Enter password: admin123 | Password masked |
| 4 | Click "Login" | Page reloads, nav shows "Hi, admin" |
| 5 | Check navigation | "New Post" and "My Drafts" links visible |
| 6 | Check "Login/Register" buttons | Hidden (replaced with user menu) |

**Status:** ✅ Pass / ❌ Fail

---

### TC007: Create Draft Post

**Preconditions:** Logged in as admin

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "New Post" in header | Navigate to /posts/new |
| 2 | Enter title: "My Test Post" | Slug auto-generates: "my-test-post" |
| 3 | Enter excerpt: "This is a test" | Excerpt saved |
| 4 | Check "Technology" and "Tutorial" categories | Categories selected |
| 5 | Write Markdown: "## Hello World" | Editor accepts Markdown |
| 6 | Click "Preview" button | Content renders as HTML heading |
| 7 | Click "Edit" button | Return to Markdown editor |
| 8 | Click "Save Draft" | Navigate to /my-drafts |
| 9 | Observe draft list | "My Test Post" appears in drafts |

**Status:** ✅ Pass / ❌ Fail

---

### TC008: Publish Post

**Preconditions:** Draft "My Test Post" exists

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Navigate to /my-drafts | See draft list |
| 2 | Click "Edit" on draft | Navigate to /posts/{id}/edit |
| 3 | Verify content loaded | Title, content, categories filled |
| 4 | Click "Update & Publish" | Navigate to /posts/my-test-post |
| 5 | Check post page | Post displays with "Published" badge |
| 6 | Navigate to homepage | Post appears in main feed |

**Status:** ✅ Pass / ❌ Fail

---

### TC009: Edit Own Post

**Preconditions:** Published post exists, logged in as author

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open published post | Post page loads |
| 2 | Check for "Edit Post" button | Button visible (author only) |
| 3 | Click "Edit Post" | Navigate to /posts/{id}/edit |
| 4 | Change title to "Updated Title" | Title updates |
| 5 | Click "Update & Publish" | Navigate to post page with new title |

**Status:** ✅ Pass / ❌ Fail

---

### TC010: Add Comment

**Preconditions:** Viewing a published post

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Scroll to comments section | Comment form visible |
| 2 | Enter name: "John Doe" | Input accepts text |
| 3 | Enter email: john@example.com | Input accepts email |
| 4 | Enter comment: "Great post!" | Textarea accepts text |
| 5 | Click "Post Comment" | Comment appears in list below |
| 6 | Check comment count | "Comments (1)" updates |

**Status:** ✅ Pass / ❌ Fail

---

### TC011: React to Post

**Preconditions:** Logged in user viewing a post

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Scroll to reactions section | 6 emoji buttons visible |
| 2 | Click "👍 Like" | Button highlights, count increments to "(1)" |
| 3 | Click "👍 Like" again | Button unhighlights, count decrements to "Like" |
| 4 | Click "❤️ Love" | Love count increments, Like stays off |
| 5 | Refresh page | Reaction state persists |

**Status:** ✅ Pass / ❌ Fail

---

### TC012: Logout

**Preconditions:** Logged in user

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Click "Logout" in header | Page reloads |
| 2 | Check navigation | "Login" and "Register" buttons visible |
| 3 | Check protected links | "New Post" and "My Drafts" hidden |
| 4 | Try to access /posts/new | Redirected or 401 error |

**Status:** ✅ Pass / ❌ Fail

---

## 📱 Responsive Design Testing

### Viewport Sizes to Test

| Device | Width | Expected Layout |
|--------|-------|----------------|
| iPhone SE | 375px | Single column, stacked |
| iPad | 768px | 2 columns (main + sidebar) |
| Desktop | 1024px+ | 3 columns (recent + main + sidebar) |

### Test Cases

**TC013: Mobile Responsive (375px)**

| Element | Expected Behavior |
|---------|------------------|
| Header | Collapses to hamburger menu (if implemented) |
| Navigation links | Stacked vertically |
| Homepage | Single column, full width |
| Sidebar | Moves below main content |
| Post cards | Full width, readable text |
| Forms | Full width inputs, easy to tap |
| Buttons | ≥44px tap target |

**TC014: Tablet Responsive (768px)**

| Element | Expected Behavior |
|---------|------------------|
| Homepage | 2 columns (main + sidebar) |
| Recent posts | Hidden or below main content |
| Navigation | Horizontal nav bar |
| Forms | Comfortable input sizing |

**TC015: Desktop (1024px+)**

| Element | Expected Behavior |
|---------|------------------|
| Homepage | 3 columns (250px + 1fr + 250px) |
| All sidebars | Visible and fixed width |
| Navigation | Full horizontal menu |
| Max content width | Comfortable reading width |

---

## 🔒 Security Testing

### TC016: XSS Prevention

| Test | Input | Expected Result |
|------|-------|----------------|
| 1 | Post content: `<script>alert('xss')</script>` | Script stripped, displays as text |
| 2 | Comment: `<img src=x onerror=alert(1)>` | Tag stripped or escaped |
| 3 | Title: `<b>Bold</b>` | HTML escaped |

---

### TC017: Authorization Checks

| Test | Action | Expected Result |
|------|--------|----------------|
| 1 | Edit other user's post | 403 Forbidden |
| 2 | Delete other user's post | 403 Forbidden |
| 3 | Access admin endpoint without admin role | 403 Forbidden |

---

### TC018: Session Security

| Test | Expected Result |
|------|----------------|
| Check session cookie | `HttpOnly`, `SameSite=Lax` flags set |
| Password in database | bcrypt hash, not plaintext |
| Logout clears session | Cookie removed, session invalid |

---

## ⚡ Performance Testing

### TC019: Page Load Performance

**Tool:** Chrome DevTools Lighthouse

| Page | Target Load Time | Target Performance Score |
|------|-----------------|------------------------|
| Homepage | <2s | ≥90 |
| Post page | <2s | ≥90 |
| Search results | <2s | ≥85 |

**Test conditions:**
- Simulated 3G connection (Fast 3G in DevTools)
- 20 posts in database
- Images optimized

---

### TC020: Database Query Performance

| Query | Target Time | Test |
|-------|------------|------|
| List posts | <100ms | GET /api/posts |
| Single post | <50ms | GET /api/posts/{slug} |
| Search | <200ms | GET /api/search?q=keyword |

**Monitor with:** SQL logging, APM tools (e.g., New Relic)

---

## 📊 Test Execution Summary

### Test Execution Template

**Date:** ____________  
**Tester:** ____________  
**Environment:** Docker / Local  
**Browser:** Chrome / Firefox / Safari  

| Test ID | Test Name | Status | Notes |
|---------|-----------|--------|-------|
| TC001 | Browse Posts | ☐ Pass ☐ Fail | |
| TC002 | Filter by Category | ☐ Pass ☐ Fail | |
| TC003 | Search Posts | ☐ Pass ☐ Fail | |
| TC004 | Sort Posts | ☐ Pass ☐ Fail | |
| TC005 | User Registration | ☐ Pass ☐ Fail | |
| TC006 | User Login | ☐ Pass ☐ Fail | |
| TC007 | Create Draft Post | ☐ Pass ☐ Fail | |
| TC008 | Publish Post | ☐ Pass ☐ Fail | |
| TC009 | Edit Own Post | ☐ Pass ☐ Fail | |
| TC010 | Add Comment | ☐ Pass ☐ Fail | |
| TC011 | React to Post | ☐ Pass ☐ Fail | |
| TC012 | Logout | ☐ Pass ☐ Fail | |
| TC013 | Mobile Responsive | ☐ Pass ☐ Fail | |
| TC014 | Tablet Responsive | ☐ Pass ☐ Fail | |
| TC015 | Desktop Layout | ☐ Pass ☐ Fail | |
| TC016 | XSS Prevention | ☐ Pass ☐ Fail | |
| TC017 | Authorization | ☐ Pass ☐ Fail | |
| TC018 | Session Security | ☐ Pass ☐ Fail | |
| TC019 | Page Load Performance | ☐ Pass ☐ Fail | |
| TC020 | Database Performance | ☐ Pass ☐ Fail | |

**Overall Status:** ____% Passed (____/20 tests)

---

## 🐛 Bug Report Template

When you find a bug during testing, report it using this template:

```markdown
**Bug ID:** BUG-XXX
**Title:** Brief description
**Severity:** Critical / High / Medium / Low
**Priority:** P1 / P2 / P3
**Environment:** Docker / Local, Browser, OS

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**


**Actual Result:**


**Screenshots:** (if applicable)


**Console Errors:** (if any)


**Additional Notes:**

```

---

## 📅 Testing Schedule

### Pre-Release Testing

- **Week 1:** Unit tests + Integration tests (Backend)
- **Week 2:** Manual testing (all user flows)
- **Week 3:** Responsive design testing
- **Week 4:** Security audit + Performance testing
- **Week 5:** Regression testing + Bug fixes

### Continuous Testing

- Run unit tests on every commit
- Run integration tests before merging to main
- Manual smoke tests before deployment
- Performance tests weekly

---

## ✅ Sign-Off

This testing guide has been reviewed and approved:

- **Developer:** ______________________ Date: ______
- **QA Lead:** ______________________ Date: ______
- **Product Owner:** ______________________ Date: ______

---

**Last Updated:** February 2026  
**Version:** 1.0
