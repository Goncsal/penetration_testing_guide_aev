# Scripts

Generic, argument-driven helpers. Python 3.9+, `pip install -r scripts/requirements.txt`
(only `requests`; `pwntools` for pwn). Every script has `-h`. Placeholders: `FUZZ` or `{}` mark
where payloads go; `-c 'name=value'` sends a cookie.

| Script | Does | Used in |
|---|---|---|
| `lib/flaggrep.py` | find `flag{}` in URL/file/dir/stdin, decoding b64/hex/url/html | everywhere |
| **recon/** | | |
| `quick_probe.py` | headers, comments, forms, + probe known leak paths | [first-10-minutes](../00-start/01-first-10-minutes.md) |
| `crawl.py` | crawl: links, forms+hidden fields, comments, mentioned paths, tokens in URLs | [crawling](../01-recon/crawling.md) |
| `dirbrute.py` | threaded path brute force (ffuf fallback) | [content-discovery](../01-recon/content-discovery.md) |
| `backup_hunt.py` | `.bak`/`~`/`.swp`/`#x#` variants of known files | [backup-files](../02-info-leak/backup-files.md) |
| `robots_follow.py` | fetch every robots/sitemap entry | [robots-sitemap](../02-info-leak/robots-sitemap.md) |
| `dirlist_grab.py` | walk & download a directory listing | [directory-listing](../02-info-leak/directory-listing.md) |
| `bypass_403.py` | 403 bypass mutations/headers/methods | [forced-browsing](../04-access-control/forced-browsing.md) |
| **leak/** | | |
| `prefix_oracle.py` | char-by-char secret from yes/no endpoint | [oracles](../02-info-leak/oracles.md) |
| `idor_enum.py` | iterate ids (with login), grep flags | [idor](../04-access-control/idor.md) |
| **auth/** | | |
| `basic_auth_brute.py`, `basic_b64.py` | HTTP Basic brute / ffuf tokens | [default-creds](../03-auth/default-creds.md) |
| `login_brute.py` | form brute/spray with CSRF + success page check | [brute-force](../03-auth/brute-force.md) |
| `user_enum.py`, `username_gen.py` | username enumeration / candidates from names | [user-enumeration](../03-auth/user-enumeration.md) |
| `mutate.py` | context password candidates | [brute-force](../03-auth/brute-force.md) |
| `jwt_tool_lite.py` | JWT decode / none / crack / sign | [jwt](../03-auth/jwt.md) |
| `token_recipe.py` | guess how a token is derived (hash of user/time) | [predictable-tokens](../03-auth/predictable-tokens.md) |
| `ts_token_brute.py` | brute time-based token after triggering a login | [predictable-tokens](../03-auth/predictable-tokens.md) |
| `session_fixation.py` | fixate sid via bot / sibling vhost | [session-fixation](../03-auth/session-fixation.md) |
| `session_swap.py` | replay sids leaked on a page | [session-hijack](../03-auth/session-hijack.md) |
| **injection/** | | |
| `probe.py` | which interpreter reacts (cmdi/ssti/sqli/traversal/xss) | [05-injection](../05-injection/README.md) |
| `charfilter_probe.py` | which chars/words a filter strips/blocks | [cmdi-filter-bypass](../05-injection/cmdi-filter-bypass.md) |
| `waf_variants.py` | HPP / double-encoding / newline variants | [cmdi-waf-evasion](../05-injection/cmdi-waf-evasion.md) |
| `blind_cmd_time.py` | read a file via time-based blind cmdi | [cmdi-blind-oob](../05-injection/cmdi-blind-oob.md) |
| `ssti_probe.py` | detect engine + RCE | [ssti](../05-injection/ssti.md) |
| `xxe_send.py` | XXE file read (raw + form) | [xxe](../05-injection/xxe.md) |
| `pickle_payload.py` | pickle RCE/file-read blob | [deserialization](../05-injection/deserialization.md) |
| **sqli/** | | |
| `sqli_probe.py` | detect + suggest technique | [detection](../06-sqli/detection.md) |
| `union_dump.py` | column count, reflected col, dump | [union-based](../06-sqli/union-based.md) |
| `error_extract.py` | updatexml/extractvalue paging | [error-based](../06-sqli/error-based.md) |
| `blind_bool.py` | boolean blind (count/marker/text oracle) | [boolean-blind](../06-sqli/boolean-blind.md) |
| `blind_time.py` | time blind (incl. INSERT context) | [time-blind](../06-sqli/time-blind.md) |
| **xss/** | | |
| `catch_server.py` | OOB/XSS/exfil HTTP listener + file server | [oob-listeners](../tools/oob-listeners.md) |
| `xss_reflect.py` | reflection context & surviving chars | [reflected](../07-xss-client-side/reflected.md) |
| **network/** `snmp_walk.py` | pure-Python SNMP walk/get | [snmp](../09-network/snmp.md) |
| **pwn/** `ret2win.py` | pwntools ret2win template | [ret2win](../10-pwn/ret2win.md) |
| **web/** | | |
| `revshell.py` | reverse shell one-liners | [reverse-shells](../11-post-exploitation/reverse-shells.md) |
| `wp_plugin_shell.py` | WordPress webshell plugin zip | [wordpress](../08-vuln-apps/wordpress.md) |
| `wordpress_wp2shell.py` | WP 6.9.4 unauth RCE chain (course CVE) | [wordpress](../08-vuln-apps/wordpress.md) |
| `shells/` | `shell.php`, `shell.phtml` (GIF89a), `revshell.php`, `.htaccess` trick | [file-upload](../05-injection/file-upload.md) |

Run scripts with an explicit path (`python scripts/x/y.py`) from the repo root; wordlist paths in
examples are relative to the repo root.

**Windows Git Bash gotcha:** MSYS rewrites arguments that look like absolute paths
(`/flag/flag` → `C:/Program Files/Git/flag/flag`). Prefix commands with `MSYS_NO_PATHCONV=1`
(e.g. `MSYS_NO_PATHCONV=1 python scripts/injection/pickle_payload.py --read /flag/flag`), or use
WSL / PowerShell / a Linux VM. Antivirus (Windows Defender) may quarantine files containing
webshell payloads (`scripts/web/shells/`, some notes) — restore them from git if they disappear.
