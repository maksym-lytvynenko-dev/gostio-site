# Gostio presentation site

## Goal

A one-page marketing site for **Gostio** — an AI front-of-house administrator for
restaurants (answers calls and messages 24/7, books tables, hands reservations to
the team). The site is a *presentation*: it explains the product and collects
interest. All brand data on it is placeholder data invented for the demo.

## How it works

A tiny static generator. `pages/index.html` is a body fragment with its front
matter in a leading HTML comment; `build.py` wraps it in `layout.html`,
substitutes `{{VARS}}` from `site.config.json`, inlines the icon SVGs, prefixes
root-absolute asset paths with the deploy base path and writes `dist/`.

```
python3 build.py        # writes dist/ (static/ is copied in first)
```

There is no backend, no build tooling and no dependencies beyond Python 3.
`dist/` is what gets published.

## Where it lives

- site: <https://maksym-lytvynenko-dev.github.io/gostio-site/>
- repo: <https://github.com/maksym-lytvynenko-dev/gostio-site> (`main` = sources,
  `gh-pages` = the published `dist/`)

## Current state

- One page (`index.html`) with anchor sections: `#problem #channels #features
  #how #dashboard #audience #tech #security #faq #cta #demo #contacts`.
- Brand, logo, favicon set, OG/Twitter tags and contacts are filled in from
  `site.config.json`, generated out of `brand-src/brand.json`.
- **Every contact is a placeholder** (numbers end in zeros). The site says so in
  three places: the ribbon at the top, the note under the demo form, and the
  footer line. The demo form has no backend — it only confirms the click.
- Legal pages (privacy, terms) do not exist yet and are rendered as
  non-clickable "скоро" labels, so the site has no dead links.

## Index

- [architecture.md](architecture.md) — layout of the repo and the build pipeline
- [operations.md](operations.md) — how to build, preview and publish
- [decisions.md](decisions.md) — non-obvious decisions and why
