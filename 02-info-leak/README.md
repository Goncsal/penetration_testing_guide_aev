# 02 — Information leakage

The app hands you the secret if you look in the right place. Check in this order (cheapest first):

| # | Check | One-liner | Note |
|---|---|---|---|
| 1 | HTML source & comments | `curl -s $T \| grep -o '<!--.*-->'` | [source-comments](source-comments.md) |
| 2 | robots.txt / sitemap | `curl -s $T/robots.txt` | [robots-sitemap](robots-sitemap.md) |
| 3 | JS files | `curl -s $T/static/app.js` | [js-secrets](js-secrets.md) |
| 4 | Directory listing | `curl -s $T/static/ $T/public/ $T/uploads/` | [directory-listing](directory-listing.md) |
| 5 | Exposed `.git` | `curl -s $T/.git/HEAD` | [exposed-git](exposed-git.md) |
| 6 | Backup / editor files | `curl -s $T/index.php.bak` | [backup-files](backup-files.md) |
| 7 | Debug / admin routes | `ffuf ... aev-paths.txt` | [debug-endpoints](debug-endpoints.md) |
| 8 | Make it crash | `curl -s "$T/item?id='"` | [verbose-errors](verbose-errors.md) |
| 9 | Tokens/cookies carry data | decode `eyJ...` | [jwt](../03-auth/jwt.md#1-decode-it-always-first) |
| 10 | Objects by id | `/api/users/1..50` | [idor](../04-access-control/idor.md) |
| 11 | Yes/no answers | `/oracle?prefix=f` | [oracles](oracles.md) |
| 12 | Account existence | login error differences | [user-enumeration](../03-auth/user-enumeration.md) |

Fast automated pass over 1–8: `python scripts/recon/quick_probe.py $T`

Course map: leak1 backup · leak2 debug route · leak3 dir listing · leak4 .git · leak5 IDOR+verbose ·
leak6 JWT payload · leak7 prefix oracle · leak8 robots · leak9 HTML comment · leak10 stack trace.
