import requests
from mini_search.storage.connection import get_connection
from mini_search.storage.scraped_pages import insert_scraped_page
from mini_search.utils.scrape_utils import ScrapedPageDto, scrape_page
from mini_search.utils.url_utils import normalize_url
from collections import deque
from requests import RequestException, Response
from urllib import robotparser, parse


def crawl(max_depth: int, max_pages: int, domains: list[str]) -> None:
    domains = [normalize_url(domain) for domain in domains]
    queue = deque([(domain, 0) for domain in domains])  # (url, depth)
    # urls crawled
    visited = set()
    # urls added to the queue but not yet crawled
    queued = set(domains)
    robotPhoneBook: dict[str, robotparser.RobotFileParser] = {}

    while queue and len(visited) < max_pages:
        url, depth = queue.popleft()
        if url in visited:
            continue
        if depth == max_depth:
            continue

        # robot.txt awareness
        urlParts = parse.urlsplit(url)
        domainUrl = f"{urlParts.scheme}://{urlParts.netloc}"
        if domainUrl not in domains:
            continue

        if domainUrl not in robotPhoneBook:
            parser = robotparser.RobotFileParser(f"{domainUrl}/robots.txt")
            robotPhoneBook[domainUrl] = parser
            parser.read()
        if robotPhoneBook[domainUrl].can_fetch("MyCrawler/1.0", url) is False:
            continue

        response = fetch_page(url)
        visited.add(url)
        print(f"[{len(visited)}/{max_pages}] Crawling: {url} (depth {depth})")

        if response is None:
            continue

        scrapedPage = scrape_page(response, url)
        save_page(scrapedPage)
        for linkFound in scrapedPage["links"]:
            if linkFound not in visited and linkFound not in queued:
                queue.append((linkFound, depth + 1))
                queued.add(linkFound)


def fetch_page(url: str) -> Response | None:
    try:
        response = requests.get(url, headers={"User-Agent": "MyCrawler/1.0"})
        if response.status_code != 200:
            return None
        if "text/html" not in response.headers.get("Content-Type", ""):
            return None
        return response
    except RequestException:
        print("An error has happened.")


def save_page(scraped_page: ScrapedPageDto) -> None:
    with get_connection() as conn:
        insert_scraped_page(conn, scraped_page)


def main():
    crawl(3, 50, ["https://books.toscrape.com", "https://quotes.toscrape.com"])


if __name__ == "__main__":
    main()
