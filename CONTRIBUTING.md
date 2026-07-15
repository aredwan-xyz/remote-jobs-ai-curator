# Contributing to Remote Tech Jobs Curator

Thanks for helping! Here's how to add a new job source, or a new role category.

## Adding a Job Board

1. Fork the repo and clone locally
2. Open `fetch_jobs.py`
3. Add a new function following this pattern:
   ```python
   def fetch_yourboard():
       jobs = []
       try:
           # fetch from API or RSS — prefer the board's broadest/general
           # feed over a pre-filtered one; classify_role() does the filtering
           for item in ...:
               title = "..."
               role = classify_role(title)   # title only — never trust the
               if role:                      # source's own tags/categories
                   jobs.append({
                       "title": title, "company": "...",
                       "location": "...", "link": "...",
                       "salary": "...", "tags": "...",
                       "source": "YourBoard", "role": role,
                   })
       except Exception as e:
           print(f"  ✗ YourBoard: {e}")
       return jobs
   ```
4. Call it in `main()`'s source list and add it to the README sources table
5. Test: `GH_TOKEN=$(gh auth token) python3 fetch_jobs.py`, then spot-check a few
   jobs per role category for false positives before opening a PR
6. Open a pull request

## Adding or Retuning a Role Category

Edit `ROLE_CATEGORIES` in `fetch_jobs.py`. Keep keywords as **specific
multi-word phrases where possible** — bare single words like `"engineer"` or
`"developer"` match far too much (`Janitor Engineer`, `Sales Engineer`,
`Curriculum Developer` are all real job titles that slipped through an
earlier version of this filter). Order matters: categories are checked
top-to-bottom and the first match wins, so put more specific categories
before broader catch-alls.

## Guidelines

- Must be a **remote-first** or **remote-friendly** job board
- Handle errors gracefully - boards go down
- Classify by **title only** — description/tag text is too noisy (company
  "about us" boilerplate mentions AI/tech buzzwords for unrelated roles)
- Deduplicate using `(title, company)` keys
- Keep descriptions short

---

_Made with ☕ by [Abid Redwan](https://aredwan.com) · [CodeBeez](https://codebeez.xyz)_
