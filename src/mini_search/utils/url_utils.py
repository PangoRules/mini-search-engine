import re
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse


def normalize_url(url: str, base: str | None = None) -> str:
    if base:
        url = urljoin(base, url)

    if is_valid_url(url) == False:
        raise ValueError("Invalid URL")

    urlParts = urlparse(url)

    scheme = urlParts.scheme.lower()  # normalize scheme
    netloc = re.sub(
        r":\d+", "", urlParts.netloc.lower()
    )  # normalize and remove port from netloc
    path = urlParts.path.lower().strip("/")
    query_pairs = parse_qsl(urlParts.query, keep_blank_values=False)
    query_pairs.sort()
    query = urlencode(query_pairs)

    return urlunparse((scheme, netloc, path, "", query, ""))


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


def main():
    test = normalize_url("https://Example.com:8080/Path?b=2&a=1#section")
    print(test)


if __name__ == "__main__":
    main()
