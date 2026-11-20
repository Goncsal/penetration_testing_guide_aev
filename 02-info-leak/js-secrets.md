# Secrets & routes in JavaScript

Front-end bundles ship everything the browser needs — including admin ids, API routes, feature
flags, keys, and the client-side "security" logic.

```bash
# list scripts on a page
curl -s $T | grep -oE '<script[^>]+src="[^"]+"' | grep -oE 'src="[^"]+"'
# grep a bundle for interesting stuff
curl -s $T/static/app.js | grep -oE '/api/[A-Za-z0-9_/{}.-]+|[A-Z_]{3,}\s*[=:]\s*["0-9][^,;]*|token|secret|admin|debug|flag\{[^}]*\}'
# pretty-print a minified bundle
curl -s $T/main.js | npx js-beautify | less
```

Look for:
- Constants like `ADMIN_PROFILE_ID = 7`, `ROLE = 'admin'` → [idor](../04-access-control/idor.md)
- Hidden routes (`/score-board` in Juice Shop, `/api/internal/...`)
- Client-side checks (`if (user.role === 'admin') showPanel()`) → call the API directly
- Source maps: `curl -s $T/main.js.map` → original source with comments
- Helper functions you can call from XSS (`grant()`, `share()`, `report()`) → [07-xss](../07-xss-client-side/README.md)
- DOM sinks (`innerHTML`, `document.write`, `eval`, `location.hash`) → [dom xss](../07-xss-client-side/dom.md)

Seen in: `leak5` (admin id in `/static/app.js`), `juiceshop` (score board route in bundle),
`xss1–3` (`grant()` helper).
