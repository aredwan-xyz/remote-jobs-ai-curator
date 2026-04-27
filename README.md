<div align="center">

# 💼 Remote AI Jobs Curator

### Every remote AI job on the internet — automatically tracked, curated & committed daily.

[![GitHub stars](https://img.shields.io/github/stars/aredwan-xyz/remote-jobs-ai-curator?style=social)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/aredwan-xyz/remote-jobs-ai-curator?style=social)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/network/members)
[![GitHub last commit](https://img.shields.io/github/last-commit/aredwan-xyz/remote-jobs-ai-curator?style=flat-square&color=green&label=last%20update)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/commits/main)
[![Automated](https://img.shields.io/badge/🤖%20automated-daily%207am%20UTC-blue?style=flat-square)](https://github.com/aredwan-xyz/remote-jobs-ai-curator/actions)
[![Sources](https://img.shields.io/badge/sources-4%20job%20boards-orange?style=flat-square)](#sources)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

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
<!-- auto-updated: 2026-04-27 -->
**Latest listings: [Monday, 2026-04-27](jobs/2026-04-27.md)** — 142 AI remote jobs

| Role | Company | Source |
|------|---------|--------|
| [HQ AI Enablement Lead](https://remoteOK.com/remote-jobs/remote-hq-ai-enablement-lead-everfield-1131322) | Everfield | RemoteOK |
| [Medical Director for Health Plan](https://remoteOK.com/remote-jobs/remote-medical-director-for-health-plan-evry-health-1131321) | Evry Health | RemoteOK |
| [Implementation Specialist](https://remoteOK.com/remote-jobs/remote-implementation-specialist-submittable-1131318) | Submittable | RemoteOK |
| [Trainer EMEA](https://remoteOK.com/remote-jobs/remote-trainer-emea-360learning-1131306) | 360Learning | RemoteOK |
| [TEST JOB](https://remoteOK.com/remote-jobs/remote-test-job-fleetio-1131302) | Fleetio | RemoteOK |
| [Mid Senior AI Video Artist](https://remoteOK.com/remote-jobs/remote-mid-senior-ai-video-artist-everai-1131288) | EverAI | RemoteOK |
| [Search Engine Evaluation Specialist Freelance AI Traine…](https://remoteOK.com/remote-jobs/remote-search-engine-evaluation-specialist-freelance-ai-trainer-project-invisible-agency-1131259) | Invisible Agency | RemoteOK |
| [Senior Account Manager](https://remoteOK.com/remote-jobs/remote-senior-account-manager-keyloop-1131249) | Keyloop | RemoteOK |
| [Crypto Trader](https://remoteOK.com/remote-jobs/remote-crypto-trader-fox-global-assets-1131243) | Fox GLobal Assets | RemoteOK |
| [Account Executive Collections Credit Card](https://remoteOK.com/remote-jobs/remote-account-executive-collections-credit-card-bhg-financial-1131237) | BHG Financial | RemoteOK |

_🔄 Updated daily · [View all 142 jobs →](jobs/2026-04-27.md)_
<!-- LATEST-END -->

---

## 📡 Sources

| Job Board | Focus |
|-----------|-------|
| 🌍 **RemoteOK** | Top remote tech jobs — AI/ML/Data tags |
| 💼 **Remotive** | Curated remote roles — Software, Data & DevOps |
| 🏠 **WeWorkRemotely** | Hand-picked remote programming & data science jobs |
| 🤖 **AIJobs.net** | Dedicated AI-only job board |

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
         ├── 🤖 scrapes AIJobs.net RSS
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
