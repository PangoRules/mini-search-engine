class Document:
    def __init__(self, path: str, title: str, content: str):
        self.path = path
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.path}, {self.title}, {self.content}"
