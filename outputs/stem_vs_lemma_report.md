# Supplementary Analysis: Stemming vs. Lemmatization

**This analysis is NOT part of the graded Part A-E pipeline.** The submitted system uses Porter stemming throughout, exactly as the assignment specifies ("apply the stemming method"). This document exists purely to demonstrate, with real evidence from this corpus, the trade-off Lecture 2 draws between stemming (crude, rule-based, e.g. Porter) and lemmatization (dictionary-based, POS-aware, e.g. WordNet).

## Summary statistics

- Total (post-stopword-removal) tokens processed: **4583**
- Tokens where stem ≠ lemma: **1375** (30.0% of all tokens)
- Distinct vocabulary under stemming (M_stem): **127** (this matches `dictionary_output.txt`'s M = 127)
- Distinct vocabulary under lemmatization (M_lemma): **129**

Lemmatization produces a larger vocabulary than stemming here. This is the expected direction: stemming deliberately over-merges related word forms into one (possibly non-word) root to maximize recall, so it tends to *collapse* the vocabulary more aggressively than a lemmatizer, which only merges forms that are truly the same dictionary headword.

## Categorized divergent examples

### 1. Over-stemming (Porter conflates two genuinely different words)

| Surface token | Porter stem | WordNet lemma | Why it matters |
|---|---|---|---|
| leggings | `leg` | `legging` | Porter's stem is the *body part* "leg" — a real but different word. A query for "leg injury" (unrelated domain) would spuriously match "leggings" documents under stemming, but not under lemmatization. |
| available | `avail` | `available` | Porter strips the "-able" suffix, producing "avail" (a *verb*), even though "available" is already a valid base-form adjective that should not be reduced further. |

### 2. Cases where lemmatization is MORE accurate (irregular morphology)

| Surface token | Porter stem | WordNet lemma | Why it matters |
|---|---|---|---|
| made | `made` (unchanged — Porter has no rule for irregular verbs) | `make` (correctly identifies the base verb *make*) | Porter is purely suffix-rule-based and cannot handle irregular forms; a POS-aware lemmatizer with a dictionary can. A query for "make" would NOT match documents containing "made" under our stemmed index, but would under a lemmatized one — a genuine recall gap our system has, worth naming honestly in viva if asked about limitations. |

### 3. Where lemmatization is actually WORSE (POS-tagger error)

Lemmatization's accuracy is entirely dependent on getting the POS tag right — and POS taggers make mistakes on short, context-poor product descriptions. Concrete example from this corpus:

| Surface token | Porter stem | WordNet lemma | What went wrong |
|---|---|---|---|
| striped | `stripe` (reasonable — recognizably related to "stripe") | `strip` | The POS tagger tags "striped" as `VBD` (past-tense verb, as in "he **striped** the wall") instead of `JJ` (adjective, as in "a **striped** shirt") given the short, determiner-only context ("this striped shirt..."). WordNetLemmatizer then correctly lemmatizes the *verb* "striped" → "strip" — linguistically correct FOR A VERB, but wrong for this sentence, because the POS tag itself was wrong. |

This is worth stating plainly if asked "so lemmatization is just better, right?" in viva: **no** — it is only as good as its POS tagger, and on short, telegraphic product-description text (little surrounding context, frequent adjective/participle ambiguity), the tagger error rate is non-trivial. Stemming's crude, context-free suffix rules are at least *consistently* wrong/right, never dependent on a second model's accuracy. This is precisely why we made a deliberate, documented choice rather than an uninformed one.

### 4. Full list of every surface token where stem ≠ lemma

| Surface token | Porter stem | WordNet lemma | Occurrences in corpus |
|---|---|---|---|
| comfortable | `comfort` | `comfortable` | 130 |
| festive | `festiv` | `festive` | 110 |
| made | `made` | `make` | 100 |
| features | `featur` | `feature` | 100 |
| office | `offic` | `office` | 100 |
| available | `avail` | `available` | 100 |
| suitable | `suitabl` | `suitable` | 100 |
| wardrobe | `wardrob` | `wardrobe` | 100 |
| essentials | `essenti` | `essential` | 100 |
| women | `women` | `woman` | 60 |
| durable | `durabl` | `durable` | 26 |
| breathable | `breathabl` | `breathable` | 20 |
| saree | `sare` | `saree` | 20 |
| fleece | `fleec` | `fleece` | 20 |
| hoodie | `hoodi` | `hoodie` | 20 |
| olive | `oliv` | `olive` | 20 |
| leggings | `leg` | `legging` | 20 |
| navy | `navi` | `navy` | 20 |
| friendly | `friendli` | `friendly` | 17 |
| easy | `easi` | `easy` | 17 |
| construction | `construct` | `construction` | 17 |
| minimal | `minim` | `minimal` | 16 |
| shrinkage | `shrinkag` | `shrinkage` | 16 |
| beige | `beig` | `beige` | 12 |
| machine | `machin` | `machine` | 10 |
| washable | `washabl` | `washable` | 10 |
| closure | `closur` | `closure` | 10 |
| fly | `fli` | `fly` | 10 |
| sleeves | `sleev` | `sleeve` | 10 |
| oversized | `overs` | `oversized` | 10 |
| poly | `poli` | `poly` | 10 |
| viscose | `viscos` | `viscose` | 10 |
| daily | `daili` | `daily` | 5 |
| quilted | `quilt` | `quilted` | 5 |
| polyester | `polyest` | `polyester` | 5 |
| striped | `stripe` | `strip` | 5 |
| pullover | `pullov` | `pullover` | 5 |
| active | `activ` | `active` | 5 |
| purple | `purpl` | `purple` | 2 |
| lavender | `lavend` | `lavender` | 2 |

## Why we still use stemming for the actual system

1. The assignment explicitly requires it ("apply the stemming method").
2. Porter stemming needs no dictionary/POS tagging and is fully deterministic and dependency-light (no data download at grading time — see `preprocessing.py`), whereas accurate lemmatization needs POS tagging plus a large lexical database (WordNet), adding real runtime and setup cost for a 100-document corpus where it would change very few actual query outcomes (only 30.0% of tokens diverge at all).
3. The over-stemming risk (Case 1 above) is a real, acknowledged limitation of our system — not something we're unaware of.