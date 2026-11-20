# Session / access token in the URL (CWE-598)

**Signs**: links like `/track?sid=…`, `/doc?token=…`, `;jsessionid=…`, `/share/<id>`; "no account
needed, use your personal link"; hint "a link meant for one", "one line too many".

URLs leak everywhere: browser history, **Referer** headers, proxy/server logs, analytics, chat
messages, screenshots, public pages where someone pasted them.

## Exploit
1. Get your own link and confirm it shows **your** (unprivileged) data.
2. Hunt for other people's links in public content:
```bash
python scripts/recon/crawl.py $T | grep -E 'sid=|token=|key=|session='
curl -s $T/stories $T/testimonials $T/blog $T/forum $T/logs | grep -oE '[?&](sid|token|key)=[A-Za-z0-9_-]+'
```
   Also: `/server-status`, debug/log pages, `.git` history, JS, error pages, Referer logs.
3. Replay each leaked token; the privileged one shows the flag.
4. If ids look sequential/short → [predictable-tokens](predictable-tokens.md) / [idor](../04-access-control/idor.md).

Seen in: `auth3` (QuickShip: VIP customer's full tracking link quoted on public `/stories` page).
