"""
positional_search.py
=====================
Part C: exact phrase search and ordered proximity search, both built
directly on InvertedIndex's positional postings (see index_builder.py
for why position numbers are computed over the full, un-filtered
token stream).

PHRASE SEARCH
-------------
Generalized to any phrase length >= 2 (the assignment's examples are
all 2-word phrases, but the algorithm is not hard-coded to 2 terms).
Standard "positional intersect" (Lecture 2, "to be or not to be"
example): a document matches iff there exists a starting position p
such that term[0] occurs at p, term[1] occurs at p+1, term[2] at p+2,
etc. We return the matching starting positions as evidence.

Note on stop words inside phrases: because stop words are not indexed
at all (Part A policy), a phrase containing one (e.g. "king of
denmark") cannot be looked up term-for-term. All of this assignment's
required/suggested phrase queries are two content words with no stop
word between them in the source text, so this limitation does not
affect our required test queries -- but it is a known, documented
trade-off (see README) directly following from Lecture 2's remark
that "you need stop words for phrase queries".

PROXIMITY SEARCH
-----------------
"ordered proximity search in which two query terms must occur within
k token positions" (assignment spec). We define this precisely (this
exact definition should be quoted in viva if asked):

    term1 WITHIN/k term2  matches document d  iff
    there exist positions p1 (of term1 in d) and p2 (of term2 in d)
    such that p1 < p2  and  (p2 - p1) <= k.

  - "ordered" -> term1's occurrence must come strictly before term2's.
  - distance is measured in the TRUE token stream (stop words count
    towards the gap), matching Lecture 2's own worked example:
    "Employment agencies that place healthcare workers" is a hit for
    employment /4 place (gap = 3, counting stop words "agencies that"),
    while "...that have learned to adapt now place..." is not (gap =
    8), which only works if position numbers are not stop-word-filtered.
  - k=1 is equivalent to an exact 2-word phrase search.
"""

from preprocessing import normalize_and_tokenize, stem, is_stopword
from index_builder import InvertedIndex


def _prep_phrase_terms(phrase: str) -> list[str]:
    """Tokenize + stem a phrase WITHOUT stop-word removal (a phrase's
    words are positional by definition; if one happens to be a stop
    word, we flag it explicitly to the caller rather than silently
    dropping it and changing the query's meaning)."""
    tokens = normalize_and_tokenize(phrase)
    for t in tokens:
        if is_stopword(t):
            raise ValueError(
                f"'{t}' is a stop word and is not indexed, so it cannot "
                f"be looked up positionally. This phrase cannot be "
                f"searched exactly (see README: stop words vs. phrase queries)."
            )
    return [stem(t) for t in tokens]


def phrase_search(index: InvertedIndex, phrase: str):
    """
    Returns dict: {docid: [start_position, ...]} for every document
    that contains the phrase as an exact, contiguous sequence.
    """
    terms = _prep_phrase_terms(phrase)
    if len(terms) < 2:
        raise ValueError("Phrase search needs at least two words.")

    # Candidate docs: intersection of docs containing every term.
    doc_sets = [set(index.postings.get(t, {}).keys()) for t in terms]
    candidate_docs = set.intersection(*doc_sets) if doc_sets else set()

    matches = {}
    for docid in sorted(candidate_docs):
        # Candidate phrase-start positions = positions of term[0].
        starts = set(index.positions(terms[0], docid))
        for i in range(1, len(terms)):
            next_positions = set(index.positions(terms[i], docid))
            # keep starts p such that p+i is a position of terms[i]
            starts = {p for p in starts if (p + i) in next_positions}
            if not starts:
                break
        if starts:
            matches[docid] = sorted(starts)
    return matches


def proximity_search(index: InvertedIndex, term1: str, term2: str, k: int):
    """
    Ordered proximity search: term1 ... term2, with 1 <= (pos2-pos1) <= k.
    Returns dict: {docid: [(p1, p2), ...]} of all matching position pairs
    (evidence for Part D's "show matching positions" requirement).
    """
    t1 = stem(normalize_and_tokenize(term1)[0])
    t2 = stem(normalize_and_tokenize(term2)[0])

    docs1 = index.postings.get(t1, {})
    docs2 = index.postings.get(t2, {})
    common_docs = set(docs1.keys()) & set(docs2.keys())

    matches = {}
    for docid in sorted(common_docs):
        pos1 = docs1[docid]
        pos2 = docs2[docid]
        pairs = []
        for p1 in pos1:
            for p2 in pos2:
                if 0 < (p2 - p1) <= k:
                    pairs.append((p1, p2))
        if pairs:
            matches[docid] = sorted(pairs)
    return matches


if __name__ == "__main__":
    from corpus import load_corpus
    docs = load_corpus("corpus_100.txt")
    index = InvertedIndex()
    index.build(docs)

    print("Phrase 'cotton shirt':", phrase_search(index, "cotton shirt"))
    print("Phrase 'high waist':  ", phrase_search(index, "high waist"))
    print("Proximity cotton WITHIN/3 shirt:",
          proximity_search(index, "cotton", "shirt", 3))
