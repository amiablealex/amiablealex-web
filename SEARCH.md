# Search engines

## What's automatic

`/sitemap.xml` is built on each request from the content folders: every
project, every guide step plus each guide's all-on-one-page view, every
explainer, and the home, projects, explainers, about and contact pages. A new
markdown file is in the sitemap the moment it's live on the site, and a
deleted one drops out. There's no sitemap file to edit.

Each URL's `<lastmod>` is the newest modification time of the files its
content comes from. On the Pi, `git pull` only rewrites files a commit
changed, so that's when the last real edit went live.

`/robots.txt` allows everything and tells crawlers where the sitemap is. Every
page carries a canonical link to its `https://amiablealex.com` address. The
home page has a few lines of `WebSite` structured data so Google can show
"amiablealex" as the site name.

## Adding content

Nothing extra. Google and Bing reread the sitemap on their own schedule and
find new pages from it, typically within days.

For a page you want in Google sooner, paste its full URL into the inspection
bar at the top of Search Console and click **Request indexing**. Optional, and
rationed per day, so keep it for significant new pages.

## One-time setup

### Google Search Console

1. At [search.google.com/search-console](https://search.google.com/search-console),
   add a property, choose **Domain**, and enter `amiablealex.com`.
2. Verify with the TXT record it gives you, added in Cloudflare → DNS (type
   `TXT`, name `@`). Leave the record there permanently; removing it
   unverifies the site.
3. **Sitemaps** → enter `sitemap.xml` → Submit.
4. Inspect the home page URL and run **Test live URL**, which confirms Google
   can reach the site through the Cloudflare tunnel. Then request indexing for
   the home page and the pages that matter most.

### Bing Webmaster Tools

At [bing.com/webmasters](https://www.bing.com/webmasters), sign in and choose
**Import from Google Search Console**. It copies the verified site and the
sitemap across. Bing's index also supplies DuckDuckGo and Yahoo.

## Worth knowing

Guide step URLs follow position, not file name: `/guide/7` is whatever is
seventh. Inserting or removing a step moves every later step to a different
address, so old links and search results land on whatever is now in that slot.
Search engines catch up on their next crawl.
