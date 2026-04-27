import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os
import re

AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "ml", "deep learning",
    "llm", "nlp", "natural language", "computer vision", "data science",
    "data scientist", "ml engineer", "ai engineer", "research scientist",
    "prompt engineer", "generative ai", "neural", "pytorch", "tensorflow",
    "openai", "anthropic", "langchain", "rag", "fine-tuning", "mlops",
]

def is_ai_job(title, desc=""):
    text = (title + " " + desc).lower()
    return any(k in text for k in AI_KEYWORDS)

def clean(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ── Source 1: RemoteOK ────────────────────────────────────────────────────────
def fetch_remoteok():
    jobs = []
    tags = ["ai", "machine-learning", "nlp", "deep-learning", "data-science"]
    seen = set()
    for tag in tags:
        try:
            url = f"https://remoteok.com/api?tag={tag}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.load(r)
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
                if title and company:
                    jobs.append({
                        "title": title, "company": company,
                        "location": location or "Worldwide",
                        "link": link, "salary": salary_str,
                        "tags": tags_str, "source": "RemoteOK",
                    })
        except Exception as e:
            print(f"  ✗ RemoteOK ({tag}): {e}")
    return jobs

# ── Source 2: Remotive ────────────────────────────────────────────────────────
def fetch_remotive():
    jobs = []
    categories = ["software-dev", "data", "devops-sysadmin"]
    seen = set()
    for cat in categories:
        try:
            url = f"https://remotive.com/api/remote-jobs?category={cat}&limit=50"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as r:
                data = json.load(r)
            for job in data.get("jobs", []):
                jid = job.get("id")
                if jid in seen:
                    continue
                seen.add(jid)
                title   = clean(job.get("title", ""))
                company = clean(job.get("company_name", ""))
                desc    = clean(job.get("description", ""))
                link    = job.get("url", "")
                salary  = clean(job.get("salary", ""))
                tags    = ", ".join(job.get("tags", [])[:5])
                if is_ai_job(title, desc) and title and company:
                    jobs.append({
                        "title": title, "company": company,
                        "location": "Worldwide",
                        "link": link, "salary": salary,
                        "tags": tags, "source": "Remotive",
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
    ]
    for url in feeds:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as r:
                root = ET.fromstring(r.read())
            for item in root.findall(".//item"):
                title_raw = clean(item.findtext("title", ""))
                parts     = title_raw.split(":", 1)
                company   = parts[0].strip() if len(parts) > 1 else "Unknown"
                title     = parts[1].strip() if len(parts) > 1 else title_raw
                link      = item.findtext("link", "")
                desc      = clean(item.findtext("description", ""))
                region    = clean(item.findtext("{https://weworkremotely.com}region", "Worldwide"))
                if is_ai_job(title, desc):
                    jobs.append({
                        "title": title, "company": company,
                        "location": region or "Worldwide",
                        "link": link, "salary": "",
                        "tags": "", "source": "WeWorkRemotely",
                    })
        except Exception as e:
            print(f"  ✗ WeWorkRemotely: {e}")
    return jobs

# ── Source 4: AI Jobs (RSS) ───────────────────────────────────────────────────
def fetch_aijobs():
    jobs = []
    try:
        url = "https://aijobs.net/feed/"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            root = ET.fromstring(r.read())
        for item in root.findall(".//item")[:20]:
            title   = clean(item.findtext("title", ""))
            link    = item.findtext("link", "")
            desc    = clean(item.findtext("description", ""))
            company = ""
            # try to extract company from description
            m = re.search(r"at\s+([A-Z][^\n.]{2,40})", desc)
            if m:
                company = m.group(1).strip()
            if title:
                jobs.append({
                    "title": title, "company": company or "See listing",
                    "location": "Worldwide",
                    "link": link, "salary": "",
                    "tags": "", "source": "AIJobs.net",
                })
    except Exception as e:
        print(f"  ✗ AIJobs.net: {e}")
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

def update_readme_preview(jobs, today, day):
    if not os.path.exists("README.md"):
        return
    with open("README.md") as f:
        content = f.read()
    lines = [f"<!-- auto-updated: {today} -->"]
    lines.append(f"**Latest listings: [{day}, {today}](jobs/{today}.md)** — {len(jobs)} AI remote jobs")
    lines.append("")
    lines.append("| Role | Company | Source |")
    lines.append("|------|---------|--------|")
    for j in jobs[:10]:
        title   = (j["title"][:55] + "…") if len(j["title"]) > 55 else j["title"]
        company = j["company"][:30]
        lines.append(f"| [{title}]({j['link']}) | {company} | {j['source']} |")
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
    now   = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")
    day   = now.strftime("%A")
    time  = now.strftime("%H:%M UTC")

    print("Fetching: RemoteOK")
    jobs = fetch_remoteok()
    print("Fetching: Remotive")
    jobs += fetch_remotive()
    print("Fetching: WeWorkRemotely")
    jobs += fetch_wwr()
    print("Fetching: AIJobs.net")
    jobs += fetch_aijobs()

    jobs = dedup(jobs)
    print(f"  ✓ {len(jobs)} unique AI remote jobs found")

    # group by source
    sources = {}
    for j in jobs:
        sources.setdefault(j["source"], []).append(j)

    lines = []
    lines.append(f"# 🤖 Remote AI Jobs — {day}, {today}")
    lines.append(f"_Curated daily by **[Abid Redwan](https://aredwan.com)** · **[CodeBeez](https://codebeez.xyz)** · {time}_")
    lines.append("")
    lines.append(f"> **{len(jobs)} remote AI opportunities** scraped from {len(sources)} sources — updated every morning.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # quick stats
    lines.append("## 📊 Today's Stats")
    lines.append("")
    lines.append("| Source | Jobs Found |")
    lines.append("|--------|-----------|")
    for src, sjobs in sorted(sources.items(), key=lambda x: -len(x[1])):
        lines.append(f"| {src} | {len(sjobs)} |")
    lines.append(f"| **Total** | **{len(jobs)}** |")
    lines.append("")

    # listings by source
    lines.append("## 💼 Job Listings")
    lines.append("")
    for src, sjobs in sorted(sources.items(), key=lambda x: -len(x[1])):
        lines.append(f"### {src}")
        lines.append("")
        lines.append("| Role | Company | Location | Salary | Tags |")
        lines.append("|------|---------|----------|--------|------|")
        for j in sjobs:
            title    = (j["title"][:60] + "…") if len(j["title"]) > 60 else j["title"]
            company  = j["company"][:35]
            location = j["location"][:25]
            salary   = j["salary"] or "—"
            tags     = j["tags"][:30] if j["tags"] else "—"
            lines.append(f"| [{title}]({j['link']}) | {company} | {location} | {salary} | {tags} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 🔔 Never Miss a Listing")
    lines.append("")
    lines.append("⭐ **Star this repo** · 👁 **Watch** for daily notifications · 🍴 **Fork** to customize your own tracker")
    lines.append("")
    lines.append("---")
    lines.append(f"_{len(jobs)} jobs · {len(sources)} sources · Next update tomorrow 8:00 AM UTC_")
    lines.append("")
    lines.append("_Made with ☕ by **[Abid Redwan](https://aredwan.com)** · A **[CodeBeez](https://codebeez.xyz)** Project_")

    os.makedirs("jobs", exist_ok=True)
    with open(f"jobs/{today}.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  ✓ Saved to jobs/{today}.md")

    update_readme_preview(jobs, today, day)
    build_archive()

if __name__ == "__main__":
    main()
