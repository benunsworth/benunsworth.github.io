# Ben Unsworth — Personal Blog ([benunsworth.co.uk](https://benunsworth.co.uk))

Personal blog and weeknotes by Ben Unsworth, hosted on [GitHub Pages](https://pages.github.com/) and built with [Jekyll](https://jekyllrb.com/) using a customised [Lanyon](https://github.com/poole/lanyon) ([Poole](https://github.com/poole/poole)) theme.

---

## Writing a New Post

Create a new Markdown file in [`_posts/`](_posts/) named with the publication date and slug:

```text
_posts/YYYY-MM-DD-your-post-slug.md
```

Include the following front matter at the top of the file:

```yaml
---
layout: post
title: Your Post Title
tags: [weeknotes, local-government, ai, service-design]
---
```

### Common Tags
- `weeknotes`
- `local-government`
- `service-design`
- `ai`
- `technology`
- `leadership`
- `open-working`

*(Any new tag added to front matter will automatically appear on the [Tags](/tags/) page.)*

---

## Site Features & Architecture

All features are implemented using whitelisted GitHub Pages plugins, pure Liquid templates, and vanilla JavaScript/CSS (no custom Ruby plugins required):

- **Home Feed & Excerpts ([`index.html`](index.html)):** Displays paginated posts (5 per page via `jekyll-paginate`), rendering the first two paragraphs of each post with a *"Continue reading →"* link.
- **Estimated Reading Time ([`_includes/reading_time.html`](_includes/reading_time.html)):** Automatically calculates reading time at 200 words per minute in pure Liquid and displays it in every post header.
- **Tags & Topic Index ([`tags.md`](tags.md), [`_includes/post_tags.html`](_includes/post_tags.html)):** Groups posts by tag at `/tags/` and renders clickable `#tag` pills on posts.
- **Archive & Instant Search ([`archive.md`](archive.md), [`search.json`](search.json), [`public/js/script.js`](public/js/script.js)):** Lists all posts chronologically by year at `/archive/` and provides instant client-side full-text search across titles, tags, and post content.
- **Post Navigation & Related Posts ([`_layouts/post.html`](_layouts/post.html)):** Includes chronological **← Previous post / Next post →** links, up to 3 tag-matched related posts, and [Giscus](https://giscus.app/) comments powered by GitHub Discussions.
- **SEO, Sitemap & Syndication ([`_config.yml`](_config.yml), [`_includes/head.html`](_includes/head.html), [`atom.xml`](atom.xml)):** Uses `jekyll-seo-tag`, `jekyll-sitemap`, and `jekyll-feed` to generate Open Graph / social preview cards, `/sitemap.xml`, `/feed.xml`, and `/atom.xml`.
- **Analytics:** Privacy-friendly, cookie-free analytics via [Fullres](https://fullres.com/).

---

## Automated Quality Checks & Agent Standards

 Architectural, design, accessibility, and security rules for AI coding assistants are documented in [`AGENTS.md`](AGENTS.md).

Every push and pull request to `main` runs the [**Site Check** workflow](.github/workflows/site-check.yml), which automatically:
1. Validates post front matter schema (`title`, `type`, `status`, `updated`).
2. Builds the site using the official `actions/jekyll-build-pages` image.
3. Validates that `_site/search.json` is valid JSON and `_site/atom.xml`, `_site/feed.xml`, and `_site/sitemap.xml` are well-formed XML.
4. Checks every generated HTML page to ensure all internal links, `#anchor` IDs, local assets, and image `alt` attributes are valid.

---

## Credits & License

- Theme based on [Lanyon](https://github.com/poole/lanyon) by [Mark Otto](https://github.com/mdo).
- Open sourced under the [MIT License](LICENSE.md).
