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

The site is published from the `main` branch. Settings → Pages → *Deploy from a
branch* → `main` / `/dist`, or copy `dist/` to a `gh-pages` branch. `dist/` is
committed on purpose so no CI is needed.

If the repository name or owner changes, update **both** keys in
`site.config.json` and rebuild:

- `base` — the path prefix Pages serves from (`/<repo>`, or `""` for a user site
  or a custom domain),
- `site_url` — the absolute origin + base, used for `canonical` and `og:image`.

A custom domain (e.g. `gostio.ai`) means `base: ""` and
`site_url: "https://gostio.ai"`, plus a `CNAME` file in `dist/`.

## Before any public use

The contact data is fake. Replace it in `brand-src/brand.json`, regenerate
`site.config.json` from it, rebuild, and only then remove the demo ribbon in
`layout.html`, the note under the form (`FORM_NOTE`) and the footer notice. The
demo form needs a real endpoint before the ribbon goes away.
