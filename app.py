"""
app.py
======
Part D: application interface.
  - Free-text search mode -> VSM (lnc.ltc), with an optional BM25
    comparison column (novelty).
  - Phrase / proximity search mode -> positional index, showing the
    actual matching term positions as evidence that the positional
    index is being used (explicit assignment requirement).

Run with:  streamlit run app.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import streamlit as st
from corpus import load_corpus
from index_builder import InvertedIndex
from vsm import vsm_search
from bm25 import bm25_search
from positional_search import phrase_search, proximity_search

ROOT = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource  # build the index once per server process, not once per widget interaction/rerun
def get_index():
    docs = load_corpus(os.path.join(ROOT, "corpus_100.txt"))
    index = InvertedIndex()
    index.build(docs)
    return index


st.set_page_config(page_title="Clothing Search Engine — CSD358 A1", layout="wide")
index = get_index()

st.title("👕 Clothing Ranked Retrieval Engine")
st.caption(
    f"CSD358 Assignment 1 — Information Retrieval | "
    f"N = {index.N} documents, vocabulary M = {len(index.vocabulary())} terms"
)

mode = st.radio(
    "Search mode",
    ["Free-text search (VSM · lnc.ltc)", "Phrase / Proximity search (positional index)"],
    horizontal=True,
)

st.divider()

# =========================================================================
# MODE 1: Free-text VSM search
# Triggered whenever the radio button selects the "Free-text" option; runs
# lnc.ltc VSM search (and optionally BM25, for the novelty comparison
# column) on every rerun triggered by a text/checkbox change.
# =========================================================================
if mode.startswith("Free-text"):
    st.subheader("Free-text ranked retrieval — lnc.ltc Vector Space Model")
    show_bm25 = st.checkbox(
        "Also show BM25 ranking (novelty comparison)", value=True
    )
    query = st.text_input("Enter a free-text query", value="cotton shirt")

    if query.strip():
        results = vsm_search(index, query, top_k=10)
        bm25_results = dict(bm25_search(index, query, top_k=10)) if show_bm25 else {}

        if not results:
            st.warning(
                "No matching documents. Every query term is either a stop "
                "word or does not occur anywhere in the corpus "
                "(out-of-vocabulary)."
            )
        else:
            st.write(f"**Top {len(results)} result(s)** for: `{query}`")
            rows = []
            for rank, (docid, score) in enumerate(results, start=1):
                meta = index.doc_meta[docid]
                row = {
                    "Rank": rank,
                    "docID": docid,
                    "Category": meta.category,
                    "Title": meta.title,
                    "Cosine score (lnc.ltc)": round(score, 4),
                }
                if show_bm25:
                    row["BM25 score"] = round(bm25_results.get(docid, 0.0), 4)
                rows.append(row)
            # renders once results is non-empty; one row per ranked (docid, score) pair
            st.dataframe(rows, use_container_width=True, hide_index=True)

            with st.expander("Show query preprocessing detail"):
                from vsm import _query_term_frequencies
                st.write("Query term frequencies after stop-word removal + stemming:")
                st.json(_query_term_frequencies(query))

# =========================================================================
# MODE 2: Phrase / Proximity search
# Triggered when the radio button selects the positional-index option;
# the nested sub_mode radio then picks exact-phrase vs. WITHIN/k proximity,
# both querying the positional index directly instead of VSM/BM25.
# =========================================================================
else:
    st.subheader("Positional index search")
    sub_mode = st.radio("Type", ["Exact phrase", "Ordered proximity (WITHIN/k)"], horizontal=True)

    if sub_mode == "Exact phrase":
        phrase = st.text_input("Enter an exact phrase (2+ words)", value="cotton shirt")
        if phrase.strip():
            try:
                matches = phrase_search(index, phrase)
            except ValueError as e:
                st.error(str(e))
                matches = None

            if matches is not None:
                if not matches:
                    st.warning("No document contains this exact phrase.")
                else:
                    st.write(f"**{len(matches)} document(s)** contain the exact phrase `\"{phrase}\"`:")
                    rows = []
                    for docid, starts in matches.items():
                        meta = index.doc_meta[docid]
                        rows.append({
                            "docID": docid,
                            "Category": meta.category,
                            "Title": meta.title,
                            "Matching start position(s)": str(starts),
                        })
                    # renders one row per document that contains the exact phrase
                    st.dataframe(rows, use_container_width=True, hide_index=True)
                    st.info(
                        "**Evidence of positional matching:** the 'Matching start "
                        "position(s)' column above is the token position at which "
                        "the phrase begins in each document — this is only "
                        "possible because we look up the *actual positions* of "
                        "each word from the positional index, not just whether "
                        "both words appear anywhere in the document."
                    )

    else:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            term1 = st.text_input("Term 1 (occurs first)", value="cotton")
        with col2:
            k = st.number_input("k (max gap)", min_value=1, max_value=50, value=3)
        with col3:
            term2 = st.text_input("Term 2 (occurs within k positions after term 1)", value="shirt")

        if term1.strip() and term2.strip():
            matches = proximity_search(index, term1, term2, int(k))
            st.write(f"`{term1} WITHIN/{int(k)} {term2}` (ordered: {term1} must appear before {term2})")
            if not matches:
                st.warning("No document satisfies this proximity constraint.")
            else:
                st.write(f"**{len(matches)} document(s)** match:")
                rows = []
                for docid, pairs in matches.items():
                    meta = index.doc_meta[docid]
                    rows.append({
                        "docID": docid,
                        "Category": meta.category,
                        "Title": meta.title,
                        "Matching (pos1, pos2) pairs": str(pairs),
                    })
                # renders one row per document satisfying the WITHIN/k proximity constraint
                st.dataframe(rows, use_container_width=True, hide_index=True)
                st.info(
                    "**Evidence of positional matching:** each (pos1, pos2) pair "
                    "shows the exact token positions of the two terms in that "
                    "document, confirming pos2 - pos1 <= k and pos1 < pos2."
                )

st.divider()
with st.expander("ℹ️ About this system / design notes"):
    st.markdown("""
    - **Preprocessing:** lowercase → strip possessive 's → regex tokenize
      → stop-word removal (145-word curated list) → Porter stemming.
    - **Indexing:** a single unified positional inverted index backs
      Part A (dictionary/postings), Part B (VSM), and Part C
      (phrase/proximity) — see `src/index_builder.py`.
    - **VSM weighting:** lnc.ltc (SMART notation) — document: log-tf,
      no idf, cosine-normalized; query: log-tf, idf, cosine-normalized.
    - **Novelty:** BM25 (Okapi, k1=1.5, b=0.75) implemented as an
      alternative scoring mode over the same index, for direct
      comparison against lnc.ltc.
    - Full design rationale and stop-word policy justification are in
      `README.md`.
    """)
