#!/usr/bin/env python3
"""Guess how a token was generated (hash of username / timestamp / both).

Give an observed token and what you know (username, approx time). It tries
md5/sha1/sha224/sha256/sha512 (+ truncations) over many input templates and
time windows, and prints the recipe that reproduces the token.

    python token_recipe.py 3f1c... --user agent --ts-window 60
    python token_recipe.py <reset_token> --user user --extra reset --no-time
    python token_recipe.py <tok> --user bob --ts 1731412345 --ts-window 5
"""
import argparse
import base64
import hashlib
import time

ALGOS = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


def templates(user, extras, with_time):
    seps = [":", "", "-", "_", "|", ".", " "]
    base = [user] + [f"{e}{s}{user}" for e in extras for s in seps] + [f"{user}{s}{e}" for e in extras for s in seps]
    for b in base:
        yield b, False
    if with_time:
        for b in base:
            for s in seps:
                yield f"{b}{s}{{ts}}", True
                yield f"{{ts}}{s}{b}", True
        yield "{ts}", True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("token")
    ap.add_argument("--user", default="admin")
    ap.add_argument("--extra", action="append", default=[], help="extra words seen in the app (e.g. reset, session, secret)")
    ap.add_argument("--ts", type=int, help="center timestamp (default: now)")
    ap.add_argument("--ts-window", type=int, default=30)
    ap.add_argument("--no-time", action="store_true")
    a = ap.parse_args()
    tok = a.token.strip().lower()
    extras = a.extra + ["reset", "session", "token", "secret", "salt"]
    center = a.ts or int(time.time())
    tss = [] if a.no_time else list(range(center - a.ts_window, center + a.ts_window + 1))

    def check(s, label):
        b = s.encode()
        for alg in ALGOS:
            h = hashlib.new(alg, b).hexdigest()
            if h == tok or (len(tok) < len(h) and h.startswith(tok)):
                print(f"[+] {alg}({label!r})" + (f"[:{len(tok)}]" if len(tok) < len(h) else ""))
                return True
        if base64.b64encode(b).decode().lower() == tok:
            print(f"[+] base64({label!r})")
            return True
        return False

    for tpl, needs_ts in templates(a.user, extras, not a.no_time):
        if not needs_ts:
            if check(tpl, tpl):
                return
            continue
        for ts in tss:
            for val in (str(ts), str(ts * 1000)):
                if check(tpl.replace("{ts}", val), tpl.replace("{ts}", val)):
                    return
    print("[-] no recipe found; try --extra words, a different --user or a wider --ts-window")


if __name__ == "__main__":
    main()
