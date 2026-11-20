# SNMP tools

Install: `sudo apt install snmp snmp-mibs-downloader onesixtyone snmpcheck` (enable MIB names:
comment out `mibs :` in `/etc/snmp/snmp.conf`).

| Tool | Use |
|---|---|
| `onesixtyone -c communities.txt host` | brute force community strings fast |
| `snmpwalk -v2c -c public host[:port] [OID]` | walk a subtree (`-On` numeric OIDs, `-Oa` show strings) |
| `snmpbulkwalk -v2c -c public host .` | faster walk (GETBULK) |
| `snmpget -v2c -c public host OID` | read one value |
| `snmpset -v2c -c private host OID s "value"` | write (RW community) |
| `snmp-check -p 161 -c public host` | formatted report (users, processes, software, network) |
| `nmap -sU -p161 --script snmp-*` | info/brute/processes/netstat |
| `scripts/network/snmp_walk.py host:port -c public` | pure-Python walker (no install) |

Tips: try `-v1` if v2c fails; non-standard port = `host:8024`; timeouts → `-t 3 -r 2`.
Guide: [09-network/snmp](../09-network/snmp.md).
