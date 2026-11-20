<div align="center">

# 💻 Remote Tech Jobs Curator

### Remote tech listings collected from four job boards, with daily snapshots.

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

- ✅ **Scheduled collection** — GitHub Actions runs the collector; source health still needs monitoring
- ✅ **Filterable by role** — Engineering, AI/ML, Data, DevOps/Infra, Frontend, Backend, Full-Stack, Mobile, Security, QA/Testing, Product & Design
- ✅ **Title-only classification** — no false positives from company "about us" boilerplate mentioning AI/tech buzzwords for unrelated roles
- ✅ **Salary info** included where available
- ✅ **Full archive** — track market trends over time
- ✅ **No API keys required** for the current source adapters
- ✅ **Forkable** — customize for any role category in minutes

---

## 🔴 Latest Listings

<!-- LATEST-START -->
<!-- auto-updated: 2026-11-20 -->
**Latest listings: [Friday, 2026-11-20](jobs/2026-11-20.md)** - 234 remote tech jobs

| Role | Company | Category | Source |
|------|---------|----------|--------|
| [Front-End Engineer, UX/UI](https://remoteOK.com/remote-jobs/remote-front-end-engineer-ux-ui-beyondtrust-1137833) | BeyondTrust | Frontend | RemoteOK |
| [Enterprise Solutions Engineer, East](https://remoteOK.com/remote-jobs/remote-enterprise-solutions-engineer-east-glean-1137826) | Glean | Engineering | RemoteOK |
| [Senior Analytics Engineer](https://remoteOK.com/remote-jobs/remote-senior-analytics-engineer-tebra-1137809) | Tebra | Data | RemoteOK |
| [Software Engineer AI Coding Tasks](https://remoteOK.com/remote-jobs/remote-software-engineer-ai-coding-tasks-askable-1137808) | Askable | AI / ML | RemoteOK |
| [SEO Full Stack Engineer](https://remoteOK.com/remote-jobs/remote-seo-full-stack-engineer-treatwell-1137805) | Treatwell | Full-Stack | RemoteOK |
| [Expert Talent Pool Physical AI](https://remoteOK.com/remote-jobs/remote-expert-talent-pool-physical-ai-clera-1137799) | Clera | AI / ML | RemoteOK |
| [Software Engineer AI Tooling](https://remoteOK.com/remote-jobs/remote-software-engineer-ai-tooling-supabase-1137793) | Supabase | AI / ML | RemoteOK |
| [Data Engineer](https://remoteOK.com/remote-jobs/remote-data-engineer-addepto-1137714) | Addepto | Data | RemoteOK |
| [Senior Software Engineer â Kubernetes Control Plane](https://remoteOK.com/remote-jobs/remote-senior-software-engineer-kubernetes-control-plane-buoyant-1137713) | Buoyant | DevOps / Infra | RemoteOK |
| [Senior Agentic AI Engineer NDA](https://remoteOK.com/remote-jobs/remote-senior-agentic-ai-engineer-nda-gt-1137710) | GT | AI / ML | RemoteOK |

_🔄 Updated daily · [View all 234 jobs →](jobs/2026-11-20.md)_
<!-- LATEST-END -->

---

## 📡 Sources

Coverage is limited to the feeds below. Listings may expire or have geographic restrictions: confirm eligibility and compensation with the employer. Missing location information is labeled unknown, never inferred to mean worldwide. Historical snapshots predate this correction and may contain incorrectly broad location labels.

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
