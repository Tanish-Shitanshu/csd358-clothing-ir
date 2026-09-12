# Clothing Ranked Retrieval Engine — CSD358 Assignment 1

**Team:**
- Tanish Shitanshu (2510110008)
- Ruchir Sharma (2310110728)

A ranked-retrieval search engine over a 100-document clothing product
corpus, built to the Assignment 1 spec (Boolean/VSM inverted index +
positional index + phrase/proximity search).

## 1. How to run

```bash
pip install -r requirements.txt

# Part A/C deliverables: dictionary, postings, positional-index dumps
python src/dump_outputs.py          # -> outputs/dictionary_output.txt
                                     #    outputs/postings_output.txt
                                     #    outputs/positional_index_output.txt

# Part E: mandatory test suite + written analysis
python tests/run_tests.py           # -> outputs/test_report.md

# Internal correctness/invariant checks (not a Part E deliverable --
# demonstrates the two search paths are mutually consistent)
python tests/test_correctness.py

# Part D: interactive application
streamlit run app.py                # opens in browser, take screenshots here
```

## 2. Project structure

```
├── corpus_100.txt              # supplied corpus (100 <DOC> records)
├── requirements.txt
├── app.py                      # Part D — Streamlit UI (2 search modes)
├── src/
│   ├── preprocessing.py        # Part A — tokenize, stop words, stemming
│   ├── corpus.py                # corpus parser
│   ├── index_builder.py        # unified positional inverted index (A+B+C)
│   ├── vsm.py                   # Part B — lnc.ltc VSM ranked retrieval
│   ├── positional_search.py    # Part C — exact phrase + proximity search
│   ├── bm25.py                  # Novelty — BM25 scoring, compared to VSM
│   └── dump_outputs.py          # writes dictionary/postings/positional dumps
├── tests/
│   ├── run_tests.py              # Part E — mandatory test suite + analysis
│   └── test_correctness.py      # internal invariants (e.g. WITHIN/1 ≡ phrase)
├── analysis/
│   └── stem_vs_lemma.py          # supplementary: stemming vs lemmatization comparison
└── outputs/                     # generated: all deliverable files land here
```

**Design principle used throughout:** there is exactly ONE index data
structure (`InvertedIndex` in `index_builder.py`). Part A's dictionary/
postings, Part B's tf/df statistics, and Part C's positions are three
different *views* over the same underlying structure — nothing is
duplicated or rebuilt. This is deliberate and is a talking point in
itself: it mirrors the assignment's own description of the positional
index, `(term → df → [(docID, tf, [positions...]), ...])`, which
already generalizes the non-positional postings `(term → df →
[(docID, tf), ...])` used in Part A/B (`tf = len(positions)`).

---

## 3. Part A — Preprocessing & dictionary (`src/preprocessing.py`)

**Pipeline:** lowercase → strip possessive `'s` → regex-tokenize
(`[a-z0-9]+`) → remove stop words → Porter-stem.

**Tokenization decisions:**
- Numbers are kept as tokens (e.g. `100` from `100%`) — Lecture 1
  notes indexing numbers is "generally a useful feature."
- Hyphens act as separators, not compounders: in this corpus a hyphen
  only ever appears as a dash before a colour name ("- Black"), never
  inside a genuine compound word, so splitting on it is safe.
- Possessive `'s` is stripped (`Men's` → `men`) rather than kept as a
  separate token, an equivalence-classing decision in the spirit of
  Lecture 2's normalization discussion ("we want to match U.S.A. and
  USA").

**Stop-word policy (documented & justified, as the assignment asks):**
We start from the standard NLTK English stop-word list (198 words)
and remove every entry that is a single character or contains an
apostrophe (145 words remain — see the `STOPWORDS` set in the source
for the full list). **Why:** those removed entries exist in NLTK's
list only to catch tokenizers that split contractions like `don't` →
`don` + `t`. Our tokenizer never produces such fragments (there are no
contractions in this corpus, and we explicitly strip possessive `'s`
before tokenizing). Left in place, the single-character entries `s`
and `m` would be a genuine bug here: garment sizes ("Available in
size **S**", "size **M**", "size **L**") tokenize to the literal
letters `s`/`m`/`l`, and NLTK's unmodified list would silently treat
them as stop words, destroying real size information. The same
stop-word list is applied to indexing **and** to queries, consistently,
per the assignment's explicit instruction.

**Stemming:** `nltk.stem.porter.PorterStemmer` — a pure-Python
implementation of exactly the Porter algorithm from Lecture 2 (same 5
phases and rule tables, e.g. `SSES→SS`, `IES→I`, `S→`). No external
data download is required (unlike the NLTK stop-word corpus, which we
avoid depending on at runtime by hardcoding our final list).

**Dictionary output:** `outputs/dictionary_output.txt` — every
distinct stemmed term with its document frequency. Vocabulary size
M = 127 (small, because the corpus is template-generated with heavy
repeated boilerplate across all 100 documents — worth mentioning in
viva if asked why M is so small compared to Lecture 1's "500,000 term"
example).

---

## 4. Part B — Vector Space Model, lnc.ltc (`src/vsm.py`)

Implements exactly the SMART-notation scheme specified:

| | tf | idf | normalization |
|---|---|---|---|
| **Document (lnc)** | `1 + log10(tf)` | none | cosine |
| **Query (ltc)** | `1 + log10(tf)` | `log10(N/df)` | cosine |

Since both vectors are cosine-normalized, `cos(q,d)` reduces to a
plain dot product of normalized weights (Lecture 6). We use the
standard **accumulator algorithm** (Lecture 7, "Computing cosine
scores"): for each query term, walk its postings list once and add
its contribution to every document containing it — we never touch a
document that shares zero terms with the query, and never
materialize a dense 127-dimensional vector.

**Document length pre-computation:** `||d||` (needed for cosine
normalization) is computed once, at index-build time, using **every**
term present in that document — not just query terms. This matches
Lecture 6's own worked example, where document length is the norm of
the *whole* document vector. Getting this wrong (normalizing only
over query-term weights) is the single most common student bug in
this kind of assignment — we specifically guard against it.

**Out-of-vocabulary handling:** a query term with `df = 0` is given
weight 0 and simply dropped from the query vector (idf would
otherwise be undefined). The rest of the query still scores normally;
if *every* term is OOV, the result set is empty. This is the required
Part E "term not in the corpus" test case (`waterproof rain trench
coat`).

**Sorting/tie-breaking:** results sorted by score descending, then
docID ascending on exact ties, truncated to top 10 (fewer if fewer
documents match — the spec says "up to 10").

---

## 5. Part C — Positional index & phrase/proximity search

### The one design decision that matters most here

Lecture 2 makes an explicit point: *"you need stop words for phrase
queries, e.g. 'King of Denmark'."* If you strip stop words **before**
numbering token positions, two content words that were separated by a
stop word in the source text become artificially adjacent in your
position numbering — a false positive for phrase matching.

**Our fix:** position numbers are assigned over the **full,
un-filtered** token stream (stop words included in the count), but we
simply never create a postings/position entry *for* a stop word (it's
not an indexed term, per Part A). The result: every indexed term keeps
its *true* position in the original text, with gaps left wherever a
stop word occurred. Phrase and proximity search are therefore faithful
to true adjacency in the source text, not to some stop-word-stripped
approximation of it. (See `index_builder.py` docstring for the full
argument — this is a good "why did you do it this way" viva answer.)

**Known limitation, stated up front:** a phrase that itself *contains*
a stop word (e.g. "king of denmark") still cannot be looked up,
because the stop word has no postings entry at all. None of this
assignment's required/suggested phrase queries contain an internal
stop word, so it does not affect our results — but it's a deliberate,
documented trade-off, not an oversight.

### Exact phrase search (`positional_search.phrase_search`)

Generalized "positional intersect" for phrases of any length ≥ 2
(Lecture 2's "to be or not to be" example, generalized): candidate
start positions = positions of the first word; for each subsequent
word at offset `i`, keep only those starts `p` where `p+i` is a
position of that word in the same document. Surviving starts are the
phrase's occurrences, returned as evidence.

### Ordered proximity search (`positional_search.proximity_search`)

Precise definition (quote this if asked in viva):

> `term1 WITHIN/k term2` matches document *d* iff there exist
> positions *p1* (of term1) and *p2* (of term2) in *d* such that
> **p1 < p2** (ordered) and **p2 − p1 ≤ k**.

Distance is measured over the *true* token stream (stop words count
towards the gap), exactly matching Lecture 2's own worked example
("Employment agencies **that** place..." is a hit for `employment /4
place`; the gap-of-3 there includes the stop words "agencies that").
`k = 1` is equivalent to an exact 2-word phrase.

### Positional index output

`outputs/positional_index_output.txt` — every term with
`df → [(docID, tf, [positions...]), ...]`.

---

## 6. Part D — Application (`app.py`, Streamlit)

Two modes, exactly as specified:
1. **Free-text search** → VSM lnc.ltc, top-10 with docID/category/title/
   cosine score, plus an optional BM25 column for the novelty
   comparison.
2. **Phrase / Proximity search** → positional index. Both sub-modes
   display the **actual matching positions** (phrase start positions;
   `(p1, p2)` pairs for proximity) as direct evidence the positional
   index — not just plain postings — is what answered the query, per
   the assignment's explicit requirement.

Run `streamlit run app.py` and take your screenshots directly from the
browser for the submission's "screenshots of the application"
deliverable.

---

## 7. Part E — Testing (`tests/run_tests.py` → `outputs/test_report.md`)

Covers every mandatory case:
- 11 free-text queries (≥10 required; the 11th, `waterproof rain
  trench coat`, is the required "term not in the corpus" case).
- 7 exact phrase queries (≥5 required), drawn from the assignment's
  suggested list.
- 5 ordered proximity queries at k ∈ {2, 3, 4} (≥3 required, different
  k values).
- Two fully-worked, **empirically verified** (not hypothetical) cases
  where positional information changes the result set or reveals
  something VSM structurally cannot see:
  1. `cotton shirt` — VSM's top document (`D001`) is entirely absent
     from the exact-phrase match set, because "cotton" and "shirt"
     are 3 tokens apart in it (not adjacent) — bag-of-words scoring
     cannot tell "made from cotton, this...shirt" apart from an actual
     adjacent "cotton shirt".
  2. `festive kurta` — `festive` has `df = 100` (it's in every
     document's boilerplate), so its **idf is exactly 0** and it
     contributes nothing to the VSM score at all — yet
     `festive WITHIN/k kurta` matches **zero** documents for *any* k,
     because "kurta" structurally always precedes "festive" in every
     document (title-derived opening sentence vs. closing boilerplate)
     and our proximity search is ordered. This is a fact about word
     order that a bag-of-words model cannot represent even in
     principle.

---

## 8. Novelty — BM25 (`src/bm25.py`)

**What:** Okapi BM25 (`k1=1.5, b=0.75`, the standard Robertson &
Sparck-Jones defaults) implemented as a second scoring function over
the *same* index used by VSM — no new indexing structure, only a new
scoring view (mirroring the "one index, multiple views" principle
used throughout this project).

**Why this, and why it's not a random bolt-on:** Lecture 6 builds
tf-idf specifically to fix two problems with raw term counts — (a) tf
shouldn't count linearly, so it's log-dampened, and (b) common terms
shouldn't count as much as rare ones, so idf is multiplied in. BM25 is
the natural next step covered in most IR courses immediately after
this material: it keeps the same idf formulation, but replaces
log-dampening with a **saturating** function of tf that has an
explicit, tunable ceiling (`k1`), and it corrects for document length
using the **average** document length across the collection
(parameter `b`) — something lnc.ltc only does implicitly, via cosine
normalization, with no way to tune how strongly length should matter.

**What the comparison actually shows on this corpus:** because the
corpus is template-generated, all documents are close to the same
length, so BM25's length-normalization term (`b`) barely matters here
— but term-frequency saturation still does, and the two models
noticeably re-order results (see `test_report.md`'s novelty table:
6 of 10 test queries produce a *different* top-5 order between BM25
and lnc.ltc, even though both use the same idf formula). We report
this honestly rather than overclaiming that BM25 is simply "better" on
this data.

---

## 9. Anticipated viva questions (short answers)

**Q: Why no idf on the document side of lnc.ltc?**
A: SMART notation `lnc.ltc` puts idf only on the query side by design
— it's the standard scheme covered in Lecture 6 ("A very standard
weighting scheme is lnc.ltc... Document: logarithmic tf, no idf and
cosine normalization"). Applying idf twice (once per document, once
per query) would double-count a term's rarity.

**Q: How is document length normalization computed — over the whole
document or just query terms?**
A: The *whole* document vector, at index-build time, independent of
any query (`index_builder._compute_doc_lengths`). This is required for
correct cosine similarity; normalizing over only query terms is a
common bug and gives an unnormalized comparison across documents of
different lengths.

**Q: What happens to a query term not in the corpus?**
A: Its idf is undefined (`log(N/0)`), so we assign it weight 0 and
drop it from the query vector rather than crashing or scoring it
arbitrarily. If every term is OOV, we return an empty result set. This
is the same graceful handling used in both VSM and BM25.

**Q: Why do positions count stop words if stop words aren't indexed?**
A: So that indexed terms keep their *true* gap relative to each other
in the source text — otherwise removing a stop word between two
content words could make them look falsely adjacent. See Section 5.

**Q: What exactly does `WITHIN/k` mean?**
A: `term1` must occur strictly before `term2`, and the position
difference `p2 - p1` must be `≤ k`. `k=1` is identical to an exact
2-word phrase.

**Q: Why BM25 as the novelty and not something else?**
A: It's a direct, explainable extension of the exact weighting
concepts taught (log-tf, idf) rather than an unrelated technique — see
Section 8's full rationale.

**Q: Why is the vocabulary only 127 terms for 100 documents?**
A: The corpus is template-generated — most sentences ("designed for
everyday Indian wear", "suitable for comfortable regular use...") are
boilerplate repeated verbatim across all 100 documents, so the
*distinct* vocabulary is small even though total token count is much
larger. This is directly visible in `dictionary_output.txt`, where
several terms (`avail`, `casual`, `colour`, `festiv`, `garment`) have
`df = 100`.

**Q: Why stemming and not lemmatization?**
A: The assignment explicitly says "apply the stemming method," so
that's what drives the actual index. We also ran a full, corpus-wide
**supplementary comparison** against lemmatization (`analysis/
stem_vs_lemma.py` → `outputs/stem_vs_lemma_report.md`) precisely so
this trade-off could be answered with evidence rather than a vague
"lemmatization is the fancier one." Highlights: stemming over-merges
"leggings" → "leg" (a real but different word — a genuine false-match
risk), while lemmatization correctly keeps "legging"; conversely
lemmatization is only as good as its POS tagger, and on short
telegraphic product-description text the tagger can get it wrong too
(e.g. "striped" tagged as a past-tense verb, incorrectly lemmatized
to "strip" instead of staying an adjective related to "stripe").
Neither technique is unconditionally better — that honest, evidenced
comparison is the actual answer, not "stemming is what we used."

---

## 10. Supplementary analysis (not part of the graded pipeline)

`analysis/stem_vs_lemma.py` → `outputs/stem_vs_lemma_report.md`:
a full corpus-wide, POS-aware stemming-vs-lemmatization comparison
(WordNet lemmatizer + `nltk.pos_tag`), run purely to document the
trade-off discussed in Lecture 2 with real numbers and real examples
from this corpus — not used anywhere in Parts A-E, which use stemming
throughout as the assignment specifies. Run it yourself with:

```bash
python analysis/stem_vs_lemma.py
```

(Requires internet access on first run only, to download WordNet +
the POS tagger via `nltk.download`; this is why it's kept separate
from the core pipeline, which needs no network access at all.)
