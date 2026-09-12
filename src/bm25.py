"""
bm25.py
=======
NOVELTY COMPONENT: Okapi BM25 ranking, implemented as a second scoring
mode alongside the required lnc.ltc VSM, with a direct comparison of
where and why the two rankings disagree.

WHY THIS IS THE CHOSEN NOVELTY (viva talking points):

1. It is a natural "next step" from what was taught, not an unrelated
   bolt-on. Lecture 6 builds tf-idf/VSM specifically to fix two
   problems with raw counts: (a) term frequency shouldn't count
   linearly (-> log dampening, "1 + log10 tf"), and (b) common terms
   shouldn't count as much as rare ones (-> idf). BM25 is the
   textbook's own next step beyond exactly this: it keeps idf, but
   replaces log-dampening with a *saturating* function of tf that has
   an explicit, tunable ceiling (parameter k1), and it explicitly
   corrects for document length using the average document length in
   the collection (parameter b) -- something lnc.ltc does only
   implicitly via cosine normalization.

2. It surfaces a genuine, explainable weakness of lnc.ltc on THIS
   corpus: because every document is close to the same length (the
   corpus is template-generated), cosine length-normalization barely
   matters here -- but term saturation still does, because a handful
   of boilerplate terms (e.g. "festiv", which -- see index_builder.py
   sanity check -- has df = 100, i.e. appears in literally every
   document from the closing "festive styling" sentence) get idf = 0
   under lnc.ltc and are silently dropped from scoring entirely. BM25
   uses the same idf formulation and would ALSO give such a term zero
   weight -- so we explicitly show in the report which OTHER terms
   behave differently under the two models' tf components, rather
   than claiming BM25 "fixes" something it structurally doesn't.

FORMULA
-------
    BM25(q, d) = sum over query terms t of:
        idf_BM25(t) * ( tf(t,d) * (k1 + 1) ) / ( tf(t,d) + k1 * (1 - b + b * |d|/avgdl) )

    idf_BM25(t) = log( (N - df(t) + 0.5) / (df(t) + 0.5) + 1 )

We use the standard "+1"-smoothed idf variant (Robertson-Sparck Jones
with a floor of 0 removed) to guarantee non-negative idf for every
term, since our corpus is small enough that some terms could otherwise
have df close to N.

|d| here is document length measured in TOKENS INDEXED (i.e. count of
non-stop-word tokens actually contributing postings), and avgdl is the
mean of this over all N documents -- both are cheap to precompute
once from the same InvertedIndex used by Part B, so BM25 adds no new
indexing structure, only a new *scoring function* over the existing
index. This mirrors the assignment's own Part B/C relationship (one
index, multiple views).

Standard parameter defaults (Robertson & Sparck Jones): k1 = 1.5, b = 0.75.
"""

import math
from collections import defaultdict

from preprocessing import normalize_and_tokenize, remove_stopwords, stem
from index_builder import InvertedIndex


def _doc_token_counts(index: InvertedIndex) -> dict[str, int]:
    """Number of indexed (non-stop-word) tokens in each document."""
    counts = defaultdict(int)
    for term, doc_dict in index.postings.items():
        for docid, positions in doc_dict.items():
            counts[docid] += len(positions)
    return counts


def bm25_search(index: InvertedIndex, query: str, top_k: int = 10,
                 k1: float = 1.5, b: float = 0.75):
    doc_len = _doc_token_counts(index)
    avgdl = sum(doc_len.values()) / index.N if index.N else 0.0

    tokens = normalize_and_tokenize(query)
    tokens = remove_stopwords(tokens)
    q_terms = sorted({stem(t) for t in tokens})  # BM25 doesn't need query tf weighting

    scores: dict[str, float] = defaultdict(float)
    for term in q_terms:
        df = index.df(term)
        if df == 0:
            continue  # OOV term contributes 0, same graceful handling as VSM
        idf = math.log((index.N - df + 0.5) / (df + 0.5) + 1)
        for docid, positions in index.postings[term].items():
            tf = len(positions)
            dl = doc_len.get(docid, 0)
            denom = tf + k1 * (1 - b + b * (dl / avgdl if avgdl else 0))
            scores[docid] += idf * (tf * (k1 + 1)) / denom if denom else 0.0

    results = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return results[:top_k]


if __name__ == "__main__":
    from corpus import load_corpus
    from vsm import vsm_search

    docs = load_corpus("corpus_100.txt")
    index = InvertedIndex()
    index.build(docs)

    for q in ["cotton shirt", "winter jacket"]:
        print(f"\nQuery: {q!r}")
        v = vsm_search(index, q, top_k=5)
        bm = bm25_search(index, q, top_k=5)
        print("  lnc.ltc VSM :", v)
        print("  BM25        :", bm)
