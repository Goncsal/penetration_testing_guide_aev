#!/usr/bin/env python3
"""Look for editor/backup copies of known files.

For each path given, tries suffixes (.bak .old ~ .orig .save .swp ...), vim swap
names (.name.swp), emacs (#name#), and archive variants. Prints hits and flags.

    python backup_hunt.py http://target /static/config.py /index.php /app.py
"""
import argparse
import posixpath
import re

import requests

FLAG = re.compile(r"flag\{[^}]+\}")
SUFFIXES = [".bak", ".old", ".orig", ".save", ".sav", ".tmp", ".temp", ".copy", ".backup", ".bk",
            "~", ".1", ".2", ".txt", ".dist", ".swp", ".swo", ".un~", ".zip", ".tar.gz", ".gz", "_bak",
            "-bak", ".bak1", ".old1", ".prev", ".inc"]


def variants(path):
    d, name = posixpath.split(path)
    stem, ext = posixpath.splitext(name)
    out = [path + s for s in SUFFIXES]
    out += [posixpath.join(d, f".{name}.swp"), posixpath.join(d, f".{name}.swo"),
            posixpath.join(d, f"#{name}#"), posixpath.join(d, f"{stem}.bak{ext}"),
            posixpath.join(d, f"{stem}_old{ext}"), posixpath.join(d, f"Copy of {name}"),
            posixpath.join(d, f"{stem} (copy){ext}")]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    hdrs = {"Cookie": a.cookie} if a.cookie else {}
    for p in a.paths:
        p = "/" + p.lstrip("/")
        for v in variants(p):
            url = base + requests.utils.quote(v, safe="/~")
            try:
                r = requests.get(url, headers=hdrs, timeout=8, allow_redirects=False)
            except requests.RequestException:
                continue
            if r.status_code == 200 and len(r.content):
                print(f"[200] {len(r.content):7d} {v}")
                for f in FLAG.findall(r.text):
                    print(f"      [FLAG] {f}")


if __name__ == "__main__":
    main()
