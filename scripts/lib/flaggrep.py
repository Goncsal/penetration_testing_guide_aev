#!/usr/bin/env python3
"""Find flag{...} in a URL response, a file, a directory tree, or stdin.

Also tries HTML-unescape, URL-decode, base64 and hex decoding of every token,
so encoded flags are found too.

    python flaggrep.py http://target/page
    python flaggrep.py dump.sql
    python flaggrep.py ./out_repo           # recursive
    curl -s ... | python flaggrep.py -
    python flaggrep.py file --regex 'CTF\\{[^}]+\\}'
"""
import argparse
import base64
import binascii
import html
import os
import re
import sys
import urllib.parse

DEFAULT_RE = r"flag\{[^}\s]{1,200}\}"


def decodings(text):
    yield text
    yield html.unescape(text)
    yield urllib.parse.unquote_plus(text)
    for tok in set(re.findall(r"[A-Za-z0-9+/_=-]{16,}", text)):
        t = tok.replace("-", "+").replace("_", "/")
        try:
            yield base64.b64decode(t + "=" * (-len(t) % 4)).decode("utf-8", "ignore")
        except (binascii.Error, ValueError):
            pass
    for tok in set(re.findall(r"(?:[0-9a-fA-F]{2}){8,}", text)):
        try:
            yield bytes.fromhex(tok).decode("utf-8", "ignore")
        except ValueError:
            pass


def find(text, rx):
    hits = []
    for d in decodings(text):
        for m in rx.findall(d):
            if m not in hits:
                hits.append(m)
    return hits


def read_source(src):
    if src == "-":
        yield "<stdin>", sys.stdin.read()
    elif re.match(r"^https?://", src):
        import requests
        r = requests.get(src, timeout=15)
        yield src, r.text + "\n" + "\n".join(f"{k}: {v}" for k, v in r.headers.items())
    elif os.path.isdir(src):
        for root, _, files in os.walk(src):
            for f in files:
                p = os.path.join(root, f)
                try:
                    yield p, open(p, "rb").read().decode("utf-8", "ignore")
                except OSError:
                    pass
    else:
        yield src, open(src, "rb").read().decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="URL, file, directory or - for stdin")
    ap.add_argument("--regex", default=DEFAULT_RE)
    a = ap.parse_args()
    rx = re.compile(a.regex)
    found = 0
    for s in a.sources:
        for name, text in read_source(s):
            for h in find(text, rx):
                print(f"{name}: {h}")
                found += 1
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
