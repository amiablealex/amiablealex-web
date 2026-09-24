# Explainers

An explainer is a self-contained interactive HTML page — its own styles, its own
scripts, its own palette — plus a small `.md` file of metadata beside it.

The HTML file is **never edited to fit the site**. It goes in exactly as
authored and still works if you open it straight off disk. The site header,
link-preview tags and self-hosted fonts are spliced in at request time.

```
content/explainers/
  _topics.md                 optional — topic order and topic summaries
  sliding-horizon.md         metadata (frontmatter only, no body)
  sliding-horizon.html       the page itself, dropped in unmodified
  sun-arc.md
  sun-arc.html

static/img/explainers/       images, if an explainer ever needs one
```

Both files live under `content/` rather than `static/` on purpose: nginx serves
`/static/` directly, so an explainer in there would be reachable raw, bypassing
the wrapper, and would pick up the 30-day `expires`.

## Adding one

1. Drop `<slug>.html` into `content/explainers/`.
2. Add `<slug>.md` beside it:

   ```yaml
   ---
   title: The sliding horizon
   topic: Sun and moon          # groups it on /explainers; omit for a one-off
   order: 10                    # position within the topic; gaps of ten
   summary: "One or two sentences, shown on the index and in link previews."
   projects: [sunrise-clock]    # optional; adds a button on those project pages
   ---
   ```

3. That's it. Markdown is read per request, so it appears on the next page load.
   No restart needed for content — only for changes to `app.py` or `templates/`.

Metadata with no matching `.html` is skipped silently, so it's safe to write the
`.md` first.

## Topics

`topic:` is the only grouping axis. `_topics.md` sets the order topics appear in
and gives each one a summary line:

```yaml
---
topics:
  - name: Sun and moon
    summary: "One line about the set."
  - name: Another topic
---
```

The file is optional. A topic used by an explainer but not listed here still
renders — it just lands after the listed ones with no summary. Explainers with
no `topic:` collect under a final heading, set by `EXPLAINERS_UNGROUPED` in
`app.py`.

Topics don't appear in URLs (`/explainers/<slug>`, flat), so moving an explainer
between topics never breaks a link.

## What the wrapper does

`wrap_explainer()` in `app.py` makes three splices, none of which touch the file
on disk:

| Where | What |
| --- | --- |
| `<html>` | adds `data-theme="light"` |
| before `</head>` | link-preview tags, favicon, `static/css/explainer.css` |
| after `<body>` / before `</body>` | the back link and the topic nav |

**Theme.** The explainers ship a full dark mode keyed off
`prefers-color-scheme`, guarded by `:root:not([data-theme="light"])`. The site
is light-only, so the wrapper pins `data-theme="light"` and the dark palette
sits unused — until you open the file standalone, where it works as authored.

**Fonts.** The wrapper strips any `<link>` to `fonts.googleapis.com` or
`fonts.gstatic.com` and `explainer.css` declares the same families from
`static/fonts/` instead: Atkinson Hyperlegible (400 / 700 / 400 italic) and
Caveat (500 / 600). Nothing is fetched from Google at runtime, matching the rest
of the site. If a new explainer asks for a font that isn't bundled, either add
its woff2 and a `@font-face` block, or let it fall back.

## Writing a compatible explainer

The injected chrome colours itself from the page's own custom properties, so it
matches whatever palette the file defines. Define these five on `:root` and the
header and nav will look like they belong:

| Variable | Used for |
| --- | --- |
| `--bg` | page background |
| `--ink` | body text, wordmark, nav titles |
| `--muted` | back link, labels |
| `--rule` | the hairlines above and around the chrome |
| `--sun-ink` | hover / accent |

Every one has a fallback, so a file missing them still renders — it just won't
colour-match. Keep the dark-mode guards in the form
`:root:not([data-theme="light"])` for the media query and `:root[data-theme="dark"]`
for the explicit case, or pinning light won't work.

Two smaller conventions worth keeping: a `<main>` at `max-width: 760px` (the
chrome is aligned to that), and `viewport-fit=cover` with the
`env(safe-area-inset-*)` padding on `:root`.
