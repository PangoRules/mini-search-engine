from collections import defaultdict
from mini_search.models import Document
from mini_search.storage.connection import get_connection
from mini_search.storage.documents import fetch_all_documents
from mini_search.tokenizer import tokenize


def build_inverted_index(documents: list[Document]):
    invertedIndex: dict[str, set[int]] = defaultdict(set)

    for document in documents:
        if document.id is None:
            continue
        tokens = tokenize(document.content)
        for token in tokens:
            invertedIndex[token].add(document.id)

    print(invertedIndex)
    return invertedIndex


if __name__ == "__main__":
    test = fetch_all_documents(get_connection())
    build_inverted_index(test)
