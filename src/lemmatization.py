"""
lemmatization.py
=================
SUPPLEMENTARY ANALYSIS ONLY — not used anywhere in the graded Part
A-E pipeline. The assignment explicitly instructs: "apply the
stemming method" (Part A), and our actual index (index_builder.py)
uses the Porter stemmer accordingly, exactly as specified.

This module exists purely to produce an honest, evidence-based
comparison of stemming vs. lemmatization for the documentation /
viva, since Lecture 2 explicitly draws this distinction:
  - STEMMING: crude, rule-based suffix-stripping (Porter). Fast,
    deterministic, no dictionary needed, but can produce non-words
    and can incorrectly conflate distinct words.
  - LEMMATIZATION: proper morphological analysis against a
    dictionary (WordNet), returns real dictionary words, but is
    slower, needs POS information to be accurate, and needs a
    (large) lexical resource.

We use NLTK's WordNetLemmatizer, made POS-aware via nltk.pos_tag +
a Penn-Treebank -> WordNet POS mapping (the lemmatizer defaults to
treating every word as a noun otherwise, which silently produces
wrong results for verbs/adjectives — e.g. lemmatizing "designed" as
a noun leaves it unchanged, but as a verb correctly gives "design").

NOTE: unlike preprocessing.py's stopword list (hardcoded specifically
so the graded pipeline needs no network access), this module DOES
call nltk.download() for wordnet/omw-1.4/the POS tagger the first
time it runs, since it is optional supplementary analysis, not part
of the submitted, graded system.
"""

from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

_ensure_done = False


def _ensure_nltk_data():
    global _ensure_done
    if _ensure_done:
        return
    import nltk
    for pkg in ["wordnet", "omw-1.4"]:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass
    for pkg in ["averaged_perceptron_tagger_eng", "averaged_perceptron_tagger"]:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass
    _ensure_done = True


_lemmatizer = None


def _get_lemmatizer():
    global _lemmatizer
    if _lemmatizer is None:
        _ensure_nltk_data()
        _lemmatizer = WordNetLemmatizer()
    return _lemmatizer


def _wordnet_pos(treebank_tag: str) -> str:
    # nltk.pos_tag returns Penn Treebank tags (e.g. "VBD", "JJ", "NNS"), but
    # WordNetLemmatizer only understands its own 4 coarse POS constants, so
    # each Treebank tag family is mapped down to the matching WordNet one.
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    if treebank_tag.startswith("V"):
        return wordnet.VERB
    if treebank_tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN  # default / fallback, matches WordNetLemmatizer's own default


def lemmatize_tokens(tokens: list[str]) -> list[str]:
    """POS-tag the token list, then lemmatize each token with its
    mapped WordNet POS. Operates on a whole token list (not one word
    at a time) because POS tagging needs surrounding context to be
    accurate."""
    lemmatizer = _get_lemmatizer()
    tagged = pos_tag(tokens)  # tag the whole sequence at once so context (surrounding tokens) informs each tag
    return [lemmatizer.lemmatize(tok, pos=_wordnet_pos(tag)) for tok, tag in tagged]


if __name__ == "__main__":
    from preprocessing import normalize_and_tokenize, remove_stopwords, stem

    sample = ("Men's Cotton Crew Neck T-Shirt - Black. Made from 100% cotton, "
              "this t-shirt is designed for everyday Indian wear. Available "
              "in size S. High waist leggings are also popular.")
    tokens = remove_stopwords(normalize_and_tokenize(sample))
    stems = [stem(t) for t in tokens]
    lemmas = lemmatize_tokens(tokens)

    print(f"{'token':<15}{'stem':<15}{'lemma':<15}{'differ?'}")
    for t, s, l in zip(tokens, stems, lemmas):
        flag = "  <-- DIFFERS" if s != l else ""
        print(f"{t:<15}{s:<15}{l:<15}{flag}")
