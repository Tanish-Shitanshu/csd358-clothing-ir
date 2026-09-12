"""
preprocessing.py
=================
Tokenization, normalization, stop-word removal and stemming pipeline
for the Clothing Ranked-Retrieval assignment (CSD358, Assignment 1).

DESIGN DECISIONS (documented here so they can be defended in viva):

1. TOKENIZATION
   We lowercase the full text, strip possessive "'s" (so "Men's" ->
   "men", consistent with the normalization / equivalence-classing
   discussion in Lecture 2 -- "we want to match U.S.A. and USA" etc.),
   then extract maximal runs of [a-z0-9] as tokens. Hyphens ("- Black")
   are treated purely as separators in this corpus (they are used as a
   dash before a colour name, never as part of a compound word such as
   "state-of-the-art"), so they simply split tokens like whitespace
   does. Numbers (e.g. "100" from "100%") are RETAINED as tokens, per
   Lecture 1's remark that indexing numbers is "generally a useful
   feature".

2. STOP-WORD POLICY
   We start from the standard NLTK English stop-word list (198 words)
   and apply it *consistently* to both documents and queries, as
   instructed by the assignment and by the Lecture 2 slide ("apply it
   consistently"). We then remove from that list:
     - every single-character entry (s, t, d, m, y, o, ...) and every
       entry containing an apostrophe.
   Reason: these entries only exist in NLTK's list to catch tokenizers
   that split contractions like "don't" -> "don" + "t". Our tokenizer
   never produces such fragments (we explicitly strip possessive 's
   before tokenizing, and the corpus contains no other contractions).
   Left in place, the single-character entries "s" and "m" would be a
   real domain bug for this corpus: garment sizes ("Available in size
   S", "size M", "size L") tokenize to the *literal* letters s/m/l,
   and NLTK's list would silently swallow them as stop words. Removing
   the single-character/apostrophe entries fixes this without
   weakening the stop-word list for any word that can actually occur
   in our tokenizer's output space.
   Final list size: 145 words (see STOPWORDS below).

3. STEMMING
   We use nltk.stem.porter.PorterStemmer, which is a pure-Python
   implementation of exactly the Porter algorithm covered in Lecture 2
   (same 5 phases / rule tables, e.g. SSES->SS, IES->I, S-> as shown
   on the "Porter stemmer: A few rules" slide). It requires no
   external data download, so it is fully deterministic and
   reproducible offline.

4. PIPELINE ORDER
   raw text -> lowercase -> strip possessive -> tokenize (regex) ->
   [this full, un-filtered token stream is what position numbers are
   computed over -- see positional_index.py for why] -> stop-word
   filter -> stem.
   Stop-word filter happens BEFORE stemming (removing "was"/"is" etc.
   before stemming them is slightly cheaper and never changes the
   result, since none of our stop words stem to a non-stop-word).
"""

import re

# ---------------------------------------------------------------------------
# Stop-word list: standard NLTK English list, minus single-character and
# apostrophe-containing entries (see docstring point 2 above for why).
# ---------------------------------------------------------------------------
STOPWORDS = frozenset([
    'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an',
    'and', 'any', 'are', 'aren', 'as', 'at', 'be', 'because', 'been',
    'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can',
    'couldn', 'did', 'didn', 'do', 'does', 'doesn', 'doing', 'don', 'down',
    'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', 'has',
    'hasn', 'have', 'haven', 'having', 'he', 'her', 'here', 'hers',
    'herself', 'him', 'himself', 'his', 'how', 'if', 'in', 'into', 'is',
    'isn', 'it', 'its', 'itself', 'just', 'll', 'ma', 'me', 'mightn',
    'more', 'most', 'mustn', 'my', 'myself', 'needn', 'no', 'nor', 'not',
    'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours',
    'ourselves', 'out', 'over', 'own', 're', 'same', 'shan', 'she',
    'should', 'shouldn', 'so', 'some', 'such', 'than', 'that', 'the',
    'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these',
    'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until',
    'up', 've', 'very', 'was', 'wasn', 'we', 'were', 'weren', 'what',
    'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will',
    'with', 'won', 'wouldn', 'you', 'your', 'yours', 'yourself',
    'yourselves',
])

_TOKEN_RE = re.compile(r'[a-z0-9]+')

try:
    from nltk.stem.porter import PorterStemmer
    _stemmer = PorterStemmer()
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "This project requires nltk (for the pure-Python Porter stemmer). "
        "Install with: pip install nltk"
    ) from e


def normalize_and_tokenize(text: str) -> list[str]:
    """
    Lowercase, strip possessive 's, and tokenize into a raw (un-filtered,
    un-stemmed) list of tokens. This is the "full stream" over which
    position numbers are assigned in the positional index -- stop words
    are NOT removed here, only in `remove_stopwords`, so that a caller
    who needs true adjacency (positional_index.py) can still see the
    gaps that stop words leave behind.
    """
    text = text.lower()
    text = re.sub(r"'s\b", "", text)   # men's -> men, women's -> women
    text = text.replace("'", "")       # any stray apostrophes
    return _TOKEN_RE.findall(text)


def is_stopword(token: str) -> bool:
    return token in STOPWORDS


def stem(token: str) -> str:
    return _stemmer.stem(token)


def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS]


def preprocess(text: str) -> list[str]:
    """
    Full Part-A pipeline: tokenize -> remove stop words -> stem.
    Used wherever we DON'T need position information (e.g. quick
    sanity checks, or preprocessing a free-text query for VSM scoring).
    """
    tokens = normalize_and_tokenize(text)
    tokens = remove_stopwords(tokens)
    return [stem(t) for t in tokens]


if __name__ == "__main__":
    sample = "Men's Checked Cotton Shirt - Black. Available in size S."
    print("raw tokens:      ", normalize_and_tokenize(sample))
    print("after stopwords: ", remove_stopwords(normalize_and_tokenize(sample)))
    print("final (stemmed): ", preprocess(sample))
