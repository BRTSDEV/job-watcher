# Job Watcher

A terminal app that searches websites for job listings, filters them by my keywords and shows the details. It only shows jobs I haven't seen yet.

I built it to learn how web scraping, project structure and terminal UIs work.

## What it does

- Downloads a page and finds all the job links on it
- Keeps only the jobs that match my keywords (and drops words like "senior")
- Opens each job page and pulls out the email addresses and phone numbers
- Remembers what it already showed me, so I only see new jobs
- Shows everything in a terminal app (Textual) with a job list and a details panel

The demo searches `quotes.toscrape.com`, a practice site made for scraping. The idea is to point it at real company career pages later.

## How to run it

```
git clone https://github.com/BRTSDEV/job-watcher.git
cd job-watcher
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python tui.py
```

Type keywords separated by commas (for example `love, life, humor`) and click Search. Use Tab and the arrow keys to move around. Quit with Ctrl + Q.

There is also a plain version without the interface: `python main.py`.

## Project structure

| File | What it does |
|---|---|
| `scraper.py` | Downloads pages, finds links, filters by keyword, extracts details |
| `storage.py` | Saves the links I have already seen in `seen_jobs.json` |
| `tui.py` | The Textual app |
| `style.tcss` | The styling of the app (a CSS-like file) |
| `main.py` | A simple command line version |

The scraper does not know the interface exists. Both `main.py` and `tui.py` use the same `find_jobs()` function.

## Problems I ran into

- **The window froze while searching.** Downloading ran on the same thread that draws the screen. I moved it to a background worker.
- **A crash when `seen_jobs.json` was empty.** Reading it raised a JSON error. Now it catches the error and starts with a fresh memory.
- **Links like `/tag/love/` could not be opened.** They were relative links. I used `urljoin` to turn them into full addresses.
- **My email pattern also grabbed a full stop at the end of a sentence.** I changed the regular expression so it can't end on a dot.
- **No internet crashed the app.** I added a timeout, `raise_for_status()` and a `try/except` that shows an error message instead.
- **A job search returned nothing because `return` was indented one level too far.** It ended the function after the first link.

## What I want to add

- A settings file with several company sites
- Real career pages, and maybe the VDAB API
- Keyboard shortcuts
- Tests for the keyword filter and the details parser

## Tech

Python, requests, BeautifulSoup, Textual