# Architecture

## Repository layout

```
build.py              the whole generator (~90 lines, stdlib only)
layout.html           single HTML shell: head, header, {{BODY}}, footer
site.config.json      lang, brand, site_url, base, nav, and 31 {{VARS}}
pages/index.html      body fragment + front matter in a leading HTML comment
static/               copied verbatim into dist/
  brand/              logo lock-up, marks, favicons, og-image.png
  css/site.css        page-specific styles (demo form, contacts, ribbon)
  design/             shared design system: tokens.css, components.css,
                      illustrations, mockups, icons/icon-*.svg
  js/site.js          burger menu, sticky header, scroll reveal, demo form
brand-src/            brand source of truth (brand.json, brand notes, HTML
                      sources used to render the logo sheet and OG image)
dist/                 build output — this is what is published
```

## Build pipeline

`build.py main()` per page:

1. `front_matter()` — parse `title` / `description` from the leading comment.
2. `inline_icons()` — replace `{{icon:name}}` with the icon file's own markup.
   Icons are `viewBox="0 0 24 24"` with `stroke="currentColor"`, so they must be
   inlined; referenced through `<img>` they lose the surrounding text colour.
3. `nav_html()` — render the nav from `cfg["nav"]`, marking the active item.
4. Substitute `{{TITLE}} {{DESCRIPTION}} {{SLUG}} {{LANG}} {{SITE_URL}}
   {{CANONICAL}}` and every key of `cfg["vars"]`.
5. `rebase()` — prefix each root-absolute `href="/…"` / `src="/…"` with
   `cfg["base"]`. GitHub Pages serves a project repo from `/<repo>/`, so
   `/design/x.svg` would 404 there. Absolute `https://…` values (canonical,
   `og:image`) are untouched, which is what social scrapers need.
6. Warn about any `{{VAR}}` left unresolved, then write
   `dist/index.html` (or `dist/<slug>/index.html`).

## Styling

Three stylesheets, in cascade order: `design/tokens.css` (palette, type scale,
spacing, the `.g-logo` lock-up), `design/components.css` (buttons, cards, grids,
`.reveal`), `css/site.css` (this page's own blocks). The palette is warm
graphite + copper on a dark background; see `decisions.md`.

The logo lock-up is an `<img>` mark plus a live `<span>Gostio</span>` rather than
a single wordmark SVG: text inside an `<img>`-ed SVG falls back to a system font
because the webfont does not load in that context. One `font-size` on `.g-logo`
scales the whole lock-up.

## JavaScript

`static/js/site.js` is optional by design. `layout.html` adds a `js` class to
`<html>` from an inline head script, and `site.css` carries
`html:not(.js) .reveal { opacity: 1 }` — if the script fails to load, the page
renders fully instead of going blank below the hero. The reveal itself uses an
IntersectionObserver, so sections animate in as they enter the viewport.
