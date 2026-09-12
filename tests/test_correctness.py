"""
test_correctness.py
====================
Internal correctness invariants — NOT part of the mandatory Part E
query suite (see run_tests.py for that), but a separate sanity-check
layer that demonstrates the index and scoring functions behave
correctly, independent of any particular query's "interesting-ness".

Run with:  python tests/test_correctness.py
Exits non-zero (and prints which assertion failed) if any check fails.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from corpus import load_corpus
from index_builder import InvertedIndex
from vsm import vsm_search
from positional_search import phrase_search, proximity_search


def build():
    docs = load_corpus(os.path.join(ROOT, "corpus_100.txt"))
    index = InvertedIndex()
    index.build(docs)
    return index


def test_corpus_size(index):
    assert index.N == 100, f"expected 100 docs, got {index.N}"


def test_tf_matches_position_count(index):
    """tf(t,d) must always equal len(positions(t,d)) -- they are the
    same underlying data, tf is never stored redundantly."""
    for term, doc_dict in index.postings.items():
        for docid, positions in doc_dict.items():
            assert index.tf(term, docid) == len(positions)
            assert positions == sorted(positions), "positions must be sorted"


def test_df_matches_number_of_docs_with_term(index):
    for term in index.vocabulary():
        assert index.df(term) == len(index.postings[term])


def test_cosine_scores_bounded(index):
    """Cosine similarity of two unit vectors must lie in [-1, 1]
    (in practice [0, 1] since all weights here are non-negative)."""
    for q in ["cotton shirt", "winter jacket", "denim", "xyz123nonexistent"]:
        for docid, score in vsm_search(index, q, top_k=100):
            assert -1e-9 <= score <= 1 + 1e-9, f"score out of range: {q} {docid} {score}"


def test_phrase_is_subset_of_vsm_matches(index):
    """Any document containing an exact phrase 'A B' necessarily
    contains both A and B, so it must also appear among VSM's matches
    for the free-text query 'A B' (VSM matches ANY doc sharing >=1
    term). This is a structural sanity check on the two search paths
    being consistent with each other."""
    phrase_matches = phrase_search(index, "cotton shirt")
    vsm_matches = {d for d, _ in vsm_search(index, "cotton shirt", top_k=1000)}
    assert set(phrase_matches.keys()).issubset(vsm_matches)


def test_proximity_k1_equals_exact_phrase():
    """WITHIN/1 proximity (ordered, gap <= 1) must match exactly the
    same document set as an exact 2-word phrase search -- both encode
    'term1 immediately followed by term2'. This is a strong internal
    consistency check between the two Part-C search functions."""
    index = build()
    prox = proximity_search(index, "cotton", "shirt", 1)
    phrase = phrase_search(index, "cotton shirt")
    assert set(prox.keys()) == set(phrase.keys()), (
        f"mismatch: proximity={set(prox.keys())} phrase={set(phrase.keys())}"
    )


def test_ordering_is_enforced(index):
    """'kurta' always precedes 'festive' in this corpus (see
    test_report.md Case 2), so festive-WITHIN/k-kurta must NEVER
    match, for any k, while kurta-WITHIN/k-festive SHOULD match for
    large enough k. This checks that 'ordered' is actually enforced,
    not just distance."""
    assert proximity_search(index, "festive", "kurta", 50) == {}
    assert proximity_search(index, "kurta", "festive", 50) != {}


def main():
    index = build()
    tests = [
        test_corpus_size,
        test_tf_matches_position_count,
        test_df_matches_number_of_docs_with_term,
        test_cosine_scores_bounded,
        test_phrase_is_subset_of_vsm_matches,
        test_ordering_is_enforced,
    ]
    for t in tests:
        t(index)
        print(f"PASS: {t.__name__}")

    test_proximity_k1_equals_exact_phrase()
    print("PASS: test_proximity_k1_equals_exact_phrase")

    print("\nALL CORRECTNESS TESTS PASSED")


if __name__ == "__main__":
    main()
