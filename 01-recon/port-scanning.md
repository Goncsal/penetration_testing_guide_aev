# Port scanning

**Why**: TCP replies SYN/ACK (open) or RST (closed); UDP replies with data (open) or ICMP port
unreachable (closed); no reply ⇒ filtered (firewall). The reply pattern also fingerprints the OS.

## Commands

```bash
nmap -p- --min-rate 2000 -T4 <host>                 # all TCP ports, fast
nmap -sV -sC -p 22,80,8080 <host>                   # versions + default scripts on found ports
sudo nmap -sS ...                                   # half-open SYN scan (needs root)
sudo nmap -sU --top-ports 100 <host>                # UDP: SNMP 161, DNS 53, TFTP 69, NTP 123
sudo nmap -O <host>                                 # OS fingerprint
nmap -sV --script vulners -p <port> <host>          # CVEs for detected versions
```
Full tool page: [tools/nmap.md](../tools/nmap.md)

## Reading results

| Port | Next |
|---|---|
| 80/443/8000-8999/3000/5000 | web → [content-discovery](content-discovery.md) |
| 161/udp | [snmp](../09-network/snmp.md) |
| 21 ftp / 22 ssh / 23 telnet / 25 smtp / 3306 mysql / 445 smb | [09-network](../09-network/README.md) |
| Odd high port, text prompt on `nc` | custom service; maybe [pwn](../10-pwn/README.md) |

In the course lab each challenge is one host:port, so scanning matters mostly for the
"network" category and for hidden extra ports.
