# Binary recon

```bash
file vuln                       # 64-bit? statically linked? stripped?
checksec --file=vuln            # (pwntools: `pwn checksec vuln`)
#   Canary: No  → stack overflow can reach saved RIP
#   NX: enabled → no shellcode on stack (use ROP/ret2win)
#   PIE: No     → function addresses fixed (win() at a constant address)
#   RELRO       → GOT overwrite possible if Partial
strings -n 6 vuln | less        # prompts, "flag", "/bin/sh", format strings
nm vuln | grep -iE ' T (win|flag|shell|secret|backdoor)'
objdump -d vuln --no-show-raw-insn | grep -A30 '<vuln>:'      # buffer size: sub rsp,0x40 / lea rax,[rbp-0x40]
objdump -d vuln | grep '<win>:'
```
Decompile: Ghidra / IDA Free / Binary Ninja / `r2 -A vuln` (`afl`, `pdf @ sym.vuln`) / dogbolt.org.

Dangerous calls: `gets`, `strcpy`, `strcat`, `sprintf`, `scanf("%s")`, `read(fd, buf, n>size)`,
`printf(buf)` (format string), `system` (look for its PLT entry → ret2plt).

Run locally: `./vuln`, then `nc` the remote. Course challenges ship the binary in `build/` with
`Dockerfile` (socat) — you can run it locally with docker ([05-local-lab](../00-start/05-local-lab.md)).
