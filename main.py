# full app
from scraper import find_jobs
from storage import load_seen, save_seen


def main():
    seen = load_seen()
    
    print("links in memory:", len(seen))
    
    jobs = find_jobs(
        "https://quotes.toscrape.com",
        "a.tag",
        ["love", "life", "humor"],
        ["inspirational"],
        seen,
    )
    
    print("new jobs found:", len(jobs))

    for job in jobs:
        print("NEW:", job["title"])
        print("     ", job["url"])
        print("      emails:", job["emails"])
        seen.add(job["url"])

    save_seen(seen)


if __name__ == "__main__":
    main()
