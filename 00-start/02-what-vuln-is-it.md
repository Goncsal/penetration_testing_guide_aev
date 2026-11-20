# What vulnerability is it? (symptom → class)

Match what you observe to the most likely class, then follow the link. Several can apply — try the
cheapest first.

## By what the app *does*

| You see… | Most likely | Go to |
|---|---|---|
| Field that takes a host/IP, "ping", "check node", "traceroute", "nslookup" | OS command injection | [cmdi](../05-injection/cmdi.md) |
| Field that takes a file/dir name for backup/archive/audit/list/log | OS cmd / argument injection | [cmdi](../05-injection/cmdi.md), [argument-injection](../05-injection/argument-injection.md) |
| "Sanitized"/"filtered"/"WAF" mentioned, `403 blocked` on `;` | Filter/WAF bypass | [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md), [cmdi-waf-evasion](../05-injection/cmdi-waf-evasion.md) |
| You **save** a setting, and *another* button runs/ships/processes it | Second-order injection | [cmdi-second-order](../05-injection/cmdi-second-order.md) |
| Upload a script/plugin/tool + "run tool X" | PATH hijack / command override | [cmdi-path-hijack](../05-injection/cmdi-path-hijack.md) |
| Output not shown, but written to a log/ledger page you can read | Blind cmdi → read the log | [cmdi-blind-oob](../05-injection/cmdi-blind-oob.md) |
| "Template", "design", "header", "greeting", `{{ }}` / `<% %>` / `${}` | SSTI | [ssti](../05-injection/ssti.md) |
| Imports **XML** (catalogue, SOAP, SVG, DOCX, RSS) | XXE | [xxe](../05-injection/xxe.md) |
| Fetches a **URL** for you (preview, image proxy, webhook, "check link") | SSRF / `file://` | [ssrf](../05-injection/ssrf.md) |
| Restores a "session"/"workspace"/base64 blob (`gASV`, `rO0AB`, `O:4:`) | Insecure deserialization | [deserialization](../05-injection/deserialization.md) |
| `?page=`, `?file=`, `?lang=`, `?template=` loads files | LFI / path traversal | [lfi-path-traversal](../05-injection/lfi-path-traversal.md) |
| File upload (avatar, attachment, plugin, theme) | Upload → webshell | [file-upload](../05-injection/file-upload.md) |
| Old CGI (`/cgi-bin/*.sh`, `.cgi`), Apache + bash | Shellshock | [shellshock](../05-injection/shellshock.md) |
| Search / filter / numeric id / login backed by a DB | SQL injection | [06-sqli](../06-sqli/README.md) |
| Input echoed back in the page | Reflected XSS (or SSTI if `{{7*7}}` → 49!) | [07-xss](../07-xss-client-side/README.md) |
| Notes/comments/guestbook shown to others | Stored XSS (or stored SQLi/cmdi) | [stored](../07-xss-client-side/stored.md) |
| URL param / `#fragment` read by JS, not in server HTML | DOM XSS | [dom](../07-xss-client-side/dom.md) |
| `/flag` needs a cookie that a page JS helper (`grant()`, "share") sets | XSS that calls that helper | [07-xss](../07-xss-client-side/README.md) |

## By what the *auth/session* looks like

| You see… | Most likely | Go to |
|---|---|---|
| Browser login popup (401 + `WWW-Authenticate: Basic`) | Default / weak creds | [default-creds](../03-auth/default-creds.md) |
| Known username, password not given, no lockout | Dictionary attack | [brute-force](../03-auth/brute-force.md) |
| Different errors for "no such user" vs "wrong password" | User enumeration | [user-enumeration](../03-auth/user-enumeration.md) |
| Cookie like `role=user`, `admin=0`, `isAdmin=false`, hidden form field | Client-side trust | [client-side-trust](../03-auth/client-side-trust.md) |
| "Staff only — come from page X"; checks Referer / X-Forwarded-For / UA | Trusted headers | [trusted-headers](../03-auth/trusted-headers.md) |
| Token / `sid` / `session` in the URL | Token leakage via URL | [token-in-url](../03-auth/token-in-url.md) |
| `eyJ...` token (3 dot-separated parts) | JWT: decode / none / weak secret | [jwt](../03-auth/jwt.md) |
| Session id = hex hash (32/40/64 chars), maybe time-based | Predictable token | [predictable-tokens](../03-auth/predictable-tokens.md) |
| "Forgot password" / reset link | Reset token flaws | [password-reset](../03-auth/password-reset.md) |
| Cookie set **before** login, same after; a "bot" logs in for you | Session fixation | [session-fixation](../03-auth/session-fixation.md) |
| Subdomain/microsite sharing a parent-domain cookie | Cookie-scope fixation | [session-fixation](../03-auth/session-fixation.md#cross-domain-cookie) |
| Session ids visible in a debug/log page; "logout" exists | Session not invalidated / hijack | [session-hijack](../03-auth/session-hijack.md) |
| "encrypted" password in a dump ending with `=` | Base64 ≠ encryption | [credential-storage](../03-auth/credential-storage.md) |

## By what *leaks*

| You see… | Most likely | Go to |
|---|---|---|
| Nothing obvious at all | Comment / robots / backup / `.git` | [02-info-leak](../02-info-leak/README.md) |
| `Index of /…` | Directory listing | [directory-listing](../02-info-leak/directory-listing.md) |
| Stack trace / 500 page with code | Verbose errors | [verbose-errors](../02-info-leak/verbose-errors.md) |
| `/note/3`, `/api/users/12`, `?id=5` | IDOR | [idor](../04-access-control/idor.md) |
| Endpoint answers only yes/no (200/404) to a guess | Oracle → char-by-char | [oracles](../02-info-leak/oracles.md) |
| Known product (WordPress, Joomla, phpMyAdmin, Tomcat…) | Version → CVE | [06-cve-research](06-cve-research.md), [08-vuln-apps](../08-vuln-apps/README.md) |

## By transport

| Target | Go to |
|---|---|
| UDP 161 / "community" / "walk" | [snmp](../09-network/snmp.md) |
| `nc host port` + a binary | [10-pwn](../10-pwn/README.md) |
| SSH/FTP/SMTP/other banner | [09-network](../09-network/README.md) |
