# 03 — Authentication & session failures (OWASP A07)

Identification (who you claim), authentication (proof), session management (how the proof is
remembered). Break any one → act as someone else. **There is no client-side security model**:
anything the client sends (headers, cookies, hidden fields, tokens) can be forged.

## Triage — answer these in order

1. **How do I log in?** Browser popup (Basic) → [default-creds](default-creds.md). Form → continue.
2. **Do I have creds?** No → [default-creds](default-creds.md), [user-enumeration](user-enumeration.md), [brute-force](brute-force.md), [SQLi bypass](../06-sqli/auth-bypass.md).
3. **What carries state after login?** Inspect `Set-Cookie`, URL, hidden fields, `Authorization`:
   - readable value (`role=`, `user=`, `admin=`) → [client-side-trust](client-side-trust.md)
   - `eyJ…` → [jwt](jwt.md)
   - hex/hash id → [predictable-tokens](predictable-tokens.md)
   - id in URL → [token-in-url](token-in-url.md)
   - Flask `session=eyJ…` / Express `s%3A…` → [client-side-trust](client-side-trust.md#signed-framework-cookies)
4. **Is the "protected" page protected by something I control?** Referer/XFF/UA → [trusted-headers](trusted-headers.md)
5. **Is there a privileged actor I can influence?** ("bot", "link checker", "probe", "admin reviews")
   → [session-fixation](session-fixation.md), [session-hijack](session-hijack.md), [stored XSS](../07-xss-client-side/stored.md)
6. **Recovery flow?** → [password-reset](password-reset.md)
7. **Credential dump found?** → [credential-storage](credential-storage.md)

Background: [http-sessions-primer](http-sessions-primer.md)

## Course map
auth1 default Basic creds · auth2 Referer · auth3 token in URL leaked in public page · auth4 role
cookie · auth5 session fixation via bot · auth6 cookie-scope fixation (vhost) · auth7 JWT none ·
auth8 JWT weak HMAC · auth9 timestamp token · auth10 user enum + default pw · auth11 predictable reset
token · auth12 base64 password in exposed dump · auth13 no rate limit · auth14 logout doesn't
invalidate + leaked sid
