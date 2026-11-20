# Tools

One short page per tool: install, the flags that matter, and recipes tuned for these challenges.

| Tool | Use it for | Page |
|---|---|---|
| curl | hand-crafting any HTTP request | [curl](curl.md) |
| Burp Suite / ZAP | proxy, repeater, intruder, sequencer | [burp](burp.md) |
| ffuf | dirs, files, params, vhosts, creds, ids | [ffuf](ffuf.md) |
| nmap | ports, versions, NSE scripts | [nmap](nmap.md) |
| whatweb / nikto | web fingerprint & quick vuln scan | [whatweb-nikto](whatweb-nikto.md) |
| searchsploit | offline Exploit-DB search | [searchsploit](searchsploit.md) |
| git-dumper | rebuild exposed `.git` | [git-dumper](git-dumper.md) |
| hydra | online login brute force | [hydra](hydra.md) |
| jwt_tool (+ our jwt_tool_lite.py) | JWT decode/forge/crack | [jwt_tool](jwt_tool.md) |
| hashcat / john / hashid | offline cracking | [hashcat-john](hashcat-john.md) |
| flask-unsign | Flask session cookies | [flask-unsign](flask-unsign.md) |
| sqlmap | automated SQLi | [sqlmap](sqlmap.md) |
| SSTImap | automated SSTI | [sstimap](sstimap.md) |
| wpscan | WordPress | [wpscan](wpscan.md) |
| snmpwalk / onesixtyone / snmp-check | SNMP | [snmp-tools](snmp-tools.md) |
| nc / socat / rlwrap | listeners, raw TCP, shells | [netcat](netcat.md) |
| OOB listeners (http.server, catch_server.py, interactsh) | callbacks/exfil | [oob-listeners](oob-listeners.md) |
| pwntools / gdb / checksec / ROPgadget | binary exploitation | [pwntools-gdb](pwntools-gdb.md) |
| CyberChef | decode/encode anything | [cyberchef](cyberchef.md) |
| smbclient / enum4linux / ftp | other network services | [network-clients](network-clients.md) |

Install most on Kali/Debian: `sudo apt install ffuf nmap hydra sqlmap wpscan nikto whatweb exploitdb snmp snmp-mibs-downloader onesixtyone snmpcheck hashcat john netcat-openbsd socat rlwrap gdb smbclient`
and `pip install requests pwntools git-dumper flask-unsign`.
