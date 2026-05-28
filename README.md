# amiablealex.com

A small, self-hosted personal project showcase. Flask + a folder of markdown
files — no database, no build step. Designed to be hosted on a Raspberry Pi
behind nginx, Gunicorn, and a Cloudflare tunnel.

> Theme: "engineer's notebook" — off-white paper, a faint dot-grid, one
> dusty-teal accent, and a single hand-drawn flourish. Tagline: *simple isn't easy*.

---

## What's where

```
amiablealex/
├── app.py                  # the whole app + SITE config (edit this)
├── requirements.txt
├── content/projects/       # ONE markdown file per project  ← add projects here
│   ├── kitsniff.md
│   ├── f1-predictions.md
│   └── sunrise-clock.md
├── templates/              # Jinja templates
│   ├── base.html  index.html  projects.html  project.html
│   ├── about.html  contact.html  404.html  _macros.html
└── static/
    ├── css/style.css       # all styling
    ├── fonts/              # self-hosted Hanken Grotesk + Caveat (woff2)
    ├── favicon.svg
    └── img/
        ├── og-image.png    # link-preview image (replace any time)
        └── projects/       # project cover images go here
```

## First things to edit

Most of the visible text is a placeholder wrapped in `[ square brackets ]`.
Search the project for `[` to find everything that's yours to write.

1. **`app.py` → `SITE`** — your email, GitHub URL, LinkedIn URL, and the
   site description used for link previews.
2. **`templates/index.html`** — the hero intro line.
3. **`templates/about.html`** and **`templates/contact.html`** — your words.
4. The three files in **`content/projects/`** — the project write-ups.

---

## Adding a new project (the only routine task)

1. Create a new file in `content/projects/`, e.g. `vantix.md`.
2. Give it frontmatter and a body. Copy an existing file as a template:

   ```markdown
   ---
   title: Vantix
   category: Web app           # shown as a pill; also a filter on /projects
   accent: blue                # pill colour (see palette below)
   summary: "A short one-liner."
   date: 2025-05               # used for ordering (newest first) — keep it sortable
   featured: true              # true = show on the home page
   cover: vantix.png           # optional; file in static/img/projects/
   links:
     - label: Live
       url: "https://..."
       icon: external-link
     - label: GitHub
       url: "https://github.com/..."
       icon: brand-github
   tech: [Flask, PostgreSQL]   # optional chips
   ---

   ## What it is
   Your write-up in markdown...
   ```

3. (Optional) drop a cover image in `static/img/projects/` and reference it in
   `cover:`. Images in the body work too:
   `![caption](/static/img/projects/photo.jpg)`
4. Save. The new project appears automatically — **no restart needed** in
   dev; on the Pi just `git pull` and `sudo systemctl restart amiablealex`.

**Pill colours (`accent:`):** `teal` (default), `clay`, `olive`, `eucalyptus`,
`blue`, `lavender`, `mauve`, `gray`.
**Link icons (`icon:`):** `external-link`, `brand-github`, `brand-linkedin`,
`printer`, `file-text`, `mail`, `arrow-right`, `arrow-left`.

---

## Run locally (your laptop or the Pi)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
# open http://127.0.0.1:5000
```

---

## Deploy on the Raspberry Pi

Assumes you already run nginx + cloudflared (you do). Adjust the paths,
username, and port to match your setup. The example uses port **8005** and
user **pi** — change if needed.

### 1. Get the code onto the Pi (git)

```bash
cd ~/apps                       # wherever you keep your apps
# either copy the unzipped folder here, or clone your repo:
# git clone git@github.com:your-username/amiablealex.git
cd amiablealex
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Quick check it serves:
```bash
gunicorn app:app --bind 127.0.0.1:8005
# Ctrl-C once you've confirmed it starts
```

### 2. systemd service (keeps Gunicorn running)

Create `/etc/systemd/system/amiablealex.service`:

```ini
[Unit]
Description=amiablealex.com (gunicorn)
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/apps/amiablealex
ExecStart=/home/pi/apps/amiablealex/venv/bin/gunicorn app:app --workers 2 --bind 127.0.0.1:8005
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now amiablealex
sudo systemctl status amiablealex      # should be "active (running)"
```

### 3. nginx (reverse proxy for the domain)

Create `/etc/nginx/sites-available/amiablealex` and symlink it into
`sites-enabled/`:

```nginx
server {
    listen 80;
    server_name amiablealex.com;

    location /static/ {
        alias /home/pi/apps/amiablealex/static/;
        expires 30d;
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/amiablealex /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 4. Cloudflare tunnel

Add a hostname to your existing tunnel config (`~/.cloudflared/config.yml`),
above the catch-all rule:

```yaml
ingress:
  - hostname: amiablealex.com
    service: http://localhost:80
  # ... your other apps ...
  - service: http_status:404
```

Route DNS once, then restart the tunnel:
```bash
cloudflared tunnel route dns <your-tunnel-name> amiablealex.com
sudo systemctl restart cloudflared
```

### Updating after a change
```bash
cd ~/apps/amiablealex
git pull
sudo systemctl restart amiablealex
```

---

## Notes

- **Fonts are bundled** (`static/fonts/`) and served locally — no Google Fonts
  request at runtime.
- **No browser storage / no database** — content lives entirely in the
  markdown files, which is also your backup (it's all in git).
- **Mobile**: the navigation never hides — it wraps below the wordmark on
  narrow screens.
