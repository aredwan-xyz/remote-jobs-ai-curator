import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import json
import os
import re
import time

SITE_URL = "https://aredwan-xyz.github.io/remote-jobs-ai-curator/"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "ml", "deep learning",
    "llm", "nlp", "natural language", "computer vision", "data science",
    "data scientist", "ml engineer", "ai engineer", "research scientist",
    "prompt engineer", "generative ai", "neural", "pytorch", "tensorflow",
    "openai", "anthropic", "langchain", "rag", "fine-tuning", "mlops",
]

# Role categories, checked in order — first match wins. AI/ML is checked
# first since it's the most specific signal; "Engineering" is a broad
# catch-all checked last so it doesn't swallow more specific roles.
# A title matching none of these is not a tech role and is dropped.
ROLE_CATEGORIES = [
    ("AI / ML", AI_KEYWORDS),
    ("Mobile", [
        "ios", "android", "react native", "flutter", "mobile engineer",
        "mobile developer", "swift developer", "kotlin developer",
    ]),
    ("DevOps / Infra", [
        "devops", "sre", "site reliability", "platform engineer",
        "infrastructure engineer", "cloud engineer", "kubernetes",
        "systems engineer", "release engineer",
    ]),
    ("Security", [
        "security engineer", "infosec", "appsec", "penetration test",
        "security architect", "cybersecurity", "security analyst",
    ]),
    ("QA / Testing", [
        "qa engineer", "test engineer", "sdet", "quality assurance",
        "automation engineer", "qa analyst",
    ]),
    ("Data", [
        "data engineer", "data analyst", "analytics engineer",
        "bi analyst", "business intelligence", "data engineering",
    ]),
    ("Frontend", [
        "frontend", "front-end", "front end", "react developer",
        "vue developer", "angular developer", "ui engineer",
    ]),
    ("Backend", [
        "backend", "back-end", "back end", "api engineer",
        "server engineer", "node.js", "golang developer", "django developer",
        "ruby on rails",
    ]),
    ("Full-Stack", ["full stack", "full-stack", "fullstack"]),
    ("Product & Design", [
        "product manager", "product designer", "ux designer", "ui designer",
        "ux researcher", "product owner", "graphic designer",
    ]),
    # Multi-word phrases only — bare "engineer"/"developer" match plenty of
    # non-tech titles (Janitor Engineer, Sales Engineer, Curriculum
    # Developer), so those single words are deliberately excluded here.
    ("Engineering", [
        "software engineer", "software developer", "web developer",
        "systems programmer", "application developer", "solutions engineer",
    ]),
]


def _build_pattern(keywords):
    return re.compile(
        r"(?<![a-z0-9])(" + "|".join(re.escape(k) for k in keywords) + r")(?![a-z0-9])"
    )


_ROLE_PATTERNS = [(name, _build_pattern(kws)) for name, kws in ROLE_CATEGORIES]


def classify_role(title):
    """Return the best-matching tech role category for a job title, or None
    if it isn't a tech role at all (e.g. Sales, HR, Accounting, Caretaker)."""
    t = (title or "").lower()
    for name, pattern in _ROLE_PATTERNS:
        if pattern.search(t):
            return name
    return None

def clean(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&mdash;|&ndash;|&#8211;|&#8212;|&#8213;", "-", text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"[‒-―]", "-", text)  # figure/en/em/horizontal-bar dashes -> hyphen
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def http_get(url, timeout=12, retries=4, backoff=1.5):
    """Fetch a URL with retries, exponential backoff and manual redirect-following.
    Returns raw bytes; raises the last error if every attempt fails. This is what
    keeps a transient 301/429/5xx (e.g. WeWorkRemotely's flaky redirect) from
    silently dropping a whole source for the day."""
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "application/json, application/rss+xml, application/xml;q=0.9, */*;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            loc = e.headers.get("Location") if e.headers else None
            if e.code in (301, 302, 303, 307, 308):
                if loc:
                    url = urllib.parse.urljoin(url, loc)  # follow redirect, then retry
                # else: bare redirect (anti-bot soft-block) — just retry the same url
            elif e.code not in (408, 425, 429, 500, 502, 503, 504):
                break                                     # non-transient (404 etc.) — stop early
        except Exception as e:
            last = e
        if attempt < retries - 1:
            time.sleep(backoff * (attempt + 1))
    raise last if last else RuntimeError(f"request failed: {url}")

# ── Source 1: RemoteOK ────────────────────────────────────────────────────────
def fetch_remoteok():
    jobs = []
    # The general (no-tag) endpoint gives the broadest recent pool; the
    # tag queries add depth per category. RemoteOK's own tags are NOT
    # trusted as a filter signal (see classify_role) — every job here is
    # re-classified from its title regardless of which query found it.
    endpoints = [None, "ai", "machine-learning", "data-science", "dev",
                 "engineer", "backend", "frontend", "devops", "security",
                 "design", "product"]
    seen = set()
    for tag in endpoints:
        try:
            url = "https://remoteok.com/api" + (f"?tag={tag}" if tag else "")
            data = json.loads(http_get(url))
            for job in data[1:]:  # first item is legal notice
                jid = job.get("id", "")
                if jid in seen:
                    continue
                seen.add(jid)
                title    = clean(job.get("position", ""))
                company  = clean(job.get("company", ""))
                location = clean(job.get("location", "Worldwide"))
                link     = job.get("url", f"https://remoteok.com/l/{jid}")
                salary   = job.get("salary_min") or job.get("salary_max")
                salary_str = f"${salary:,}+" if salary else ""
                tags_str = ", ".join(job.get("tags", [])[:5])
                role = classify_role(title)
                if title and company and role:
                    jobs.append({
                        "title": title, "company": company,
                        "location": location or "Worldwide",
                        "link": link, "salary": salary_str,
                        "tags": tags_str, "source": "RemoteOK", "role": role,
                    })
        except Exception as e:
            print(f"  ✗ RemoteOK ({tag}): {e}")
    return jobs

# ── Source 2: Remotive ────────────────────────────────────────────────────────
def fetch_remotive():
    jobs = []
    categories = ["software-dev", "data", "devops-sysadmin", "design",
                  "product", "qa", "all-others"]
    seen = set()
    for cat in categories:
        try:
            url = f"https://remotive.com/api/remote-jobs?category={cat}&limit=100"
            data = json.loads(http_get(url))
            for job in data.get("jobs", []):
                jid = job.get("id")
                if jid in seen:
                    continue
                seen.add(jid)
                title   = clean(job.get("title", ""))
                company = clean(job.get("company_name", ""))
                link    = job.get("url", "")
                salary  = clean(job.get("salary", ""))
                tags    = ", ".join(job.get("tags", [])[:5])
                role = classify_role(title)
                if role and title and company:
                    jobs.append({
                        "title": title, "company": company,
                        "location": "Worldwide",
                        "link": link, "salary": salary,
                        "tags": tags, "source": "Remotive", "role": role,
                    })
        except Exception as e:
            print(f"  ✗ Remotive ({cat}): {e}")
    return jobs

# ── Source 3: We Work Remotely (RSS) ─────────────────────────────────────────
def fetch_wwr():
    jobs = []
    feeds = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-data-science-jobs.rss",
        "https://weworkremotely.com/categories/remote-design-jobs.rss",
        "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
        "https://weworkremotely.com/categories/remote-product-jobs.rss",
        "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss",
    ]
    for url in feeds:
        try:
            root = ET.fromstring(http_get(url))
            for item in root.findall(".//item"):
                title_raw = clean(item.findtext("title", ""))
                parts     = title_raw.split(":", 1)
                company   = parts[0].strip() if len(parts) > 1 else "Unknown"
                title     = parts[1].strip() if len(parts) > 1 else title_raw
                link      = item.findtext("link", "")
                region    = clean(item.findtext("{https://weworkremotely.com}region", "Worldwide"))
                role = classify_role(title)
                if role:
                    jobs.append({
                        "title": title, "company": company,
                        "location": region or "Worldwide",
                        "link": link, "salary": "",
                        "tags": "", "source": "WeWorkRemotely", "role": role,
                    })
        except Exception as e:
            print(f"  ✗ WeWorkRemotely: {e}")
    return jobs

# ── Source 4: Jobicy ──────────────────────────────────────────────────────────
def fetch_jobicy():
    jobs = []
    try:
        # Already unfiltered by category — one broad pull, classify by title.
        url = "https://jobicy.com/api/v2/remote-jobs?count=200"
        data = json.loads(http_get(url))
        for job in data.get("jobs", []):
            title    = clean(job.get("jobTitle", ""))
            company  = clean(job.get("companyName", ""))
            link     = job.get("url", "")
            geo      = clean(job.get("jobGeo", "Worldwide"))
            smin     = job.get("annualSalaryMin")
            salary   = f"${int(smin):,}+" if smin else ""
            industry = clean(", ".join(job.get("jobIndustry", []) or []))
            role = classify_role(title)
            if role and title and company:
                jobs.append({
                    "title": title, "company": company,
                    "location": geo or "Worldwide",
                    "link": link, "salary": salary,
                    "tags": industry[:30], "source": "Jobicy", "role": role,
                })
    except Exception as e:
        print(f"  ✗ Jobicy: {e}")
    return jobs

# ── Dedup + rank ──────────────────────────────────────────────────────────────
def dedup(jobs):
    seen = set()
    out  = []
    for j in jobs:
        key = (j["title"].lower()[:40], j["company"].lower()[:20])
        if key not in seen:
            seen.add(key)
            out.append(j)
    return out

def load_previous_links():
    """Job links from the last published snapshot, used to flag NEW listings."""
    try:
        with open("docs/jobs.json") as f:
            prev = json.load(f)
        return {j.get("link") for j in prev.get("jobs", []) if j.get("link")}
    except Exception:
        return set()

def write_health_report(raw, sources, total, new_count, today):
    """Print a per-source health summary and (in CI) write it to the job summary."""
    up = [n for n in raw if raw[n]]
    down = [n for n in raw if not raw[n]]
    rows = []
    for name in raw:
        fetched, kept = len(raw[name]), len(sources.get(name, []))
        rows.append(f"| {name} | {'✅' if raw[name] else '⚠️ DOWN'} | {fetched} | {kept} |")
    summary = "\n".join([
        f"## 🤖 Remote AI Jobs — {today}",
        "",
        f"**{total} unique jobs** · **{new_count} new** · **{len(up)}/{len(raw)} sources up**",
        "",
        "| Source | Status | Fetched | After dedup |",
        "|--------|--------|---------|-------------|",
        *rows,
    ])
    gh = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh:
        try:
            with open(gh, "a") as f:
                f.write(summary + "\n")
        except Exception:
            pass
    if down:
        print(f"  ⚠️  SOURCES DOWN: {', '.join(down)}")
    print(f"  ✓ {len(up)}/{len(raw)} sources healthy")

def write_seo(today):
    """robots.txt + sitemap.xml for crawlability (lastmod refreshed daily)."""
    os.makedirs("docs", exist_ok=True)
    with open("docs/robots.txt", "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
    with open("docs/sitemap.xml", "w") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"  <url><loc>{SITE_URL}</loc><lastmod>{today}</lastmod>"
            "<changefreq>daily</changefreq><priority>1.0</priority></url>\n"
            "</urlset>\n"
        )
    print("  ✓ robots.txt + sitemap.xml written")

def update_readme_preview(jobs, today, day):
    if not os.path.exists("README.md"):
        return
    with open("README.md") as f:
        content = f.read()
    lines = [f"<!-- auto-updated: {today} -->"]
    lines.append(f"**Latest listings: [{day}, {today}](jobs/{today}.md)** - {len(jobs)} remote tech jobs")
    lines.append("")
    lines.append("| Role | Company | Category | Source |")
    lines.append("|------|---------|----------|--------|")
    for j in jobs[:10]:
        title   = (j["title"][:55] + "…") if len(j["title"]) > 55 else j["title"]
        company = j["company"][:30]
        lines.append(f"| [{title}]({j['link']}) | {company} | {j['role']} | {j['source']} |")
    lines.append("")
    lines.append(f"_🔄 Updated daily · [View all {len(jobs)} jobs →](jobs/{today}.md)_")

    new_block = "\n".join(lines)
    updated = re.sub(
        r"<!-- LATEST-START -->.*?<!-- LATEST-END -->",
        f"<!-- LATEST-START -->\n{new_block}\n<!-- LATEST-END -->",
        content, flags=re.DOTALL,
    )
    with open("README.md", "w") as f:
        f.write(updated)
    print(f"  ✓ README preview updated")

def write_site_data(jobs, today, day, stamp, sources, new_count):
    """Emit structured data for the GitHub Pages site (docs/jobs.json)."""
    os.makedirs("docs", exist_ok=True)
    roles = {}
    for j in jobs:
        roles.setdefault(j["role"], []).append(j)
    data = {
        "updated": today,
        "updated_human": f"{day}, {today} · {stamp}",
        "total": len(jobs),
        "new_count": new_count,
        "sources": {src: len(s) for src, s in sorted(sources.items(), key=lambda x: -len(x[1]))},
        "roles": {r: len(s) for r, s in sorted(roles.items(), key=lambda x: -len(x[1]))},
        "jobs": jobs,
    }
    with open("docs/jobs.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"  ✓ docs/jobs.json written ({len(jobs)} jobs)")

def build_archive():
    files = sorted([f for f in os.listdir("jobs") if f.endswith(".md")], reverse=True)
    lines = ["# 📚 Archive\n", "| Date | Jobs |", "|------|------|"]
    for fname in files:
        date = fname.replace(".md", "")
        lines.append(f"| {date} | [View listings](jobs/{fname}) |")
    with open("ARCHIVE.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  ✓ ARCHIVE.md updated ({len(files)} snapshots)")

def main():
    now   = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    day   = now.strftime("%A")
    stamp = now.strftime("%H:%M UTC")

    raw = {}
    for name, fn in [("RemoteOK", fetch_remoteok), ("Remotive", fetch_remotive),
                     ("WeWorkRemotely", fetch_wwr), ("Jobicy", fetch_jobicy)]:
        print(f"Fetching: {name}")
        raw[name] = fn()

    jobs = [j for lst in raw.values() for j in lst]
    jobs = dedup(jobs)
    print(f"  ✓ {len(jobs)} unique remote tech jobs found")

    # flag listings not present in the previous snapshot
    prev_links = load_previous_links()
    new_count  = 0
    for j in jobs:
        j["is_new"] = bool(prev_links) and j["link"] not in prev_links
        new_count += j["is_new"]
    print(f"  ✓ {new_count} new since last run")

    # group by source (for the health table) and role (for listings)
    sources = {}
    for j in jobs:
        sources.setdefault(j["source"], []).append(j)
    roles = {}
    for j in jobs:
        roles.setdefault(j["role"], []).append(j)

    lines = []
    lines.append(f"# 💻 Remote Tech Jobs - {day}, {today}")
    lines.append(f"_Curated daily by **[Abid Redwan](https://aredwan.com)** · **[CodeBeez](https://codebeez.xyz)** · {stamp}_")
    lines.append("")
    lines.append(f"> **{len(jobs)} remote tech opportunities** across {len(roles)} role categories, scraped from {len(sources)} sources - updated every morning.")
    if new_count:
        lines.append(">")
        lines.append(f"> 🆕 **{new_count} new** since the last update.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # quick stats
    lines.append("## 📊 Today's Stats")
    lines.append("")
    lines.append("| Role Category | Jobs Found |")
    lines.append("|--------|-----------|")
    for role, rjobs in sorted(roles.items(), key=lambda x: -len(x[1])):
        lines.append(f"| {role} | {len(rjobs)} |")
    lines.append(f"| **Total** | **{len(jobs)}** |")
    lines.append("")

    # listings by role
    lines.append("## 💼 Job Listings")
    lines.append("")
    for role, rjobs in sorted(roles.items(), key=lambda x: -len(x[1])):
        lines.append(f"### {role}")
        lines.append("")
        lines.append("| Role | Company | Location | Salary | Source |")
        lines.append("|------|---------|----------|--------|--------|")
        for j in rjobs:
            title    = (j["title"][:60] + "…") if len(j["title"]) > 60 else j["title"]
            flag     = "🆕 " if j.get("is_new") else ""
            company  = j["company"][:35]
            location = j["location"][:25]
            salary   = j["salary"] or "-"
            lines.append(f"| {flag}[{title}]({j['link']}) | {company} | {location} | {salary} | {j['source']} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🔔 Never Miss a Listing")
    lines.append("")
    lines.append("⭐ **Star this repo** · 👁 **Watch** for daily notifications · 🍴 **Fork** to customize your own tracker")
    lines.append("")
    lines.append("---")
    lines.append(f"_{len(jobs)} jobs · {len(sources)} sources · Next update tomorrow 7:00 AM UTC_")
    lines.append("")
    lines.append("_Made with ☕ by **[Abid Redwan](https://aredwan.com)** · A **[CodeBeez](https://codebeez.xyz)** Project_")

    os.makedirs("jobs", exist_ok=True)
    with open(f"jobs/{today}.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  ✓ Saved to jobs/{today}.md")

    update_readme_preview(jobs, today, day)
    build_archive()
    write_site_data(jobs, today, day, stamp, sources, new_count)
    write_seo(today)
    write_health_report(raw, sources, len(jobs), new_count, today)

if __name__ == "__main__":
    main()
