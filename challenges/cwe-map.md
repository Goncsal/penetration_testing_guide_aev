# CWE → note

| CWE | Name | Note |
|---|---|---|
| 22 | Path traversal | [lfi-path-traversal](../05-injection/lfi-path-traversal.md) |
| 77 / 78 | Command / OS command injection | [cmdi](../05-injection/cmdi.md) |
| 79 | XSS | [07-xss](../07-xss-client-side/README.md) |
| 88 | Argument injection | [argument-injection](../05-injection/argument-injection.md) |
| 89 | SQL injection | [06-sqli](../06-sqli/README.md) |
| 94 / 95 | Code injection / eval | [code-injection](../05-injection/code-injection.md), [ssti](../05-injection/ssti.md) |
| 98 | PHP file inclusion | [lfi-path-traversal](../05-injection/lfi-path-traversal.md) |
| 121 | Stack buffer overflow | [ret2win](../10-pwn/ret2win.md) |
| 200 | Sensitive info exposure | [02-info-leak](../02-info-leak/README.md) |
| 204 | Response discrepancy (user enum) | [user-enumeration](../03-auth/user-enumeration.md) |
| 209 | Error message info | [verbose-errors](../02-info-leak/verbose-errors.md) |
| 256 / 257 | Plaintext / recoverable password storage | [credential-storage](../03-auth/credential-storage.md) |
| 287 | Improper authentication | [03-auth](../03-auth/README.md) |
| 290 / 293 | Spoofing / Referer auth | [trusted-headers](../03-auth/trusted-headers.md) |
| 307 | No rate limiting | [brute-force](../03-auth/brute-force.md) |
| 327 | Broken crypto | [jwt](../03-auth/jwt.md) |
| 330 / 331 | Insufficient randomness/entropy | [predictable-tokens](../03-auth/predictable-tokens.md) |
| 347 | Improper signature verification | [jwt](../03-auth/jwt.md) |
| 352 | CSRF | [csrf](../07-xss-client-side/csrf.md) |
| 384 | Session fixation | [session-fixation](../03-auth/session-fixation.md) |
| 426 | Untrusted search path | [cmdi-path-hijack](../05-injection/cmdi-path-hijack.md) |
| 434 | Unrestricted upload | [file-upload](../05-injection/file-upload.md) |
| 445 / 530 / 538 | Backup/cache files exposed | [backup-files](../02-info-leak/backup-files.md), [exposed-git](../02-info-leak/exposed-git.md) |
| 489 | Active debug code | [debug-endpoints](../02-info-leak/debug-endpoints.md) |
| 502 | Deserialization | [deserialization](../05-injection/deserialization.md) |
| 521 / 1392 | Weak / default credentials | [default-creds](../03-auth/default-creds.md) |
| 522 | Insufficiently protected creds | [credential-storage](../03-auth/credential-storage.md) |
| 548 | Directory listing | [directory-listing](../02-info-leak/directory-listing.md) |
| 598 | Sensitive data in GET/URL | [token-in-url](../03-auth/token-in-url.md) |
| 602 | Client-side enforcement | [client-side-trust](../03-auth/client-side-trust.md) |
| 611 | XXE | [xxe](../05-injection/xxe.md) |
| 613 | Insufficient session expiration | [session-hijack](../03-auth/session-hijack.md) |
| 624 | Executable regex | [code-injection](../05-injection/code-injection.md) |
| 639 | IDOR (user-controlled key) | [idor](../04-access-control/idor.md) |
| 640 | Weak password recovery | [password-reset](../03-auth/password-reset.md) |
| 915 | Mass assignment | [mass-assignment](../04-access-control/mass-assignment.md) |
| 917 | Expression language injection | [code-injection](../05-injection/code-injection.md#expression-languages-cwe-917) |
| 918 | SSRF | [ssrf](../05-injection/ssrf.md) |
| 1104 | Unmaintained third-party components | [06-cve-research](../00-start/06-cve-research.md), [wordpress](../08-vuln-apps/wordpress.md) |
| 1336 | Template injection | [ssti](../05-injection/ssti.md) |
| 1427 | Prompt injection | [prompt-injection](../05-injection/prompt-injection.md) |
