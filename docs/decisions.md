# Decisions

## 2026-09-17 — Keep the dark theme, remap the hexes

The brand kit specifies a light, warm-cream palette; the existing site artwork
(hero, diagrams, mockups, illustrations) was authored for a dark cool-blue
theme. Re-drawing every SVG for a light theme was out of budget, so the palette
was applied as a hex-for-hex remap: cool graphite → warm graphite, orange →
copper, accent greens/yellows → muted brand equivalents. The result is
on-brand in colour while every illustration survived untouched in shape.
Consequence: the site is dark although the brand sheet shows light — a later
light variant would have to re-author the artwork.

## 2026-09-17 — One page with anchors instead of ten pages

The navigation and footer linked to ten pages (`/how-it-works`, `/technology`,
`/security`, `/faq`, …) that were never written; only `index.html` existed. Since
the deliverable is a presentation, the content was consolidated into one page
with real section ids and every internal link rewritten to an on-page anchor.
The site now has zero dead links. Privacy and terms, which cannot be faked, are
rendered as non-clickable "скоро" labels instead of broken links.

## 2026-09-17 — `base` + `rebase()` for GitHub Pages subpaths

GitHub Pages serves a project repository from `https://<user>.github.io/<repo>/`,
so the root-absolute asset paths in the markup would 404. Rather than rewriting
every path in the sources (which breaks a future custom domain), the base prefix
lives in `site.config.json` and is applied at build time by `rebase()`. Moving
to `gostio.ai` later is a two-key config change. `canonical` and `og:image` stay
absolute via `site_url`, because social scrapers do not resolve relative URLs.

## 2026-09-17 — `brand-src/brand-tokens.css` is a reference copy, not linked

The brand kit's `tokens.css` defines `--g-accent: var(--g-copper)` (a colour),
while the site's own `design/tokens.css` already defines `--g-accent` as a
`linear-gradient` consumed by `.btn-primary`. Linking both would silently break
every primary button. Only the `.g-logo` lock-up rules were copied into the
site's `tokens.css`; the brand file is kept under `static/brand/` as a reference
for whoever authors the next theme.

## 2026-09-17 — The demo form deliberately has no backend

The site is static and there is no place to deliver leads to yet. The submit
button does not post anywhere: it prints "this is a demo, the request went
nowhere, write to us on WhatsApp or by email". Silently swallowing submissions
would lose real leads without anyone noticing, and a fake success message would
be a lie to a visitor.

## 2026-09-17 — Placeholder data is labelled on the page, not hidden

All contacts come from `brand.json`, whose `_warning` requires a visible
"demo data" badge. The placeholder state is stated in three places (top ribbon,
form note, footer line) and the phone card repeats it, so the page can be shown
to anyone without them mistaking the numbers for real ones.

## 2026-09-17 — Progressive enhancement for `.reveal`

`.reveal { opacity: 0 }` is applied only while JavaScript is running
(`html:not(.js) .reveal { opacity: 1 }` plus an inline head script adding the
class). Previously a failed or blocked `site.js` left the whole page blank below
the hero.
