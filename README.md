<div align="center">

# 💼 Remote AI Jobs Curator

### Every remote AI job on the internet — automatically tracked, curated & committed daily.

[![GitHub stars](https://img.shields.io/github/stars/aredwan-xyz/remote-jobs-ai-curator?style=social)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aredwan-xyz/remote-jobs-ai-curator?style=social)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/network/members)
[![GitHub last commit](https://img.shields.io/github/last-commit/aredwan-xyz/remote-jobs-ai-curator?style=flat-square&color=green&label=last%20update)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/commits/main)
[![Automated](https://img.shields.io/badge/🤖%20automated-daily%207am%20UTC-blue?style=flat-square)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/actions)
[![Sources](https://img.shields.io/badge/sources-4%20job%20boards-orange?style=flat-square)](#sources)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

### **[🌐 Live Site →](https://aredwan-xyz.github.io/remote-jobs-ai-curator/)**

**[💼 Today's Listings](#latest-listings) · [📚 Full Archive](ARCHIVE.md) · [⭐ Star this repo](https://github.com/aredwan-xyz/remote-jobs-ai-curator)**

</div>

---

## 💡 What is this?

**Remote AI Jobs Curator** automatically scrapes **4 major remote job boards** every morning, filters for AI/ML roles, and commits a clean markdown snapshot — so you never miss an opportunity.

- ✅ **Zero manual effort** — GitHub Actions does everything
- ✅ **AI-filtered** — only ML, Data Science, LLM, NLP, Computer Vision & AI Engineering roles
- ✅ **Salary info** included where available
- ✅ **Full archive** — track market trends over time
- ✅ **Free forever** — no API keys, no subscriptions
- ✅ **Forkable** — customize for any job category in minutes

---

## 🔴 Latest Listings

<!-- LATEST-START -->
<!-- auto-updated: 2026-06-26 -->
**Latest listings: [Friday, 2026-06-26](jobs/2026-06-26.md)** — 209 AI remote jobs

| Role | Company | Source |
|------|---------|--------|
| [Mid Senior AI Cinematic Video Editor](https://remoteOK.com/remote-jobs/remote-mid-senior-ai-cinematic-video-editor-everai-1134014) | EverAI | RemoteOK |
| [Head of Public Understanding](https://remoteOK.com/remote-jobs/remote-head-of-public-understanding-nope-1133914) | NOPE | RemoteOK |
| [Senior Backend Engineer](https://remoteOK.com/remote-jobs/remote-senior-backend-engineer-gameplay-galaxy-1132512) | Gameplay Galaxy | RemoteOK |
| [Client Delivery Manager](https://remoteOK.com/remote-jobs/remote-client-delivery-manager-storyteller-1132435) | Storyteller | RemoteOK |
| [Data Annotator](https://remoteOK.com/remote-jobs/remote-data-annotator-curasenseai-1132152) | CuraSenseAI | RemoteOK |
| [2D Artist](https://remoteOK.com/remote-jobs/remote-2d-artist-rubyplay-1131918) | RubyPlay | RemoteOK |
| [Head of Operations Overtime.ai](https://remoteOK.com/remote-jobs/remote-head-of-operations-overtime-ai-acclaim-ai-1131709) | Acclaim AI | RemoteOK |
| [Janitor Engineer](https://remoteOK.com/remote-jobs/remote-janitor-engineer-neutrality-1131716) | Neutrality | RemoteOK |
| [Chief Technology Officer](https://remoteOK.com/remote-jobs/remote-chief-technology-officer-access-softek-1131633) | Access Softek | RemoteOK |
| [adm Permanent Fulltime MEX](https://remoteOK.com/remote-jobs/remote-adm-permanent-fulltime-mex-adm-indicia-1131776) | adm Indicia | RemoteOK |

_🔄 Updated daily · [View all 209 jobs →](jobs/2026-06-26.md)_
<!-- LATEST-END -->

---

## 📡 Sources

| Job Board | Focus |
|-----------|-------|
| 🌍 **RemoteOK** | Top remote tech jobs — AI/ML/Data tags |
| 💼 **Remotive** | Curated remote roles — Software, Data & DevOps |
| 🏠 **WeWorkRemotely** | Hand-picked remote programming & data science jobs |
| 🤖 **Jobicy** | Remote AI, ML & Data Science roles |

---

## 🎯 Job Categories Tracked

`AI Engineer` · `ML Engineer` · `Data Scientist` · `Research Scientist` · `NLP Engineer` · `Computer Vision` · `LLM Engineer` · `Prompt Engineer` · `MLOps` · `AI Product Manager` · `Deep Learning` · `Generative AI`

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
         ├── 🌍 scrapes RemoteOK (AI/ML/Data tags)
         ├── 💼 scrapes Remotive (filters by AI keywords)
         ├── 🏠 scrapes WeWorkRemotely RSS
         ├── 🤖 scrapes Jobicy API
         ├── 🧹 deduplicates all listings
         ├── 📝 writes jobs/YYYY-MM-DD.md
         ├── 🔄 updates README with latest listings
         ├── 📚 updates ARCHIVE.md index
         └── ✅ git commit + push
```

---

## 🍴 Fork & Run Your Own

```bash
# 1. Fork this repo on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/remote-jobs-ai-curator.git

# 3. That's it — GitHub Actions runs automatically every morning!
# Trigger manually: Actions → Daily Remote AI Jobs → Run workflow
```

> **Customize it:** Edit `AI_KEYWORDS` in `fetch_jobs.py` to track different roles. Add new job boards to the fetch functions.

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

**Looking for your next AI role? ⭐ Star this repo and watch it for daily updates!**

Made with ☕ by **[Abid Redwan](https://aredwan.com)** · A **[CodeBeez](https://codebeez.xyz)** Project

</div>
