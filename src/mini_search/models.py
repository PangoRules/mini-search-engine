class Document:
    def __init__(self, path: str, title: str, content: str, id: int | None = None):
        self.id = id
        self.path = path
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.id}, {self.path}, {self.title}, {self.content}"


class ScrapedPage:
    def __init__(
        self,
        url: str,
        title: str,
        meta_description: str | None,
        headings: str,
        paragraphs: str,
        links: str,
        images: str,
        lists: str,
        tables: str,
        id: int | None = None,
    ):
        self.id = id
        self.url = url
        self.title = title
        self.meta_description = meta_description
        self.headings = headings
        self.paragraphs = paragraphs
        self.links = links
        self.images = images
        self.lists = lists
        self.tables = tables

    def __repr__(self):
        return f"{self.id}, {self.url}, {self.title}, {self.meta_description}, {self.headings}, {self.paragraphs}, {self.links}, {self.images}, {self.lists}, {self.tables}"
