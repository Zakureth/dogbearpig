#!/usr/bin/env python3

import os
import random
import argparse
import sys

# ─── Configuration ─────────────────────────────────────────────────────────────
WORD_DIR     = "/usr/share/memogen"
MAX_OUTLEN   = 15
PAD_THRESHOLD = 12

# ─── CLI Setup ─────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Multi-mode generator: ‘rpg’ for passwords, ‘rug’ for usernames."
)
args = parser.parse_args()

# ─── Load Words ────────────────────────────────────────────────────────────────
def load_wordlist(filename):
    path = os.path.join(WORD_DIR, filename)
    try:
        with open(path, "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"⚠️ Missing wordlist: {path}", file=sys.stderr)
        return []

def load_wordbank():
    return {
        "verbs": load_wordlist("verbs.txt"),
        "adverbs": load_wordlist("adverbs.txt"),
        "adjectives": load_wordlist("adjectives.txt"),
        "nouns": load_wordlist("nouns.txt"),
    }

# ─── Password Generator ────────────────────────────────────────────────────────
def generate_password(bank):
    for _ in range(100):
        adv = random.choice(bank["adverbs"]).capitalize()
        vb  = random.choice(bank["verbs"]).capitalize()
        nn  = random.choice(bank["nouns"]).capitalize()
        num = str(random.randint(0, 99))

        short = f"{adv}-{vb}-{num}"
        if len(short) < PAD_THRESHOLD:
            long = f"{adv}-{vb}-{nn}-{num}"
            if len(long) <= MAX_OUTLEN:
                return {"combo": long}
        if len(short) <= MAX_OUTLEN:
            return {"combo": short}

    return {"combo": "Soft-Jump-42"}  # fallback


# ─── Username Generator ────────────────────────────────────────────────────────
def generate_username(bank):
    for _ in range(100):
        adj = random.choice(bank["adjectives"])
        nn  = random.choice(bank["nouns"])
        num = str(random.randint(1, 9999)).zfill(3)
        uname = f"{adj}{nn}{num}"
        if len(uname) <= MAX_OUTLEN:
            return uname
    return f"{adj[:3]}{nn[:3]}{num}"

# ─── Dispatcher ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mode = os.path.basename(sys.argv[0])
    bank = load_wordbank()

    if mode == "rpg":
        print(f"combo: {generate_password(bank)['combo']}")
    elif mode == "rug":
        print(generate_username(bank))
    else:
        print("Invoke this script as either “rpg” or “rug”.", file=sys.stderr)
        sys.exit(1)

