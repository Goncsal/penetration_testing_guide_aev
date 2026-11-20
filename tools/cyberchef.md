# CyberChef

https://gchq.github.io/CyberChef — drag "operations" into a recipe. Runs locally in the browser.

Most useful: **Magic** (auto-detect encodings), From Base64 / Base64url, URL Decode, From Hex,
ROT13, XOR (+ brute force), JWT Decode, Gunzip/Zlib Inflate, HTML Entity decode, From Charcode,
Regular expression (extract `flag\{[^}]+\}`).

CLI equivalents: `base64 -d`, `xxd -r -p`, `python -c "import urllib.parse;print(urllib.parse.unquote('...'))"`,
`python scripts/lib/flaggrep.py` (tries base64/hex/url-decoding automatically).
