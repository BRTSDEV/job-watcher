import requests
from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, OptionList, Static

from scraper import find_jobs
from storage import load_seen, save_seen


class JobWatcherApp(App):
    CSS_PATH = "style.tcss"
    TITLE = "Job Watcher"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="search-bar"):
            yield Input(placeholder="keywords, separated by commas", id="keywords")
            yield Button("Search", id="search-button")
        with Horizontal(id="main"):
            yield OptionList(id="jobs", classes="panel")
            with Vertical(id="right"):
                yield Static("Select a job to see details.", id="details", classes="panel")
                yield Static("Ready.", id="log", classes="panel")
        yield Footer()

    def on_mount(self) -> None:
        self.jobs: list[dict] = []
        self.query_one("#search-bar").border_title = "search"
        self.query_one("#jobs").border_title = "jobs"
        self.query_one("#details").border_title = "details"
        self.query_one("#log").border_title = "log"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        text = self.query_one("#keywords", Input).value
        include = [word.strip() for word in text.split(",") if word.strip()]

        self.query_one("#search-button", Button).disabled = True
        self.query_one("#log", Static).update("Searching...")
        self.run_search(include)

    @work(thread=True)
    def run_search(self, include: list[str]) -> None:
        seen = load_seen()
        try:
            jobs = find_jobs(
                "https://quotes.toscrape.com",
                "a.tag",
                include,
                ["inspirational"],
                seen,
            )
        except requests.RequestException as error:
            self.call_from_thread(self.show_error, type(error).__name__)
            return
        self.call_from_thread(self.show_results, jobs, seen)

    def show_error(self, error_name: str) -> None:
        self.query_one("#log", Static).update(f"Error: could not reach the site ({error_name})")
        self.query_one("#search-button", Button).disabled = False

    def show_results(self, jobs: list[dict], seen: set) -> None:
        self.jobs.extend(jobs)
        job_list = self.query_one("#jobs", OptionList)
        job_list.clear_options()
        job_list.add_options([Text(job["title"]) for job in self.jobs])

        for job in jobs:
            seen.add(job["url"])
        save_seen(seen)

        self.query_one("#log", Static).update(f"Found {len(jobs)} new job(s).")
        self.query_one("#search-button", Button).disabled = False

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        job = self.jobs[event.option_index]
        emails = ", ".join(job["emails"]) or "-"
        phones = ", ".join(job["phones"]) or "-"
        details = (
            f"{job['title']}\n"
            f"{job['url']}\n\n"
            f"email: {emails}\n"
            f"phone: {phones}\n\n"
            f"{job['preview']}"
        )
        self.query_one("#details", Static).update(Text(details))


if __name__ == "__main__":
    JobWatcherApp().run()