#!/usr/bin/env python3
"""Out-of-band catcher: logs every request (method, path, query, headers of
interest, body), answers 200 with permissive CORS, and serves files from
--serve-dir (e.g. x.js, evil.dtd, shell.php for RFI). Decodes base64-looking
query values and highlights flags.

    python catch_server.py --port 8000
    sudo python catch_server.py --port 443          # lab egress allows 80/443 only (plain HTTP on 443 is fine)
    python catch_server.py --port 80 --serve-dir ./payloads
"""
import argparse
import base64
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qsl, unquote

FLAG = re.compile(r"flag\{[^}]+\}")


def try_b64(v):
    try:
        d = base64.b64decode(v + "=" * (-len(v) % 4), validate=False).decode("utf-8")
        return d if d.isprintable() or "\n" in d else None
    except Exception:
        return None


def make_handler(serve_dir):
    class H(BaseHTTPRequestHandler):
        def _log(self, body=b""):
            u = urlparse(self.path)
            print(f"\n=== {self.client_address[0]} {self.command} {unquote(self.path)}")
            for k in ("Host", "User-Agent", "Cookie", "Referer", "Origin", "Content-Type"):
                if self.headers.get(k):
                    print(f"    {k}: {self.headers[k]}")
            text = unquote(self.path) + "\n" + body.decode("utf-8", "ignore")
            for k, v in parse_qsl(u.query, keep_blank_values=True):
                d = try_b64(v)
                if d:
                    print(f"    [b64 {k}] {d}")
                    text += "\n" + d
            if body:
                print(f"    body: {body[:2000].decode('utf-8', 'ignore')}")
            for f in FLAG.findall(text):
                print(f"    [FLAG] {f}")

        def _reply(self):
            path = urlparse(self.path).path.lstrip("/")
            data, ctype = b"ok", "text/plain"
            if serve_dir and path:
                fp = os.path.realpath(os.path.join(serve_dir, path))
                if fp.startswith(os.path.realpath(serve_dir)) and os.path.isfile(fp):
                    data = open(fp, "rb").read()
                    ctype = "application/javascript" if fp.endswith(".js") else "application/xml-dtd" \
                        if fp.endswith(".dtd") else "text/plain"
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", self.headers.get("Origin") or "*")
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self._log()
            self._reply()

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            self._log(self.rfile.read(n) if n else b"")
            self._reply()

        do_PUT = do_POST

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", self.headers.get("Origin") or "*")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def log_message(self, *a):
            pass
    return H


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--bind", default="0.0.0.0")
    ap.add_argument("--serve-dir")
    a = ap.parse_args()
    print(f"[*] listening on {a.bind}:{a.port}")
    ThreadingHTTPServer((a.bind, a.port), make_handler(a.serve_dir)).serve_forever()


if __name__ == "__main__":
    main()
