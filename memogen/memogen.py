#!/usr/bin/env python3

import os
import json
import random
import requests
import argparse
import sys

# ─── Configuration ─────────────────────────────────────────────────────────────
CACHE_DIR   = os.path.expanduser("~/.adjustwords")
CACHE_FILE  = os.path.join(CACHE_DIR, "wordbank.json")
DATAMUSE_API= "https://api.datamuse.com/words?md=p&max=1000"

# ─── CLI Setup ─────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Multi‐mode generator: ‘rpg’ for passwords, ‘rug’ for usernames."
)
parser.add_argument(
    "--refresh", action="store_true",
    help="Force refresh of the cached word lists"
)
parser.add_argument(
    "--no-adverb", action="store_true",
    help="(rpg only) omit adverb in password combos"
)
args = parser.parse_args()

# ─── Cache Utilities ────────────────────────────────────────────────────────────
def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_words(pos_tag):
    try:
        resp = requests.get(DATAMUSE_API)
        data = resp.json()
        return [w["word"] for w in data if pos_tag in w.get("tags", [])]
    except Exception:
        return []

def build_wordbank():
    ensure_cache_dir()
    vb = sorted(set(fetch_words("v")))
    adv = sorted(set(fetch_words("adv")))
    aj  = sorted(set(fetch_words("adj")))
    nn  = sorted(set(fetch_words("n")))
    wb = {"verbs": vb, "adverbs": adv, "adjectives": aj, "nouns": nn}
    with open(CACHE_FILE, "w") as f:
        json.dump(wb, f)
    return wb

def load_wordbank(force=False):
    if force or not os.path.exists(CACHE_FILE):
        return build_wordbank()
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

# ─── Generation Routines ───────────────────────────────────────────────────────
def generate_password_variants(bank, use_adverb=True):
    verb   = random.choice(bank["verbs"]).capitalize()
    noun   = random.choice(bank["nouns"]).capitalize()
    adverb = random.choice(bank["adverbs"]).capitalize() if use_adverb else ""
    symbol = random.choice(["$", "#", "!", "=", "_", "-"])
    number = str(random.randint(0, 99))
    core   = f"{verb}{adverb}{noun}"

    return {
        "basic":      core,
        "withNumber": f"{core}{number}",
        "withSymbol": f"{core}{symbol}",
        "wrapped":    f"{symbol}{core}{symbol}{number}",
        "hyphenated": f"{verb}-{adverb}-{noun}-{number}" if use_adverb
                      else f"{verb}-{noun}-{number}",
        "underscore": f"{verb}_{adverb}_{noun}_{number}" if use_adverb
                      else f"{verb}_{noun}_{number}",
        "obfuscated": f"{verb[0].lower()}_{noun.upper()}_{number}{symbol}",
    }

def generate_username(bank):
    adj    = random.choice(bank["adjectives"]).capitalize()
    noun   = random.choice(bank["nouns"]).capitalize()
    number = str(random.randint(1, 9999)).zfill(3)
    return f"{adj}{noun}{number}"

# ─── Dispatcher ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mode = os.path.basename(sys.argv[0])
    wb   = load_wordbank(force=args.refresh)

    if mode == "rpg":
        variants = generate_password_variants(wb, use_adverb=not args.no_adverb)
        for name, pwd in variants.items():
            print(f"{name}: {pwd}")

    elif mode == "rug":
        print(generate_username(wb))

    else:
        print("Invoke this script as either “rpg” or “rug”.", file=sys.stderr)
        sys.exit(1)
