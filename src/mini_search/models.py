import json


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
        self.title = json.loads(title) if title else None
        self.meta_description = meta_description
        self.headings = json.loads(headings)
        self.paragraphs = json.loads(paragraphs)
        self.links = json.loads(links)
        self.images = json.loads(images)
        self.lists = json.loads(lists)
        self.tables = json.loads(tables)

    def __repr__(self):
        return f"{self.id}, {self.url}, {self.title}, {self.meta_description}, {self.headings}, {self.paragraphs}, {self.links}, {self.images}, {self.lists}, {self.tables}"
