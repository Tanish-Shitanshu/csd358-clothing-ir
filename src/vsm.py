"""
vsm.py
======
Part B: Vector Space Model ranked retrieval using lnc.ltc weighting
(SMART notation), exactly as specified in the assignment and covered
in Lecture 6 ("Weighting may differ in queries vs documents" / the
worked lnc.ltc car-insurance example).

  Document weight (lnc):  w_d,t = 1 + log10(tf_d,t)     for tf_d,t > 0
                                   0                      otherwise
                           -> Logarithmic tf, No idf, Cosine-normalized.

  Query weight (ltc):     w_q,t = (1 + log10(tf_q,t)) * log10(N / df_t)
                           -> Logarithmic tf, idf, Cosine-normalized.

Because BOTH vectors are cosine-normalized before the dot product,
cosine similarity reduces to a plain dot product over normalized
weights (Lecture 6: "For length-normalized vectors, cosine similarity
is simply the dot product"). We exploit this with the standard
accumulator algorithm from Lecture 7 ("Computing cosine scores"):
walk the postings of the query terms only, and accumulate a running
score per candidate document -- we never touch documents that share
no term with the query, and we never need to materialize the full
|V|-dimensional vectors.
"""

import math
from collections import defaultdict

from preprocessing import normalize_and_tokenize, remove_stopwords, stem
from index_builder import InvertedIndex


def _query_term_frequencies(query: str) -> dict[str, int]:
    tokens = normalize_and_tokenize(query)
    tokens = remove_stopwords(tokens)
    tf = defaultdict(int)
    for t in tokens:
        tf[stem(t)] += 1
    return dict(tf)


def vsm_search(index: InvertedIndex, query: str, top_k: int = 10):
    """
    Returns a list of (docid, score) sorted by decreasing score, then
    by increasing docid for ties, truncated to top_k. Documents that
    share no (in-vocabulary) term with the query are simply absent
    (score 0), matching the assignment's "up to 10" wording -- if
    fewer than top_k documents match, fewer are returned.
    """
    q_tf = _query_term_frequencies(query)

    # Build the query's ltc weight for each query term.
    # A term with df == 0 (out-of-vocabulary term) gets weight 0 and is
    # simply skipped -- it contributes nothing, but the rest of the
    # query still scores normally. This is how the OOV test case in
    # Part E is meant to be handled: gracefully, not as an error.
    q_weights = {}
    for term, tf in q_tf.items():
        df = index.df(term)
        if df == 0:
            continue  # OOV term: idf undefined / infinite in theory, weight 0 in practice
        idf = math.log10(index.N / df)
        q_weights[term] = (1 + math.log10(tf)) * idf

    if not q_weights:
        return []  # every query term was OOV or stripped as a stop word

    q_norm = math.sqrt(sum(w * w for w in q_weights.values()))

    # Accumulator: for each query term, walk its postings and add its
    # contribution to every document that contains it.
    scores: dict[str, float] = defaultdict(float)
    for term, qw in q_weights.items():
        doc_dict = index.postings.get(term, {})
        for docid, positions in doc_dict.items():
            tf_d = len(positions)
            dw = 1 + math.log10(tf_d)               # lnc, un-normalized
            scores[docid] += dw * qw

    # Apply cosine normalization: divide by (||d|| * ||q||).
    results = []
    for docid, raw_score in scores.items():
        d_norm = index.doc_length[docid]
        if d_norm == 0 or q_norm == 0:
            cos = 0.0
        else:
            cos = raw_score / (d_norm * q_norm)
        results.append((docid, cos))

    results.sort(key=lambda x: (-x[1], x[0]))  # score desc, docid asc on ties
    return results[:top_k]


if __name__ == "__main__":
    from corpus import load_corpus
    docs = load_corpus("corpus_100.txt")
    index = InvertedIndex()
    index.build(docs)

    for q in ["cotton shirt", "winter jacket", "waterproof rain coat"]:
        print(f"\nQuery: {q!r}")
        for docid, score in vsm_search(index, q, top_k=5):
            meta = index.doc_meta[docid]
            print(f"  {docid}  {score:.4f}  {meta.category:12s} {meta.title}")
