#!/usr/bin/env python3
"""Generate username candidates from full names (common corporate formats).

    python username_gen.py "Priya Natarajan" "John Smith" > users.txt
    python username_gen.py -f names.txt --format '{f}{last}'      # only one format
Placeholders: {first} {last} {f} {l}
"""
import argparse

FORMATS = ["{f}{last}", "{first}.{last}", "{first}{last}", "{first}", "{last}", "{first}_{last}",
           "{f}.{last}", "{last}{f}", "{first}{l}", "{last}.{first}", "{f}{l}", "{first}-{last}"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*")
    ap.add_argument("-f", "--file")
    ap.add_argument("--format", action="append")
    a = ap.parse_args()
    names = list(a.names)
    if a.file:
        names += [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()]
    seen = set()
    for n in names:
        parts = n.lower().split()
        if not parts:
            continue
        first, last = parts[0], parts[-1]
        for fmt in a.format or FORMATS:
            u = fmt.format(first=first, last=last, f=first[0], l=last[0])
            if u not in seen:
                seen.add(u)
                print(u)


if __name__ == "__main__":
    main()
