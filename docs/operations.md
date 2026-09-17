# Operations

## Build

```
python3 build.py
```

Rewrites `dist/` from scratch (`static/` is copied in, then each page is
rendered). A clean run prints `build dist/index.html (NN KB)` and nothing else;
any `! index: unresolved {{VAR}}` line means a variable is missing from
`site.config.json`.

## Local preview

`site.config.json` sets `base: "/gostio-site"`, so assets resolve under that
path. Serve a directory in which `dist/` is reachable as `gostio-site/`:

```
mkdir -p /tmp/serve && ln -s "$PWD/dist" /tmp/serve/gostio-site
cd /tmp/serve && python3 -m http.server 8777 --bind 127.0.0.1
# open http://127.0.0.1:8777/gostio-site/
```

Worth checking after a change: the header lock-up and favicon, the hero, that
sections reveal while scrolling, the `#demo` form button (it must answer with the
"this is a demo" message and send nothing), and the `#contacts` cards.

## Publishing (GitHub Pages)

Live: <https://maksym-lytvynenko-dev.github.io/gostio-site/>
Repo: <https://github.com/maksym-lytvynenko-dev/gostio-site>

Pages serves the **`gh-pages`** branch from its root. GitHub only offers `/` and
`/docs` as source folders, never `/dist`, so `dist/` is pushed to `gh-pages` as a
subtree:

```
python3 build.py
git add -A && git commit -m "..."
git push origin main
git subtree push --prefix dist origin gh-pages
```

`main` keeps the sources (including a committed `dist/`, so the published state
is always visible in the default branch too); `gh-pages` holds only the built
site. The Pages source is set once in Settings → Pages → *Deploy from a branch*
→ `gh-pages` / `/ (root)`; a deploy takes about a minute.

If the repository name or owner changes, update **both** keys in
`site.config.json` and rebuild:

- `base` — the path prefix Pages serves from (`/<repo>`, or `""` for a user site
  or a custom domain),
- `site_url` — the absolute origin + base, used for `canonical` and `og:image`.

A custom domain (e.g. `gostio.ai`) means `base: ""`,
`site_url: "https://gostio.ai"` and a `CNAME` file in `static/`.

## Before any public use

The contact data is fake. Replace it in `brand-src/brand.json`, regenerate
`site.config.json` from it, rebuild, and only then remove the demo ribbon in
`layout.html`, the note under the form (`FORM_NOTE`) and the footer notice. The
demo form needs a real endpoint before the ribbon goes away.
