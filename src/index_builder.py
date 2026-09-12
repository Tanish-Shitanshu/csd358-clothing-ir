"""
index_builder.py
=================
Builds ONE unified data structure that serves Part A (dictionary +
postings), Part B (term frequencies / document frequencies for VSM),
and Part C (positional index) simultaneously:

    postings[term] = {
        docid: [pos1, pos2, ...],   # sorted list of positions of `term` in docid
        ...
    }
    df[term] = number of distinct documents containing term

Conceptually this matches the assignment's own description of the
positional index:  (term -> df -> [(docID, tf, [p1, p2, ...]), ...])
-- tf is simply len(positions) and df is len(postings[term]), so we
don't store them redundantly.

KEY DESIGN DECISION -- how positions are numbered (stop words vs.
phrase queries):

Lecture 2 makes an explicit point that is directly relevant here:
"you need stop words for phrase queries, e.g. 'King of Denmark'"
-- i.e. if you strip stop words before numbering positions, a phrase
that legitimately contains a stop word can no longer be verified as
truly adjacent, and worse, two content words that were NOT originally
adjacent (but had a stop word removed from between them) could be
miscounted as adjacent.

To avoid this, we number positions over the FULL, UN-FILTERED token
stream (i.e. including stop words), but we simply never create a
postings entry for a stop word (since it's not indexed as a
dictionary term at all, per Part A's stop-word policy). The result:
indexed terms keep their TRUE original position numbers, with gaps
left wherever a stop word (or any other un-indexed token) occurred.
This makes phrase search (Part C) exact with respect to the source
text, not with respect to some filtered version of it.

This is why index_builder is the single place all three parts (A/B/C)
draw from: Part A/B only look at `df` and `len(positions)` and never
look at the position VALUES themselves, so they are completely
unaffected by this choice; Part C uses the position values directly
and benefits from their being faithful to the original text.
"""

from collections import defaultdict

from preprocessing import normalize_and_tokenize, is_stopword, stem
from corpus import Document


class InvertedIndex:
    def __init__(self):
        # term -> {docid -> [positions]}
        self.postings: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
        self.doc_ids: list[str] = []
        self.doc_meta: dict[str, Document] = {}
        self.doc_length: dict[str, float] = {}   # ||d|| under lnc weighting (Part B)
        self.N = 0

    # ------------------------------------------------------------------
    def build(self, documents: list[Document]):
        self.doc_ids = [d.docid for d in documents]
        self.doc_meta = {d.docid: d for d in documents}
        self.N = len(documents)

        for doc in documents:
            raw_tokens = normalize_and_tokenize(doc.text)
            for position, token in enumerate(raw_tokens, start=1):
                if is_stopword(token):
                    continue  # occupies a position slot, but is not indexed
                term = stem(token)
                self.postings[term][doc.docid].append(position)

        self._compute_doc_lengths()

    # ------------------------------------------------------------------
    def _compute_doc_lengths(self):
        """
        Pre-compute ||d|| (L2 norm of the lnc-weighted document vector)
        for every document, using ALL terms present in that document
        -- not just query terms. This is required for correct cosine
        normalization (Lecture 6: "maintain document length information
        for cosine normalization"; the worked example there also sums
        over the *whole* document vector, not just query terms).
        """
        import math
        sumsq: dict[str, float] = defaultdict(float)
        for term, doc_dict in self.postings.items():
            for docid, positions in doc_dict.items():
                tf = len(positions)
                w = 1 + math.log10(tf)  # lnc: log-tf, NO idf on the document side
                sumsq[docid] += w * w
        for docid in self.doc_ids:
            self.doc_length[docid] = math.sqrt(sumsq.get(docid, 0.0))

    # ------------------------------------------------------------------
    def df(self, term: str) -> int:
        return len(self.postings.get(term, {}))

    def tf(self, term: str, docid: str) -> int:
        return len(self.postings.get(term, {}).get(docid, []))

    def positions(self, term: str, docid: str) -> list[int]:
        return self.postings.get(term, {}).get(docid, [])

    def vocabulary(self):
        return sorted(self.postings.keys())


if __name__ == "__main__":
    from corpus import load_corpus
    docs = load_corpus("corpus_100.txt")
    idx = InvertedIndex()
    idx.build(docs)
    print(f"N documents        : {idx.N}")
    print(f"Vocabulary size (M): {len(idx.vocabulary())}")
    print(f"df('cotton')       : {idx.df('cotton')}")
    print(f"df('festiv')       : {idx.df('festiv')}   (stem of 'festive')")
    print(f"postings('cotton') sample:", dict(list(idx.postings['cotton'].items())[:3]))
    print(f"doc_length['D001'] : {idx.doc_length['D001']:.4f}")
