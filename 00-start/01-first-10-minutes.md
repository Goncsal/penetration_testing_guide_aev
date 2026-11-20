# First 10 minutes on any challenge

Do the same steps every time. Most course flags fall out of steps 1–5.

## 1. Read everything you were given
- Title, description, the 3-line "haiku" hint, listed credentials, CWE if shown → [03-reading-hints.md](03-reading-hints.md)
- Handout files (binary? source?) → if binary: [10-pwn](../10-pwn/README.md)

## 2. What is listening?
```bash
nmap -sV -sC -p- --min-rate 2000 <host>          # TCP
sudo nmap -sU --top-ports 50 <host>              # UDP (SNMP 161!)
```
Non-HTTP port → [09-network](../09-network/README.md). Details: [tools/nmap.md](../tools/nmap.md)

## 3. Look at the raw HTTP
```bash
curl -si $T/ | head -40            # status, Server, X-Powered-By, Set-Cookie
curl -s  $T/ | grep -iE 'flag\{|<!--|href=|src=|action=|TODO|debug|admin'
```
- Read **response headers & cookies** → stack fingerprint ([01-recon/fingerprinting.md](../01-recon/fingerprinting.md))
- Read **HTML source + comments** → [02-info-leak/source-comments.md](../02-info-leak/source-comments.md)
- Read **every JS file** → [02-info-leak/js-secrets.md](../02-info-leak/js-secrets.md)

## 4. Cheap known files (10 seconds)
```bash
for p in robots.txt sitemap.xml .git/HEAD .env backup/ admin/ debug/ api/ static/ \
         .DS_Store server-status phpinfo.php crash error; do
  printf '%-16s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code} %{size_download}' $T/$p)"; done
```
Or the script: `python scripts/recon/quick_probe.py $T`

## 5. Content discovery
```bash
ffuf -u $T/FUZZ -w wordlists/web/aev-paths.txt -mc all -fc 404
ffuf -u $T/FUZZ -w wordlists/web/common.txt -e .bak,.old,.txt,.php,.zip -mc all -fc 404
```
→ [tools/ffuf.md](../tools/ffuf.md), [01-recon/content-discovery.md](../01-recon/content-discovery.md)

## 6. Use the app like a user (with a proxy)
Burp/ZAP on, click everything, submit every form, log in with given creds. Note:
- every **input** (query, form, JSON, header, cookie, upload, URL path segment)
- every **state carrier** (cookie, hidden field, token in URL, JWT)
- every **"bot"/background feature** (link checker, report viewer, scheduler) — these are attack gadgets

## 7. Decide the class
Go to [02-what-vuln-is-it.md](02-what-vuln-is-it.md) with what you saw.
