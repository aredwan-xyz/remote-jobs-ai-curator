# Contributing to Remote AI Jobs Curator

Thanks for helping! Here's how to add a new job source.

## Adding a Job Board

1. Fork the repo and clone locally
2. Open `fetch_jobs.py`
3. Add a new function following this pattern:
   ```python
   def fetch_yourboard():
       jobs = []
       try:
           # fetch from API or RSS
           # filter with is_ai_job(title, desc)
           jobs.append({
               "title": "...", "company": "...",
               "location": "...", "link": "...",
               "salary": "...", "tags": "...",
               "source": "YourBoard",
           })
       except Exception as e:
           print(f"  ✗ YourBoard: {e}")
       return jobs
   ```
4. Call it in `main()` and add it to the README sources table
5. Test: `python3 fetch_jobs.py`
6. Open a pull request

## Guidelines

- Must be a **remote-first** or **remote-friendly** job board
- Handle errors gracefully - boards go down
- Deduplicate using `(title, company)` keys
- Keep descriptions short

---

_Made with ☕ by [Abid Redwan](https://aredwan.com) · [CodeBeez](https://codebeez.xyz)_
