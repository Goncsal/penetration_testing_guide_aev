# 07 — XSS & client-side attacks

XSS = your HTML/JS runs in **someone else's browser** on the target origin. In CTFs the "someone"
is either you (flag gated by something only page JS can do) or a **bot/admin** that visits pages.

## Which kind?
| Your input… | Type | Note |
|---|---|---|
| appears in the **server response** of the same request (`?q=`) | Reflected | [reflected](reflected.md) |
| is **saved** and shown to others later (notes, comments, profile) | Stored | [stored](stored.md) |
| is **not** in the server response, but JS puts it in the page (`innerHTML`, `location.hash`) | DOM | [dom](dom.md) |

Check: `curl -s "$T/?q=ZZTEST123" | grep -c ZZTEST123` → >0 reflected/stored; 0 but visible in
browser → DOM.

## How do I turn XSS into a flag?
1. **A helper on the page sets a grant cookie / calls `/flag`** (course xss1–3: `grant()`):
   payload `<img src=x onerror=grant()>` → open in your browser → you get redirected to `/flag`.
   Read the page JS for such helpers ([js-secrets](../02-info-leak/js-secrets.md)).
2. **An admin bot visits** → steal its cookie / make it fetch an admin page and send it to you
   → [cookie-theft](cookie-theft.md).
3. **Make the victim perform an action** (change email/role) → [csrf](csrf.md).

Payload list & filter bypasses: [payloads](payloads.md). Same-origin & CORS: [cors](cors.md).

**Is it really XSS?** If `{{7*7}}` renders `49` the server evaluated it → [SSTI](../05-injection/ssti.md) (RCE!).
