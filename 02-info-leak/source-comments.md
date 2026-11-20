# HTML source & comments

**Signs**: page looks empty/boring; hint mentions "between the lines", "private thoughts".

```bash
curl -s $T | grep -oE '<!--[^>]*-->'                    # single-line comments
curl -s $T | python -c "import re,sys;[print(m) for m in re.findall(r'<!--(.*?)-->',sys.stdin.read(),re.S)]"
curl -s $T | grep -o 'flag{[^}]*}'
```

Also look at:
- `<input type="hidden" ...>` values, `data-*` attributes, `<meta>` tags
- inline `<script>` blocks (API keys, endpoints, ids) → [js-secrets](js-secrets.md)
- CSS files (`/* TODO remove /admin-old */`)
- every page, not just `/` → `python scripts/recon/crawl.py $T` prints all comments site-wide
- browser *view-source*, not DevTools Elements (JS may have removed nodes)

Seen in: `leak9` (flag in an HTML comment on `/`).
Next if empty: [robots-sitemap](robots-sitemap.md).
