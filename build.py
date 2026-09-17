#!/usr/bin/env python3
"""Static builder for the Gostio presentation site.

Every page is a body fragment in pages/<slug>.html that starts with an HTML
comment holding its front matter (title / description). The builder wraps the
fragment in layout.html, substitutes {{VARS}} from site.config.json and writes
dist/<slug>/index.html (dist/index.html for the home page).
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


def front_matter(text):
    m = re.match(r"\s*<!--(.*?)-->", text, re.S)
    if not m:
        raise SystemExit("page without front matter")
    meta = {}
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def inline_icons(html):
    """{{icon:phone}} -> the icon source itself, so `currentColor` keeps working."""
    icons = ROOT / "static" / "design" / "icons"

    def sub(m):
        f = icons / f"icon-{m.group(1)}.svg"
        if not f.exists():
            raise SystemExit(f"missing icon: {f.name}")
        return f.read_text(encoding="utf-8").strip()

    return re.sub(r"\{\{icon:([a-z]+)\}\}", sub, html)


def rebase(html, base):
    """Prefix every root-absolute href/src with the deploy base path.

    GitHub Pages serves a project repo from /<repo>/, so "/design/x.svg" would
    404 there. Protocol-relative and anchor URLs are left alone.
    """
    if not base:
        return html
    base = "/" + base.strip("/")
    return re.sub(r'(href|src)="/(?!/)', r'\1="%s/' % base, html)


def nav_html(items, slug):
    out = []
    for href, label in items:
        active = ' class="is-active"' if href.strip("/") == slug else ""
        out.append(f'<a href="{href}"{active}>{label}</a>')
    return "\n      ".join(out)


def main():
    cfg = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
    layout = (ROOT / "layout.html").read_text(encoding="utf-8")

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST)

    pages = sorted((ROOT / "pages").glob("*.html"))
    if not pages:
        raise SystemExit("no pages found")

    for page in pages:
        meta, body = front_matter(page.read_text(encoding="utf-8"))
        slug = page.stem
        html = layout
        html = html.replace("{{BODY}}", inline_icons(body))
        html = html.replace("{{NAV}}", nav_html(cfg["nav"], slug))
        html = html.replace("{{TITLE}}", meta.get("title", cfg["brand"]))
        html = html.replace("{{DESCRIPTION}}", meta.get("description", ""))
        html = html.replace("{{SLUG}}", slug)
        html = html.replace("{{LANG}}", cfg["lang"])
        html = html.replace("{{SITE_URL}}", cfg.get("site_url", ""))
        html = html.replace("{{CANONICAL}}", "/" if slug == "index" else f"/{slug}/")
        for k, v in cfg["vars"].items():
            html = html.replace("{{%s}}" % k, v)
        html = rebase(html, cfg.get("base", ""))
        left = set(re.findall(r"\{\{[A-Z_]+\}\}", html))
        if left:
            print(f"  ! {slug}: unresolved {', '.join(sorted(left))}", file=sys.stderr)
        target = DIST / ("index.html" if slug == "index" else f"{slug}/index.html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print(f"  build {target.relative_to(ROOT)}  ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
