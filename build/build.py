#!/usr/bin/env python3
"""Render the static documentation site.

Content lives in content_emop.py and content_coe.py. This module owns the
shared chrome — top bar, sidebar, breadcrumbs, on-page contents, pager — so
every page is structurally identical.

Usage: python3 build/build.py
"""

from __future__ import annotations

import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from content_coe import COE_PAGES, COE_SECTIONS  # noqa: E402
from content_emop import EMOP_PAGES, EMOP_SECTIONS  # noqa: E402

AUTHOR = "Gehad Sayed Ahmed"
BASE = "https://gegesay89.github.io"

MARK = (
    '<svg width="19" height="19" viewBox="0 0 20 20" aria-hidden="true">'
    '<rect x="1" y="1" width="18" height="18" rx="4" fill="none" stroke="#0f5d6e" stroke-width="1.7"/>'
    '<path d="M5.5 12.5 L8 7.5 L10.5 12.5 L14.5 7.5" fill="none" stroke="#0f5d6e" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

PROJECTS = {
    "emop": {
        "badge": "Data model",
        "name": "EMOP",
        "root": "/emop/",
        "sections": EMOP_SECTIONS,
        "pages": EMOP_PAGES,
        "repo": "https://github.com/gegesay89/emop",
        "footer": "Core model courtesy of the OHDSI community",
    },
    "coe": {
        "badge": "Software",
        "name": "COE",
        "root": "/coe/",
        "sections": COE_SECTIONS,
        "pages": COE_PAGES,
        "repo": "https://github.com/gegesay89/coe-corpus-ontology-enricher",
        "footer": "Apache License 2.0",
    },
}


def topbar(active: str) -> str:
    def link(href: str, label: str, key: str) -> str:
        cls = ' class="on"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'

    return f"""<header class="topbar">
  <div class="topbar-inner">
    <a class="wordmark" href="/">{MARK}<span>{AUTHOR}</span></a>
    <nav class="topnav">
      {link("/", "Overview", "home")}
      {link("/emop/", "EMOP", "emop")}
      {link("/coe/", "COE", "coe")}
      <a href="https://github.com/gegesay89">GitHub</a>
    </nav>
  </div>
</header>"""


def sidebar(project_key: str, slug: str) -> str:
    project = PROJECTS[project_key]
    out = [
        '<aside class="sidebar">',
        f'<span class="project-badge">{project["badge"]}</span>',
        f'<a class="project-name" href="{project["root"]}">{project["name"]}</a>',
        '<div class="nav-groups">',
    ]
    for group_title, entries in project["sections"]:
        out.append('<div class="nav-group">')
        out.append(f"<h4>{group_title}</h4><ul>")
        for entry_slug, label in entries:
            href = project["root"] if entry_slug == "" else f'{project["root"]}{entry_slug}/'
            current = ' aria-current="page"' if entry_slug == slug else ""
            out.append(f'<li><a href="{href}"{current}>{label}</a></li>')
        out.append("</ul></div>")
    out.append("</div></aside>")
    return "\n".join(out)


def slugify(text: str) -> str:
    plain = re.sub(r"<[^>]+>", "", text)
    plain = html.unescape(plain).lower()
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-")


def add_heading_anchors(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Give every h2 an id and collect them for the on-page contents."""
    found: list[tuple[str, str]] = []

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        anchor = slugify(inner)
        found.append((anchor, re.sub(r"<[^>]+>", "", inner)))
        return f'<h2 id="{anchor}">{inner}<a class="anchor" href="#{anchor}" aria-label="Link to this section">#</a></h2>'

    return re.sub(r"<h2>(.*?)</h2>", repl, body, flags=re.S), found


def toc(items: list[tuple[str, str]]) -> str:
    if len(items) < 3:
        return ""
    links = "\n".join(f'<li><a href="#{a}">{html.escape(t)}</a></li>' for a, t in items)
    return f'<aside class="toc"><h4>On this page</h4><ul>\n{links}\n</ul></aside>'


def pager(project_key: str, slug: str) -> str:
    project = PROJECTS[project_key]
    ordered: list[tuple[str, str]] = []
    for _group, entries in project["sections"]:
        ordered.extend(entries)
    slugs = [s for s, _ in ordered]
    if slug not in slugs:
        return ""
    index = slugs.index(slug)
    parts = []
    if index > 0:
        s, label = ordered[index - 1]
        href = project["root"] if s == "" else f'{project["root"]}{s}/'
        parts.append(
            f'<a class="prev" href="{href}"><span class="dir">Previous</span>'
            f'<span class="ttl">{label}</span></a>'
        )
    if index < len(ordered) - 1:
        s, label = ordered[index + 1]
        href = project["root"] if s == "" else f'{project["root"]}{s}/'
        parts.append(
            f'<a class="next" href="{href}"><span class="dir">Next</span>'
            f'<span class="ttl">{label}</span></a>'
        )
    return f'<nav class="pager">{"".join(parts)}</nav>' if parts else ""


def footer(extra: str) -> str:
    return f"""<footer class="foot">
  <div class="foot-inner">
    <p>{AUTHOR}</p>
    <p>{extra}</p>
  </div>
</footer>"""


def page_shell(*, title: str, description: str, canonical: str, active: str, body: str, foot: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/assets/docs.css">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
</head>
<body>
{topbar(active)}
{body}
{foot}
<script src="/assets/docs.js" defer></script>
</body>
</html>
"""


def write(rel_dir: str, content: str) -> pathlib.Path:
    target = ROOT / rel_dir / "index.html" if rel_dir else ROOT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def build_doc_pages() -> list[pathlib.Path]:
    written = []
    for key, project in PROJECTS.items():
        for slug, spec in project["pages"].items():
            body_html, headings = add_heading_anchors(spec["body"].strip())
            contents = toc(headings)
            shell_class = "shell" if contents else "shell no-toc"

            crumbs = (
                '<nav class="crumbs"><a href="/">Overview</a><span>/</span>'
                f'<a href="{project["root"]}">{project["name"]}</a>'
            )
            crumbs += "" if slug == "" else f'<span>/</span>{html.escape(spec["nav"])}'
            crumbs += "</nav>"

            main = (
                f"<main>{crumbs}"
                f'<h1>{spec["h1"]}</h1>'
                f'<p class="standfirst">{spec["standfirst"]}</p>'
                f"{body_html}"
                f"{pager(key, slug)}"
                "</main>"
            )

            body = f'<div class="{shell_class}">{sidebar(key, slug)}{main}{contents}</div>'
            rel = project["root"].strip("/") if slug == "" else f'{project["root"].strip("/")}/{slug}'
            written.append(
                write(
                    rel,
                    page_shell(
                        title=spec["title"],
                        description=spec["description"],
                        canonical=f"{BASE}{project['root']}" + ("" if slug == "" else f"{slug}/"),
                        active=key,
                        body=body,
                        foot=footer(project["footer"]),
                    ),
                )
            )
    return written


HOME_BODY = """
<div class="shell plain">
  <div class="masthead">
    <div class="measure">
      <span class="eyebrow">Open source</span>
      <h1>Health data standards and clinical text tooling.</h1>
      <p>Two independent projects, documented in full and published under the Apache License 2.0:
      a relational data model for observational health records collected in Egypt, and a
      deterministic system for analysing clinical text against controlled terminologies.</p>
      <a class="cta" href="/emop/">Read the EMOP documentation</a>
      <a class="cta ghost" href="/coe/">Read the COE documentation</a>
    </div>
  </div>

  <section class="band">
    <h2>Projects</h2>
    <div class="cardgrid">
      <article class="card">
        <h3>EMOP</h3>
        <p class="sub">Egyptian Medical Observational Profile &middot; version 0.1</p>
        <p>A PostgreSQL data model for observational health records in Egypt. Thirty-nine
        international core tables carry the clinical record; thirteen additional tables carry
        national identifiers, the twenty-seven governorates, public and military insurance,
        referrals between facilities, bilingual names, and national code lists mapped to
        standard concepts.</p>
        <div class="links">
          <a href="/emop/">Documentation</a>
          <a href="https://github.com/gegesay89/emop">Repository</a>
        </div>
      </article>
      <article class="card">
        <h3>COE</h3>
        <p class="sub">Corpus Ontology Enricher &middot; version 0.4 alpha</p>
        <p>An offline system that matches phrases in clinical text to pinned terminology
        releases and reports coding frequency, mention context, unmapped candidate terms, and
        code co-occurrence. Suppression and scrubbing are applied before any row leaves the
        process, and every result is bound to the exact inputs that produced it.</p>
        <div class="links">
          <a href="/coe/">Documentation</a>
          <a href="https://github.com/gegesay89/coe-corpus-ontology-enricher">Repository</a>
        </div>
      </article>
    </div>
  </section>

  <section class="band">
    <h2>Principles</h2>
    <div class="tw"><table class="tight">
      <thead><tr><th style="width:14rem">Principle</th><th>In practice</th></tr></thead>
      <tbody>
        <tr><td><strong>Build on standards</strong></td>
            <td>Both projects extend established specifications rather than replacing them, and
            state precisely where and why they diverge.</td></tr>
        <tr><td><strong>Declare provenance</strong></td>
            <td>Every code carries its source and its status. Illustrative content is labelled
            in the data itself, never presented as an official release.</td></tr>
        <tr><td><strong>Stay reproducible</strong></td>
            <td>Deterministic execution with no network dependency. Results can be rebuilt from
            pinned inputs and verified against them afterwards.</td></tr>
        <tr><td><strong>Protect by construction</strong></td>
            <td>No patient data in either repository. Licensed terminology payloads are never
            committed to public source control.</td></tr>
      </tbody>
    </table></div>
  </section>
</div>
"""

NOT_FOUND_BODY = """
<div class="shell plain">
  <div class="masthead">
    <div class="measure">
      <span class="eyebrow">Error 404</span>
      <h1>That page does not exist.</h1>
      <p>The address may be mistyped, or the page may have moved. The two documentation
      sections below are the best place to start.</p>
      <a class="cta" href="/emop/">EMOP documentation</a>
      <a class="cta ghost" href="/coe/">COE documentation</a>
    </div>
  </div>
</div>
"""


def build_static() -> list[pathlib.Path]:
    written = [
        write(
            "",
            page_shell(
                title=f"{AUTHOR} — Health data standards and clinical text tooling",
                description=(
                    "Open-source health data standards and clinical text tooling: EMOP, a data "
                    "model for Egyptian observational health records, and COE, a corpus "
                    "ontology enricher."
                ),
                canonical=f"{BASE}/",
                active="home",
                body=HOME_BODY,
                foot=footer('Apache License 2.0 · <a href="https://github.com/gegesay89">github.com/gegesay89</a>'),
            ),
        )
    ]
    not_found = page_shell(
        title="Page not found",
        description="The requested page does not exist.",
        canonical=f"{BASE}/404.html",
        active="home",
        body=NOT_FOUND_BODY,
        foot=footer("Apache License 2.0"),
    )
    (ROOT / "404.html").write_text(not_found, encoding="utf-8")
    written.append(ROOT / "404.html")
    return written


def main() -> int:
    written = build_static() + build_doc_pages()
    for path in sorted(written):
        print(path.relative_to(ROOT))
    print(f"\n{len(written)} pages written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
