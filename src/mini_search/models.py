class Document:
    def __init__(self, path: str, title: str, content: str, id: int | None = None):
        self.id = id
        self.path = path
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.id}, {self.path}, {self.title}, {self.content}"
