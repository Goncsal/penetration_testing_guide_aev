# nmap

| Option | Meaning |
|---|---|
| `-p-` / `-p 80,443` / `--top-ports 100` | port selection |
| `-sS` (root) / `-sT` | SYN half-open / full connect scan |
| `-sU` | UDP (slow — limit ports) |
| `-sV` | service/version detection (banners) |
| `-sC` | default NSE scripts |
| `-O` | OS fingerprint (root) |
| `-A` | `-sV -sC -O --traceroute` |
| `-Pn` | skip ping (host "seems down") |
| `--min-rate 2000`, `-T4` | speed |
| `-oA name` | save all formats |

## Recipes
```bash
nmap -p- --min-rate 2000 -T4 host                    # find every TCP port
nmap -sV -sC -p <ports> host                         # what are they
sudo nmap -sU -p 161,53,69,123 host                  # key UDP
nmap -sV --script vulners -p <port> host             # CVEs from versions
nmap -p 80 --script http-enum,http-headers,http-methods,http-robots.txt host
nmap -sU -p 161 --script snmp-info,snmp-brute host
nmap -p 21 --script ftp-anon host ; nmap -p 445 --script smb-enum-shares host
nmap -p 80 --script http-shellshock --script-args uri=/cgi-bin/x.sh host
```
NSE scripts live in `/usr/share/nmap/scripts/` (`ls | grep http`). States: open / closed /
filtered (firewall) / open|filtered (UDP no reply).
