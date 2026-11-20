# 10 — Binary exploitation (pwn)

You get a binary (`vuln`) and `nc host port`. Workflow:

1. **Recon the binary** → [binary-recon](binary-recon.md) (`file`, `checksec`, `strings`, symbols like `win`)
2. **Find the bug**: `gets`, `scanf("%s")`, `strcpy`, `read(0,buf,big)`, `printf(buf)`
3. **Pick the technique**:

| Protections / situation | Technique | Note |
|---|---|---|
| No canary, no PIE, `win()` exists | overwrite return address with `win` | [ret2win](ret2win.md) |
| `win(arg)` needs args (x86-64) | ROP `pop rdi; ret` + arg + `win` | [rop-basics](rop-basics.md) |
| No `win`, NX on, libc available | ret2libc (`system("/bin/sh")`) | [rop-basics](rop-basics.md#ret2libc) |
| NX off (executable stack) | shellcode on stack | [rop-basics](rop-basics.md#shellcode) |
| `printf(user_input)` | format string leak / write | [format-string](format-string.md) |
| Canary on | leak it (format string) first | [format-string](format-string.md) |

Tools: [pwntools-gdb](../tools/pwntools-gdb.md). Template exploit: `scripts/pwn/ret2win.py`.
