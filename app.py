"""
amiablealex.com — personal project showcase.

A small, dependency-light Flask app. All project content lives as markdown
files in content/projects/ (one file per project). To add a project you create
one .md file and (optionally) drop a cover image in static/img/projects/ —
there is no database and no code to touch. See README.md.

Multi-step assembly guides live in content/guides/<slug>/ (one .md file per
step). See GUIDES.md.

Interactive explainers live in content/explainers/ as a self-contained .html
file plus a .md file of metadata beside it. See EXPLAINERS.md.

Run locally:      flask --app app run --debug
Run with gunicorn: gunicorn app:app --bind 127.0.0.1:8005
"""

from datetime import datetime
from pathlib import Path

import frontmatter
import markdown
import os
import re
from flask import Flask, abort, redirect, render_template, url_for

# ---------------------------------------------------------------------------
# SITE CONFIG  —  edit these values. Anything in [square brackets] is a
# placeholder for you to replace. None of this is generated content; it's yours.
# ---------------------------------------------------------------------------
SITE = {
    "name": "amiablealex",
    "tagline": "simple isn't easy",
    # The professional email shown on the Contact page (placeholder for now).
    "email": "contact@amiablealex.com",
    # Social links shown in the header and footer.
    "github": "https://github.com/amiablealex",
    "linkedin": "https://www.linkedin.com/in/alexbritten",
    # Used for <meta> description and link previews. One or two sentences.
    "description": "Engineer in the UK.",
    # Canonical base URL, used for absolute Open Graph URLs (no trailing slash).
    "url": "https://amiablealex.com",
}

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "content" / "projects"
GUIDES_DIR = BASE_DIR / "content" / "guides"
EXPLAINERS_DIR = BASE_DIR / "content" / "explainers"

# Heading used on /explainers for anything without a `topic:`. [ your wording ]
EXPLAINERS_UNGROUPED = "One-offs"

# Where guide media lives. Bare image filenames in a guide's markdown resolve
# against IMG_BASE/<guide-slug>/, and video: shortcodes against VIDEO_BASE.
GUIDE_IMG_BASE = "/static/img/guides"
GUIDE_VIDEO_BASE = "/static/video/guides"

# Markdown features: fenced code, tables, footnotes, attribute lists, etc.
MD_EXTENSIONS = ["extra", "sane_lists", "toc", "pymdownx.arithmatex"]
MD_EXTENSION_CONFIGS = {
    "toc": {"toc_depth": "2-3"},
    "pymdownx.arithmatex": {"generic": True},
}

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Project loading
# ---------------------------------------------------------------------------
def load_projects():
    """Read every markdown file in content/projects/ and return a list of
    project dicts, newest first. Called per request so adding a file shows up
    without restarting the server."""
    projects = []
    if not PROJECTS_DIR.exists():
        return projects

    for path in PROJECTS_DIR.glob("*.md"):
        post = frontmatter.load(path)
        meta = post.metadata
        slug = str(meta.get("slug") or path.stem)
        projects.append(
            {
                "slug": slug,
                "title": meta.get("title", slug),
                "category": meta.get("category", ""),
                "accent": meta.get("accent", "teal"),
                "summary": meta.get("summary", ""),
                "date": str(meta.get("date", "")),
                "featured": bool(meta.get("featured", False)),
                "order": meta.get("order"),
                "cover": meta.get("cover"),
                "links": meta.get("links") or [],
                "tech": meta.get("tech") or [],
                # Optional: name of a folder under content/guides/. Setting
                # `guide: true` uses a folder with the same name as the slug.
                "guide": meta.get("guide"),
                "_body": post.content,
            }
        )

    # Optional `order:` (lower number wins) overrides date. Projects without
    # an explicit order fall to the end, sorted newest-date first.
    projects.sort(key=lambda p: (
        p.get("order") if p.get("order") is not None else float("inf"),
        [-int(x) for x in p["date"].replace("-", " ").split() if x.isdigit()],
    ))
    return projects


def get_project(slug):
    for project in load_projects():
        if project["slug"] == slug:
            return project
    return None


# ---------------------------------------------------------------------------
# Guide loading
#
# content/guides/<slug>/
#   _guide.md              step 0 — guide metadata + the tools & parts list
#   010-print-the-parts.md step 1
#   020-build-the-frame.md step 2
#
# Steps sort by filename, so the numeric prefix sets the order. Leave gaps of
# ten so a step can be inserted later without renaming anything — the step
# number shown on the page comes from position in the list, not the prefix.
# ---------------------------------------------------------------------------
def guide_slug_for(project):
    """The guide folder a project points at, or None."""
    value = project.get("guide")
    if not value:
        return None
    return project["slug"] if value is True else str(value)


def load_guide(slug):
    """Return a guide dict with its ordered steps, or None if there isn't one.
    Read per request, so a new step file appears without a restart."""
    folder = GUIDES_DIR / slug
    intro_path = folder / "_guide.md"
    if not folder.is_dir() or not intro_path.exists():
        return None

    intro = frontmatter.load(intro_path)
    meta = intro.metadata

    steps = [
        {
            "number": 0,
            "title": meta.get("step_title", "Tools & parts"),
            "summary": meta.get("step_summary", ""),
            "_body": intro.content,
        }
    ]

    for number, path in enumerate(sorted(folder.glob("[0-9]*.md")), start=1):
        post = frontmatter.load(path)
        steps.append(
            {
                "number": number,
                "title": post.metadata.get("title", path.stem),
                "summary": post.metadata.get("summary", ""),
                "_body": post.content,
            }
        )

    return {
        "slug": slug,
        "title": meta.get("title", "Assembly guide"),
        "summary": meta.get("summary", ""),
        "accent": meta.get("accent", "teal"),
        "time": meta.get("time", ""),
        "difficulty": meta.get("difficulty", ""),
        "notice_title": meta.get("notice_title", ""),
        "notice": markdown.markdown(str(meta["notice"])) if meta.get("notice") else "",
        "steps": steps,
    }


# ---------------------------------------------------------------------------
# Guide media shortcodes
#
# Written as ordinary markdown images so the source stays valid markdown:
#   ![Caption](youtube:VIDEO_ID)   → click-to-load YouTube embed
#   ![Caption](video:clip.mp4)     → silent looping <video> from the repo
#   ![Caption](photo.jpg)          → bare filename → this guide's image folder
# Absolute paths (/static/...) and full URLs are left untouched.
# ---------------------------------------------------------------------------
_IMG_TAG_RE = re.compile(r"<img\b[^>]*>")
_FIGURE_IN_P_RE = re.compile(r"<p>\s*(<figure class=\"media.*?</figure>)\s*</p>", re.S)


def _attr(tag, name):
    match = re.search(r'\b%s="([^"]*)"' % name, tag)
    return match.group(1) if match else ""


def _caption(text):
    return f"<figcaption>{text}</figcaption>" if text else ""


def _youtube_figure(video_id, caption):
    label = f"Play video: {caption}" if caption else "Play video"
    return (
        '<figure class="media media-video">'
        f'<button class="video-facade" type="button" data-yt="{video_id}" aria-label="{label}">'
        f'<img class="video-thumb" src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="" loading="lazy">'
        '<span class="video-play" aria-hidden="true"></span>'
        "</button>"
        f"{_caption(caption)}"
        "</figure>"
    )


def _clip_figure(src, caption):
    return (
        '<figure class="media media-clip">'
        f'<video src="{src}" autoplay loop muted playsinline preload="metadata"></video>'
        f"{_caption(caption)}"
        "</figure>"
    )


def _expand_media(html, guide_slug):
    def replace(match):
        tag = match.group(0)
        src = _attr(tag, "src")
        alt = _attr(tag, "alt")

        if src.startswith("youtube:"):
            return _youtube_figure(src.split(":", 1)[1].strip(), alt)
        if src.startswith("video:"):
            filename = src.split(":", 1)[1].strip()
            return _clip_figure(f"{GUIDE_VIDEO_BASE}/{guide_slug}/{filename}", alt)
        if "/" not in src and ":" not in src:
            resolved = f"{GUIDE_IMG_BASE}/{guide_slug}/{src}"
            return tag.replace(f'src="{src}"', f'src="{resolved}"')
        return tag

    html = _IMG_TAG_RE.sub(replace, html)
    # A lone image becomes <p><img></p>; unwrap the <figure> we swapped in.
    return _FIGURE_IN_P_RE.sub(r"\1", html)


def render_step(step, guide_slug):
    md = markdown.Markdown(
        extensions=MD_EXTENSIONS, extension_configs=MD_EXTENSION_CONFIGS
    )
    return _expand_media(md.convert(step["_body"]), guide_slug)


def _guide_or_404(slug):
    """Resolve a project slug to (project, guide), 404ing if either is missing."""
    project = get_project(slug)
    if project is None:
        abort(404)
    folder = guide_slug_for(project)
    guide = load_guide(folder) if folder else None
    if guide is None:
        abort(404)
    return project, guide


# ---------------------------------------------------------------------------
# Explainer loading
#
# content/explainers/
#   _topics.md              optional — topic order and topic summaries
#   sliding-horizon.md      metadata only (frontmatter, no body)
#   sliding-horizon.html    the self-contained interactive page
#
# The .html file is authored elsewhere and dropped in unmodified — it keeps its
# own <head>, styles and scripts. Nothing edits it; the site header, link-preview
# tags and self-hosted fonts are spliced in at request time by wrap_explainer().
# Living under content/ rather than static/ means nginx can't serve the raw file
# straight past Flask, so there's exactly one URL for each explainer.
# ---------------------------------------------------------------------------
def load_explainers():
    """Every explainer with both a .md and a matching .html, ordered within
    topic by `order:` (lower first), then by title."""
    items = []
    if not EXPLAINERS_DIR.exists():
        return items

    for path in sorted(EXPLAINERS_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta = frontmatter.load(path).metadata
        slug = str(meta.get("slug") or path.stem)
        # Metadata without a page yet is skipped rather than 500-ing.
        if not (EXPLAINERS_DIR / f"{slug}.html").exists():
            continue
        items.append(
            {
                "slug": slug,
                "title": meta.get("title", slug),
                "topic": str(meta.get("topic") or ""),
                "order": meta.get("order"),
                "summary": meta.get("summary", ""),
                # Slugs of projects that should show a link to this explainer.
                "projects": meta.get("projects") or [],
            }
        )

    items.sort(key=lambda e: (
        e["order"] if e["order"] is not None else float("inf"),
        e["title"],
    ))
    return items


def load_topics():
    """The declared topics from _topics.md, in the order they're listed."""
    path = EXPLAINERS_DIR / "_topics.md"
    if not path.exists():
        return []
    topics = frontmatter.load(path).metadata.get("topics") or []
    return [t for t in topics if isinstance(t, dict) and t.get("name")]


def grouped_explainers():
    """Explainers bucketed by topic: declared topics first in their declared
    order, then any undeclared topic alphabetically, then the untopiced."""
    declared = load_topics()
    position = {t["name"]: i for i, t in enumerate(declared)}
    summary_for = {t["name"]: t.get("summary", "") for t in declared}

    buckets = {}
    for item in load_explainers():
        buckets.setdefault(item["topic"], []).append(item)

    names = sorted(
        (n for n in buckets if n),
        key=lambda n: (position.get(n, len(position)), n),
    )

    groups = [
        {
            "name": name,
            "summary": summary_for.get(name, ""),
            "declared": name in position,
            "explainers": buckets[name],
        }
        for name in names
    ]
    if "" in buckets:
        groups.append(
            {
                "name": EXPLAINERS_UNGROUPED,
                "summary": "",
                "declared": False,
                "explainers": buckets[""],
            }
        )
    return groups


def explainers_for_project(slug):
    return [e for e in load_explainers() if slug in e["projects"]]


# ---------------------------------------------------------------------------
# Explainer page wrapping
#
# Three splices into the file as authored, none of which touch it on disk:
#   1. data-theme="light" on <html>  — pins the site's light palette, leaving
#      the file's own dark mode intact when it's opened standalone
#   2. before </head>  — link-preview tags, favicon, and explainer.css, which
#      self-hosts the fonts the file would otherwise pull from Google
#   3. after <body> and before </body>  — the back link and the topic nav
#
# The injected chrome styles itself from the explainer's own CSS variables, so
# any file defining --ink, --muted, --rule and --sun-ink is compatible as-is.
# ---------------------------------------------------------------------------
_WEBFONT_LINK_RE = re.compile(
    r"[ \t]*<link\b[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*", re.I
)
_HTML_TAG_RE = re.compile(r"<html\b", re.I)
_BODY_OPEN_RE = re.compile(r"<body\b[^>]*>", re.I)


def wrap_explainer(explainer, prev_item=None, next_item=None):
    path = EXPLAINERS_DIR / f"{explainer['slug']}.html"
    html = path.read_text(encoding="utf-8")

    html = _WEBFONT_LINK_RE.sub("", html)
    html = _HTML_TAG_RE.sub('<html data-theme="light"', html, count=1)

    head = render_template("_explainer_head.html", explainer=explainer)
    top = render_template("_explainer_chrome.html", explainer=explainer)
    foot = render_template(
        "_explainer_nav.html",
        explainer=explainer,
        prev_item=prev_item,
        next_item=next_item,
    )

    html = html.replace("</head>", f"{head}\n</head>", 1)
    html = _BODY_OPEN_RE.sub(lambda m: f"{m.group(0)}\n{top}", html, count=1)
    html = html.replace("</body>", f"{foot}\n</body>", 1)
    return html


@app.context_processor
def inject_globals():
    return {"site": SITE, "current_year": datetime.now().year}

@app.context_processor
def inject_static_url():
    def static_url(filename):
        path = os.path.join(app.static_folder, filename)
        try:
            v = int(os.path.getmtime(path))
        except OSError:
            v = 0
        return url_for("static", filename=filename) + f"?v={v}"
    return {"static_url": static_url}

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    featured = [p for p in load_projects() if p["featured"]]
    return render_template("index.html", projects=featured)


@app.route("/projects")
def projects():
    all_projects = load_projects()
    # Distinct categories, in first-seen order, for the filter controls.
    categories = []
    for p in all_projects:
        if p["category"] and p["category"] not in categories:
            categories.append(p["category"])
    return render_template(
        "projects.html", projects=all_projects, categories=categories
    )


@app.route("/projects/<slug>")
def project_detail(slug):
    project = get_project(slug)
    if project is None:
        abort(404)
    md = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_EXTENSION_CONFIGS)
    body_html = md.convert(project["_body"])
    # Only render the sidebar if there are 2+ top-level sections worth navigating.
    toc_html = md.toc if len(getattr(md, "toc_tokens", [])) >= 2 else None
    has_guide = load_guide(guide_slug_for(project)) is not None if guide_slug_for(project) else False
    return render_template(
        "project.html",
        project=project,
        body_html=body_html,
        toc_html=toc_html,
        has_guide=has_guide,
        related_explainers=explainers_for_project(slug),
    )


@app.route("/projects/<slug>/guide")
def project_guide(slug):
    _guide_or_404(slug)
    return redirect(url_for("project_guide_step", slug=slug, number=0))


@app.route("/projects/<slug>/guide/<int:number>")
def project_guide_step(slug, number):
    project, guide = _guide_or_404(slug)
    if not 0 <= number < len(guide["steps"]):
        abort(404)
    step = guide["steps"][number]
    return render_template(
        "guide_step.html",
        project=project,
        guide=guide,
        step=step,
        body_html=render_step(step, guide["slug"]),
        prev_step=guide["steps"][number - 1] if number > 0 else None,
        next_step=guide["steps"][number + 1] if number + 1 < len(guide["steps"]) else None,
    )


@app.route("/projects/<slug>/guide/all")
def project_guide_all(slug):
    project, guide = _guide_or_404(slug)
    rendered = [(s, render_step(s, guide["slug"])) for s in guide["steps"]]
    return render_template(
        "guide_all.html", project=project, guide=guide, rendered=rendered
    )


@app.route("/explainers")
def explainers():
    return render_template("explainers.html", groups=grouped_explainers())


@app.route("/explainers/<slug>")
def explainer_detail(slug):
    for group in grouped_explainers():
        for i, item in enumerate(group["explainers"]):
            if item["slug"] == slug:
                return wrap_explainer(
                    item,
                    prev_item=group["explainers"][i - 1] if i > 0 else None,
                    next_item=group["explainers"][i + 1] if i + 1 < len(group["explainers"]) else None,
                )
    abort(404)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=8005)
