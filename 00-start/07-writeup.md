# Writing it up

Course grading asks *why*, not just the flag: name the **precise class**, the **payload and why it
works**, and the **correct fix**. Template (from the "anatomy of a finding" slides):

```markdown
## <ID> — <short title>            e.g. AUTH-04 — Role taken from a client-writable cookie
Risk: High (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N) — why: any employee becomes manager
Asset: http://auth4.chal.deti:8063 /manager
Weakness: CWE-602 Client-side enforcement of server-side security (OWASP A07)
Evidence:
  1. Login as employee → Set-Cookie: role=employee
  2. GET /manager → 403
  3. Cookie: role=manager → 200 + flag
Impact: what the attacker gains + preconditions
Remediation: store role in the server-side session; never branch on client values
Status / retest: open
```

## Common "precise names" graders look for

| Instead of… | Say |
|---|---|
| "the app is hackable" | OS command injection via unquoted interpolation into `sh -c` (CWE-78) |
| "I logged in as admin" | Authentication bypass via SQLi tautology/comment in the login query (CWE-89) |
| "I changed the URL" | IDOR / broken object-level authorization — authenticated but no ownership check (CWE-639) |
| "blacklist bypass" | Incomplete denylist; newline (`\n`) not filtered → command separator |
| "used a WAF trick" | HTTP Parameter Pollution (WAF reads first value, app reads last) / double URL-encoding |
| "found a file" | Exposed backup (CWE-530/538), directory listing (CWE-548), exposed VCS (CWE-527) |
| "decoded the token" | Sensitive data in JWT payload — encoded, not encrypted (CWE-200) |

## Fix vocabulary (what the decks recommend)

- Injection: **don't use a shell** (argument arrays), allowlist input shape, escape as last layer;
  parameterised queries for SQL; safe loaders (`yaml.safe_load`, JSON) for deserialization; disable
  DTDs for XML; scheme/host allowlist for URL fetchers; render user text as data, not templates.
- Auth: slow salted hashes (Argon2id/bcrypt), rate limiting (progressive delay), MFA, generic error
  messages, random ≥128-bit session ids from a CSPRNG, regenerate id on login, server-side logout,
  `Secure; HttpOnly; SameSite`, pin JWT algorithm and use long random secrets.
- Leaks: remove debug artefacts, disable listing, don't serve `.git`/backups, generic errors.
- XSS: context-aware output encoding, CSP, `HttpOnly` cookies, CSRF tokens / SameSite.
