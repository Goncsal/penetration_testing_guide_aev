# netcat / socat / rlwrap

```bash
nc -nv host port                    # connect, read banner, talk raw (pwn services, SMTP, FTP)
nc -lvnp 443                        # listen (reverse shells); sudo for <1024
rlwrap nc -lvnp 443                 # + arrow keys/history
nc -lvnp 9001 > loot.bin            # receive a file
nc -zv host 20-100                  # quick port check
printf 'GET / HTTP/1.1\r\nHost: x\r\n\r\n' | nc host 80     # raw HTTP (deck: "anything can be a client")
ncat --ssl host 443                 # TLS (nmap's ncat)
socat TCP-LISTEN:443,reuseaddr,fork -     # listener
socat file:`tty`,raw,echo=0 TCP-LISTEN:443   # fully interactive reverse shell listener
```
bash without nc: `exec 5<>/dev/tcp/host/80; printf 'GET / HTTP/1.1\r\nHost: host\r\n\r\n' >&5; cat <&5`.
Variants: OpenBSD nc has no `-e`; ncat/traditional nc do. Windows: `ncat.exe` from nmap.
