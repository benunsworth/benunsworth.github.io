# Agent Instructions & Project Standards (`benunsworth.co.uk`)

This document defines the mandatory workflow, architectural constraints, Digital Garden taxonomy, design/accessibility standards, and security rules for any AI coding agent working on this repository.

> **Important Context:** The site owner is a digital leader, not a full-time software developer. Every technical decision must prioritise **zero ongoing maintenance**, **clarity**, **backward compatibility**, and **resilience**. Never introduce build tools, external dependencies, or fragile patterns that require developer intervention down the line.

---

## 1. Mandatory Agent Workflow

1. **Inspect First, Plan Second, Execute Only After Approval:**
   - Before making any code or content changes, inspect the relevant files in the repository.
   - Present a clear **Implementation Plan** listing the exact files to be created, modified, or deleted.
   - **Wait for explicit user approval** before modifying any repository files.
2. **Visual Preview Before Deploying UI / Layout Changes:**
   - When iterating toward **Digital Garden** visual features (e.g., card grids, status badges, typography changes, callouts, side-notes, or homepage layout updates), first create a self-contained `.html` preview artifact in Antigravity so the user can visually review and approve the design before it is committed to `main`.
3. **Clean, Atomic Commit History:**
   - Group changes into small, logical commits with descriptive commit messages explaining *what* changed and *why*.
4. **Post-Push Verification:**
   - After pushing to `origin/main`, always check the GitHub Actions runs (`gh run list`) to confirm that both the **Site Check** workflow ([`.github/workflows/site-check.yml`](.github/workflows/site-check.yml)) and **GitHub Pages deployment** (`pages-build-deployment`) succeed.

---

## 2. Strict Architectural Constraints ("No Build-Chain Creep")

- **Framework:** Native Jekyll hosted on GitHub Pages (`https://benunsworth.co.uk`).
- **Zero Custom Ruby Plugins:** Do **NOT** add files to `_plugins/` or add non-whitelisted Ruby gems to `Gemfile` / `_config.yml`. Only official GitHub Pages whitelisted plugins (`jekyll-paginate`, `jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-feed`) are permitted.
- **Zero Node / Bundler Build Pipelines:** Do **NOT** introduce `package.json`, `node_modules`, Webpack, Vite, Tailwind CLI, PostCSS, or React/Next.js build steps. The repository must always build directly via GitHub Pages with zero external pre-compilation steps.
- **Progressive Enhancement Only:**
  - All content, navigation, and metadata must render in static HTML via Liquid templates at build time so RSS readers, search engines, and users without JavaScript always receive the full content.
  - Client-side JavaScript (`public/js/script.js`) must be vanilla ES6+, dependency-free, and used strictly for progressive enhancement (e.g., live search, interactive filtering, sidebar toggle).

---

## 3. Digital Garden Architecture & "Working in the Open" Ontology

As this site evolves from a chronological blog into a **Digital Garden**, all garden features must use the site's grounded **Plain English / Working in the Open** vocabulary and be implemented with pure Liquid, Markdown front matter, and CSS:

### Content Streams (`type`)
- `weeknote` — Regular weekly reflections.
- `note` — Short thoughts, links, and fragments (*"Things I emailed myself"*). Default if `type` is omitted.
- `essay` — Longer, structured articles and arguments.
- `reading` — Books, papers, articles, and media notes (*Reading / Library*).

### Development Stage (`status`)
- `rough` — Early thinking, scratchpad notes, or a working hypothesis shared openly.
- `in-progress` — Actively being shaped, tested, or added to over time.
- `settled` — Well-formed thinking or a completed reflection.

### Dates (`date` and `updated`)
- `date` — Original publication date (automatically derived from `YYYY-MM-DD` in the `_posts/` filename unless overridden).
- `updated` — Optional `YYYY-MM-DD` date indicating when an older note or essay was last revisited and tended.

### How to Implement Digital Garden Features in Pure Liquid
- **Stream & Status Filtering:** Render `data-type="{{ post.type }}"` and `data-status="{{ post.status }}"` attributes on post cards in Liquid so pages can be filtered both via static collection pages and instant vanilla JS toggles.
- **Bidirectional Links (Backlinks):** Never use a Ruby plugin for backlinks. Instead, compute incoming links in pure Liquid within `_layouts/post.html` or an `_includes/backlinks.html` partial by checking `site.posts` where `post.url != page.url` and `post.content contains page.url`.
- **Callouts & Margin Notes:** Use standard Markdown blockquotes or semantic HTML `<aside class="callout">` styled in CSS rather than custom Liquid tags.

---

## 4. Canonical Front Matter Schema & Backward Compatibility

All existing posts in `_posts/` must continue to work without requiring manual migration. Every Digital Garden front matter field is **optional**:

```yaml
---
layout: post                                        # Defaulted in _config.yml
title: "Post Title"                                 # Required
tags: [weeknotes, local-government, ai]             # Recommended (lowercase, hyphenated)
type: note                                          # Optional: weeknote | note | essay | reading (defaults to 'note')
status: in-progress                                 # Optional: rough | in-progress | settled
updated: 2026-11-11                                 # Optional: YYYY-MM-DD date when last tended
summary: "One-sentence summary for cards and SEO."  # Optional: used in cards/previews if present
---
```

- **Tag Naming Convention:** Lowercase, hyphen-separated (`weeknotes`, `local-government`, `service-design`, `ai`, `technology`, `leadership`, `open-working`).

---

## 5. Design, CSS & Accessibility Standards

- **Design Tokens (`:root` CSS Custom Properties):**
  - When adding new visual components in `public/css/lanyon.css` (or a dedicated stylesheet), use CSS Custom Properties (`--color-text`, `--color-muted`, `--color-accent`, `--color-surface`, `--color-border`, `--radius-sm`) rather than scattering hardcoded hex values across selectors.
- **Typography & Hierarchy:**
  - Preserve the clean editorial pairing of `PT Serif` (body prose) and `PT Sans` (headings, UI controls, metadata badges, navigation).
  - Keep line lengths comfortable for reading (`32rem`–`38rem` max prose measure).
- **Mobile-First & Responsive:**
  - Every layout (especially multi-column Digital Garden card grids or sidebars) must collapse cleanly to a single column on narrow viewports (`< 38em`) with no horizontal overflow.
- **Accessibility (WCAG 2.2 AA):**
  - Maintain at least `4.5:1` colour contrast for normal text and `3:1` for large text / UI borders.
  - Use semantic HTML (`<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`, proper `<h1>`–`<h3>` nesting).
  - Every `<img>` must include a descriptive `alt` attribute (or `alt=""` if purely decorative).
  - Interactive controls (inputs, filter buttons, toggles) must be keyboard-accessible with visible `:focus-visible` outlines and appropriate `aria-label` attributes.
  - Respect `prefers-reduced-motion: reduce` for any CSS transitions or animations.
- **Language:** Use UK English spelling (`organisation`, `programme`, `user-centred`, `colour`, `prioritise`).

---

## 6. Security & Privacy Standards

- **Privacy-First:**
  - Never add third-party ad networks, tracking pixels, or cookie-based analytics. Analytics is handled exclusively by cookie-free Fullres (`_includes/head.html`).
- **DOM & XSS Safety:**
  - Whenever rendering dynamic strings in client-side JavaScript (such as search results from `search.json`), always escape HTML entities (`escapeHtml` / `textContent`) before inserting into the DOM.
- **External Links:**
  - When opening external links in a new tab (`target="_blank"`), always include `rel="noopener noreferrer"`.
- **GitHub Actions Security:**
  - All workflows in `.github/workflows/` must specify `permissions: contents: read` (least privilege) and never expose secrets or write to the repository unnecessarily.
