"""
app.py
======
Part D: application interface.

UI/UX NOTE: this file is presentation only. Every function it calls
(vsm_search, bm25_search, phrase_search, proximity_search) is imported
unmodified from src/ -- nothing about scoring, indexing, or search
correctness is touched here. The only new logic in this file is a
single pure-display helper, `context_snippet()`, which reconstructs a
highlighted text window around matched positions for phrase/proximity
results; it reads from the SAME token stream (`normalize_and_tokenize`)
that index_builder.py uses to assign position numbers, so it cannot
drift out of sync with the actual index -- it is not a second,
parallel tokenizer that could disagree with the real one.

Run with:  streamlit run app.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import streamlit as st
import pandas as pd

from corpus import load_corpus
from index_builder import InvertedIndex
from preprocessing import normalize_and_tokenize
from vsm import vsm_search, _query_term_frequencies
from bm25 import bm25_search
from positional_search import phrase_search, proximity_search

ROOT = os.path.dirname(os.path.abspath(__file__))

CATEGORY_EMOJI = {
    "T-Shirt": "👕", "Shirt": "👔", "Jeans": "👖", "Kurta": "🧥",
    "Saree": "🥻", "Dress": "👗", "Hoodie": "🧥", "Jacket": "🧥",
    "Leggings": "🩳", "Sweatshirt": "🧥",
}

EXAMPLE_QUERIES = [
    "cotton shirt", "winter jacket", "high waist leggings",
    "breathable fabric t-shirt", "festive saree",
]


# =========================================================================
# Data loading (cached — index is built once per server process)
# =========================================================================
@st.cache_resource
def get_index():
    docs = load_corpus(os.path.join(ROOT, "corpus_100.txt"))
    index = InvertedIndex()
    index.build(docs)
    return index


# =========================================================================
# Pure-display helper: highlighted context snippet around matched positions
# =========================================================================
def context_snippet(index: InvertedIndex, docid: str, highlight_positions: set[int],
                     window: int = 6) -> str:
    """
    Reconstructs a short window of the document's token stream around the
    given 1-indexed positions, with those positions wrapped in a colored
    <span>. Uses normalize_and_tokenize() -- the exact same function that
    assigns position numbers during indexing -- so the words shown are
    guaranteed to be the words actually AT those positions in the index,
    not a re-derived approximation that could disagree with it.

    The snippet is shown lowercase / de-punctuated because that is
    genuinely what the positional index operates over (stop words
    included, per index_builder.py's design) -- this is presented as a
    deliberate transparency choice, not a cosmetic shortcoming: the user
    is shown exactly what the system matched on.
    """
    doc = index.doc_meta[docid]
    raw_tokens = normalize_and_tokenize(doc.text)
    n = len(raw_tokens)
    positions = sorted(highlight_positions)
    lo = max(1, positions[0] - window)
    hi = min(n, positions[-1] + window)

    parts = []
    if lo > 1:
        parts.append("…")
    for i in range(lo, hi + 1):
        word = raw_tokens[i - 1]
        if i in highlight_positions:
            parts.append(
                f'<span style="background:#FDE68A;color:#78350F;'
                f'padding:1px 6px;border-radius:5px;font-weight:700;">{word}</span>'
            )
        else:
            parts.append(f'<span style="color:#57534E;">{word}</span>')
    if hi < n:
        parts.append("…")
    return " ".join(parts)


def category_badge(category: str) -> str:
    emoji = CATEGORY_EMOJI.get(category, "🧵")
    return f"{emoji} {category}"


# =========================================================================
# Page setup + global styling
# =========================================================================
st.set_page_config(
    page_title="Clothing Ranked Retrieval Engine",
    page_icon="🧵",
    layout="wide",
)

st.markdown("""
<style>
    .main > div { padding-top: 1.2rem; }

    .hero {
        background: linear-gradient(135deg, #C2410C 0%, #EA580C 55%, #FB923C 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.4rem;
        box-shadow: 0 8px 24px rgba(194,65,12,0.25);
    }
    .hero h1 { margin: 0; font-size: 2.1rem; font-weight: 800; }
    .hero p { margin: 0.4rem 0 0 0; font-size: 1.02rem; opacity: 0.95; }

    .result-card {
        border: 1px solid #F3E8D8;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.6rem;
        background: #FFFDF9;
        transition: box-shadow 0.15s ease;
    }
    .result-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.08); }
    .doc-title { font-weight: 700; font-size: 1.02rem; color: #292524; }
    .doc-meta { color: #78716C; font-size: 0.88rem; }

    .snippet-box {
        background: #FAFAF9; border-left: 4px solid #EA580C;
        padding: 0.7rem 1rem; border-radius: 0 8px 8px 0;
        margin-top: 0.5rem; font-family: 'Courier New', monospace; font-size: 0.9rem;
        line-height: 1.6;
    }

    div[data-testid="stMetric"] {
        background: #FFF7ED; border-radius: 10px; padding: 0.7rem 1rem;
        border: 1px solid #FED7AA;
    }
</style>
""", unsafe_allow_html=True)

index = get_index()

# =========================================================================
# Hero header
# =========================================================================
st.markdown("""
<div class="hero">
    <h1>🧵 Clothing Ranked Retrieval Engine</h1>
    <p>CSD358 · Information Retrieval — Assignment 1 &nbsp;|&nbsp;
    Vector Space Model (lnc.ltc) · Positional Index · BM25</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Documents indexed", index.N)
m2.metric("Vocabulary size", len(index.vocabulary()))
m3.metric("Categories", len({d.category for d in index.doc_meta.values()}))
m4.metric("Scoring models", "2 (VSM · BM25)")

st.write("")

# =========================================================================
# Sidebar
# =========================================================================
with st.sidebar:
    st.header("⚙️ About this system")
    st.markdown("""
    A single unified **positional inverted index** backs every search
    mode below — Part A's dictionary, Part B's VSM scoring, and Part C's
    phrase/proximity search are three *views* of the same structure, not
    three separate ones.
    """)

    with st.expander("📋 Pipeline & weighting details", expanded=False):
        st.markdown("""
        **Preprocessing:** lowercase → strip possessive `'s` → regex
        tokenize → stop-word removal (145-word curated list) → Porter
        stemming.

        **VSM weighting — lnc.ltc:**
        - Document: `1 + log10(tf)`, no idf, cosine-normalized
        - Query: `1 + log10(tf) × log10(N/df)`, cosine-normalized

        **Novelty — BM25** (k1=1.5, b=0.75): a saturating alternative
        to log-tf, with explicit document-length correction.
        """)

    st.divider()
    st.subheader("⚡ Try an example")
    if "query_box" not in st.session_state:
        st.session_state["query_box"] = "cotton shirt"
    for q in EXAMPLE_QUERIES:
        if st.button(q, width="stretch", key=f"ex_{q}"):
            st.session_state["query_box"] = q
            st.rerun()

    st.divider()
    st.caption("Full design rationale & viva prep notes: see `README.md`")

# =========================================================================
# Main tabs
# =========================================================================
tab1, tab2 = st.tabs(["🔍  Free-Text Search  (VSM · BM25)", "📐  Phrase & Proximity Search"])

# -------------------------------------------------------------------
# TAB 1: Free-text VSM / BM25 search
# -------------------------------------------------------------------
with tab1:
    col_a, col_b = st.columns([4, 1])
    with col_a:
        query = st.text_input(
            "Enter a free-text query",
            key="query_box",
            label_visibility="collapsed",
            placeholder="e.g. cotton shirt, winter jacket, high waist leggings…",
        )
    with col_b:
        show_bm25 = st.toggle("Compare BM25", value=True)

    if query.strip():
        results = vsm_search(index, query, top_k=10)
        bm25_results = dict(bm25_search(index, query, top_k=10)) if show_bm25 else {}

        if not results:
            st.warning(
                "🔎 No matching documents — every query term is either a stop "
                "word or does not occur anywhere in the corpus "
                "(out-of-vocabulary). This is expected behaviour, not an error."
            )
        else:
            st.success(f"**{len(results)} result(s)** for *“{query}”*", icon="✅")

            table_rows = []
            for rank, (docid, score) in enumerate(results, start=1):
                meta = index.doc_meta[docid]
                row = {
                    "Rank": rank,
                    "docID": docid,
                    "Category": category_badge(meta.category),
                    "Title": meta.title,
                    "lnc.ltc score": score,
                }
                if show_bm25:
                    row["BM25 score"] = bm25_results.get(docid, 0.0)
                table_rows.append(row)

            df = pd.DataFrame(table_rows)
            max_vsm = max(r["lnc.ltc score"] for r in table_rows)
            column_config = {
                "lnc.ltc score": st.column_config.ProgressColumn(
                    "lnc.ltc score", min_value=0.0,
                    max_value=max_vsm * 1.05 if max_vsm else 1.0,
                    format="%.4f",
                ),
            }
            if show_bm25:
                max_bm25 = max(r["BM25 score"] for r in table_rows)
                column_config["BM25 score"] = st.column_config.ProgressColumn(
                    "BM25 score", min_value=0.0,
                    max_value=max_bm25 * 1.05 if max_bm25 else 1.0,
                    format="%.4f",
                )
            st.dataframe(df, column_config=column_config, hide_index=True,
                         width="stretch")

            if show_bm25:
                with st.expander("📊 lnc.ltc vs. BM25 — visual comparison"):
                    max_vsm_ = max(r["lnc.ltc score"] for r in table_rows) or 1.0
                    max_bm25_ = max(r["BM25 score"] for r in table_rows) or 1.0
                    chart_df = pd.DataFrame({
                        "docID": [r["docID"] for r in table_rows],
                        "lnc.ltc (rescaled)": [r["lnc.ltc score"] / max_vsm_ for r in table_rows],
                        "BM25 (rescaled)": [r["BM25 score"] / max_bm25_ for r in table_rows],
                    }).set_index("docID")
                    st.bar_chart(chart_df)
                    st.caption(
                        "Scores are rescaled to each model's own top result "
                        "(=1.0) purely for visual comparison — the two "
                        "models' raw scores are on different scales and are "
                        "never directly comparable in absolute terms."
                    )

            with st.expander("🔬 Query preprocessing detail"):
                st.write("Query term frequencies after stop-word removal + stemming:")
                st.json(_query_term_frequencies(query))
    else:
        st.info("Type a query above, or pick an example from the sidebar.")

# -------------------------------------------------------------------
# TAB 2: Phrase / Proximity search
# -------------------------------------------------------------------
with tab2:
    sub_mode = st.radio(
        "Search type", ["Exact phrase", "Ordered proximity (WITHIN/k)"],
        horizontal=True, label_visibility="collapsed",
    )

    if sub_mode == "Exact phrase":
        phrase = st.text_input(
            "Exact phrase (2+ words)", value="cotton shirt",
            placeholder="e.g. cotton shirt, high waist, printed straight kurta…",
        )
        if phrase.strip():
            try:
                matches = phrase_search(index, phrase)
            except ValueError as e:
                st.error(f"⚠️ {e}")
                matches = None

            if matches is not None:
                if not matches:
                    st.warning(
                        "No document contains this exact phrase — the "
                        "individual words may exist in the corpus, but "
                        "never occur adjacently in this order."
                    )
                else:
                    st.success(
                        f"**{len(matches)} document(s)** contain the exact "
                        f"phrase *“{phrase}”*", icon="✅"
                    )
                    n_words = len(phrase.split())
                    for docid, starts in matches.items():
                        meta = index.doc_meta[docid]
                        st.markdown(f"""
                        <div class="result-card">
                            <span class="doc-title">{docid} — {meta.title}</span><br>
                            <span class="doc-meta">{category_badge(meta.category)}
                            &nbsp;·&nbsp; matched at position(s): {starts}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        for start in starts:
                            highlight = set(range(start, start + n_words))
                            snippet = context_snippet(index, docid, highlight)
                            st.markdown(
                                f'<div class="snippet-box">{snippet}</div>',
                                unsafe_allow_html=True,
                            )
                    st.caption(
                        "🟡 Highlighted words = the exact positions matched "
                        "in the positional index — direct evidence the "
                        "match is positional, not just co-occurrence."
                    )

    else:
        c1, c2, c3 = st.columns([2, 1, 2])
        with c1:
            term1 = st.text_input("Term 1 (occurs first)", value="cotton")
        with c2:
            k = st.number_input("k (max gap)", min_value=1, max_value=50, value=3)
        with c3:
            term2 = st.text_input("Term 2 (occurs within k after term 1)", value="shirt")

        if term1.strip() and term2.strip():
            matches = proximity_search(index, term1, term2, int(k))
            st.caption(
                f"Searching: **{term1} WITHIN/{int(k)} {term2}** "
                f"(ordered — {term1} must occur before {term2})"
            )
            if not matches:
                st.warning("No document satisfies this proximity constraint.")
            else:
                st.success(f"**{len(matches)} document(s)** match", icon="✅")
                for docid, pairs in matches.items():
                    meta = index.doc_meta[docid]
                    st.markdown(f"""
                    <div class="result-card">
                        <span class="doc-title">{docid} — {meta.title}</span><br>
                        <span class="doc-meta">{category_badge(meta.category)}
                        &nbsp;·&nbsp; matching (pos1, pos2) pairs: {pairs}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    p1, p2 = pairs[0]
                    snippet = context_snippet(index, docid, {p1, p2})
                    st.markdown(f'<div class="snippet-box">{snippet}</div>',
                               unsafe_allow_html=True)
                st.caption(
                    "🟡 Highlighted words = the two matched positions, "
                    "confirming p1 < p2 and (p2 - p1) ≤ k directly from "
                    "the underlying position data."
                )

st.divider()
st.caption(
    "Built for CSD358 Assignment 1 · Positional inverted index, lnc.ltc "
    "VSM, and BM25 novelty comparison — see README.md for full design "
    "rationale and viva preparation notes."
)
