import re
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


def tokenize(text: str) -> list[str]:
    normText = text.lower()
    normText = re.sub(r"[^\w\s]", "", normText)

    tokens = normText.split()

    stop_words = set(stopwords.words("english"))
    tokens = [w for w in tokens if w not in stop_words]

    print(tokens)
    return tokens


if __name__ == "__main__":
    tokenize("Python. is GREAT for building tools!!")
