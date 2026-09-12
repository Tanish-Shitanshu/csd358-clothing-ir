"""
dump_outputs.py
===============
Generates the required deliverable files:
  outputs/dictionary_output.txt      (Part A: term, df)
  outputs/postings_output.txt        (Part A: term -> df -> [(docID, tf), ...])
  outputs/positional_index_output.txt (Part C: term -> df -> [(docID, tf, [positions]), ...])

Run from the project root: python src/dump_outputs.py
"""

import os
from corpus import load_corpus
from index_builder import InvertedIndex

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "outputs")


def main():
    docs = load_corpus(os.path.join(ROOT, "corpus_100.txt"))
    index = InvertedIndex()
    index.build(docs)
    os.makedirs(OUT_DIR, exist_ok=True)

    vocab = index.vocabulary()

    # ---------------- dictionary_output.txt ----------------
    with open(os.path.join(OUT_DIR, "dictionary_output.txt"), "w") as f:
        f.write(f"# Dictionary for clothing corpus (N = {index.N} documents)\n")
        f.write(f"# Vocabulary size (M) = {len(vocab)}\n")
        f.write(f"# {'term':<20}{'df':>6}\n")
        f.write("#" + "-" * 30 + "\n")
        for term in vocab:
            f.write(f"{term:<22}{index.df(term):>4}\n")

    # ---------------- postings_output.txt ----------------
    with open(os.path.join(OUT_DIR, "postings_output.txt"), "w") as f:
        f.write("# Non-positional postings: term -> df -> [(docID, tf), ...]\n\n")
        for term in vocab:
            doc_dict = index.postings[term]
            df = len(doc_dict)
            postings_list = [(docid, len(pos)) for docid, pos in sorted(doc_dict.items())]
            f.write(f"{term} -> df={df} -> {postings_list}\n")

    # ---------------- positional_index_output.txt ----------------
    with open(os.path.join(OUT_DIR, "positional_index_output.txt"), "w") as f:
        f.write("# Positional postings: term -> df -> [(docID, tf, [positions]), ...]\n\n")
        for term in vocab:
            doc_dict = index.postings[term]
            df = len(doc_dict)
            postings_list = [(docid, len(pos), pos) for docid, pos in sorted(doc_dict.items())]
            f.write(f"{term} -> df={df} -> {postings_list}\n")

    print(f"Wrote dictionary_output.txt, postings_output.txt, "
          f"positional_index_output.txt to {OUT_DIR}")
    print(f"N = {index.N}, M (vocabulary size) = {len(vocab)}")


if __name__ == "__main__":
    main()
