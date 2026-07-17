<div align="center">

# 💻 Remote Tech Jobs Curator

### Every remote tech role on the internet — automatically tracked, curated & committed daily.

[![GitHub stars](https://img.shields.io/github/stars/aredwan-xyz/remote-jobs-ai-curator?style=social)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aredwan-xyz/remote-jobs-ai-curator?style=social)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/network/members)
[![GitHub last commit](https://img.shields.io/github/last-commit/aredwan-xyz/remote-jobs-ai-curator?style=flat-square&color=green&label=last%20update)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/commits/main)
[![Automated](https://img.shields.io/badge/🤖%20automated-daily%207am%20UTC-blue?style=flat-square)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/actions)
[![Sources](https://img.shields.io/badge/sources-4%20job%20boards-orange?style=flat-square)](#sources)
[![Roles](https://img.shields.io/badge/role%20categories-11-6f7fb0?style=flat-square)](#role-categories)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

### **[🌐 Live Site →](https://aredwan-xyz.github.io/remote-jobs-ai-curator/)**

**[💼 Today's Listings](#latest-listings) · [📚 Full Archive](ARCHIVE.md) · [⭐ Star this repo](https://github.com/aredwan-xyz/remote-jobs-ai-curator)**

</div>

---

## 💡 What is this?

**Remote Tech Jobs Curator** automatically scrapes **4 major remote job boards** every morning, classifies every listing into a **role category by its title**, and commits a clean markdown + JSON snapshot — so you can filter to exactly the kind of role you want.

- ✅ **Zero manual effort** — GitHub Actions does everything
- ✅ **Filterable by role** — Engineering, AI/ML, Data, DevOps/Infra, Frontend, Backend, Full-Stack, Mobile, Security, QA/Testing, Product & Design
- ✅ **Title-only classification** — no false positives from company "about us" boilerplate mentioning AI/tech buzzwords for unrelated roles
- ✅ **Salary info** included where available
- ✅ **Full archive** — track market trends over time
- ✅ **Free forever** — no API keys, no subscriptions
- ✅ **Forkable** — customize for any role category in minutes

---

## 🔴 Latest Listings

<!-- LATEST-START -->
<!-- auto-updated: 2026-07-17 -->
**Latest listings: [Friday, 2026-07-17](jobs/2026-07-17.md)** - 269 remote tech jobs

| Role | Company | Category | Source |
|------|---------|----------|--------|
| [Junior Power BI Analyst](https://remoteOK.com/remote-jobs/remote-junior-power-bi-analyst-statusneo-1134912) | StatusNeo | Data | RemoteOK |
| [Record Your Daily Routine & Get Paid AI Training](https://remoteOK.com/remote-jobs/remote-record-your-daily-routine-amp-get-paid-ai-training-toloka-annotators-1134939) | Toloka Annotators | AI / ML | RemoteOK |
| [Graphic Designer](https://remoteOK.com/remote-jobs/remote-graphic-designer-huzzle-com-1134799) | Huzzle.com | Product & Design | RemoteOK |
| [Software development Frontend Developer](https://remoteOK.com/remote-jobs/remote-software-developmentfrontend-developer-defdone-1134928) | defdone | Frontend | RemoteOK |
| [Senior AI Engineer Architect](https://remoteOK.com/remote-jobs/remote-senior-ai-engineer-architect-lemon-io-1134396) | Lemon.io | AI / ML | RemoteOK |
| [Mid Senior AI Cinematic Video Editor](https://remoteOK.com/remote-jobs/remote-mid-senior-ai-cinematic-video-editor-everai-1134014) | EverAI | AI / ML | RemoteOK |
| [Graphic Designer](https://remoteOK.com/remote-jobs/remote-graphic-designer-swoon-1133676) | Swoon | Product & Design | RemoteOK |
| [Head of Operations Overtime.ai](https://remoteOK.com/remote-jobs/remote-head-of-operations-overtime-ai-acclaim-ai-1131709) | Acclaim AI | AI / ML | RemoteOK |
| [Member of Technical Staff Applied ML RecSys](https://remoteOK.com/remote-jobs/remote-member-of-technical-staff-applied-ml-recsys-liquid-ai-1131627) | Liquid AI | AI / ML | RemoteOK |
| [Business Owners Freelance AI Trainer Project](https://remoteOK.com/remote-jobs/remote-business-owners-freelance-ai-trainer-project-invisible-agency-1131600) | Invisible Agency | AI / ML | RemoteOK |

_🔄 Updated daily · [View all 269 jobs →](jobs/2026-07-17.md)_
<!-- LATEST-END -->

---

## 📡 Sources

| Job Board | Query strategy |
|-----------|-------|
| 🌍 **RemoteOK** | General feed + 11 category tags, classified by title |
| 💼 **Remotive** | 7 categories (software-dev, data, devops, design, product, qa, all-others) |
| 🏠 **WeWorkRemotely** | 8 RSS feeds (programming, data science, design, devops, product, full-stack, backend, frontend) |
| 🤖 **Jobicy** | General feed (200 most recent), classified by title |

Every source is queried broadly, then every listing is independently classified by **its own title** — the source's own tags/categories are never trusted as a filter signal (they're too permissive; see [`fetch_jobs.py`](fetch_jobs.py) for the false-positive cases that drove this).

---

## 🎯 Role Categories

`AI / ML` · `Engineering` · `Frontend` · `Backend` · `Full-Stack` · `Mobile` · `DevOps / Infra` · `Data` · `Security` · `QA / Testing` · `Product & Design`

Browse and filter by any of these live on the **[site](https://aredwan-xyz.github.io/remote-jobs-ai-curator/)**.

---

## ⚙️ How It Works

```
Every day at 7:00 AM UTC
         │
         ▼
  GitHub Actions triggers
         │
         ▼
  fetch_jobs.py runs
         │
         ├── 🌍 scrapes RemoteOK (general + 11 category tags)
         ├── 💼 scrapes Remotive (7 categories)
         ├── 🏠 scrapes WeWorkRemotely (8 RSS feeds)
         ├── 🤖 scrapes Jobicy (general feed)
         ├── 🏷️  classifies every listing by title into a role category
         ├── 🧹 deduplicates all listings
         ├── 📝 writes jobs/YYYY-MM-DD.md
         ├── 🔄 updates README + docs/jobs.json with latest listings
         ├── 📚 updates ARCHIVE.md index
         └── ✅ git commit + push
```

---

## 🍴 Fork & Run Your Own

```bash
# 1. Fork this repo on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/remote-jobs-ai-curator.git

# 3. That's it - GitHub Actions runs automatically every morning!
# Trigger manually: Actions → Daily Remote Tech Jobs → Run workflow
```

> **Customize it:** Edit `ROLE_CATEGORIES` in `fetch_jobs.py` to add, remove, or retune role categories. Add new job boards as `fetch_*()` functions.

---

## 📚 Archive

All past snapshots are indexed in **[ARCHIVE.md](ARCHIVE.md)** and stored in the [`jobs/`](./jobs/) folder. Use the archive to track hiring trends over time.

---

## 🤝 Contributing

Know a job board we're missing? Open a PR!

1. Fork the repo
2. Add a new `fetch_*()` function in `fetch_jobs.py`
3. Add it to `main()`
4. Open a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT © [Abid Redwan](https://aredwan.com) · [CodeBeez](https://codebeez.xyz)

---

<div align="center">

**Looking for your next remote role? ⭐ Star this repo and watch it for daily updates!**

Made with ☕ by **[Abid Redwan](https://aredwan.com)** · A **[CodeBeez](https://codebeez.xyz)** Project

</div>
