# dwnld the page // finds jobs titles in the html // filter by keywords (senior / junior)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE_RE = re.compile(r"(?:\+32|0032|0)\s?\d(?:[\s./-]?\d){7,9}")

def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.text

def get_links(html, selector, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.select(selector):
        full_url = urljoin(base_url, a.get("href"))
        links.append((a.text.strip(), full_url))
    return links

def matches(title , include, exclude):
    title = title.lower()
    if any(word.lower() in title for word in exclude):
        return False
    return any(word.lower() in title for word in include)

def get_details(html, url,):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    return {
        "title": soup.title.text.strip(),
        "url": url,
        "preview": text[:200],
        "emails": find_emails(text),
        "phones": find_phones(text),
    }

def find_emails(text):
    return sorted(set(EMAIL_RE.findall(text)))

def find_phones(text):
    return sorted(set(match.strip() for match in PHONE_RE.findall(text)))

def find_jobs(url, selector, include, exclude, seen):
    html = fetch_page(url)
    jobs = []
    done = set(seen)
    for text, link in get_links(html, selector, url):
        if link in done:
            continue
        if matches(text, include, exclude):
            details = get_details(fetch_page(link), link)
            details["title"] = text
            jobs.append(details)
            done.add(link)
    return jobs