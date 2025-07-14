#!/usr/bin/env python3

import os
import random
import nltk
from nltk.corpus import wordnet as wn

# Ensure WordNet data is ready
try:
    wn.synsets("test")
except LookupError:
    nltk.download("wordnet")
    nltk.download("omw-1.4")

# ─── Configuration ─────────────────────────────────────────────────────────────
DICT_PATH  = "/usr/share/dict/words"
TARGET_DIR = "/usr/share/randgen"
MAX_LENGTH = 7
MAX_WORDS  = 1000

os.makedirs(TARGET_DIR, exist_ok=True)

def load_raw_words():
    try:
        with open(DICT_PATH, "r") as f:
            return {
                w.strip().lower()
                for w in f
                if w.strip().isalpha() and len(w.strip()) <= MAX_LENGTH
            }
    except FileNotFoundError:
        print(f"❌ Can't find dictionary at {DICT_PATH}")
        return set()

def is_pos(word, tag):
    return any(s.pos() == tag for s in wn.synsets(word))

def classify(words, pos_tag):
    pool = []
    for w in words:
        if is_pos(w, pos_tag):
            pool.append(w.capitalize())
        if len(pool) >= MAX_WORDS:
            break
    return sorted(pool)

def save(filename, words):
    path = os.path.join(TARGET_DIR, filename)
    with open(path, "w") as f:
        f.write("\n".join(words))
    print(f"✅ Saved {len(words)} words to {path}")

# ─── Execution ─────────────────────────────────────────────────────────────────
print("🔎 Generating POS-specific wordlists...")
source_words = load_raw_words()

save("verbs.txt",       classify(source_words, "v"))
save("nouns.txt",       classify(source_words, "n"))
save("adjectives.txt",  classify(source_words, "a"))
save("adverbs.txt",     classify(source_words, "r"))

