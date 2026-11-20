# Backup & editor leftovers

**Signs**: hint "dusty twin", "the second one"; you know a source/config filename (from errors,
listings, JS, `.git`); static dir serves files raw.

Editors and admins leave copies that the server serves as **plain text** (no execution):

| Pattern | Origin |
|---|---|
| `file.bak` `file.old` `file.orig` `file.save` `file.tmp` `file.copy` `file1` | manual copies |
| `file~` | emacs/gedit |
| `.file.swp` `.file.swo` | vim swap (use `vim -r` to recover) |
| `#file#` | emacs autosave |
| `file.zip` `file.tar.gz` `site.tar.gz` `backup.sql` `db.sql.bak` `dump.sql` | archives / DB dumps |
| `config.php.bak`, `settings.py.bak`, `.env.bak`, `web.config.old` | configs with secrets |

## Hunt
```bash
# suffix fuzz on a known file
ffuf -u $T/static/config.pyFUZZ -w wordlists/web/backup-suffixes.txt -mc 200
# all forms (suffix, .swp prefix, #file#) for several files at once
python scripts/recon/backup_hunt.py $T /static/config.py /app.py /index.php /config.php
# generic backup file names in each directory
ffuf -u $T/FUZZ -w wordlists/web/backup-files.txt -mc 200
```
Guess filenames from the stack: Flask → `app.py`, `config.py`, `settings.py`; PHP → `index.php`,
`config.php`, `wp-config.php`; Node → `server.js`, `app.js`, `.env`, `package.json`.

## Then
- Read secrets (DB creds, `SECRET_KEY` → forge Flask cookies with `flask-unsign`, JWT secret →
  [jwt](../03-auth/jwt.md), admin passwords → log in).
- `.sql` dumps: look for `INSERT INTO users` rows → crack/decode → [credential-storage](../03-auth/credential-storage.md).

Seen in: `leak1` (`/static/config.py.bak`), `auth12` (`/export/cornerstone_staging.sql.bak`).
