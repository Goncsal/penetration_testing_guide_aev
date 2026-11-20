# Reading the challenge hint

Course challenges ship a 3-line haiku + a title. Names are neutral (`auth7`, `leak5`) on purpose —
the **hint is the real signal**. Keyword map:

| Hint words | Means | Note |
|---|---|---|
| "door", "basic word", "never changed since birth" | default creds (HTTP Basic) | [default-creds](../03-auth/default-creds.md) |
| "who sent you", "trusts whatever you say" | Referer / header trust | [trusted-headers](../03-auth/trusted-headers.md) |
| "a link meant for one", "one line too many" | token leaked in a public URL | [token-in-url](../03-auth/token-in-url.md) |
| "your browser alone decides", "edit the lock's note" | client-side cookie/field | [client-side-trust](../03-auth/client-side-trust.md) |
| "hand them a hallway before they sign in" | session fixation | [session-fixation](../03-auth/session-fixation.md) |
| "two houses one key", "cut too wide" | cookie Domain scope | [session-fixation](../03-auth/session-fixation.md#cross-domain-cookie) |
| "picks its own lock", "say none" | JWT `alg:none` | [jwt](../03-auth/jwt.md) |
| "four digits", "small enough to try every one" | brute-forceable secret | [jwt](../03-auth/jwt.md), [brute-force](../03-auth/brute-force.md) |
| "minted from a clock", "a second's width" | timestamp-derived token | [predictable-tokens](../03-auth/predictable-tokens.md) |
| "wrong name gets a no" | user enumeration | [user-enumeration](../03-auth/user-enumeration.md) |
| "same key cut twice", "no clock", "never wears out" | deterministic reset token | [password-reset](../03-auth/password-reset.md) |
| "wrapped twice but never sealed" | base64 posing as encryption | [credential-storage](../03-auth/credential-storage.md) |
| "try the door all night", "Dictionary" | no rate limit → wordlist | [brute-force](../03-auth/brute-force.md) |
| "goodbye at the door, yet the key still turns" | logout doesn't kill server session | [session-hijack](../03-auth/session-hijack.md) |
| "dusty twin", "look for the second" | backup file (`.bak`, `~`, `.swp`) | [backup-files](../02-info-leak/backup-files.md) |
| "make it stumble", "spill its insides" | verbose error | [verbose-errors](../02-info-leak/verbose-errors.md) |
| "back room", "machine confesses" | hidden debug route | [debug-endpoints](../02-info-leak/debug-endpoints.md) |
| "open shelving", "drawer left ajar" | directory listing | [directory-listing](../02-info-leak/directory-listing.md) |
| "all the changes kept", "read the old pages" | exposed `.git` | [exposed-git](../02-info-leak/exposed-git.md) |
| "profiles in a row", "count them, then ask more" | IDOR + verbose/hidden field | [idor](../04-access-control/idor.md) |
| "the badge you carry", "peel back the layers" | decode JWT/cookie | [jwt](../03-auth/jwt.md) |
| "it only says yes", "one letter, then another" | oracle | [oracles](../02-info-leak/oracles.md) |
| "crawlers must obey" | robots.txt | [robots-sitemap](../02-info-leak/robots-sitemap.md) |
| "read between the lines", "private thoughts" | HTML comment | [source-comments](../02-info-leak/source-comments.md) |
| "answer comes from deeper", "one word splits the line" | command injection (`;`) | [cmdi](../05-injection/cmdi.md) |
| "the second line is yours", "takes a breath" | newline injection | [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md) |
| "page obeys your marks", "the design keeps the house" | SSTI | [ssti](../05-injection/ssti.md) |
| "reader trusts all doors", "open the outside one" | XXE | [xxe](../05-injection/xxe.md) |
| "the star shows more" | glob `*` bypass | [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md) |
| "writes it down… even the ones that act" | cmdi output lands in a log | [cmdi-blind-oob](../05-injection/cmdi-blind-oob.md) |
| "courier checks no papers", "any road" | SSRF / `file://` | [ssrf](../05-injection/ssrf.md) |
| "first name it finds wins", "lend its path" | PATH hijack | [cmdi-path-hijack](../05-injection/cmdi-path-hijack.md) |
| "the form only stores it, the shipper runs it" | second-order | [cmdi-second-order](../05-injection/cmdi-second-order.md) |
| "what it carries is not data" | deserialization | [deserialization](../05-injection/deserialization.md) |
| "two readers, one request" | HPP / double encoding | [cmdi-waf-evasion](../05-injection/cmdi-waf-evasion.md) |
| "says isolated… one uid" | exec API / function body is a shell | [cmdi](../05-injection/cmdi.md#exec-apis--function-platforms) |
| "One wrong line and it swings wide" | SQLi login bypass | [auth-bypass](../06-sqli/auth-bypass.md) |
| "the shelves talk when ruffled" | error-based SQLi | [error-based](../06-sqli/error-based.md) |
| "count the columns" | UNION SQLi | [union-based](../06-sqli/union-based.md) |
| "ask, then count the answers" | boolean blind (count oracle) | [boolean-blind](../06-sqli/boolean-blind.md) |
| "some lines appear, some don't" | boolean blind (row oracle) | [boolean-blind](../06-sqli/boolean-blind.md) |
| "measure the silence", "takes longer" | time-based blind | [time-blind](../06-sqli/time-blind.md) |
| "we fetch the link… send it somewhere you can see" | SQLi + out-of-band | [out-of-band](../06-sqli/out-of-band.md) |
| "it writes whatever you name", "rows kept out" | `INTO OUTFILE` / table-name injection | [file-read-write](../06-sqli/file-read-write.md) |
| "repeats what you type" / "written once, read by all" / "your browser does the rest" | reflected / stored / DOM XSS | [07-xss](../07-xss-client-side/README.md) |
| "some doors belong to others, try them anyway" | IDOR | [idor](../04-access-control/idor.md) |
| "a port that talks", "walk it" | SNMP walk | [snmp](../09-network/snmp.md) |
| "will not count the letters", "say something long" | buffer overflow | [ret2win](../10-pwn/ret2win.md) |
| "has not seen a patch in many moons" | outdated software → CVE | [06-cve-research](06-cve-research.md) |

**CWE given?** Look it up in [challenges/cwe-map.md](../challenges/cwe-map.md).
