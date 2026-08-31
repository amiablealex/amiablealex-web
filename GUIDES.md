# Assembly guides

A guide is a folder of markdown files. One file per step, no code to touch.

```
content/guides/<guide-slug>/
  _guide.md                  step 0 — guide metadata + tools & parts
  010-clean-up-the-gears.md  step 1
  020-build-the-frame.md     step 2
  030-fit-the-cams.md        step 3

static/img/guides/<guide-slug>/     photos
static/video/guides/<guide-slug>/   short looping clips
```

## Hooking a guide to a project

Add one line to the project's markdown frontmatter in `content/projects/`:

```yaml
guide: sunrise-clock      # the folder name under content/guides/
```

or `guide: true` to use a folder with the same name as the project slug. An
"Assembly guide" button appears on the project page automatically. If the
folder or its `_guide.md` is missing, the button doesn't render and the guide
URLs 404 — so it's safe to add the line before the content exists.

## Ordering steps

Steps sort by filename, so the number prefix sets the order. Leave gaps of ten
(010, 020, 030) so a step can be slotted in later. The step number shown on the
page comes from position in the list, not from the prefix — inserting `025-`
between two steps renumbers the display correctly with no other edits.

## `_guide.md` frontmatter

```yaml
---
title: Assembly guide       # shown in the pill at the top of every step
summary: "One line."        # used for link previews
accent: clay                # any pill colour: teal, clay, olive, blue…
time: "3–4 hours"           # optional
difficulty: "No soldering"  # optional
step_title: "Tools & parts" # the heading for step 0
step_summary: "…"           # optional one-liner under it
---
```

Step files only need `title:` and an optional `summary:`.

## Media

Inside a guide, three shorthands work in ordinary markdown image syntax:

| Written | Renders as |
| --- | --- |
| `![Caption](photo.jpg)` | image from `static/img/guides/<slug>/` |
| `![Caption](video:clip.mp4)` | silent looping video from `static/video/guides/<slug>/` |
| `![Caption](youtube:VIDEO_ID)` | click-to-load YouTube embed |

Absolute paths (`/static/...`) and full URLs still work unchanged.

Two photos side by side — put them in one paragraph and tag it:

```markdown
![Before](gear-lip-before.jpg)
![After](gear-lip-after.jpg)
{: .figure-row }
```

**Where video goes.** Silent loops under ~15 seconds get encoded to MP4 and
committed to the repo. Anything longer, or with narration, goes to YouTube as
unlisted. Encoding a loop:

```bash
ffmpeg -i input.mov -t 6 -vf "scale=960:-2,fps=24" -an \
       -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p -movflags +faststart \
       clip.mp4
```

Aim for under 1.5 MB. Raise `-crf` to 30 if it comes out bigger.

## URLs

| Path | Page |
| --- | --- |
| `/projects/<slug>/guide` | redirects to step 0 |
| `/projects/<slug>/guide/0` | tools & parts |
| `/projects/<slug>/guide/4` | step 4 |
| `/projects/<slug>/guide/all` | every step on one page, for printing |

Progress ticks are stored in the reader's own browser (`localStorage`), keyed
by guide slug. Nothing is sent to the server.

## After editing

Markdown changes are read per request — a new step file appears on the next
page load. Changes to `app.py` or to anything in `templates/` need the gunicorn
service restarted.
