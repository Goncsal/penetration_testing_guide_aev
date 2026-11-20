# Known course challenges → notes

Use this to (a) practise on known challenges with the local docker setup, and (b) recognise the
same pattern in new ones. Lab host = `<name>.chal.deti`; local = `127.0.0.1:<port>`.

## auth
| Chall | Port | Title | Vulnerability | Note |
|---|---|---|---|---|
| auth1 | 8060 | NetGuard Router | Basic auth default creds | [default-creds](../03-auth/default-creds.md) |
| auth2 | 8061 | Harbor Wiki | Referer-based access control | [trusted-headers](../03-auth/trusted-headers.md) |
| auth3 | 8062 | QuickShip Tracker | sid in URL leaked on public page | [token-in-url](../03-auth/token-in-url.md) |
| auth4 | 8063 | ExpenseFlow | role cookie trusted | [client-side-trust](../03-auth/client-side-trust.md) |
| auth5 | 8064 | Alma Portal | session fixation via bot | [session-fixation](../03-auth/session-fixation.md) |
| auth6 | 8065 | Brightleaf | cross-subdomain cookie fixation | [session-fixation](../03-auth/session-fixation.md#cross-domain-cookie) |
| auth7 | 8066 | ConnectAPI | JWT `alg:none` | [jwt](../03-auth/jwt.md) |
| auth8 | 8067 | PocketBank Lite | JWT 4-digit HMAC secret | [jwt](../03-auth/jwt.md) |
| auth9 | 8068 | DeskHero | timestamp-based token | [predictable-tokens](../03-auth/predictable-tokens.md) |
| auth10 | 8069 | PeopleFirst HR | user enumeration + default pw | [user-enumeration](../03-auth/user-enumeration.md) |
| auth11 | 8070 | InboxNow | deterministic reset token | [password-reset](../03-auth/password-reset.md) |
| auth12 | 8071 | Cornerstone CMS | robots → listing → base64 pw dump | [credential-storage](../03-auth/credential-storage.md) |
| auth13 | 8072 | RemoteLink VPN | no rate limit, weak pw | [brute-force](../03-auth/brute-force.md) |
| auth14 | 8073 | FernBank | logout not server-side + sid in diagnostics | [session-hijack](../03-auth/session-hijack.md) |

## infoleak
| Chall | Port | Vulnerability | Note |
|---|---|---|---|
| leak1 | 8010 | editor backup `config.py.bak` | [backup-files](../02-info-leak/backup-files.md) |
| leak2 | 8011 | hidden `/debug/env` | [debug-endpoints](../02-info-leak/debug-endpoints.md) |
| leak3 | 8012 | directory listing `/public/` | [directory-listing](../02-info-leak/directory-listing.md) |
| leak4 | 8013 | exposed `.git` (commit msg) | [exposed-git](../02-info-leak/exposed-git.md) |
| leak5 | 8014 | IDOR + `?verbose=true` | [idor](../04-access-control/idor.md) |
| leak6 | 8015 | flag in JWT payload | [jwt](../03-auth/jwt.md) |
| leak7 | 8016 | prefix oracle | [oracles](../02-info-leak/oracles.md) |
| leak8 | 8017 | robots.txt Disallow | [robots-sitemap](../02-info-leak/robots-sitemap.md) |
| leak9 | 8018 | HTML comment | [source-comments](../02-info-leak/source-comments.md) |
| leak10 | 8019 | stack trace on `/crash` | [verbose-errors](../02-info-leak/verbose-errors.md) |

## inj
| Chall | Port | Title | Vulnerability | Note |
|---|---|---|---|---|
| inj1 | 8040 | LibraryNet | ping `;` cmdi | [cmdi](../05-injection/cmdi.md) |
| inj2 | 8041 | ShelfTag | denylist misses newline | [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md) |
| inj3 | 8042 | OpsBoard | Jinja2 SSTI | [ssti](../05-injection/ssti.md) |
| inj4 | 8043 | Catalogo | XXE (Java) | [xxe](../05-injection/xxe.md) |
| inj5 | 8044 | NightPack | tar dir arg `;` | [cmdi](../05-injection/cmdi.md) |
| inj6 | 8045 | CardCraft | EJS SSTI | [ssti](../05-injection/ssti.md) |
| inj7 | 8046 | DeskOne | `$()` into log file | [cmdi-blind-oob](../05-injection/cmdi-blind-oob.md) |
| inj8 | 8047 | StockEye | glob `/flag/*` | [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md) |
| inj9 | 8048 | PicLink | SSRF `file://` | [ssrf](../05-injection/ssrf.md) |
| inj10 | 8049 | ToolDesk | PATH hijack via plugin | [cmdi-path-hijack](../05-injection/cmdi-path-hijack.md) |
| inj11 | 8050 | LogWarden | second-order cmdi | [cmdi-second-order](../05-injection/cmdi-second-order.md) |
| inj12 | 8051 | SessionVault | pickle deserialization | [deserialization](../05-injection/deserialization.md) |
| inj13 | 8052 | FaaSDeck | exec API + `flag` word filter | [cmdi](../05-injection/cmdi.md#exec-apis--function-platforms) |
| inj14 | 8053 | GateKeeper | WAF: HPP / double encoding | [cmdi-waf-evasion](../05-injection/cmdi-waf-evasion.md) |

## sqli
| Chall | Port | Title | DB | Technique | Note |
|---|---|---|---|---|---|
| sqli1 | 8030 | Staff Portal | SQLite | login bypass | [auth-bypass](../06-sqli/auth-bypass.md) |
| sqli2 | 8031 | TechBazaar | MariaDB | error (`updatexml`) | [error-based](../06-sqli/error-based.md) |
| sqli3 | 8032 | PhotoVault | SQLite | UNION (4 cols) | [union-based](../06-sqli/union-based.md) |
| sqli4 | 8033 | DropLite | SQLite | boolean (count) | [boolean-blind](../06-sqli/boolean-blind.md) |
| sqli5 | 8034 | Daily Byte | SQLite | boolean (marker row) | [boolean-blind](../06-sqli/boolean-blind.md) |
| sqli6 | 8035 | Guestbook | MariaDB | time-based in INSERT | [time-blind](../06-sqli/time-blind.md) |
| sqli7 | 8036 | Linkly | SQLite | UNION → app fetches URL (OOB) | [out-of-band](../06-sqli/out-of-band.md) |
| sqli8 | 8037 | TransferOps | MariaDB | table name → INTO OUTFILE | [file-read-write](../06-sqli/file-read-write.md) |

## web / network / pwn
| Chall | Port | Vulnerability | Note |
|---|---|---|---|
| notes1 | 8020 | IDOR (`/note/<id>`) | [idor](../04-access-control/idor.md) |
| xss1 | 8021 | reflected XSS → `grant()` | [reflected](../07-xss-client-side/reflected.md) |
| xss2 | 8022 | stored XSS → `grant()` | [stored](../07-xss-client-side/stored.md) |
| xss3 | 8023 | DOM XSS (`innerHTML`) → `grant()` | [dom](../07-xss-client-side/dom.md) |
| bwapp | 8081 | many exercises | [bwapp](../08-vuln-apps/bwapp.md) |
| dvwa | 8082 | many exercises | [dvwa](../08-vuln-apps/dvwa.md) |
| mutillidae | 8083 | many labs | [mutillidae](../08-vuln-apps/mutillidae.md) |
| wordpress | 8084 | WP 6.9.4 wp2shell CVE chain | [wordpress](../08-vuln-apps/wordpress.md) |
| juiceshop | 3000 | many challenges | [juiceshop](../08-vuln-apps/juiceshop.md) |
| snmp1 | 8024/udp | SNMP `public` walk | [snmp](../09-network/snmp.md) |
| pwn1 | 9001 | ret2win (offset 72) | [ret2win](../10-pwn/ret2win.md) |

Generic solvers in [scripts/](../scripts/README.md) take the target URL, so they work on these and
on variants (different paths/params) with flags changed.
