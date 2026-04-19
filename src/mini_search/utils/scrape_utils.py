from typing import TypedDict
from bs4 import BeautifulSoup
from requests import Response
from mini_search.tokenizer import tokenize
from mini_search.utils.url_utils import normalize_url


class ScrapedPageDto(TypedDict):
    id: int | None
    url: str
    title: list[str] | None
    meta_description: str | None
    headings: dict
    paragraphs: list[list[str]]
    links: list[str]
    images: list[list[str]]
    lists: list[list[str]]
    tables: list[ParsedTables]


class ParsedTables(TypedDict):
    headersTag: list[str]
    tableDatatag: list[str]


def scrape_page(response: Response, url: str) -> ScrapedPageDto:
    soup = BeautifulSoup(response.text, "html.parser")

    # remove noise tags
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    # object to return
    result: ScrapedPageDto = {
        "id": None,
        "url": url,
        "title": tokenize(clean_text(soup.title.get_text())) if soup.title else None,
        "meta_description": None,
        "headings": parse_headers(soup),
        "paragraphs": parse_paragraphs(soup),
        "links": parse_links(soup, url),
        "images": parse_images(soup, url),
        "lists": parse_lists(soup),
        "tables": parse_tables(soup),
    }

    return result


def parse_headers(soup: BeautifulSoup) -> dict:
    headers = {}
    for level in range(1, 7):
        tag_name = f"h{level}"
        headers[tag_name] = [
            tokenize(clean_text(tag.get_text(" ", strip=True)))
            for tag in soup.find_all(tag_name)
            if clean_text(tag.get_text(" ", strip=True))
        ]
    return headers


def parse_paragraphs(soup: BeautifulSoup) -> list[list[str]]:
    return [
        tokenize(clean_text(tag.get_text(" ", strip=True)))
        for tag in soup.find_all("p")
        if clean_text(tag.get_text(" ", strip=True))
    ]


def parse_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    anchors = soup.find_all("a", href=True)

    links = []
    for anchor in anchors:
        try:
            links.append(normalize_url(str(anchor["href"]), base_url))
        except ValueError:
            print(f'unable to add: {anchor["href"]}')
    return links


def parse_images(soup: BeautifulSoup, base_url: str) -> list[list[str]]:
    images = []
    for img in soup.find_all("img"):
        image = {}
        if src := img.get("src"):
            image["url"] = normalize_url(str(src), base_url)
        if altText := img.get("alt"):
            image["altTokens"] = tokenize(clean_text(str(altText)))
        if image:
            images.append(image)
    return images


def parse_lists(soup: BeautifulSoup) -> list[list[str]]:
    listGroups = soup.find_all(["ul", "ol"])
    results = []
    for groupedList in listGroups:
        results.append(
            [
                tokenize(clean_text(item.get_text()))
                for item in groupedList.find_all("li")
            ]
        )
    return results


def parse_tables(soup: BeautifulSoup) -> list[ParsedTables]:
    listTables = soup.find_all("table")
    results = []
    for table in listTables:
        headersTag = [
            tokenize(clean_text(header.get_text())) for header in table.find_all("th")
        ]
        tableDataTab = []
        for tableRow in table.find_all("tr"):
            tempRow = []
            for tableRow in tableRow.find_all("td"):
                tempRow.append(tokenize(clean_text(tableRow.get_text())))
            if tempRow:
                tableDataTab.append(tempRow)

        results.append({"headersTag": headersTag, "tableDataTag": tableDataTab})

    return results


def clean_text(value: str) -> str:
    return " ".join(value.split()).strip()
