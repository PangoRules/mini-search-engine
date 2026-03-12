import requests
from mini_search.utils.scrape_utils import scrape_page
from mini_search.utils.url_utils import normalize_url
from collections import deque
from requests import RequestException, Response


def crawl(seed_url: str, max_depth: int, max_pages: int) -> None:
    normalizedUrl = normalize_url(seed_url)
    queue = deque([(normalizedUrl, 0)])  # (url, depth)
    visited = set()

    while queue and len(visited) < max_pages:
        url, depth = queue.popleft()
        if url in visited:
            continue
        if depth == max_depth:
            continue

        response = fetch_page(url)
        visited.add(url)
        print(f"[{len(visited)}/{max_pages}] Crawling: {url} (depth {depth})")

        if response is None:
            continue

        scrapedPage = scrape_page(response, url)
        # save_page(scrapedPage)
        for linkFound in scrapedPage["links"]:
            if linkFound not in visited:
                queue.append((linkFound, depth + 1))


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


# def save_page(scraped_page: dict) -> None:
#     print(scraped_page)


def main():
    crawl("https://books.toscrape.com/", 50, 5)


if __name__ == "__main__":
    main()
