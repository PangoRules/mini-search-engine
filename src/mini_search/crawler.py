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

    print(f"Starting crawl with max depth {max_depth}, max pages {max_pages}")
    
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
    
    print(f"Crawl completed. Visited {len(visited)} pages.")


def fetch_page(url: str) -> Response | None:
    try:
        print(f"Fetching page: {url}")
        response = requests.get(url, headers={"User-Agent": "MyCrawler/1.0"})
        if response.status_code != 200:
            print(f"Page fetch failed: {url} (status: {response.status_code})")
            return None
        if "text/html" not in response.headers.get("Content-Type", ""):
            print(f"Page content type not HTML: {url}")
            return None
        print(f"Page fetched successfully: {url}")
        return response
    except RequestException as e:
        print(f"Error fetching page: {url} - {e}")
        return None


def save_page(scraped_page: ScrapedPageDto) -> None:
    print(f"Saving page: {scraped_page['url']}")
    with get_connection() as conn:
        insert_scraped_page(conn, scraped_page)
    print(f"Page saved successfully: {scraped_page['url']}")


def main():
    crawl(3, 50, ["https://books.toscrape.com", "https://quotes.toscrape.com"])


if __name__ == "__main__":
    main()
