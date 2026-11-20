# Directory listing

**Signs**: a directory URL returns `Index of /…` or a list of `<a href>` file links; hint "open
shelving", "drawers ajar".

```bash
for d in public static uploads files backup backups export exports files data logs tmp assets media; do
  curl -s $T/$d/ | grep -qi 'index of\|<a href' && echo "LISTING: /$d/"; done
```
Then download everything listed and grep:
```bash
python scripts/recon/dirlist_grab.py $T/public/      # follows listing links (recursive), greps flag{
wget -r -np -nH -q $T/public/ && grep -rI 'flag{' .  # wget alternative
```

Tips:
- The flag is often **not** in the obviously named file — fetch them all.
- Listings show neighbours: `.htaccess`, `README.txt`, `*.bak`, `*.sql` → [backup-files](backup-files.md).
- nginx `autoindex`, Apache `Options +Indexes`, Python `http.server` all look different; check
  the raw HTML for links.

Seen in: `leak3` (`/public/` listing, flag in one of several files), `auth12` (`/export/`).
