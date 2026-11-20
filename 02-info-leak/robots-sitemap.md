# robots.txt & sitemap.xml

`robots.txt` is a *courtesy for crawlers*, not access control — devs list exactly what they
want hidden.

```bash
curl -s $T/robots.txt
curl -s $T/sitemap.xml
curl -s $T/.well-known/security.txt
```

Follow every `Disallow:` / `Allow:` path (and its directory listing):
```bash
python scripts/recon/robots_follow.py $T          # fetches each entry, prints status + flag matches
```

If a disallowed path is a directory → [directory-listing](directory-listing.md) /
[content-discovery](../01-recon/content-discovery.md) inside it.

Seen in:
- `leak8` — `Disallow:` path holds the flag directly.
- `auth12` — `Disallow: /export/` → listing → `cornerstone_staging.sql.bak` → base64 admin password
  ([credential-storage](../03-auth/credential-storage.md)).
