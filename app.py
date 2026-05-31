"""
amiablealex.com — personal project showcase.

A small, dependency-light Flask app. All project content lives as markdown
files in content/projects/ (one file per project). To add a project you create
one .md file and (optionally) drop a cover image in static/img/projects/ —
there is no database and no code to touch. See README.md.

Run locally:      flask --app app run --debug
Run with gunicorn: gunicorn app:app --bind 127.0.0.1:8005
"""

from datetime import datetime
from pathlib import Path

import frontmatter
import markdown
import os
from flask import Flask, abort, render_template, url_for

# ---------------------------------------------------------------------------
# SITE CONFIG  —  edit these values. Anything in [square brackets] is a
# placeholder for you to replace. None of this is generated content; it's yours.
# ---------------------------------------------------------------------------
SITE = {
    "name": "amiablealex",
    "tagline": "simple isn't easy",
    # The professional email shown on the Contact page (placeholder for now).
    "email": "alex@profdomain.com",
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
    return render_template("project.html", project=project, body_html=body_html, toc_html=toc_html)


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
