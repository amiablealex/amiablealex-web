"""
amiablealex.com — personal project showcase.

A small, dependency-light Flask app. All project content lives as markdown
files in content/projects/ (one file per project). To add a project you create
one .md file and (optionally) drop a cover image in static/img/projects/ —
there is no database and no code to touch. See README.md.

Multi-step assembly guides live in content/guides/<slug>/ (one .md file per
step). See GUIDES.md.

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
