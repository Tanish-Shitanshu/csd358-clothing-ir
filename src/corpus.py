"""
corpus.py
=========
Parses corpus_100.txt (100 <DOC>...</DOC> records) into a list of
Document objects.

DESIGN DECISION: which field(s) do we index?
We index only the <TEXT> field. Looking at the corpus, <TEXT> always
begins by restating the <TITLE> verbatim as its first sentence, e.g.:

    <TITLE>Men's Checked Cotton Shirt - Black</TITLE>
    <TEXT>Men's Checked Cotton Shirt - Black. Made from linen blend...

So indexing TITLE separately in addition to TEXT would double-count
every title term and artificially inflate its term frequency. We keep
TITLE and CATEGORY only as *display metadata* for search results (Part
D: "Display docID, product title/category, and cosine score"), not as
part of the scored/indexed content.
"""

import re
from dataclasses import dataclass


@dataclass
class Document:
    docid: str
    category: str
    title: str
    text: str


# Capture groups, in order: (1) docid, (2) category, (3) title, (4) text.
# re.DOTALL lets `.` match newlines so multi-line <TEXT> bodies are captured;
# `.*?` (non-greedy) stops at the first closing tag rather than the last.
_DOC_RE = re.compile(
    r"<DOC>\s*"
    r"<DOCID>(.*?)</DOCID>\s*"
    r"<CATEGORY>(.*?)</CATEGORY>\s*"
    r"<TITLE>(.*?)</TITLE>\s*"
    r"<TEXT>(.*?)</TEXT>\s*"
    r"</DOC>",
    re.DOTALL,
)


def load_corpus(path: str) -> list[Document]:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    docs = []
    for m in _DOC_RE.finditer(raw):
        # finditer walks every <DOC>...</DOC> record in the raw text in order;
        # .strip() trims the leading/trailing whitespace left over from \s*.
        docid, category, title, text = (g.strip() for g in m.groups())
        docs.append(Document(docid=docid, category=category, title=title, text=text))
    return docs


if __name__ == "__main__":
    docs = load_corpus("corpus_100.txt")
    print(f"Parsed {len(docs)} documents.")
    print(docs[0])
    print(docs[-1])
    assert len(docs) == 100, f"expected 100 docs, got {len(docs)}"
    ids = [d.docid for d in docs]
    assert len(set(ids)) == 100, "duplicate docIDs found"
    print("OK: 100 unique documents parsed.")
