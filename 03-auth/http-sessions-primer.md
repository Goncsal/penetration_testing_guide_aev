# HTTP, cookies & sessions — primer

- HTTP is **stateless**; state rides in the URL, body (hidden fields), headers (`Cookie`,
  `Authorization`) or a token. Whoever presents the token *is* the user.
- **Basic auth**: `Authorization: Basic base64(user:pass)` — encoding, not encryption; resent on
  every request; no logout.
- **Digest**: hash challenge/response (MD5); rare today.
- **Cookie**: `Set-Cookie: NAME=VALUE; Domain; Path; Expires/Max-Age; Secure; HttpOnly; SameSite`.
  - `Domain=.site.com` → every subdomain receives (and can set) it.
  - no `HttpOnly` → readable by JS → stealable by XSS.
  - no `Secure` → sent over plain HTTP.
- **Opaque session id** → server-side store (revocable). **Self-contained token (JWT)** → state
  inside the token (signed, *not* encrypted).
- **JWT** = `b64url(header).b64url(payload).b64url(sig)`, `sig = HMAC(secret, h.p)` or RSA/ECDSA.
- **401** = not authenticated; **403** = authenticated but not allowed.

## Manipulating state

```bash
curl -i -c jar.txt -b jar.txt -d 'user=a&pass=b' $T/login     # keep cookies across requests
curl -s -b 'role=admin; sid=abc' $T/manager                    # send arbitrary cookies
curl -s -H 'Authorization: Bearer eyJ...' $T/api/admin
curl -s -u admin:admin $T/admin                                # Basic auth
```
Browser: DevTools → Application → Cookies (edit value), or Burp Repeater. Python:
`requests.Session()` keeps cookies; to **replace** one, use `cookies={'sid': x}` on a fresh
request (a session jar may keep its own value).

Testing tools from the deck: Burp (Intruder, Sequencer for token randomness), Hydra, ffuf, jwt_tool.
