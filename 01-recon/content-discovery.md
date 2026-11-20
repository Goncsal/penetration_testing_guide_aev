# Content discovery (directories & files)

Hidden routes are the #1 infoleak vector: `/debug/env`, `/crash`, `/oracle`, `/export/`,
`/public/`, `/.git/`, `/static/config.py.bak`, `/diagnostics`, `/bot/...`.

## Order of operations

1. **Free hints first**: `robots.txt`, `sitemap.xml`, HTML/JS links → [robots-sitemap](../02-info-leak/robots-sitemap.md), [crawling](crawling.md)
2. **Course list** (small, fast): `wordlists/web/aev-paths.txt`
3. **Generic list**: `wordlists/web/common.txt` then `raft-medium-directories.txt`
4. **Files with extensions / backups** in every directory you found
5. **Recurse** into new directories

## ffuf recipes  (full guide: [tools/ffuf.md](../tools/ffuf.md))

```bash
# 1. course paths, show everything except 404
ffuf -u $T/FUZZ -w wordlists/web/aev-paths.txt -mc all -fc 404

# 2. generic dirs; auto-calibrate to drop "soft 404" pages
ffuf -u $T/FUZZ -w wordlists/web/common.txt -mc all -fc 404 -ac

# 3. files with extensions
ffuf -u $T/FUZZ -w wordlists/web/raft-small-files.txt -mc all -fc 404 -ac

# 4. backups of a known file (static/config.py → config.py.bak, config.py~, config.py.old …)
ffuf -u $T/static/config.pyFUZZ -w wordlists/web/backup-suffixes.txt -mc 200
python scripts/recon/backup_hunt.py $T /static/config.py /index.php   # suffixes + .swp/prefix forms

# 5. recursive
ffuf -u $T/FUZZ -w wordlists/web/common.txt -recursion -recursion-depth 2 -mc all -fc 404 -ac

# authenticated (copy your session cookie)
ffuf -u $T/FUZZ -w wordlists/web/common.txt -H 'Cookie: session=...' -mc all -fc 404 -ac
```

## Read the results

| Status | Meaning |
|---|---|
| 200 | exists — open it |
| 301/302 | directory or redirect to login — follow it, note where it goes |
| 401 | HTTP auth → [default-creds](../03-auth/default-creds.md) |
| 403 | exists but blocked → try [access-control bypasses](../04-access-control/forced-browsing.md) |
| 405 | exists, wrong method → try POST/PUT |
| 500 | you made it crash → read it ([verbose-errors](../02-info-leak/verbose-errors.md)) |

Script alternative (no ffuf installed): `python scripts/recon/dirbrute.py $T wordlists/web/aev-paths.txt`
