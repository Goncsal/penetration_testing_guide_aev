# Crawling & reading the app

Before fuzzing, collect every link, form, script and comment the app already gives you.

```bash
python scripts/recon/crawl.py $T                 # same-origin crawl: links, forms, scripts, comments, flags
python scripts/recon/crawl.py $T -c 'session=...' # authenticated
```
The crawler prints:
- every URL + status,
- every `<form>` (method, action, input names, **hidden values**),
- every HTML comment,
- every `flag{` match.

Manual equivalents:
```bash
curl -s $T | grep -oE '(href|src|action)="[^"]+"' | sort -u
curl -s $T | grep -oE '<!--.*?-->'
curl -s $T | grep -iE '<input[^>]+type="?hidden'
```

## Things to note while browsing
- Text that **mentions a path but doesn't link it** (e.g. `<code>/wiki/internal/ops-runbook</code>`) — `auth2`.
- Footers with emails/usernames (`postmaster@...`) — `auth11`.
- Team/staff lists → username format (`first initial + last name`) — `auth10`.
- "Bots" / "link checker" / "monitoring probe" / "rotate now" buttons — they act as a privileged user (`auth5`, `auth6`, `auth9`, `auth14`).
- Public "stories"/"testimonials"/"logs" pages that quote other users' data — `auth3`, `inj7`.
